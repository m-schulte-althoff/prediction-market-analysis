"""Tests for platform-schema normalization."""

import pytest

from src.preprocessing import build_contract_table, normalize_polymarket


def test_build_contract_table_orients_yes_outcomes() -> None:
    """Both platform rows use YES as the probability/outcome orientation."""

    kalshi = {
        "markets": [
            {
                "ticker": "KX-ONE",
                "event_ticker": "EVENT-ONE",
                "title": "Will X happen?",
                "rules_primary": "Yes if X happens.",
                "result": "yes",
                "open_time": "2025-01-01T00:00:00Z",
                "close_time": "2025-02-01T00:00:00Z",
                "settlement_ts": "2025-02-02T00:00:00Z",
                "volume_fp": "12.5",
                "sample_category": "Politics",
                "sample_series_ticker": "KX",
            }
        ]
    }
    polymarket = {
        "markets": [
            {
                "id": "2",
                "question": "Will X happen?",
                "description": "Resolves Yes if X happens.",
                "outcomes": '["Yes", "No"]',
                "outcomePrices": '["0", "1"]',
                "clobTokenIds": '["yes-token", "no-token"]',
                "startDate": "2025-01-01T00:00:00Z",
                "endDate": "2025-02-01T00:00:00Z",
                "closedTime": "2025-02-02T00:00:00Z",
                "volumeNum": 30,
                "events": [{"id": "event-2", "ticker": "x-event"}],
            }
        ]
    }

    result = build_contract_table(kalshi, polymarket)

    assert result["outcome"].tolist() == ["yes", "no"]
    assert result.loc[result["platform"] == "Polymarket", "yes_token_id"].iloc[0] == "yes-token"
    assert result["market_duration_days"].tolist() == [31.0, 31.0]


def test_non_binary_polymarket_contract_is_excluded() -> None:
    """Scalar or categorical markets cannot silently enter binary YES analysis."""

    result = normalize_polymarket(
        {
            "markets": [
                {
                    "id": "3",
                    "question": "Who wins?",
                    "outcomes": '["A", "B"]',
                    "outcomePrices": '["1", "0"]',
                }
            ]
        }
    )

    assert result.empty


def test_official_sports_flags_exclude_polymarket_contract() -> None:
    """Sports rows do not contaminate the deliberately non-sports design."""

    result = normalize_polymarket(
        {
            "markets": [
                {
                    "id": "4",
                    "question": "Will Team A win?",
                    "outcomes": '["Yes", "No"]',
                    "outcomePrices": '["1", "0"]',
                    "sportsMarketType": "moneyline",
                }
            ]
        }
    )

    assert result.empty


def test_sports_taxonomy_excludes_unflagged_tournament_contract() -> None:
    """Tournament families lacking official game flags remain outside the design."""

    result = normalize_polymarket(
        {
            "markets": [
                {
                    "id": "5",
                    "question": "Will Club A win the FIFA Club World Cup?",
                    "description": "Resolves according to the FIFA tournament winner.",
                    "outcomes": '["Yes", "No"]',
                    "outcomePrices": '["1", "0"]',
                }
            ]
        }
    )

    assert result.empty


def test_mixed_timestamp_formats_preserve_polymarket_resolution_dates() -> None:
    """Pandas mixed ISO precision must not erase otherwise valid closure timestamps."""

    result = normalize_polymarket(
        {
            "retrieved_at_date": "2026-09-10",
            "markets": [
                {
                    "id": "6",
                    "question": "Will X happen by 2026?",
                    "description": "Resolves Yes if X happens.",
                    "outcomes": '["Yes", "No"]',
                    "outcomePrices": '["1", "0"]',
                    "startDate": "2025-01-01T00:00:00Z",
                    "endDate": "2025-03-01T00:00:00.123456Z",
                    "closedTime": "2025-03-02T12:34:56Z",
                }
            ],
        }
    )

    assert result["resolution_timestamp"].notna().all()
    assert result["resolution_year"].iloc[0] == 2025
    assert result["observed_exposure_days"].iloc[0] == pytest.approx(59.0, abs=0.001)
