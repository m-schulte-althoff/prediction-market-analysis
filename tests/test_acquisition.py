"""Focused offline checks for immutable acquisition provenance and cache reuse."""

from __future__ import annotations

from collections.abc import Callable
from copy import deepcopy
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

import pytest

import src.config as config_module
from src.config import KALSHI_BASE_URL, KALSHI_CATEGORIES, POLYMARKET_GAMMA_URL, SampleConfig
from src.http_client import PublicApiClient
from src.io_utils import write_immutable_json
from src.kalshi import download_kalshi, kalshi_snapshot_path
from src.polymarket import download_polymarket, polymarket_snapshot_path

ACQUISITION_TIME = datetime(2026, 10, 13, 14, 15, 16, tzinfo=UTC)
HISTORICAL_DATE = date(2026, 9, 10)
Downloader = Callable[[SampleConfig, PublicApiClient], dict[str, Any]]
SnapshotPath = Callable[[SampleConfig], Path]


class RecordingClient(PublicApiClient):
    """Record injected requests and never access the public network."""

    def __init__(self, responses: dict[str, Any] | None = None) -> None:
        self.responses = responses or {}
        self.calls: list[tuple[str, dict[str, Any] | None]] = []

    def get_json(self, url: str, params: dict[str, Any] | None = None) -> Any:
        """Return a fresh fixture response, failing for unexpected requests."""

        self.calls.append((url, params))
        if url not in self.responses:
            raise AssertionError(f"Unexpected API request: {url}")
        return deepcopy(self.responses[url])


@pytest.fixture(autouse=True)
def isolated_acquisition_paths(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Keep all test snapshots local and make the UTC clock deterministic."""

    monkeypatch.setattr(config_module, "RAW_DIR", tmp_path)
    monkeypatch.setattr(config_module, "utc_now", lambda: ACQUISITION_TIME)


def _legacy_kalshi_payload() -> dict[str, Any]:
    """Represent the original archive format with a per-tier cap and no UTC time."""

    return {
        "retrieved_at_date": HISTORICAL_DATE.isoformat(),
        "selection": {
            "categories": list(KALSHI_CATEGORIES),
            "series_limit": 120,
            "markets_per_series_tier": 1_000,
        },
        "markets": [],
    }


def _legacy_polymarket_payload() -> dict[str, Any]:
    """Represent the original archive format without inventing its missing fields."""

    return {
        "retrieved_at_date": HISTORICAL_DATE.isoformat(),
        "selection": {
            "closed": True,
            "sports_excluded_before_volume_cap": True,
            "order": "volumeNum descending",
            "limit": 8_000,
            "raw_rows_scanned": 23_700,
        },
        "markets": [],
    }


@pytest.mark.parametrize("downloader", [download_kalshi, download_polymarket])
def test_missing_historical_snapshot_fails_before_network(downloader: Downloader) -> None:
    """Current public responses cannot be labeled as an absent historical cache."""

    client = RecordingClient()

    with pytest.raises(FileNotFoundError, match="Historical snapshot is absent"):
        downloader(SampleConfig(retrieval_date=HISTORICAL_DATE), client)

    assert client.calls == []


@pytest.mark.parametrize("downloader", [download_kalshi, download_polymarket])
def test_future_snapshot_label_fails_before_network(downloader: Downloader) -> None:
    """New acquisition also cannot be given a future date label."""

    client = RecordingClient()

    with pytest.raises(ValueError, match="in the future"):
        downloader(SampleConfig(retrieval_date=date(2026, 10, 14)), client)

    assert client.calls == []


@pytest.mark.parametrize(
    ("downloader", "snapshot_path", "legacy_payload"),
    [
        (download_kalshi, kalshi_snapshot_path, _legacy_kalshi_payload),
        (download_polymarket, polymarket_snapshot_path, _legacy_polymarket_payload),
    ],
)
def test_legacy_snapshot_is_loaded_without_mutation_or_invented_timestamp(
    downloader: Downloader,
    snapshot_path: SnapshotPath,
    legacy_payload: Callable[[], dict[str, Any]],
) -> None:
    """Compatible old archives remain exactly as saved and cause no requests."""

    config = SampleConfig(retrieval_date=HISTORICAL_DATE)
    path = snapshot_path(config)
    payload = legacy_payload()
    assert write_immutable_json(path, payload)
    original_bytes = path.read_bytes()
    client = RecordingClient()

    result = downloader(config, client)

    assert result == payload
    assert "acquired_at_utc" not in result
    assert path.read_bytes() == original_bytes
    assert not write_immutable_json(path, {"replacement": "forbidden"})
    assert path.read_bytes() == original_bytes
    assert client.calls == []


def test_cached_kalshi_per_tier_cap_must_match_requested_sample() -> None:
    """The series-only filename cannot conceal a changed market cap."""

    config = SampleConfig(retrieval_date=HISTORICAL_DATE, kalshi_markets_per_series=500)
    path = kalshi_snapshot_path(config)
    write_immutable_json(path, _legacy_kalshi_payload())
    original_bytes = path.read_bytes()
    client = RecordingClient()

    with pytest.raises(ValueError, match="markets_per_series_tier"):
        download_kalshi(config, client)

    assert client.calls == []
    assert path.read_bytes() == original_bytes


def test_cached_polymarket_page_size_must_match_when_recorded() -> None:
    """Known acquisition settings are validated even though legacy fields may be absent."""

    config = SampleConfig(retrieval_date=HISTORICAL_DATE, polymarket_page_size=50)
    payload = _legacy_polymarket_payload()
    payload["selection"]["page_size"] = 100
    write_immutable_json(polymarket_snapshot_path(config), payload)
    client = RecordingClient()

    with pytest.raises(ValueError, match="page_size"):
        download_polymarket(config, client)

    assert client.calls == []


@pytest.mark.parametrize(
    ("downloader", "snapshot_path", "legacy_payload"),
    [
        (download_kalshi, kalshi_snapshot_path, _legacy_kalshi_payload),
        (download_polymarket, polymarket_snapshot_path, _legacy_polymarket_payload),
    ],
)
def test_recorded_snapshot_date_must_match_label(
    downloader: Downloader,
    snapshot_path: SnapshotPath,
    legacy_payload: Callable[[], dict[str, Any]],
) -> None:
    """A misdated file cannot pass validation merely because its filename matches."""

    config = SampleConfig(retrieval_date=HISTORICAL_DATE)
    payload = legacy_payload()
    payload["retrieved_at_date"] = "2026-09-11"
    write_immutable_json(snapshot_path(config), payload)
    client = RecordingClient()

    with pytest.raises(ValueError, match="snapshot date"):
        downloader(config, client)

    assert client.calls == []


def test_new_kalshi_responses_record_actual_utc_time_and_per_tier_parameters() -> None:
    """The new source version records completion time and actual request caps."""

    config = SampleConfig(kalshi_series_limit=1, kalshi_markets_per_series=2)
    client = RecordingClient(
        {
            f"{KALSHI_BASE_URL}/series": {
                "series": [{"ticker": "KXTEST", "category": "Politics", "volume_fp": "4"}]
            },
            f"{KALSHI_BASE_URL}/historical/markets": {"markets": [{"ticker": "KXOLD"}]},
            f"{KALSHI_BASE_URL}/markets": {"markets": [{"ticker": "KXNEW"}]},
            f"{KALSHI_BASE_URL}/historical/cutoff": {"market_settled_ts": "2025-01-01"},
        }
    )

    payload = download_kalshi(config, client)

    assert config.retrieval_date == ACQUISITION_TIME.date()
    assert payload["retrieved_at_date"] == "2026-10-13"
    assert payload["acquired_at_utc"] == ACQUISITION_TIME.isoformat()
    assert payload["selection"]["markets_per_series_tier"] == 2
    for url, parameters in client.calls:
        if url.endswith("/markets"):
            assert parameters == {"series_ticker": "KXTEST", "limit": 2}
    assert [row["ticker"] for row in payload["markets"]] == ["KXNEW", "KXOLD"]


def test_new_polymarket_responses_record_utc_time_and_declared_filter() -> None:
    """New selection metadata distinguishes the current filter from legacy archives."""

    config = SampleConfig(polymarket_limit=1, polymarket_page_size=50)
    client = RecordingClient(
        {
            f"{POLYMARKET_GAMMA_URL}/markets/keyset": {
                "markets": [{"id": "2", "question": "Will X happen?"}],
                "next_cursor": "",
            }
        }
    )

    payload = download_polymarket(config, client)

    assert payload["retrieved_at_date"] == "2026-10-13"
    assert payload["acquired_at_utc"] == ACQUISITION_TIME.isoformat()
    assert payload["selection"]["page_size"] == 50
    assert payload["selection"]["sports_filter_version"] == "substantive-sports-v3"
    assert client.calls[0][1] == {
        "limit": 50,
        "closed": "true",
        "order": "volumeNum",
        "ascending": "false",
    }
