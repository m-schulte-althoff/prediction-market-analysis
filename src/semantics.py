"""Transparent semantic-determinacy and divergence measures."""

from __future__ import annotations

import math
import re
from collections.abc import Iterable

import numpy as np
import pandas as pd

DATE_PATTERN = re.compile(
    r"\b(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|"
    r"jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)"
    r"\s+\d{1,2}(?:st|nd|rd|th)?(?:,?\s+\d{4})?|\b\d{4}-\d{2}-\d{2}\b|"
    r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",
    re.IGNORECASE,
)
TIME_PATTERN = re.compile(r"\b\d{1,2}(?::\d{2})?\s*(?:a\.?m\.?|p\.?m\.?)\b", re.I)
TIMEZONE_PATTERN = re.compile(r"\b(?:utc|gmt|est|edt|cst|cdt|mst|mdt|pst|pdt)\b", re.I)
URL_PATTERN = re.compile(r"https?://[^\s)]+", re.I)
NUMBER_PATTERN = re.compile(r"(?<![a-z])[-+]?\$?\d+(?:\.\d+)?%?", re.I)
QUANTITATIVE_THRESHOLD_PATTERN = re.compile(
    r"(?:\b(?:at least|at most|more than|less than|greater than|fewer than|"
    r"exactly|above|below|over|under|exceed(?:s|ed)?|between)\s+"
    r"[-+]?\$?\d+(?:\.\d+)?(?:%|\s*(?:percent|percentage points?|basis points?|bps|"
    r"dollars?|votes?|points?|seats?|degrees?|times?|cuts?|hikes?))?\b)"
    r"|(?:[-+]?\$?\d+(?:\.\d+)?\s*(?:%|percent|percentage points?|basis points?|bps|"
    r"dollars?|votes?|points?|seats?|degrees?)\b)",
    re.IGNORECASE,
)

AUTHORITIES = (
    "associated press",
    "reuters",
    "national weather service",
    "bureau of labor statistics",
    "federal reserve",
    "department of",
    "secretary of state",
    "congress.gov",
    "census bureau",
    "electoral college",
    "white house",
    "supreme court",
    "official website",
    "official results",
    "company announcement",
)
DISCRETION_TERMS = (
    "credible reporting",
    "consensus of",
    "preponderance of evidence",
    "sole discretion",
    "best judgment",
    "unclear",
    "sufficient evidence",
    "widely reported",
)
AMBIGUOUS_TERMS = (
    "significant",
    "substantial",
    "deal",
    "agreement",
    "launch",
    "release",
    "wearing",
    "recession",
    "officially",
    "major",
    "meaningful",
    "active role",
)
EDGE_TERMS = (
    "otherwise",
    "in the event",
    "if no",
    "if neither",
    "if unavailable",
    "postpon",
    "cancel",
    "tie",
    "replacement",
    "revised",
    "fallback",
    "inaugurat",
)
DEFINITION_TERMS = (
    "defined as",
    "for the purpose",
    "will resolve to yes if",
    "resolves to yes if",
    "measured by",
    "according to",
    "greater than",
    "less than",
    "at least",
    "more than",
)
STAGE_TERMS = (
    "announce",
    "agree",
    "sign",
    "enact",
    "implement",
    "effective",
    "inaugurat",
    "call the race",
    "certif",
    "filed",
    "released",
    "launched",
)


def _contains_count(text: str, terms: Iterable[str]) -> int:
    """Count distinct configured terms present in lower-cased text."""

    lowered = text.lower()
    return sum(term in lowered for term in terms)


def _bounded(value: float) -> float:
    """Clamp a floating-point component to the unit interval."""

    return min(1.0, max(0.0, value))


def semantic_features(question: str, rules: str, resolution_source: str = "") -> dict[str, float]:
    """Compute interpretable, pre-specified determinacy components for one contract."""

    text = " ".join(part for part in (question, rules, resolution_source) if part)
    lowered = text.lower()
    words = re.findall(r"\b[\w'-]+\b", text)
    explicit_sources = len(URL_PATTERN.findall(text)) + _contains_count(text, AUTHORITIES)
    vague_source = _contains_count(text, DISCRETION_TERMS)
    source_specificity = _bounded(
        0.75 * (explicit_sources > 0)
        + 0.25 * bool(resolution_source.strip())
        - 0.25 * (vague_source > 0)
    )

    has_date = bool(DATE_PATTERN.search(text))
    has_time = bool(TIME_PATTERN.search(text))
    has_timezone = bool(TIMEZONE_PATTERN.search(text))
    deadline_language = any(term in lowered for term in ("by ", "before ", "at ", "deadline"))
    temporal_specificity = _bounded(
        0.55 * has_date + 0.15 * has_time + 0.15 * has_timezone + 0.15 * deadline_language
    )

    definition_hits = _contains_count(text, DEFINITION_TERMS)
    numeric_mention = bool(NUMBER_PATTERN.search(text))
    quantitative_threshold = bool(QUANTITATIVE_THRESHOLD_PATTERN.search(text))
    ambiguity_hits = _contains_count(text, AMBIGUOUS_TERMS)
    outcome_definition = _bounded(
        0.25
        + 0.35 * (definition_hits > 0)
        + 0.30 * quantitative_threshold
        - 0.12 * ambiguity_hits
    )

    edge_hits = _contains_count(text, EDGE_TERMS)
    conditional_count = len(re.findall(r"\b(?:if|unless|otherwise|except)\b", lowered))
    edge_completeness = _bounded(0.12 * min(edge_hits + conditional_count, 6))
    discretion_clarity = _bounded(1.0 - 0.25 * vague_source)

    conditional_clauses = len(
        re.findall(r"\b(?:if|unless|except|provided that|otherwise)\b", lowered)
    )
    determinacy = float(
        np.mean(
            [
                source_specificity,
                temporal_specificity,
                outcome_definition,
                edge_completeness,
                discretion_clarity,
            ]
        )
    )
    return {
        "source_specificity": source_specificity,
        "temporal_specificity": temporal_specificity,
        "outcome_definition": outcome_definition,
        "edge_completeness": edge_completeness,
        "discretion_clarity": discretion_clarity,
        "determinacy_score": determinacy,
        "rule_word_count": float(len(words)),
        "conditional_clauses": float(conditional_clauses),
        "ambiguous_terms": float(ambiguity_hits),
        "explicit_sources": float(explicit_sources),
        "numeric_mention": float(numeric_mention),
        "quantitative_threshold": float(quantitative_threshold),
    }


def add_semantic_features(contracts: pd.DataFrame) -> pd.DataFrame:
    """Attach semantic components to every contract row."""

    rows = [
        semantic_features(str(row.question), str(row.rules), str(row.resolution_source))
        for row in contracts.itertuples(index=False)
    ]
    features = pd.DataFrame.from_records(rows, index=contracts.index)
    return pd.concat([contracts, features], axis=1)


def extracted_numbers(text: str) -> set[str]:
    """Extract normalized numeric/date tokens for matching and divergence."""

    return {match.replace("$", "").replace("%", "") for match in NUMBER_PATTERN.findall(text)}


def extracted_stages(text: str) -> set[str]:
    """Extract event-stage predicates from operative language."""

    lowered = text.lower()
    return {term for term in STAGE_TERMS if term in lowered}


def extracted_sources(text: str) -> set[str]:
    """Extract known authorities and URL domains from contract text."""

    lowered = text.lower()
    sources = {term for term in AUTHORITIES if term in lowered}
    sources.update(
        re.sub(r"^https?://(?:www\.)?", "", url.lower()).split("/")[0]
        for url in URL_PATTERN.findall(text)
    )
    return sources


def jaccard_distance(left: set[str], right: set[str]) -> float:
    """Return Jaccard distance, treating two empty sets as equivalent."""

    if not left and not right:
        return 0.0
    return 1.0 - len(left & right) / len(left | right)


def pair_divergence(
    kalshi_text: str,
    polymarket_text: str,
    lexical_similarity: float,
    deadline_days: float,
) -> dict[str, float | str]:
    """Measure interpretable resolution-condition divergence for a matched pair."""

    left_numbers = extracted_numbers(kalshi_text)
    right_numbers = extracted_numbers(polymarket_text)
    number_divergence = jaccard_distance(left_numbers, right_numbers)
    source_divergence = jaccard_distance(
        extracted_sources(kalshi_text), extracted_sources(polymarket_text)
    )
    stage_divergence = jaccard_distance(
        extracted_stages(kalshi_text), extracted_stages(polymarket_text)
    )
    deadline_divergence = _bounded(abs(deadline_days) / 90) if math.isfinite(deadline_days) else 0.5
    wording_divergence = _bounded(1 - lexical_similarity)
    composite = float(
        np.average(
            [
                wording_divergence,
                number_divergence,
                source_divergence,
                stage_divergence,
                deadline_divergence,
            ],
            weights=[0.20, 0.20, 0.25, 0.20, 0.15],
        )
    )
    differences: list[str] = []
    kalshi_lower = kalshi_text.lower()
    polymarket_lower = polymarket_text.lower()
    announcement_rejected = (
        "announcement" in polymarket_lower and "not alone qualify" in polymarket_lower
    )
    announcement_accepted = "announcement" in kalshi_lower and any(
        phrase in kalshi_lower
        for phrase in ("resolves to yes", "then the market resolves to yes", "encompassed")
    )
    if announcement_rejected and announcement_accepted:
        differences.append("announcement can qualify on Kalshi but not alone on Polymarket")
    death_left = any(term in kalshi_lower for term in ("death", "died"))
    death_right = any(term in polymarket_lower for term in ("death", "died"))
    if death_left != death_right:
        differences.append("death treatment is explicit on only one platform")
    cancel_left = any(term in kalshi_lower for term in ("cancel", "postpon"))
    cancel_right = any(term in polymarket_lower for term in ("cancel", "postpon"))
    if cancel_left != cancel_right:
        differences.append("cancellation/postponement fallback appears on one platform")
    if ("social media" in kalshi_lower) != ("social media" in polymarket_lower):
        differences.append("permitted attendance evidence differs")
    clarification_left = any(
        term in kalshi_lower for term in ("typographical error", "has been changed")
    )
    clarification_right = any(
        term in polymarket_lower for term in ("typographical error", "has been changed")
    )
    if clarification_left != clarification_right:
        differences.append("one contract records a rule correction")
    if number_divergence > 0:
        differences.append("numeric/date conditions differ")
    if source_divergence > 0:
        differences.append("named resolution sources differ")
    if stage_divergence > 0:
        differences.append("required event stage differs")
    if deadline_divergence >= 0.10:
        differences.append(f"deadlines differ by {abs(deadline_days):.0f} days")
    if not differences:
        differences.append("no structured difference detected")
    return {
        "wording_divergence": wording_divergence,
        "number_divergence": number_divergence,
        "source_divergence": source_divergence,
        "stage_divergence": stage_divergence,
        "deadline_divergence": deadline_divergence,
        "semantic_divergence": composite,
        "identified_semantic_difference": "; ".join(differences),
    }
