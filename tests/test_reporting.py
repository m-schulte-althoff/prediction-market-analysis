"""Check report audit gates and persistence of the controller's research history."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
import pytest

import main as controller
from src.anecdotes import CLAIM_AUDITS, add_claim_relations, case_assertion_fingerprint
from src.coherence import ClaimRelation
from src.reporting import _opening_lines, case_exhibit_lines, write_claim_confidence


def _audited_case(monkeypatch: pytest.MonkeyPatch) -> pd.DataFrame:
    """Bind one synthetic observed case to a controlled complete-input fingerprint."""

    record: dict[str, Any] = {
        "case_id": "hilton-first-vs-advance",
        "phenomenon": "Synthetic separating settlement",
        "a_contract_id": "synthetic-A",
        "b_contract_id": "synthetic-B",
        "a_url": "https://example.test/A",
        "b_url": "https://example.test/B",
        "a_question": "Does X happen?",
        "b_question": "Does X or Y happen?",
        "a_rule": "YES if X.",
        "b_rule": "YES if X or Y.",
        "a_operative_inputs": '{"deadline":"2026-01-01"}',
        "b_operative_inputs": '{"deadline":"2026-01-01"}',
        "signature_a": "X happens",
        "signature_b": "X or Y happens",
        "witness_state": "SYNTHETIC-WITNESS: Y happens and X does not.",
        "payout_a": "SYNTHETIC-PAYOUT-A: NO/$0",
        "payout_b": "SYNTHETIC-PAYOUT-B: YES/$1",
        "scenario_status": "realized settlement in a synthetic fixture",
        "evidence_kind": "observed_synthetic_paired_settlements",
        "observed_settlement_a": 0,
        "observed_settlement_b": 1,
    }
    monkeypatch.setitem(
        CLAIM_AUDITS,
        record["case_id"],
        (
            case_assertion_fingerprint(record),
            ClaimRelation.SUBSET,
            "determinate_binary",
            "Controlled fixture audit; no actual case evidence is supplied.",
        ),
    )
    return add_claim_relations(pd.DataFrame([record]))


@pytest.mark.parametrize(
    ("changed_field", "changed_value"),
    [
        ("a_question", "Does Z happen?"),
        ("b_question", "Does X happen without Y?"),
        ("a_operative_inputs", '{"deadline":"2026-02-01"}'),
        ("b_operative_inputs", '{"deadline":"2026-02-01"}'),
    ],
)
def test_generated_reports_reaudit_stale_case_assertions(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    changed_field: str,
    changed_value: str,
) -> None:
    """A stale true CSV flag cannot publish witnesses or settlements after input edits."""

    audited = _audited_case(monkeypatch)
    assert bool(audited.iloc[0]["claim_relation_validated"])
    original_exhibit = "\n".join(case_exhibit_lines(audited, observed_only=True))
    for field in ("witness_state", "payout_a", "payout_b"):
        assert audited.iloc[0][field] in original_exhibit

    stale = audited.copy()
    stale.at[0, changed_field] = changed_value
    assert bool(stale.iloc[0]["claim_relation_validated"])
    path = tmp_path / "claims.md"
    write_claim_confidence(path, pd.DataFrame(), stale, pd.DataFrame())
    claim_row = next(
        line for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("| 1 |")
    )
    generated = (
        "\n".join(case_exhibit_lines(stale, observed_only=True)),
        "\n".join(_opening_lines(stale)),
        claim_row,
    )
    for output in generated:
        for field in ("witness_state", "payout_a", "payout_b"):
            assert audited.iloc[0][field] not in output
        assert "NO/$0" not in output
        assert "resolved YES" not in output
    assert "withheld" in generated[0].lower()
    assert "withheld" in claim_row.lower()
    # Re-auditing occurs on copies; report generation also leaves its caller's
    # stale input untouched rather than disguising the test with an earlier edit.
    assert bool(stale.iloc[0]["claim_relation_validated"])


def test_observed_exhibits_omit_hypothetical_witness_with_negative_realized_phrase(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A phrase denying realized evidence cannot promote a witness into main exhibits."""

    hypothetical = _audited_case(monkeypatch)
    hypothetical.at[0, "evidence_kind"] = "hypothetical_rule_witness"
    hypothetical.at[0, "scenario_status"] = (
        "hypothetical witness; archived rules, not a realized payout audit"
    )
    record = {str(key): value for key, value in hypothetical.iloc[0].to_dict().items()}
    previous_audit = CLAIM_AUDITS[record["case_id"]]
    monkeypatch.setitem(
        CLAIM_AUDITS,
        record["case_id"],
        (case_assertion_fingerprint(record), *previous_audit[1:]),
    )
    hypothetical = add_claim_relations(hypothetical)
    assert bool(hypothetical.iloc[0]["claim_relation_validated"])
    witness = hypothetical.iloc[0]["witness_state"]
    assert witness in "\n".join(case_exhibit_lines(hypothetical))
    assert witness not in "\n".join(case_exhibit_lines(hypothetical, observed_only=True))


def test_analysis_rerun_preserves_existing_research_log(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Run the controller and real report writers with tiny data and mocked fitting."""

    output_dir = tmp_path / "output"
    table_dir = output_dir / "tables"
    processed_dir = tmp_path / "processed"
    output_dir.mkdir()
    processed_dir.mkdir()
    log_path = output_dir / "research-log.md"
    previous_history = (
        b"# Research log\n\n"
        b"## Previous author decision\nPreserve the unsuccessful specification.\n\n"
        b"## Approved revision\nRetain the earlier source limitation.\n"
    )
    log_path.write_bytes(previous_history)
    paths = {
        "OUTPUT_DIR": output_dir,
        "TABLE_DIR": table_dir,
        "FIGURE_DIR": output_dir / "figures",
        "PROCESSED_DIR": processed_dir,
        "CONTRACT_PATH": processed_dir / "contracts.csv",
        "MATCH_PATH": processed_dir / "matches.csv",
        "PANEL_PATH": processed_dir / "absent-panel.csv",
        "PANEL_SUMMARY_PATH": processed_dir / "absent-panel-summary.csv",
        "CASE_PATH": table_dir / "absent-cases.csv",
    }
    for name, path in paths.items():
        monkeypatch.setattr(controller, name, path)
    pd.DataFrame([{"platform": "Kalshi"}]).to_csv(paths["CONTRACT_PATH"], index=False)
    pd.DataFrame(
        [{"match_label": "high_confidence", "underlying_event_id": "synthetic"}]
    ).to_csv(paths["MATCH_PATH"], index=False)

    monkeypatch.setattr(controller, "prepare_market_analysis", lambda frame: frame.copy())
    model_frames = {
        "market_level_models": pd.DataFrame(columns=["model"]),
        "determinacy_bins": pd.DataFrame(columns=["platform", "determinacy_group"]),
        "matched_model": pd.DataFrame(),
        "terminal_error_model": pd.DataFrame(),
        "platform_profiles": pd.DataFrame(columns=["platform", "stratum"]),
    }
    for name, frame in model_frames.items():
        monkeypatch.setattr(controller, name, lambda _, result=frame: result.copy())
    for name in (
        "conceptual_schematic",
        "platform_rule_profiles",
        "determinacy_distribution",
        "determinacy_volume_bins",
        "divergence_disagreement",
        "price_trajectories",
    ):
        monkeypatch.setattr(controller, name, lambda *_: None)

    for _ in range(2):
        controller.run_analysis()
        assert log_path.read_bytes() == previous_history
        assert (output_dir / "RESEARCH_STATUS.md").exists()
        assert (table_dir / "analysis-market-models.csv").exists()
