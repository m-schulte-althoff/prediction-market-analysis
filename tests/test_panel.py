"""Tests for matched price alignment."""

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd
import pytest

from src.config import SampleConfig
from src.panel import (
    _uses_historical_endpoint,
    build_matched_panel,
    download_matched_histories,
    summarize_matched_panel,
)


def _ts(day: int) -> int:
    """Return a deterministic UTC timestamp in January 2025."""

    return int(datetime(2025, 1, day, tzinfo=UTC).timestamp())


def test_panel_uses_yes_prices_and_absolute_disagreement() -> None:
    """A tiny understandable pair yields the exact expected disagreement."""

    payload = {
        "pairs": [
            {
                "match": {
                    "underlying_event_id": "match:one",
                    "kalshi_question": "Will X?",
                    "polymarket_question": "Will X?",
                    "semantic_divergence": 0.2,
                    "match_confidence": 0.9,
                    "aligned_end": "2025-01-03T00:00:00+00:00",
                },
                "kalshi": {
                    "candlesticks": [
                        {
                            "end_period_ts": _ts(1),
                            "price": {"close": "0.40"},
                            "yes_bid": {"close": "0.38"},
                            "yes_ask": {"close": "0.42"},
                            "volume": "10",
                        },
                        {
                            "end_period_ts": _ts(2),
                            "price": {"close": "0.60"},
                            "yes_bid": {"close": "0.58"},
                            "yes_ask": {"close": "0.62"},
                            "volume": "15",
                        },
                    ]
                },
                "polymarket": {
                    "history": [{"t": _ts(1), "p": 0.5}, {"t": _ts(2), "p": 0.65}]
                },
            }
        ]
    }

    panel = build_matched_panel(payload)
    summary = summarize_matched_panel(panel)

    assert panel["disagreement"].round(2).tolist() == [0.10, 0.05]
    assert summary.iloc[0]["observations"] == 2
    assert round(summary.iloc[0]["mean_disagreement"], 3) == 0.075


def test_original_observations_are_clipped_before_daily_aggregation() -> None:
    """A same-day observation after the contract cutoff must not become its final price."""

    end = _ts(3)
    payload = {"pairs": [{
        "match": {"underlying_event_id": "match:boundary", "kalshi_question": "Will X?",
                  "polymarket_question": "Will X?", "semantic_divergence": 0.2,
                  "match_confidence": 0.9, "aligned_start": "2025-01-01T00:00:00Z",
                  "aligned_end": "2025-01-03T00:00:00Z"},
        "kalshi": {"candlesticks": [{"end_period_ts": _ts(1), "price": {"close": "0.4"}},
                                     {"end_period_ts": end + 1, "price": {"close": "0.9"}}]},
        "polymarket": {"history": [{"t": _ts(1) + 3600, "p": 0.5},
                                      {"t": _ts(2) + 3600, "p": 0.6},
                                      {"t": end + 3600, "p": 0.99}]},
    }]}
    panel = build_matched_panel(payload)
    assert panel["polymarket_price"].tolist() == [0.5, 0.6]
    assert panel["kalshi_price"].tolist() == [0.4, 0.4]
    assert (panel["timestamp"] <= pd.Timestamp(end, unit="s", tz="UTC")).all()
    assert (panel["polymarket_source_timestamp"] <= panel["timestamp"]).all()
    assert panel["kalshi_forward_filled"].tolist() == [False, True]
    assert panel["kalshi_fill_age_hours"].tolist() == [24.0, 48.0]
    assert not panel["synchronized_price_test_eligible"].any()


def test_exact_endpoint_does_not_duplicate_as_of_timestamp() -> None:
    """An exact midnight observation and the prior bucket have one diagnostic weight."""

    payload = {"pairs": [{
        "match": {"underlying_event_id": "match:midnight", "kalshi_question": "Will X?",
                  "polymarket_question": "Will X?", "semantic_divergence": 0.2,
                  "match_confidence": 0.9, "aligned_start": "2025-01-01T00:00:00Z",
                  "aligned_end": "2025-01-02T00:00:00Z"},
        "kalshi": {"candlesticks": [{"end_period_ts": _ts(1), "price": {"close": "0.4"}},
                                     {"end_period_ts": _ts(2), "price": {"close": "0.6"}}]},
        "polymarket": {"history": [{"t": _ts(1) + 3600, "p": 0.5},
                                      {"t": _ts(2), "p": 0.7}]},
    }]}
    panel = build_matched_panel(payload)
    assert not panel.duplicated(["underlying_event_id", "timestamp"]).any()
    assert panel["kalshi_price"].tolist() == [0.6]
    assert panel["polymarket_price"].tolist() == [0.7]


class _NoNetworkClient:
    """Fail immediately if a historical-cache test touches the network."""

    def get_json(self, *args: object, **kwargs: object) -> dict[str, Any]:
        """Reject unexpected public API requests."""

        raise AssertionError("No network call is permitted for historical cache misses")


def test_missing_historical_panel_does_not_download(monkeypatch: pytest.MonkeyPatch,
                                                   tmp_path: Path) -> None:
    """An absent selected-ID cache cannot be recreated with fresh historical labels."""

    from datetime import date

    monkeypatch.setattr("src.panel.RAW_DIR", tmp_path)
    matches = pd.DataFrame(columns=["match_label", "kalshi_ticker", "polymarket_id",
                                   "polymarket_yes_token_id", "kalshi_open_timestamp",
                                   "kalshi_close_timestamp", "match_confidence",
                                   "underlying_event_id"])
    config = SampleConfig(retrieval_date=date(2000, 1, 1))
    with pytest.raises(FileNotFoundError, match="historical"):
        download_matched_histories(matches, config, _NoNetworkClient())  # type: ignore[arg-type]


def test_explicit_saved_panel_is_loaded_without_matching_selected_hash(tmp_path: Path) -> None:
    """The user may explicitly reproduce an older immutable selected-pair archive."""

    from datetime import date

    path = tmp_path / "matched-price-histories-2000-01-01-bad72f8883-interval-max.json"
    path.write_text('{"retrieved_at_date": "2000-01-01", "pairs": []}')
    matches = pd.DataFrame(columns=["match_label", "kalshi_ticker", "polymarket_id",
                                   "polymarket_yes_token_id", "kalshi_open_timestamp",
                                   "kalshi_close_timestamp", "match_confidence",
                                   "underlying_event_id"])
    payload = download_matched_histories(
        matches, SampleConfig(retrieval_date=date(2000, 1, 1)),
        _NoNetworkClient(),  # type: ignore[arg-type]
        snapshot_path=path,
    )
    assert payload["pairs"] == []


def test_historical_routing_uses_settlement_timestamp() -> None:
    """An old scheduled close cannot substitute for settlement before the cutoff."""

    cutoff = pd.Timestamp("2025-07-01", tz="UTC")
    assert _uses_historical_endpoint("2025-06-30T23:59:59Z", cutoff)
    assert not _uses_historical_endpoint("2025-07-01T00:00:00Z", cutoff)
    assert not _uses_historical_endpoint(None, cutoff)
