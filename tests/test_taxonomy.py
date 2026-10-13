"""Tests for substantive sports classification and its reason ledger."""

import pytest

from src.taxonomy import classify_polymarket_sports


@pytest.mark.parametrize(
    ("market_id", "question"),
    [
        ("521607", "Ukraine agrees to a minerals deal before April?"),
        ("546814", "Will Zelenskyy wear a suit before July?"),
    ],
)
def test_game_start_time_does_not_exclude_nonsports(market_id: str, question: str) -> None:
    """The named historical false positives need substantive sport evidence."""

    decision, reason = classify_polymarket_sports(
        {"id": market_id, "question": question, "gameStartTime": "2025-01-01T00:00:00Z"}
    )
    assert not decision
    assert reason == "game_start_time_without_sports_evidence"


@pytest.mark.parametrize(
    ("row", "reason"),
    [
        ({"sportsMarketType": "moneyline"}, "sports_market_type"),
        ({"question": "Will Club A win the FIFA Club World Cup?"}, "sports_text:fifa"),
        ({"events": [{"tags": [{"label": "Sports"}]}]}, "sports_category_or_tag"),
        ({"id": "514435", "question": "Will Everton vs. Liverpool end in a draw?",
          "description": "In the upcoming EPL game, scheduled for December 7.",
          "gameStartTime": "2024-12-07T00:00:00Z"}, "sports_game_phrase:epl game"),
    ],
)
def test_actual_sports_have_reason_codes(row: dict[str, object], reason: str) -> None:
    """Explicit type, substantive taxonomy and category evidence stay auditable."""

    assert classify_polymarket_sports(row) == (True, reason)


def test_generic_tournament_does_not_by_itself_prove_sports() -> None:
    """An ambiguous tournament word requires a substantive sport cue."""

    assert not classify_polymarket_sports({"question": "Will X win the AI coding tournament?"})[0]
