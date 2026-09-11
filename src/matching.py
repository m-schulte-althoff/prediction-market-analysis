"""Precision-oriented matching of cross-platform underlying events."""

from __future__ import annotations

import re

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

from src.semantics import extracted_numbers, pair_divergence

GENERIC_WORDS = re.compile(
    r"\b(?:will|the|a|an|be|by|on|in|at|to|of|market|resolve|yes|no|before|after)\b",
    re.I,
)
SPACE = re.compile(r"\s+")


def matching_text(question: str) -> str:
    """Normalize contract wording while retaining entities, dates, and thresholds."""

    text = re.sub(r"[^a-z0-9$%.-]+", " ", question.lower())
    return SPACE.sub(" ", GENERIC_WORDS.sub(" ", text)).strip()


def phenomenon_text(question: str) -> str:
    """Remove claim-specific quantities when retrieving shared-phenomenon candidates."""

    return SPACE.sub(" ", re.sub(r"\b\d+(?:\.\d+)?%?\b", " ", matching_text(question))).strip()


def _token_similarity(left: str, right: str) -> float:
    """Return auditable Jaccard similarity for full claim wording."""

    left_tokens = set(matching_text(left).split())
    right_tokens = set(matching_text(right).split())
    if not left_tokens and not right_tokens:
        return 1.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


def _number_overlap(left: str, right: str) -> float:
    """Return set overlap for explicit thresholds and year/date numbers."""

    left_values = extracted_numbers(left)
    right_values = extracted_numbers(right)
    if not left_values and not right_values:
        return 1.0
    if not left_values or not right_values:
        return 0.0
    return len(left_values & right_values) / len(left_values | right_values)


def _day_difference(left: object, right: object) -> float:
    """Return signed close-date difference in days or NaN."""

    left_text = str(left)
    right_text = str(right)
    if left_text in {"NaT", "nan", "None", ""} or right_text in {"NaT", "nan", "None", ""}:
        return float("nan")
    delta = pd.Timestamp(left_text) - pd.Timestamp(right_text)
    return delta.total_seconds() / 86_400


def _predicate_compatible(left: str, right: str) -> bool:
    """Reject threshold-vs-winner candidates that share an event but not a claim."""

    threshold_terms = ("margin", "above", "below", "over ", "under ", "more than", "less than")
    winner_terms = (" win ", "winner", "nominee")
    left_padded = f" {left.lower()} "
    right_padded = f" {right.lower()} "
    left_threshold = any(term in left_padded for term in threshold_terms)
    right_threshold = any(term in right_padded for term in threshold_terms)
    left_winner = any(term in left_padded for term in winner_terms)
    right_winner = any(term in right_padded for term in winner_terms)
    return not ((left_threshold and right_winner) or (right_threshold and left_winner))


def _label_match(
    lexical: float, number_overlap: float, absolute_days: float, predicate_compatible: bool
) -> str:
    """Assign conservative review strata favoring precision over recall."""

    if (
        lexical >= 0.60
        and number_overlap >= 0.50
        and absolute_days <= 45
        and predicate_compatible
    ):
        return "high_confidence"
    if lexical >= 0.44 and number_overlap >= 0.25 and absolute_days <= 180:
        return "probable"
    return "rejected"


def _nearest_candidates(
    kalshi_text: list[str], polymarket_text: list[str], neighbors: int
) -> tuple[np.ndarray, np.ndarray]:
    """Return cosine distances and indices for nearest Polymarket questions."""

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True)
    matrix: csr_matrix = vectorizer.fit_transform([*kalshi_text, *polymarket_text]).tocsr()
    left = matrix[: len(kalshi_text)]
    right = matrix[len(kalshi_text) :]
    model = NearestNeighbors(
        n_neighbors=min(neighbors, len(polymarket_text)), metric="cosine", algorithm="brute"
    )
    model.fit(right)
    distances, indices = model.kneighbors(left)
    return np.asarray(distances), np.asarray(indices)


def match_contracts(contracts: pd.DataFrame, neighbors: int = 3) -> pd.DataFrame:
    """Retrieve shared phenomena, then separately classify claim-equivalence candidates."""

    kalshi = contracts.loc[contracts["platform"] == "Kalshi"].reset_index(drop=True)
    poly = contracts.loc[contracts["platform"] == "Polymarket"].reset_index(drop=True)
    if kalshi.empty or poly.empty:
        return pd.DataFrame()
    kalshi_text = kalshi["question"].map(phenomenon_text).tolist()
    poly_text = poly["question"].map(phenomenon_text).tolist()
    distances, indices = _nearest_candidates(kalshi_text, poly_text, neighbors)

    candidates: list[dict[str, object]] = []
    for left_index in range(len(kalshi)):
        left = kalshi.iloc[left_index]
        for rank, (distance, right_index) in enumerate(
            zip(distances[left_index], indices[left_index], strict=True), start=1
        ):
            right = poly.iloc[int(right_index)]
            phenomenon_similarity = _bounded_similarity(1 - float(distance))
            lexical = _token_similarity(str(left["question"]), str(right["question"]))
            number_overlap = _number_overlap(left["question"], right["question"])
            deadline_days = _day_difference(left["close_timestamp"], right["close_timestamp"])
            absolute_days = abs(deadline_days) if np.isfinite(deadline_days) else 9_999.0
            predicate_compatible = _predicate_compatible(left["question"], right["question"])
            label = _label_match(lexical, number_overlap, absolute_days, predicate_compatible)
            left_rules = " ".join(
                [str(left["question"]), str(left["rules"]), str(left["resolution_source"])]
            )
            right_rules = " ".join(
                [str(right["question"]), str(right["rules"]), str(right["resolution_source"])]
            )
            divergence = pair_divergence(left_rules, right_rules, lexical, deadline_days)
            candidates.append(
                {
                    "underlying_event_id": (
                        f"match:{left['platform_contract_id']}:{right['platform_contract_id']}"
                    ),
                    "kalshi_contract_id": left["contract_id"],
                    "polymarket_contract_id": right["contract_id"],
                    "kalshi_ticker": left["platform_contract_id"],
                    "polymarket_id": right["platform_contract_id"],
                    "kalshi_question": left["question"],
                    "polymarket_question": right["question"],
                    "kalshi_rule": left["rules"],
                    "polymarket_rule": right["rules"],
                    "kalshi_series": left["series"],
                    "polymarket_yes_token_id": right["yes_token_id"],
                    "kalshi_volume": left["volume"],
                    "polymarket_volume": right["volume"],
                    "kalshi_open_timestamp": left["open_timestamp"],
                    "polymarket_open_timestamp": right["open_timestamp"],
                    "kalshi_close_timestamp": left["close_timestamp"],
                    "polymarket_close_timestamp": right["close_timestamp"],
                    "candidate_rank": rank,
                    "phenomenon_similarity": phenomenon_similarity,
                    "phenomenon_match_label": (
                        "strong_candidate"
                        if phenomenon_similarity >= 0.55
                        else "possible_candidate"
                        if phenomenon_similarity >= 0.40
                        else "weak_candidate"
                    ),
                    "lexical_similarity": lexical,
                    "number_overlap": number_overlap,
                    "predicate_compatible": predicate_compatible,
                    "deadline_difference_days": deadline_days,
                    "match_confidence": 0.55 * lexical
                    + 0.15 * number_overlap
                    + 0.10 * max(0.0, 1 - absolute_days / 180)
                    + 0.20 * phenomenon_similarity,
                    "match_label": label,
                    **divergence,
                }
            )
    result = pd.DataFrame.from_records(candidates)
    return result.sort_values(
        ["match_label", "match_confidence", "underlying_event_id"],
        ascending=[True, False, True],
        kind="stable",
        ignore_index=True,
    )


def _bounded_similarity(value: float) -> float:
    """Clamp numerical noise around cosine similarity."""

    return min(1.0, max(0.0, value))
