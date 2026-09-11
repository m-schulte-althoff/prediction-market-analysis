"""Tests for the witness-state representation casebook."""

from src.anecdotes import build_representation_case_matrix


def _poly_market(slug: str, question: str) -> dict[str, str]:
    """Build a minimal official-market fixture."""

    return {"id": slug, "slug": slug, "question": question, "description": f"Rules for {slug}."}


def test_case_matrix_requires_witnesses_and_distinguishes_indeterminacy() -> None:
    """Every coded mechanism has a witness and does not conflate the constructs."""

    payload = {
        "retrieved_at_date": "2026-09-11",
        "kalshi_events": {
            "KXPRESPERSON-28": {
                "markets": [
                    {
                        "ticker": "KXPRESPERSON-28-MRUB",
                        "title": "Who wins?",
                        "rules_primary": "Inaugurated.",
                    }
                ]
            },
            "KXFEDDECISION-26SEP": {
                "markets": [
                    {
                        "ticker": "KXFEDDECISION-26SEP-C25",
                        "title": "25 bp cut?",
                        "rules_primary": "Exactly 25 bp.",
                    }
                ]
            },
        },
        "polymarket_events": {
            "presidential-election-winner-2028": {
                "markets": [
                    _poly_market(
                        "will-marco-rubio-win-the-2028-us-presidential-election", "Rubio wins?"
                    )
                ]
            },
            "fed-decision-in-september-762": {
                "markets": [
                    _poly_market(
                        "will-the-fed-decrease-interest-rates-by-25-bps-after-the-september-2026-meeting-586",
                        "25 bp decrease?",
                    )
                ]
            },
            "ukraine-agrees-to-give-trump-rare-earth-metals-before-april": {
                "markets": [
                    _poly_market(
                        "ukraine-agrees-to-give-trump-rare-earth-metals-before-april", "Agreement?"
                    )
                ]
            },
            "trump-x-ukraine-mineral-deal-signed-before-may": {
                "markets": [
                    _poly_market(
                        "trump-x-ukraine-mineral-deal-signed-before-may", "Signed agreement?"
                    )
                ]
            },
            "will-zelenskyy-wear-a-suit-before-july": {
                "markets": [
                    _poly_market("will-zelenskyy-wear-a-suit-before-july", "Suit?")
                ]
            },
        },
    }

    result = build_representation_case_matrix(payload)

    assert len(result) == 4
    assert result["witness_state"].str.len().gt(20).all()
    suit = result.loc[result["case_id"] == "suit-category-boundary"].iloc[0]
    assert bool(suit["determinacy_issue"])
    assert not bool(suit["truth_condition_divergent"])
