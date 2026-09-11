"""Acquire and align price histories for accepted cross-platform matches."""

from __future__ import annotations

import hashlib
import logging
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from src.config import KALSHI_BASE_URL, POLYMARKET_CLOB_URL, RAW_DIR, SampleConfig
from src.http_client import PublicApiClient
from src.io_utils import read_json, write_immutable_json

LOGGER = logging.getLogger(__name__)


def select_panel_matches(matches: pd.DataFrame, limit: int) -> pd.DataFrame:
    """Select unique high-confidence pairs spanning the divergence distribution."""

    accepted = matches.loc[matches["match_label"] == "high_confidence"].copy()
    accepted = accepted.drop_duplicates(["kalshi_ticker", "polymarket_id"])
    accepted = accepted.loc[
        (accepted["polymarket_yes_token_id"].astype(str).str.len() > 5)
        & accepted["kalshi_open_timestamp"].notna()
        & accepted["kalshi_close_timestamp"].notna()
    ]
    if len(accepted) <= limit:
        return accepted.sort_values("match_confidence", ascending=False, kind="stable")
    # Stratified deterministic selection prevents an exhibit consisting only of
    # either nearly identical or maximally different contracts.
    accepted = accepted.sort_values("semantic_divergence", kind="stable").reset_index(drop=True)
    positions = np.linspace(0, len(accepted) - 1, limit).round().astype(int)
    return accepted.iloc[positions].drop_duplicates("underlying_event_id")


def _snapshot_path(selected: pd.DataFrame, config: SampleConfig) -> Path:
    """Return a content-addressed raw path for the exact selected match set."""

    identifiers = "|".join(selected["underlying_event_id"].astype(str).sort_values())
    digest = hashlib.sha256(identifiers.encode("utf-8")).hexdigest()[:10]
    return RAW_DIR / (
        f"matched-price-histories-{config.retrieval_date.isoformat()}-{digest}-interval-max.json"
    )


def _unix(value: object) -> int:
    """Convert a timestamp-like value to Unix seconds."""

    return int(pd.Timestamp(str(value)).timestamp())


def _numeric(value: object) -> float:
    """Convert a scalar API value to float, returning NaN for missing values."""

    try:
        return float(str(value)) if value not in (None, "") else float("nan")
    except (TypeError, ValueError):
        return float("nan")


def download_matched_histories(
    matches: pd.DataFrame,
    config: SampleConfig,
    client: PublicApiClient,
) -> dict[str, Any]:
    """Download or load daily price histories for selected accepted pairs."""

    selected = select_panel_matches(matches, config.matched_panel_limit)
    path = _snapshot_path(selected, config)
    if path.exists():
        payload = read_json(path)
        if not isinstance(payload, dict):
            raise TypeError("Matched-history snapshot must contain a JSON object")
        LOGGER.info("Using cached matched histories: %s", path)
        return payload

    cutoff_payload = client.get_json(f"{KALSHI_BASE_URL}/historical/cutoff")
    cutoff = pd.Timestamp(cutoff_payload["market_settled_ts"])
    pairs: list[dict[str, Any]] = []
    for row in selected.itertuples(index=False):
        start = max(
            pd.Timestamp(str(row.kalshi_open_timestamp)),
            pd.Timestamp(str(row.polymarket_open_timestamp)),
        )
        end = min(
            pd.Timestamp(str(row.kalshi_close_timestamp)),
            pd.Timestamp(str(row.polymarket_close_timestamp)),
        )
        if pd.isna(start) or pd.isna(end) or start >= end:
            continue
        archived = pd.Timestamp(str(row.kalshi_close_timestamp)) < cutoff
        if archived:
            kalshi_url = f"{KALSHI_BASE_URL}/historical/markets/{row.kalshi_ticker}/candlesticks"
        else:
            kalshi_url = (
                f"{KALSHI_BASE_URL}/series/{row.kalshi_series}/markets/"
                f"{row.kalshi_ticker}/candlesticks"
            )
        try:
            kalshi = client.get_json(
                kalshi_url,
                {"start_ts": _unix(start), "end_ts": _unix(end), "period_interval": 1440},
            )
            polymarket = client.get_json(
                f"{POLYMARKET_CLOB_URL}/prices-history",
                {
                    "market": row.polymarket_yes_token_id,
                    "interval": "max",
                },
            )
        except RuntimeError as error:
            LOGGER.warning("Skipping unavailable pair %s: %s", row.underlying_event_id, error)
            continue
        pairs.append(
            {
                "match": {
                    "underlying_event_id": row.underlying_event_id,
                    "kalshi_ticker": row.kalshi_ticker,
                    "polymarket_id": row.polymarket_id,
                    "kalshi_question": row.kalshi_question,
                    "polymarket_question": row.polymarket_question,
                    "semantic_divergence": row.semantic_divergence,
                    "match_confidence": row.match_confidence,
                    "aligned_start": start.isoformat(),
                    "aligned_end": end.isoformat(),
                },
                "kalshi": kalshi,
                "polymarket": polymarket,
            }
        )
    payload = {
        "retrieved_at_date": config.retrieval_date.isoformat(),
        "historical_cutoff": cutoff_payload,
        "pairs": pairs,
    }
    write_immutable_json(path, payload)
    LOGGER.info("Saved histories for %d matched pairs to %s", len(pairs), path)
    return payload


def _kalshi_history(payload: dict[str, Any]) -> pd.DataFrame:
    """Normalize daily Kalshi candles."""

    rows: list[dict[str, object]] = []
    for candle in payload.get("candlesticks", []):
        price = candle.get("price") or {}
        bid = candle.get("yes_bid") or {}
        ask = candle.get("yes_ask") or {}
        trade_close = _numeric(price.get("close_dollars") or price.get("close"))
        bid_close = _numeric(bid.get("close_dollars") or bid.get("close"))
        ask_close = _numeric(ask.get("close_dollars") or ask.get("close"))
        midpoint = (
            (float(bid_close) + float(ask_close)) / 2
            if pd.notna(bid_close) and pd.notna(ask_close)
            else float("nan")
        )
        rows.append(
            {
                "timestamp": pd.to_datetime(candle.get("end_period_ts"), unit="s", utc=True),
                "kalshi_price": trade_close if pd.notna(trade_close) else midpoint,
                "kalshi_bid": bid_close,
                "kalshi_ask": ask_close,
                "kalshi_volume": _numeric(candle.get("volume_fp") or candle.get("volume")),
            }
        )
    return pd.DataFrame.from_records(rows)


def _polymarket_history(payload: dict[str, Any]) -> pd.DataFrame:
    """Normalize Polymarket token price history."""

    rows = [
        {
            "timestamp": pd.to_datetime(item.get("t"), unit="s", utc=True),
            "polymarket_price": _numeric(item.get("p")),
        }
        for item in payload.get("history", [])
    ]
    return pd.DataFrame.from_records(rows)


def build_matched_panel(payload: dict[str, Any]) -> pd.DataFrame:
    """Align both platforms to daily observations using only prior prices."""

    panels: list[pd.DataFrame] = []
    for pair in payload.get("pairs", []):
        kalshi = _kalshi_history(pair["kalshi"])
        polymarket = _polymarket_history(pair["polymarket"])
        if kalshi.empty or polymarket.empty:
            continue
        kalshi = kalshi.set_index("timestamp").sort_index().resample("1D").last()
        polymarket = polymarket.set_index("timestamp").sort_index().resample("1D").last()
        aligned = kalshi.join(polymarket, how="outer").sort_index().ffill(limit=7)
        aligned = aligned.dropna(subset=["kalshi_price", "polymarket_price"])
        aligned = aligned.loc[
            aligned["kalshi_price"].between(0, 1)
            & aligned["polymarket_price"].between(0, 1)
        ].copy()
        if aligned.empty:
            continue
        metadata = pair["match"]
        aligned["underlying_event_id"] = metadata["underlying_event_id"]
        aligned["kalshi_question"] = metadata["kalshi_question"]
        aligned["polymarket_question"] = metadata["polymarket_question"]
        aligned["semantic_divergence"] = metadata["semantic_divergence"]
        aligned["match_confidence"] = metadata["match_confidence"]
        aligned["disagreement"] = (
            aligned["kalshi_price"] - aligned["polymarket_price"]
        ).abs()
        aligned_index = pd.DatetimeIndex(aligned.index)
        timestamp_series = pd.Series(aligned_index, index=aligned.index)
        aligned["days_to_close"] = (
            pd.Timestamp(str(metadata["aligned_end"])) - timestamp_series
        ).dt.total_seconds() / 86_400
        panels.append(aligned.reset_index())
    if not panels:
        return pd.DataFrame()
    return pd.concat(panels, ignore_index=True).sort_values(
        ["underlying_event_id", "timestamp"], kind="stable", ignore_index=True
    )


def summarize_matched_panel(panel: pd.DataFrame) -> pd.DataFrame:
    """Summarize disagreement overall and near contract close for each pair."""

    if panel.empty:
        return pd.DataFrame()
    records: list[dict[str, object]] = []
    for event_id, group in panel.groupby("underlying_event_id", sort=True):
        near_30 = group.loc[group["days_to_close"].between(0, 30)]
        near_7 = group.loc[group["days_to_close"].between(0, 7)]
        records.append(
            {
                "underlying_event_id": event_id,
                "kalshi_question": group["kalshi_question"].iloc[0],
                "polymarket_question": group["polymarket_question"].iloc[0],
                "semantic_divergence": group["semantic_divergence"].iloc[0],
                "match_confidence": group["match_confidence"].iloc[0],
                "observations": len(group),
                "mean_disagreement": group["disagreement"].mean(),
                "mean_disagreement_30d": near_30["disagreement"].mean(),
                "mean_disagreement_7d": near_7["disagreement"].mean(),
                "max_disagreement": group["disagreement"].max(),
            }
        )
    return pd.DataFrame.from_records(records)
