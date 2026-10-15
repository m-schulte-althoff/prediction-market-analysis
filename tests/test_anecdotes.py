"""Tests for the witness-state representation casebook."""

import json
from datetime import date, datetime
from pathlib import Path
from typing import Any, cast

import pandas as pd
import pytest

from src.anecdotes import (
    CLAIM_AUDITS,
    add_claim_relations,
    build_representation_case_matrix,
    case_assertion_fingerprint,
    download_anecdote_sources,
    load_case_evidence,
    write_casebook,
)
from src.coherence import ClaimRelation, case_price_diagnostics
from src.config import SampleConfig, utc_today
from src.http_client import PublicApiClient


def _poly_market(slug: str, question: str) -> dict[str, str]:
    """Build a minimal official-market fixture."""

    return {"id": slug, "slug": slug, "question": question, "description": f"Rules for {slug}."}


def _rules_payload() -> dict[str, Any]:
    """Supply deliberately unaudited rules to exercise the changed-input gate."""

    return {
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


def test_unreviewed_inputs_block_dependent_witness_assertions(tmp_path: Path) -> None:
    """Changed operative text cannot leave the old witness/payout prose publishable."""

    result = build_representation_case_matrix(_rules_payload())

    assert len(result) == 4
    assert result["witness_state"].str.contains("Withheld").all()
    assert result["payout_a"].str.contains("Withheld").all()
    suit = result.loc[result["case_id"] == "suit-category-boundary"].iloc[0]
    assert not bool(suit["determinacy_issue"])
    assert not bool(suit["truth_condition_divergent"])
    assert result.claim_relation.eq("unclassified").all()
    assert not result.claim_relation_validated.any()
    assert not result.coherence_test_applicable.any()
    assert result.probability_coherence_implication.eq("none").all()
    assert result.claim_relation_basis.str.contains("manual review required").all()
    path = tmp_path / "casebook.md"
    write_casebook(path, result)
    prose = path.read_text(encoding="utf-8")
    assert "assertions are withheld" in prose
    assert "unusual 12.5 bp" not in prose


def test_claim_audit_requires_same_rules_and_ids(monkeypatch: pytest.MonkeyPatch) -> None:
    """A validated relation must not transfer to a changed contract or rule version."""

    record = {
        "case_id": "synthetic", "a_contract_id": "A", "a_rule": "YES if X.",
        "a_question": "Does X happen?", "a_operative_inputs": '{"deadline": "2026-01-01"}',
        "b_contract_id": "B", "b_rule": "YES if X or Y.", "b_question": "X or Y?",
        "witness_state": "Y happens and X does not.", "payout_a": "NO", "payout_b": "YES",
    }
    fingerprint = case_assertion_fingerprint(record)
    monkeypatch.setitem(CLAIM_AUDITS, "synthetic", (
        fingerprint, ClaimRelation.SUBSET, "determinate_binary", "Synthetic full-rule proof.",
    ))
    cases = pd.DataFrame([record])
    result = add_claim_relations(cases).iloc[0]
    assert result.claim_relation == "subset"
    assert result.coherence_test_applicable
    assert result.probability_coherence_implication == "q_A <= q_B"
    whitespace = cases.copy()
    whitespace.loc[0, "a_rule"] = "YES  if\nX."
    assert add_claim_relations(whitespace).iloc[0].claim_relation_validated
    for column in (
        "a_contract_id", "b_contract_id", "a_rule", "b_rule", "a_question", "b_question",
        "a_operative_inputs", "witness_state", "payout_b",
    ):
        changed = cases.copy()
        changed.loc[0, column] = "different"
        changed_record = add_claim_relations(changed).iloc[0]
        assert changed_record.claim_relation == "unclassified"
        assert changed_record.representation_status == "unreviewed"
        assert not changed_record.coherence_test_applicable
        assert "Withheld" in changed_record.witness_state
        assert "Withheld" in changed_record.payout_a


def _observed_evidence() -> dict[str, Any]:
    """Load the relevant fields of the preserved named final-settlement records."""

    path = Path(__file__).parent / "fixtures/representation-observed-cases.json"
    return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))


def test_observed_cases_separate_splits_disputes_and_chronology(tmp_path: Path) -> None:
    """Verified outcomes support two realized splits; the minerals chronology stays YES/YES."""

    cases = build_representation_case_matrix(_rules_payload(), case_evidence=_observed_evidence())
    observed = cases.loc[cases.evidence_kind.ne("hypothetical_rule_witness")]
    assert observed.claim_relation_validated.all()
    indexed = observed.set_index("case_id")
    assert indexed.loc["hilton-first-vs-advance", "observed_settlement_a"] == "0"
    assert indexed.loc["hilton-first-vs-advance", "observed_settlement_b"] == "1"
    scalar = indexed.loc["khamenei-death-allocation"]
    assert scalar.observed_settlement_a == "0.45"
    assert scalar.observed_settlement_b == "1"
    assert scalar.representation_status == "non_binary_and_adjudicated_exceptions"
    assert not scalar.coherence_test_applicable
    assert case_price_diagnostics(observed).status.eq("not_estimable").all()
    minerals = indexed.loc["minerals-observed-chronology"]
    assert minerals.observed_settlement_a == minerals.observed_settlement_b == "1"
    assert not minerals.truth_condition_divergent
    suit = indexed.loc["suit-adjudication-episode"]
    assert suit.observed_settlement_a == "0"
    assert not suit.determinacy_issue
    assert suit.claim_relation == "not_applicable"
    assert suit.representation_status == "delegated_determination"
    settlement = suit["settlement_evidence"]
    assert isinstance(settlement, str)
    protocol = json.loads(settlement)["protocol_evidence"]
    assert protocol["condition_link_verified"]
    assert protocol["payout_numerators"] == [0, 1]
    assert "May 29" in suit.chronology
    assert "individual timestamps unavailable" in suit.chronology
    assert "July 9" in suit.chronology
    csv = tmp_path / "cases.csv"
    observed.to_csv(csv, index=False)
    assert add_claim_relations(pd.read_csv(csv)).claim_relation_validated.all()
    path = tmp_path / "casebook.md"
    write_casebook(path, cases)
    prose = path.read_text()
    assert prose.index("Steve Hilton:") < prose.index("Ali Khamenei departure:")
    assert "normalized settlement $0.45" in prose
    assert "two recorded YES outcomes; no realized split" in prose


def test_changed_observed_question_and_settlement_block_stale_prose(tmp_path: Path) -> None:
    """A different candidate, operative boundary or settlement must trigger a new audit."""

    original = build_representation_case_matrix(
        _rules_payload(), case_evidence=_observed_evidence()
    )
    hilton = original.loc[original.case_id.eq("hilton-first-vs-advance")].copy()
    for column in ("a_question", "b_question", "a_operative_inputs", "settlement_evidence"):
        changed = hilton.copy()
        changed.loc[changed.index[0], column] = "Different operative input"
        result = add_claim_relations(changed)
        assert not result.claim_relation_validated.any()
        assert not result.truth_condition_divergent.any()
        path = tmp_path / "blocked.md"
        write_casebook(path, changed)
        prose = path.read_text()
        assert "Finishing second loses" not in prose
        assert "normalized payout $1" not in prose
        assert "Recorded settlements:" not in prose


@pytest.mark.parametrize(
    ("field", "value"),
    [("umaResolutionStatus", "proposed"), ("outcomePrices", '["0.999", "0.001"]')],
)
def test_observed_cases_require_final_status_and_payout_vector(field: str, value: str) -> None:
    """Extreme prices and unresolved proposals cannot become realized settlement claims."""

    evidence = _observed_evidence()
    evidence["observed_cases"]["hilton"]["b"][field] = value
    with pytest.raises(ValueError, match="final"):
        build_representation_case_matrix(_rules_payload(), case_evidence=evidence)


@pytest.mark.parametrize("field", ["condition_id", "payout_numerators", "creator_updates"])
def test_changed_protocol_evidence_withholds_derived_case(field: str) -> None:
    """Protocol corroboration cannot transfer to a different question, payout or update."""

    evidence = _observed_evidence()
    evidence["observed_cases"]["suit"]["protocol_evidence"][field] = "changed"
    cases = build_representation_case_matrix(_rules_payload(), case_evidence=evidence)
    suit = cases.loc[cases.case_id.eq("suit-adjudication-episode")].iloc[0]
    assert not suit.claim_relation_validated
    assert "Withheld" in suit.witness_state
    assert not suit.coherence_test_applicable


class _OfflineClient:
    """Record acquisition attempts without permitting a network request."""

    def __init__(self) -> None:
        self.calls = 0

    def get_json(self, url: str, params: dict[str, str] | None = None) -> Any:
        """Return sufficient deterministic event responses for acquisition metadata checks."""
        self.calls += 1
        return [{"id": "event"}] if params is not None else {"markets": []}


def test_missing_historical_anecdote_cache_never_calls_network(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """A historical filename cannot label fresh responses as historical evidence."""

    monkeypatch.setattr("src.anecdotes.anecdote_snapshot_path", lambda _: tmp_path / "absent.json")
    client = _OfflineClient()
    with pytest.raises(FileNotFoundError, match="historical"):
        download_anecdote_sources(SampleConfig(retrieval_date=date(2000, 1, 1)), cast(
            PublicApiClient, client
        ))
    assert client.calls == 0


def test_new_anecdote_acquisition_carries_actual_utc_timestamp(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Actual acquisition time is recorded separately from the requested date label."""

    monkeypatch.setattr("src.anecdotes.anecdote_snapshot_path", lambda _: tmp_path / "new.json")
    client = _OfflineClient()
    payload = download_anecdote_sources(
        SampleConfig(retrieval_date=utc_today()), cast(PublicApiClient, client)
    )
    assert client.calls == 7
    acquired = datetime.fromisoformat(payload["acquired_at_utc"])
    assert acquired.tzinfo is not None
    assert acquired.date().isoformat() == payload["retrieved_at_date"]
    assert payload["selection"]["kalshi_event_tickers"] == [
        "KXPRESPERSON-28", "KXFEDDECISION-26SEP"
    ]


def test_legacy_anecdote_cache_remains_immutable_without_invented_timestamp(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Legacy date-only snapshots remain usable without silently filling provenance gaps."""

    path = tmp_path / "old.json"
    original = json.dumps(_rules_payload()).encode()
    path.write_bytes(original)
    monkeypatch.setattr("src.anecdotes.anecdote_snapshot_path", lambda _: path)
    client = _OfflineClient()
    payload = download_anecdote_sources(
        SampleConfig(retrieval_date=date(2026, 9, 11)), cast(PublicApiClient, client)
    )
    assert "acquired_at_utc" not in payload
    assert path.read_bytes() == original
    assert client.calls == 0


def test_explicit_missing_or_corrupted_evidence_fails(tmp_path: Path) -> None:
    """Selecting an absent evidence bundle fails instead of manufacturing realized cases."""

    with pytest.raises(FileNotFoundError):
        load_case_evidence(tmp_path / "absent.json")
    path = tmp_path / "corrupt.json"
    path.write_text('{"schema_version": 0}')
    with pytest.raises(ValueError, match="schema"):
        load_case_evidence(path)


def test_changed_cached_case_selection_fails_before_network(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """A selection-marked cache cannot silently satisfy another named-case request."""

    payload = _rules_payload()
    payload["selection"] = {"polymarket_event_slugs": [], "kalshi_event_tickers": []}
    path = tmp_path / "different-selection.json"
    path.write_text(json.dumps(payload))
    monkeypatch.setattr("src.anecdotes.anecdote_snapshot_path", lambda _: path)
    client = _OfflineClient()
    with pytest.raises(ValueError, match="selection"):
        download_anecdote_sources(
            SampleConfig(retrieval_date=date(2026, 9, 11)), cast(PublicApiClient, client)
        )
    assert client.calls == 0


def test_preserved_evidence_source_hash_is_checked(tmp_path: Path) -> None:
    """An altered source copy cannot be used as though it were the approved version."""

    evidence = _observed_evidence()
    evidence["source_versions"] = [{
        "preserved_path": "source.json", "sha256": "incorrect-sha256"
    }]
    (tmp_path / "source.json").write_text("{}")
    path = tmp_path / "bundle.json"
    path.write_text(json.dumps(evidence))
    with pytest.raises(ValueError, match="hash"):
        load_case_evidence(path)
