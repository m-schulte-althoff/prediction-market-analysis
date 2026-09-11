"""Acquire high-volume closed Polymarket metadata and token price histories."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from src.config import POLYMARKET_GAMMA_URL, SampleConfig, dated_raw_path
from src.http_client import PublicApiClient
from src.io_utils import read_json, write_immutable_json
from src.taxonomy import is_polymarket_sports

LOGGER = logging.getLogger(__name__)


def polymarket_snapshot_path(config: SampleConfig) -> Path:
    """Return a versioned path because the requested sample size affects raw content."""

    return dated_raw_path(
        f"polymarket-nonsports-markets-v2-n{config.polymarket_limit}", config.retrieval_date
    )


def download_polymarket(config: SampleConfig, client: PublicApiClient) -> dict[str, Any]:
    """Download or load a date-stamped high-volume Polymarket snapshot."""

    path = polymarket_snapshot_path(config)
    if path.exists():
        LOGGER.info("Using cached Polymarket snapshot: %s", path)
        payload = read_json(path)
        if not isinstance(payload, dict):
            raise TypeError("Polymarket snapshot must contain a JSON object")
        return payload

    markets: list[dict[str, Any]] = []
    scanned = 0
    cursor = ""
    while len(markets) < config.polymarket_limit:
        LOGGER.info(
            "Polymarket non-sports markets %d/%d (%d raw rows scanned)",
            len(markets),
            config.polymarket_limit,
            scanned,
        )
        parameters = {
            "limit": config.polymarket_page_size,
            "closed": "true",
            "order": "volumeNum",
            "ascending": "false",
        }
        if cursor:
            parameters["after_cursor"] = cursor
        page = client.get_json(f"{POLYMARKET_GAMMA_URL}/markets/keyset", parameters)
        if not isinstance(page, dict) or not isinstance(page.get("markets"), list):
            raise TypeError("Polymarket keyset endpoint returned an unexpected payload")
        page_markets = page["markets"]
        scanned += len(page_markets)
        markets.extend(row for row in page_markets if not is_polymarket_sports(row))
        next_cursor = str(page.get("next_cursor") or "")
        if not page_markets or not next_cursor or next_cursor == cursor:
            break
        cursor = next_cursor

    selected = markets[: config.polymarket_limit]
    by_id = {str(row["id"]): row for row in selected}
    payload = {
        "retrieved_at_date": config.retrieval_date.isoformat(),
        "selection": {
            "closed": True,
            "sports_excluded_before_volume_cap": True,
            "order": "volumeNum descending",
            "limit": config.polymarket_limit,
            "raw_rows_scanned": scanned,
        },
        "markets": [by_id[key] for key in sorted(by_id, key=lambda value: int(value))],
    }
    write_immutable_json(path, payload)
    LOGGER.info("Saved %d Polymarket markets to %s", len(by_id), path)
    return payload
