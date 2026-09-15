"""Tests for the witness-state representation casebook."""

import hashlib
import json
from pathlib import Path

import pandas as pd
import pytest

from src.anecdotes import (
    CLAIM_AUDITS,
    add_claim_relations,
    build_representation_case_matrix,
    write_casebook,
)
from src.coherence import ClaimRelation


def _poly_market(slug: str, question: str) -> dict[str, str]:
    """Build a minimal official-market fixture."""

    return {"id": slug, "slug": slug, "question": question, "description": f"Rules for {slug}."}


def test_case_matrix_requires_witnesses_and_distinguishes_indeterminacy(tmp_path: Path) -> None:
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
    assert result.claim_relation.eq("unclassified").all()
    assert not result.claim_relation_validated.any()
    assert not result.coherence_test_applicable.any()
    assert result.probability_coherence_implication.eq("none").all()
    assert result.claim_relation_basis.str.contains("manual review required").all()
    path = tmp_path / "casebook.md"
    write_casebook(path, result)
    assert "Claim relation: unclassified" in path.read_text(encoding="utf-8")


def test_claim_audit_requires_same_rules_and_ids(monkeypatch: pytest.MonkeyPatch) -> None:
    """A validated relation must not transfer to a changed contract or rule version."""

    payload = [["A", "YES if X."], ["B", "YES if X or Y."]]
    fingerprint = hashlib.sha256(json.dumps(payload, ensure_ascii=False).encode()).hexdigest()
    monkeypatch.setitem(CLAIM_AUDITS, "synthetic", (
        fingerprint, ClaimRelation.SUBSET, "determinate_binary", "Synthetic full-rule proof.",
    ))
    cases = pd.DataFrame([{
        "case_id": "synthetic", "a_contract_id": "A", "a_rule": "YES if X.",
        "b_contract_id": "B", "b_rule": "YES if X or Y.",
    }])
    result = add_claim_relations(cases).iloc[0]
    assert result.claim_relation == "subset"
    assert result.coherence_test_applicable
    assert result.probability_coherence_implication == "q_A <= q_B"
    whitespace = cases.copy()
    whitespace.loc[0, "a_rule"] = "YES  if\nX."
    assert add_claim_relations(whitespace).iloc[0].claim_relation_validated
    for column in ("a_contract_id", "b_contract_id", "a_rule", "b_rule"):
        changed = cases.copy()
        changed.loc[0, column] = "different"
        record = add_claim_relations(changed).iloc[0]
        assert record.claim_relation == "unclassified"
        assert record.representation_status == "unreviewed"
        assert not record.coherence_test_applicable
