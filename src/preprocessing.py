"""Normalize platform metadata into a reusable contract table."""

from __future__ import annotations

import json
from typing import Any

import numpy as np
import pandas as pd

from src.taxonomy import classify_polymarket_sports


def _number(value: object) -> float:
    """Convert a possibly string-valued number to a float."""

    try:
        return float(str(value)) if value not in (None, "") else float("nan")
    except (TypeError, ValueError):
        return float("nan")


def _text(value: object) -> str:
    """Normalize nullable API values as stripped text."""

    return str(value or "").strip()


def _first_event(row: dict[str, Any]) -> dict[str, Any]:
    """Return the first embedded Polymarket event, if present."""

    events = row.get("events")
    if isinstance(events, list) and events and isinstance(events[0], dict):
        return events[0]
    return {}


def _json_list(value: object) -> list[str]:
    """Parse a JSON-encoded list while accepting an already decoded list."""

    if isinstance(value, list):
        return [str(item) for item in value]
    if not isinstance(value, str) or not value:
        return []
    try:
        decoded = json.loads(value)
    except json.JSONDecodeError:
        return []
    return [str(item) for item in decoded] if isinstance(decoded, list) else []


DOMAIN_TERMS = {
    "Elections and Politics": (
        "election",
        "president",
        "trump",
        "biden",
        "congress",
        "senate",
        "house control",
        "governor",
        "mayor",
        "nominee",
        "primary",
        "cabinet",
        "supreme court",
        "approval rating",
        "political party",
    ),
    "Economics": (
        "federal reserve",
        "fed chair",
        "interest rate",
        "rate cut",
        "inflation",
        "cpi",
        "gdp",
        "unemployment",
        "nonfarm payroll",
        "recession",
        "tariff",
    ),
    "World": (
        "ceasefire",
        "peace deal",
        "ukraine",
        "russia",
        "iran",
        "israel",
        "gaza",
        "nato",
        "north korea",
        "greenland",
        "military strike",
        "prime minister",
    ),
    "Technology and Science": (
        "artificial intelligence",
        "openai",
        "gpt-",
        "ai model",
        "spacex",
        "rocket",
        "space launch",
        "nasa",
        "quantum",
    ),
    "Companies and Markets": (
        "ipo",
        "market cap",
        "stock price",
        "ceo",
        "acquire",
        "merger",
        "apple",
        "google",
        "microsoft",
        "tesla",
    ),
    "Crypto": ("bitcoin", "ethereum", "crypto", "solana", "xrp"),
    "Entertainment": ("oscar", "grammy", "album", "box office", "movie", "emmy"),
}


def _polymarket_category(row: dict[str, Any], event: dict[str, Any]) -> str:
    """Use supplied domains, then a fixed keyword taxonomy when archives omit them."""

    supplied = _text(row.get("category") or event.get("category"))
    if supplied:
        return supplied
    tags = event.get("tags", [])
    if isinstance(tags, list):
        labels = [
            _text(tag.get("label"))
            for tag in tags
            if isinstance(tag, dict) and tag.get("label")
        ]
        if labels:
            return labels[0]
    text = " ".join(
        _text(value).lower()
        for value in (row.get("question"), row.get("description"), event.get("title"))
    )
    for domain, terms in DOMAIN_TERMS.items():
        if any(term in text for term in terms):
            return domain
    return "Other non-sports"


def normalize_kalshi(payload: dict[str, Any]) -> pd.DataFrame:
    """Normalize Kalshi API rows to the contract schema."""

    records: list[dict[str, Any]] = []
    for row in payload.get("markets", []):
        result = _text(row.get("result")).lower()
        recorded_outcome = result if result in {"yes", "no"} else ""
        scalar = result == "scalar"
        settlement_sources = row.get("series_settlement_sources", [])
        source_names = " | ".join(
            _text(source.get("name"))
            for source in settlement_sources
            if isinstance(source, dict)
        )
        records.append(
            {
                "contract_id": f"kalshi:{row.get('ticker')}",
                "platform": "Kalshi",
                "platform_contract_id": _text(row.get("ticker")),
                "platform_event_id": _text(row.get("event_ticker")),
                "question": _text(row.get("title")),
                "rules": "\n".join(
                    part
                    for part in (
                        _text(row.get("rules_primary")),
                        _text(row.get("rules_secondary")),
                        _text(row.get("early_close_condition")),
                    )
                    if part
                ),
                "resolution_source": source_names,
                "open_timestamp": row.get("open_time") or row.get("created_time"),
                "close_timestamp": row.get("close_time") or row.get("expiration_time"),
                "resolution_timestamp": row.get("settlement_ts"),
                "outcome": recorded_outcome,
                "recorded_outcome": recorded_outcome,
                "price_inferred_outcome": "",
                "outcome_category": (
                    "recorded_binary" if recorded_outcome else "scalar_settlement"
                    if scalar else "no_recorded_outcome"
                ),
                "outcome_evidence": "platform_result" if recorded_outcome or scalar else "none",
                "resolution_status": _text(row.get("status")).lower(),
                "yes_settlement_payoff": (
                    _number(row.get("settlement_value_dollars")) if scalar
                    else {"yes": 1.0, "no": 0.0}.get(recorded_outcome, float("nan"))
                ),
                "terminal_price": _number(row.get("last_price_dollars")),
                "volume": _number(row.get("volume_fp") or row.get("volume")),
                "liquidity": _number(row.get("liquidity_dollars")),
                "open_interest": _number(row.get("open_interest_fp")),
                "category": _text(row.get("sample_category")) or "Uncategorized",
                "series": _text(row.get("sample_series_ticker")),
                "yes_token_id": "",
                "outcome_prices_aligned": True,
                "outcome_tokens_aligned": True,
                "sports_classification_reason": "kalshi_selected_category",
                "raw_status": _text(row.get("status")),
                "snapshot_date": payload.get("retrieved_at_date"),
                "acquired_at_utc": payload.get("acquired_at_utc"),
                "source_updated_at": row.get("updated_time"),
            }
        )
    return _finalize(pd.DataFrame.from_records(records))


def normalize_polymarket(payload: dict[str, Any]) -> pd.DataFrame:
    """Normalize binary Polymarket API rows to the contract schema."""

    records: list[dict[str, Any]] = []
    for row in payload.get("markets", []):
        sports, sports_reason = classify_polymarket_sports(row)
        if sports:
            continue
        outcomes = [item.lower() for item in _json_list(row.get("outcomes"))]
        if len(outcomes) != 2 or set(outcomes) != {"yes", "no"}:
            continue
        yes_index = outcomes.index("yes")
        prices = _json_list(row.get("outcomePrices"))
        prices_aligned = len(prices) == 2 and all(0 <= _number(price) <= 1 for price in prices)
        yes_price = _number(prices[yes_index]) if prices_aligned else float("nan")
        inferred = "yes" if yes_price >= 0.99 else "no" if yes_price <= 0.01 else ""
        resolution_status = _text(row.get("umaResolutionStatus")).lower()
        final_status = resolution_status in {"resolved", "settled"}
        outcome = inferred if final_status else ""
        if inferred:
            outcome_category = "price_inferred_binary"
        elif prices_aligned:
            outcome_category = "intermediate_price"
        else:
            outcome_category = "unavailable_price_vector"
        outcome_evidence = (
            f"price_inferred_{resolution_status or 'missing_status'}" if inferred else
            f"intermediate_price_{resolution_status or 'missing_status'}" if prices_aligned else
            "none"
        )
        tokens = _json_list(row.get("clobTokenIds"))
        tokens_aligned = len(tokens) == 2 and all(tokens) and len(set(tokens)) == 2
        event = _first_event(row)
        records.append(
            {
                "contract_id": f"polymarket:{row.get('id')}",
                "platform": "Polymarket",
                "platform_contract_id": _text(row.get("id")),
                "platform_event_id": _text(event.get("id") or row.get("questionID")),
                "question": _text(row.get("question")),
                "rules": _text(row.get("description")),
                "resolution_source": _text(
                    row.get("resolutionSource") or event.get("resolutionSource")
                ),
                "open_timestamp": row.get("startDate") or row.get("createdAt"),
                "close_timestamp": row.get("endDate") or row.get("closedTime"),
                "resolution_timestamp": row.get("closedTime") or row.get("umaEndDate"),
                "outcome": outcome,
                "recorded_outcome": "",
                "price_inferred_outcome": inferred,
                "outcome_category": outcome_category,
                "outcome_evidence": outcome_evidence,
                "resolution_status": resolution_status,
                # An archived price vector is not a separately recorded payout.
                "yes_settlement_payoff": float("nan"),
                # Gamma's archived lastTradePrice is not consistently oriented
                # to YES for legacy AMM markets, so it is not used as an error metric.
                "terminal_price": float("nan"),
                "volume": _number(row.get("volumeNum") or row.get("volume")),
                "liquidity": _number(row.get("liquidityNum") or row.get("liquidity")),
                "open_interest": _number(event.get("openInterest")),
                "category": _polymarket_category(row, event),
                "series": _text(event.get("ticker") or event.get("slug")),
                "yes_token_id": tokens[yes_index] if tokens_aligned else "",
                "outcome_prices_aligned": prices_aligned,
                "outcome_tokens_aligned": tokens_aligned,
                "sports_classification_reason": sports_reason,
                "raw_status": "closed" if row.get("closed") else "open",
                "snapshot_date": payload.get("retrieved_at_date"),
                "acquired_at_utc": payload.get("acquired_at_utc"),
                "source_updated_at": row.get("updatedAt"),
            }
        )
    return _finalize(pd.DataFrame.from_records(records))


def _finalize(frame: pd.DataFrame) -> pd.DataFrame:
    """Apply common timestamp, duration, and validity transformations."""

    if frame.empty:
        return frame
    for column in (
        "open_timestamp", "close_timestamp", "resolution_timestamp",
        "acquired_at_utc", "source_updated_at",
    ):
        frame[column] = pd.to_datetime(frame[column], utc=True, errors="coerce", format="mixed")
    frame["snapshot_timestamp"] = pd.to_datetime(
        frame["snapshot_date"], utc=True, errors="coerce", format="mixed"
    )
    frame["snapshot_boundary_kind"] = "requested_date_midnight_utc"
    frame["market_duration_days"] = (
        (frame["close_timestamp"] - frame["open_timestamp"]).dt.total_seconds() / 86_400
    )
    frame["market_duration_days"] = frame["market_duration_days"].where(
        frame["market_duration_days"] >= 0
    )
    exposure_end = pd.concat(
        [frame["close_timestamp"], frame["resolution_timestamp"], frame["snapshot_timestamp"]],
        axis=1,
    ).min(axis=1)
    frame["raw_exposure_days"] = (
        (exposure_end - frame["open_timestamp"]).dt.total_seconds() / 86_400
    )
    frame["observed_exposure_days"] = frame["raw_exposure_days"].clip(lower=0)
    frame["observed_exposure_days"] = frame["observed_exposure_days"].fillna(
        frame["market_duration_days"]
    )
    frame["exposure_basis"] = "metadata_elapsed_time_to_min_close_resolution_snapshot_midnight"
    frame["negative_exposure_reason"] = np.select(
        [
            (frame["raw_exposure_days"] < 0)
            & (frame["open_timestamp"] >= frame["snapshot_timestamp"] + pd.Timedelta(days=1)),
            (frame["raw_exposure_days"] < 0)
            & (frame["close_timestamp"] < frame["open_timestamp"]),
            frame["raw_exposure_days"] < 0,
        ],
        ["scheduled_after_snapshot_day", "close_before_open", "within_snapshot_day"],
        default="",
    )
    frame["resolution_year"] = frame["resolution_timestamp"].dt.year.astype("Int64")
    frame["log_volume"] = np.log1p(frame["volume"].clip(lower=0))
    outcome_binary = frame["outcome"].map({"yes": 1.0, "no": 0.0})
    frame["terminal_abs_error"] = (frame["terminal_price"] - outcome_binary).abs()
    frame = frame.drop_duplicates("contract_id", keep="last")
    frame = frame[frame["question"].str.len() > 4].copy()
    return frame.sort_values("contract_id", kind="stable").reset_index(drop=True)


def build_contract_table(
    kalshi_payload: dict[str, Any],
    polymarket_payload: dict[str, Any],
) -> pd.DataFrame:
    """Combine both normalized platform samples with a stable row order."""

    return pd.concat(
        [normalize_kalshi(kalshi_payload), normalize_polymarket(polymarket_payload)],
        ignore_index=True,
    ).sort_values(["platform", "contract_id"], kind="stable", ignore_index=True)


def normalization_ledger(payload: dict[str, Any], platform: str) -> pd.DataFrame:
    """Describe raw-row normalization attrition separately from acquisition filtering."""

    if platform not in {"Kalshi", "Polymarket"}:
        raise ValueError(f"Unsupported platform: {platform}")
    records: list[dict[str, object]] = []
    seen: set[str] = set()
    for position, row in reversed(list(enumerate(payload.get("markets", [])))):
        identifier = _text(row.get("ticker" if platform == "Kalshi" else "id"))
        question = _text(row.get("title" if platform == "Kalshi" else "question"))
        reason = "retained"
        sports_reason = "kalshi_selected_category"
        if platform == "Polymarket":
            sports, sports_reason = classify_polymarket_sports(row)
            outcomes = [item.lower() for item in _json_list(row.get("outcomes"))]
            if sports:
                reason = "sports_at_normalization"
            elif len(outcomes) != 2 or set(outcomes) != {"yes", "no"}:
                reason = "unsupported_binary_labels"
        if reason == "retained":
            if identifier in seen:
                reason = "duplicate_keep_last"
            else:
                seen.add(identifier)
                if len(question) <= 4:
                    reason = "question_length_le4"
        records.append({
            "platform": platform, "raw_row_position": position,
            "platform_contract_id": identifier, "question": question,
            "normalization_reason": reason, "sports_classification_reason": sports_reason,
        })
    columns = [
        "platform", "raw_row_position", "platform_contract_id", "question",
        "normalization_reason", "sports_classification_reason",
    ]
    return pd.DataFrame.from_records(records, columns=columns).sort_values(
        "raw_row_position", kind="stable", ignore_index=True
    )


def outcome_ledger(contracts: pd.DataFrame) -> pd.DataFrame:
    """Count outcome evidence without equating extreme prices with recorded settlements."""

    keys = ["platform", "outcome_category", "outcome_evidence", "resolution_status"]
    return contracts.groupby(keys, dropna=False, sort=True).agg(
        contracts=("contract_id", "size"),
        binary_outcomes=("outcome", lambda values: values.isin(["yes", "no"]).sum()),
        price_inferred_outcomes=(
            "price_inferred_outcome", lambda values: values.isin(["yes", "no"]).sum()
        ),
        resolution_timestamps=("resolution_timestamp", "count"),
    ).reset_index()


def exposure_ledger(contracts: pd.DataFrame) -> pd.DataFrame:
    """Count negative elapsed-time categories and keep positive-volume timing exceptions."""

    return contracts.groupby(
        ["platform", "negative_exposure_reason"], dropna=False, sort=True
    ).agg(
        contracts=("contract_id", "size"),
        positive_volume=("volume", lambda values: (values > 0).sum()),
        zero_volume=("volume", lambda values: (values == 0).sum()),
        zero_clipped_exposure=("observed_exposure_days", lambda values: (values == 0).sum()),
    ).reset_index()
