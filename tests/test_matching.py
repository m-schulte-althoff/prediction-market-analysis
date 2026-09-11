"""Tests for precision-oriented cross-platform event matching."""

import pandas as pd

from src.matching import match_contracts


def _contract(
    contract_id: str,
    platform: str,
    question: str,
    close: str,
) -> dict[str, object]:
    """Build a minimal normalized contract fixture."""

    return {
        "contract_id": contract_id,
        "platform": platform,
        "platform_contract_id": contract_id.split(":", 1)[1],
        "question": question,
        "rules": f"{question} according to Reuters.",
        "resolution_source": "Reuters",
        "open_timestamp": pd.Timestamp("2024-01-01", tz="UTC"),
        "close_timestamp": pd.Timestamp(close, tz="UTC"),
        "series": "SERIES",
        "yes_token_id": "token-123456",
        "volume": 100.0,
    }


def test_exact_same_event_is_high_confidence() -> None:
    """Near-identical questions with equal dates pass conservative gates."""

    frame = pd.DataFrame(
        [
            _contract(
                "kalshi:TRUMP24",
                "Kalshi",
                "Will Donald Trump win the 2024 US Presidential Election?",
                "2024-11-05",
            ),
            _contract(
                "polymarket:42",
                "Polymarket",
                "Will Donald Trump win the 2024 US Presidential Election?",
                "2024-11-05",
            ),
        ]
    )

    result = match_contracts(frame, neighbors=1)

    assert len(result) == 1
    assert result.iloc[0]["match_label"] == "high_confidence"
    assert result.iloc[0]["lexical_similarity"] > 0.99


def test_same_words_but_remote_deadlines_are_not_accepted() -> None:
    """Lexical similarity cannot override an incompatible event window."""

    frame = pd.DataFrame(
        [
            _contract("kalshi:X", "Kalshi", "Will X happen in 2024?", "2024-12-31"),
            _contract("polymarket:X", "Polymarket", "Will X happen in 2024?", "2026-12-31"),
        ]
    )

    result = match_contracts(frame, neighbors=1)

    assert result.iloc[0]["match_label"] == "rejected"


def test_margin_threshold_is_not_same_contract_as_winner() -> None:
    """A shared election does not make a victory-margin claim a winner claim."""

    frame = pd.DataFrame(
        [
            _contract(
                "kalshi:MARGIN",
                "Kalshi",
                "Will the margin of victory for Smith in the 2026 primary be above 15%?",
                "2026-08-01",
            ),
            _contract(
                "polymarket:WIN",
                "Polymarket",
                "Will Smith win the 2026 primary?",
                "2026-08-01",
            ),
        ]
    )

    result = match_contracts(frame, neighbors=1)

    assert not bool(result.iloc[0]["predicate_compatible"])
    assert result.iloc[0]["match_label"] != "high_confidence"
