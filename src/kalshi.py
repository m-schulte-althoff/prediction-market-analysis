"""Acquire a semantically relevant Kalshi market-metadata sample."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from src.config import (
    KALSHI_BASE_URL,
    KALSHI_CATEGORIES,
    SampleConfig,
    acquisition_metadata,
    dated_raw_path,
    require_current_acquisition_date,
    validate_snapshot_date,
)
from src.http_client import PublicApiClient
from src.io_utils import read_json, write_immutable_json

LOGGER = logging.getLogger(__name__)


def kalshi_snapshot_path(config: SampleConfig) -> Path:
    """Return a versioned path because the selected-series count affects raw content."""

    return dated_raw_path(f"kalshi-markets-s{config.kalshi_series_limit}", config.retrieval_date)


def _as_float(value: object) -> float:
    """Convert API numeric strings to floats, treating missing values as zero."""

    try:
        return float(str(value or 0))
    except (TypeError, ValueError):
        return 0.0


def select_series(series: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    """Select the highest-volume series in theory-relevant categories."""

    eligible = [row for row in series if row.get("category") in KALSHI_CATEGORIES]
    return sorted(
        eligible,
        key=lambda row: (-_as_float(row.get("volume_fp")), str(row.get("ticker", ""))),
    )[:limit]


def _series_markets(
    client: PublicApiClient,
    series_ticker: str,
    limit: int,
) -> list[dict[str, Any]]:
    """Fetch archived and live markets for one series."""

    archived = client.get_json(
        f"{KALSHI_BASE_URL}/historical/markets",
        {"series_ticker": series_ticker, "limit": limit},
    ).get("markets", [])
    live = client.get_json(
        f"{KALSHI_BASE_URL}/markets",
        {"series_ticker": series_ticker, "limit": limit},
    ).get("markets", [])
    by_ticker = {str(row["ticker"]): row for row in [*archived, *live]}
    return [by_ticker[key] for key in sorted(by_ticker)]


def validate_kalshi_snapshot(payload: dict[str, Any], config: SampleConfig) -> None:
    """Reject reuse with changed category, series-limit, or per-tier sampling caps."""

    validate_snapshot_date(payload, config.retrieval_date, "Kalshi")
    selection = payload.get("selection")
    expected = {
        "categories": list(KALSHI_CATEGORIES),
        "series_limit": config.kalshi_series_limit,
        "markets_per_series_tier": config.kalshi_markets_per_series,
    }
    if not isinstance(selection, dict):
        raise ValueError("Kalshi snapshot does not record its sampling parameters")
    for parameter, value in expected.items():
        if selection.get(parameter) != value:
            raise ValueError(
                f"Kalshi cached sampling parameter {parameter!r} is "
                f"{selection.get(parameter)!r}; requested {value!r}. "
                "The immutable snapshot cannot serve this sample configuration."
            )


def download_kalshi(config: SampleConfig, client: PublicApiClient) -> dict[str, Any]:
    """Download or load the date-stamped Kalshi metadata snapshot."""

    path = kalshi_snapshot_path(config)
    if path.exists():
        LOGGER.info("Using cached Kalshi snapshot: %s", path)
        payload = read_json(path)
        if not isinstance(payload, dict):
            raise TypeError("Kalshi snapshot must contain a JSON object")
        validate_kalshi_snapshot(payload, config)
        return payload

    require_current_acquisition_date(path, config.retrieval_date)
    catalog = client.get_json(
        f"{KALSHI_BASE_URL}/series",
        {"include_volume": "true"},
    ).get("series", [])
    chosen = select_series(catalog, config.kalshi_series_limit)
    markets: list[dict[str, Any]] = []
    for position, series in enumerate(chosen, start=1):
        ticker = str(series["ticker"])
        LOGGER.info("Kalshi series %d/%d: %s", position, len(chosen), ticker)
        rows = _series_markets(client, ticker, config.kalshi_markets_per_series)
        for row in rows:
            row["sample_series_ticker"] = ticker
            row["sample_category"] = series.get("category")
            row["series_title"] = series.get("title")
            row["series_settlement_sources"] = series.get("settlement_sources", [])
        markets.extend(rows)

    cutoff = client.get_json(f"{KALSHI_BASE_URL}/historical/cutoff")
    payload = {
        **acquisition_metadata(config.retrieval_date),
        "selection": {
            "categories": list(KALSHI_CATEGORIES),
            "series_limit": config.kalshi_series_limit,
            "markets_per_series_tier": config.kalshi_markets_per_series,
        },
        "historical_cutoff": cutoff,
        "selected_series": chosen,
        "markets": markets,
    }
    write_immutable_json(path, payload)
    LOGGER.info("Saved %d Kalshi markets to %s", len(markets), path)
    return payload
