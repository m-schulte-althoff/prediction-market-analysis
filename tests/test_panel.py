"""Tests for matched price alignment."""

from datetime import UTC, datetime

from src.panel import build_matched_panel, summarize_matched_panel


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
