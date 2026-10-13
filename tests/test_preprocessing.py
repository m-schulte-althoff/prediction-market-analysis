"""Tests for platform-schema normalization."""

import pytest

from src.preprocessing import build_contract_table, normalization_ledger, normalize_polymarket


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
                "umaResolutionStatus": "resolved",
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


def test_extra_outcome_is_excluded() -> None:
    """A YES/NO prefix does not make a three-outcome vector binary."""

    result = normalize_polymarket({"markets": [{
        "id": "extra", "question": "Will X happen?",
        "outcomes": '["Yes", "No", "Other"]', "outcomePrices": '["1", "0", "0"]',
    }]})
    assert result.empty


def test_reversed_binary_vectors_preserve_yes_orientation() -> None:
    """YES token and price must follow their label, including reversed ordering."""

    result = normalize_polymarket({"markets": [{
        "id": "reverse", "question": "Will X happen?", "outcomes": '["No", "Yes"]',
        "outcomePrices": '["0", "1"]', "clobTokenIds": '["no-token", "yes-token"]',
        "umaResolutionStatus": "settled", "closed": True,
    }]})
    assert result["outcome"].iloc[0] == "yes"
    assert result["yes_token_id"].iloc[0] == "yes-token"
    assert result["outcome_evidence"].iloc[0] == "price_inferred_settled"


@pytest.mark.parametrize("status", [None, "proposed", "disputed"])
def test_extreme_price_does_not_prove_final_resolution(status: str | None) -> None:
    """Closed and extreme-price records without final status retain explicit inference."""

    result = normalize_polymarket({"markets": [{
        "id": "inferred", "question": "Will X happen?", "outcomes": '["Yes", "No"]',
        "outcomePrices": '["1", "0"]', "closed": True, "umaResolutionStatus": status,
    }]})
    assert result["outcome"].iloc[0] == ""
    assert result["price_inferred_outcome"].iloc[0] == "yes"
    assert result["outcome_evidence"].iloc[0] == f"price_inferred_{status or 'missing_status'}"


def test_scalar_and_intermediate_price_are_separate_categories() -> None:
    """An explicit fractional payout differs from an intermediate archived price."""

    result = build_contract_table(
        {"markets": [{"ticker": "SCALAR", "title": "Will X happen?", "result": "scalar",
                      "status": "finalized", "settlement_value_dollars": "0.45"}]},
        {"markets": [{"id": "fraction", "question": "Will X happen?",
                      "outcomes": '["Yes", "No"]', "outcomePrices": '["0.5", "0.5"]',
                      "umaResolutionStatus": "resolved"}]},
    )
    assert result["outcome_category"].tolist() == ["scalar_settlement", "intermediate_price"]
    assert result["yes_settlement_payoff"].iloc[0] == pytest.approx(0.45)
    assert result["yes_settlement_payoff"].iloc[1] != result["yes_settlement_payoff"].iloc[1]


def test_unaligned_vectors_do_not_guess_tokens_or_prices() -> None:
    """Missing vector entries remain observable rather than silently assigned to YES."""

    result = normalize_polymarket({"markets": [{
        "id": "short", "question": "Will X happen?", "outcomes": '["Yes", "No"]',
        "outcomePrices": '["1"]', "clobTokenIds": '["only-token"]',
        "umaResolutionStatus": "resolved",
    }]})
    assert result["outcome"].iloc[0] == ""
    assert result["yes_token_id"].iloc[0] == ""
    assert not result["outcome_prices_aligned"].iloc[0]
    assert not result["outcome_tokens_aligned"].iloc[0]


def test_normalization_ledger_reconciles_raw_rows_and_retention() -> None:
    """Attrition reasons preserve raw positions and distinguish filtering from duplicates."""

    payload = {"markets": [
        {"id": "same", "question": "Will X happen?", "outcomes": '["Yes", "No"]'},
        {"id": "same", "question": "Will X happen?", "outcomes": '["Yes", "No"]'},
        {"id": "extra", "question": "Will X happen?", "outcomes": '["Yes", "No", "A"]'},
        {"id": "empty", "question": "", "outcomes": '["Yes", "No"]'},
    ]}
    ledger = normalization_ledger(payload, "Polymarket")
    assert ledger["normalization_reason"].tolist() == [
        "duplicate_keep_last", "retained", "unsupported_binary_labels", "question_length_le4"
    ]
    assert len(normalize_polymarket(payload)) == (ledger.normalization_reason == "retained").sum()


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
