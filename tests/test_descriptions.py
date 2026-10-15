"""Check descriptive denominators, offline exports and stale-case suppression."""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd
import pytest

import main as controller
from description_views import COMPONENT_LABELS, write_data_descriptions
from src.anecdotes import CLAIM_AUDITS, case_assertion_fingerprint
from src.coherence import ClaimRelation
from src.config import TABLE_DIR


def _contracts() -> pd.DataFrame:
    """Include score endpoints and length-bin boundaries on both platforms."""

    rows = []
    for platform in ("Kalshi", "Polymarket"):
        for i, (score, words) in enumerate(zip([0, 0.3, 0.7, 1], [49, 50, 499, 1000], strict=True)):
            rows.append(
                {
                    "platform": platform,
                    "contract_id": f"{platform}:{i}",
                    "platform_event_id": str(i // 2),
                    "series": str(i // 2),
                    "category": "<script>unsafe</script>" if i == 0 else "Economics",
                    "snapshot_date": "2026-09-10",
                    "volume": 100.0,
                    "log_volume": 4.6,
                    "market_duration_days": 30.0,
                    "open_timestamp": "2026-01-01",
                    "ambiguous_terms": 0,
                    "rule_word_count": words,
                    "determinacy_score": score,
                    "quantitative_threshold": i % 2,
                    "outcome_category": "recorded_binary",
                    "outcome_evidence": "platform_result",
                    **dict.fromkeys(COMPONENT_LABELS, score),
                }
            )
    return pd.DataFrame(rows)


def test_atlas_reconciles_counts_escapes_text_and_withholds_stale_settlements(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Exercise real exports with synthetic evidence, then change an audited input."""

    contracts = _contracts()
    normalization = contracts[["platform"]].assign(normalization_reason="retained")
    normalization.loc[len(normalization)] = ["Kalshi", "missing_title"]
    case = {
        "case_id": "synthetic",
        "phenomenon": "Synthetic settlement contrast",
        "display_order": 1,
        "a_contract_id": "A",
        "b_contract_id": "B",
        "a_platform": "Kalshi",
        "b_platform": "Polymarket",
        "a_question": "Does X happen?",
        "a_rule": "YES if X.",
        "b_question": "Does X or Y happen?",
        "b_rule": "YES if X or Y.",
        "a_operative_inputs": "{}",
        "b_operative_inputs": "{}",
        "a_url": "javascript:alert(1)",
        "b_url": "https://example.test/B",
        "witness_state": "UNIQUE-SYNTHETIC-WITNESS",
        "signature_a": "X",
        "signature_b": "X or Y",
        "payout_a": "UNIQUE-SYNTHETIC-PAYOUT",
        "payout_b": "YES",
        "explanation": "Synthetic only",
        "evidence_kind": "observed_settlement_divergence",
        "scenario_status": "observed synthetic",
        "observed_settlement_a": "0.45",
        "observed_settlement_b": "1",
    }
    monkeypatch.setitem(
        CLAIM_AUDITS,
        "synthetic",
        (
            case_assertion_fingerprint(case),
            ClaimRelation.SUBSET,
            "determinate_binary",
            "Test audit",
        ),
    )
    cases = pd.DataFrame([case])
    path = tmp_path / "output" / "descriptions-data.html"
    write_data_descriptions(path, contracts, cases, normalization)
    original = path.read_bytes()
    html = original.decode()
    assert html.count("<svg ") == 6
    identifiers = re.findall(r'\bid="([^"]+)"', html)
    assert len(identifiers) == len(set(identifiers))
    assert 'role="img"' in html
    assert "UNIQUE-SYNTHETIC-WITNESS" in html
    assert "&lt;script&gt;unsafe&lt;/script&gt;" in html
    assert "javascript:alert(1)" not in html
    assert 'src="https://' not in html
    assert len(list((path.parent / "figures").glob("*.svg"))) == 6

    for name in ("distribution", "length", "categories", "outcomes"):
        exported = pd.read_csv(path.parent / "tables" / f"descriptions-{name}.csv")
        assert exported.groupby("platform").contracts.sum().to_dict() == {
            "Kalshi": 4,
            "Polymarket": 4,
        }
        assert exported.groupby("platform").share.sum().tolist() == pytest.approx([1, 1])
    bins = pd.read_csv(path.parent / "tables" / "descriptions-distribution.csv")
    assert bins.loc[bins.upper.eq(1), "contracts"].tolist() == [1, 1]
    lengths = pd.read_csv(path.parent / "tables" / "descriptions-length.csv")
    assert lengths.loc[lengths.words.eq("500+"), "contracts"].tolist() == [1, 1]
    settlements = pd.read_csv(path.parent / "tables" / "descriptions-settlements.csv")
    assert settlements.observed_settlement_a.tolist() == [0.45]
    write_data_descriptions(path, contracts, cases, normalization)
    assert path.read_bytes() == original

    cases.at[0, "a_rule"] = "Changed operative rule."
    write_data_descriptions(path, contracts, cases, normalization)
    html = path.read_text()
    assert "UNIQUE-SYNTHETIC-WITNESS" not in html
    assert "UNIQUE-SYNTHETIC-PAYOUT" not in html
    assert 'data-kind="unreviewed"' in html
    assert pd.read_csv(path.parent / "tables" / "descriptions-settlements.csv").empty


def test_atlas_rejects_nonreconciling_ledger_before_writing(tmp_path: Path) -> None:
    """A mismatched ledger cannot publish a misleading sample accounting."""

    contracts = _contracts()
    ledger = contracts.iloc[:1][["platform"]].assign(normalization_reason="retained")
    path = tmp_path / "atlas.html"
    with pytest.raises(ValueError, match="does not reconcile"):
        write_data_descriptions(path, contracts, pd.DataFrame(), ledger)
    assert not path.exists()


def test_describe_controller_uses_only_required_local_inputs(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """The new command dispatches local tables without invoking acquisition or fitting."""

    monkeypatch.setattr(controller, "OUTPUT_DIR", tmp_path)
    reads = []
    writes = []

    def read_frame(path: Path) -> pd.DataFrame:
        """Record each required local input."""
        reads.append(path)
        return pd.DataFrame()

    monkeypatch.setattr(controller, "_read_frame", read_frame)
    monkeypatch.setattr(controller, "write_data_descriptions", lambda *args: writes.append(args))
    controller.run_describe()
    assert reads == [
        controller.CONTRACT_PATH,
        controller.CASE_PATH,
        TABLE_DIR / "preprocessing-normalization-ledger.csv",
    ]
    assert writes[0][0] == tmp_path / "descriptions-data.html"
