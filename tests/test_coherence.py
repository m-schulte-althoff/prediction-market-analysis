"""Offline checks of mathematical implications and evidence gates."""

import pandas as pd
import pytest

from src.coherence import (
    ClaimRelation,
    case_price_diagnostics,
    price_coherence_diagnostic,
    probability_implication,
)


@pytest.mark.parametrize(
    ("relation", "restriction", "a", "b", "excess"),
    [
        ("equivalent", "q_A = q_B", 0.3, 0.6, 0.3),
        ("subset", "q_A <= q_B", 0.6, 0.3, 0.3),
        ("superset", "q_A >= q_B", 0.3, 0.6, 0.3),
        ("disjoint", "q_A + q_B <= 1", 0.7, 0.6, 0.3),
        ("complement", "q_A + q_B = 1", 0.2, 0.5, 0.3),
    ],
)
def test_implication_and_price_excess(
    relation: str,
    restriction: str,
    a: float,
    b: float,
    excess: float,
) -> None:
    """Every supported inequality uses the correct orientation and excess."""

    implication = probability_implication(relation)
    assert implication.probability_restriction == restriction
    assert implication.diagnostic_available
    result = price_coherence_diagnostic(
        relation,
        a,
        b,
        relation_validated=True,
        determinate_binary=True,
        comparable_prices=True,
    )
    assert result.status == "estimated"
    assert result.excess == pytest.approx(excess)
    assert result.exceeds_tolerance
    assert "Not a Bayesian violation" in result.reason


@pytest.mark.parametrize(
    "relation",
    [
        "indeterminate",
        "unclassified",
        "non_equivalent_unclassified",
        "overlap_non_nested",
    ],
)
def test_no_restriction_is_not_a_zero_excess(relation: str) -> None:
    """Unavailable restrictions never masquerade as an observed pass."""

    assert not probability_implication(relation).diagnostic_available
    result = price_coherence_diagnostic(
        relation,
        0.9,
        0.1,
        relation_validated=True,
        determinate_binary=True,
        comparable_prices=True,
    )
    assert result.status == "not_estimable"
    assert result.excess is None
    assert result.exceeds_tolerance is None


@pytest.mark.parametrize("relation", list(ClaimRelation)[:5])
def test_boundary_and_tolerance(relation: ClaimRelation) -> None:
    """Equality at one half satisfies every restriction, including disjointness."""

    result = price_coherence_diagnostic(
        relation,
        0.5,
        0.5,
        relation_validated=True,
        determinate_binary=True,
        comparable_prices=True,
    )
    assert result.excess == 0
    assert result.exceeds_tolerance is False
    near = price_coherence_diagnostic(
        "equivalent",
        0.5 + 1e-10,
        0.5,
        relation_validated=True,
        determinate_binary=True,
        comparable_prices=True,
    )
    assert near.excess is not None and near.excess > 0
    assert near.exceeds_tolerance is False


@pytest.mark.parametrize("invalid", [float("nan"), float("inf"), -0.1, 1.1])
def test_invalid_prices_are_unavailable(invalid: float) -> None:
    """Invalid observations are not clipped into apparent coherent prices."""

    result = price_coherence_diagnostic(
        "subset",
        invalid,
        0.5,
        relation_validated=True,
        determinate_binary=True,
        comparable_prices=True,
    )
    assert result.status == "not_estimable"
    assert result.excess is None


@pytest.mark.parametrize("tolerance", [-1.0, float("nan"), float("inf")])
def test_invalid_tolerance_rejected(tolerance: float) -> None:
    """An invalid tolerance cannot suppress all diagnostic flags."""

    with pytest.raises(ValueError, match="tolerance"):
        price_coherence_diagnostic("subset", 0.5, 0.4, tolerance=tolerance)


def _case() -> pd.DataFrame:
    """Supply a synthetic fully audited pair, never a real case classification."""

    return pd.DataFrame(
        [
            {
                "case_id": "synthetic",
                "claim_relation": "subset",
                "claim_relation_validated": True,
                "representation_status": "determinate_binary",
            }
        ]
    )


def _observation() -> pd.DataFrame:
    """Supply an explicit synthetic synchronous comparison."""

    return pd.DataFrame(
        [
            {
                "case_id": "synthetic",
                "price_a": 0.7,
                "price_b": 0.4,
                "observed_at_a": "2026-01-01T12:00:00Z",
                "observed_at_b": "2026-01-01T12:00:00Z",
                "comparable_prices": True,
                "comparison_basis": "Synthetic fresh YES quotes; common horizon and conditions.",
            }
        ]
    )


def test_evidence_gates_and_table() -> None:
    """Only a complete audit and explicit comparison produce a table estimate."""

    assert case_price_diagnostics(_case()).iloc[0].status == "not_estimable"
    result = case_price_diagnostics(_case(), _observation()).iloc[0]
    assert result.status == "estimated"
    assert result.excess == pytest.approx(0.3)
    changes: list[tuple[str, bool | str]] = [
        ("claim_relation_validated", False),
        ("claim_relation_validated", "False"),
        ("representation_status", "non_binary_exceptions"),
    ]
    for column, value in changes:
        cases = _case().astype(object)
        cases[column] = value
        assert case_price_diagnostics(cases, _observation()).iloc[0].status == "not_estimable"


@pytest.mark.parametrize(
    ("column", "value"),
    [
        ("observed_at_b", "2026-01-01T12:01:00Z"),
        ("observed_at_a", "2026-01-01T12:00:00"),
        ("observed_at_a", ""),
        ("comparable_prices", "False"),
        ("comparison_basis", ""),
        ("comparison_basis", float("nan")),
        ("price_a", "bad"),
    ],
)
def test_incomparable_observations_do_not_pass(column: str, value: str | float) -> None:
    """Daily timestamps and absent freshness evidence cannot authorize a diagnostic."""

    observations = _observation().astype(object)
    observations.loc[0, column] = value
    assert case_price_diagnostics(_case(), observations).iloc[0].status == "not_estimable"


def test_unknown_relations_and_observation_ids_rejected() -> None:
    """Reject typos and silently unmatched observations."""

    with pytest.raises(ValueError):
        probability_implication("looks_broader")
    observations = _observation()
    observations.loc[0, "case_id"] = "missing"
    with pytest.raises(ValueError, match="unaudited"):
        case_price_diagnostics(_case(), observations)


def test_common_posterior_can_value_different_claims_differently() -> None:
    """A synthetic rank model illustrates the bridge without estimating real beliefs."""

    posterior = {"first": 0.2, "second": 0.3, "other": 0.5}
    a = posterior["first"]
    b = posterior["first"] + posterior["second"]
    assert a != b
    result = price_coherence_diagnostic(
        "subset",
        a,
        b,
        relation_validated=True,
        determinate_binary=True,
        comparable_prices=True,
    )
    assert result.excess == 0
    # Different non-nested sets can also have equal mass; divergence need not imply a gap.
    assert sum(posterior[s] for s in ("first", "second")) == posterior["other"]
