"""Probability implications of audited binary claims; conditional price diagnostics.

Set relationships constrain probabilities under a common distribution. Applying
them to prices additionally requires a justified probability-price approximation.
Neither a matching score nor a single payout witness establishes set inclusion.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from math import isfinite

import pandas as pd


class ClaimRelation(StrEnum):
    """Logical relations, oriented from claim A to claim B."""

    EQUIVALENT = "equivalent"
    SUBSET = "subset"
    SUPERSET = "superset"
    DISJOINT = "disjoint"
    COMPLEMENT = "complement"
    OVERLAP_NON_NESTED = "overlap_non_nested"
    NON_EQUIVALENT_UNCLASSIFIED = "non_equivalent_unclassified"
    INDETERMINATE = "indeterminate"
    UNCLASSIFIED = "unclassified"


@dataclass(frozen=True)
class CoherenceImplication:
    """An exact mathematical implication, conditional on validated representation."""

    probability_restriction: str
    diagnostic_available: bool
    reason: str


def probability_implication(relation: ClaimRelation | str) -> CoherenceImplication:
    """Describe a relation's implication without claiming its empirical validation."""

    relation = ClaimRelation(relation)
    restrictions = {
        ClaimRelation.EQUIVALENT: "q_A = q_B",
        ClaimRelation.SUBSET: "q_A <= q_B",
        ClaimRelation.SUPERSET: "q_A >= q_B",
        ClaimRelation.DISJOINT: "q_A + q_B <= 1",
        ClaimRelation.COMPLEMENT: "q_A + q_B = 1",
    }
    if relation in restrictions:
        return CoherenceImplication(
            restrictions[relation],
            True,
            "Exact for determinate binary claims under a common probability distribution.",
        )
    reasons = {
        ClaimRelation.OVERLAP_NON_NESTED: (
            "No additional pairwise marginal restriction; useful restrictions need "
            "additional set structure or probability information."
        ),
        ClaimRelation.NON_EQUIVALENT_UNCLASSIFIED: (
            "A payout witness establishes non-equivalence, not global inclusion or ordering."
        ),
        ClaimRelation.INDETERMINATE: (
            "The written representation alone supplies no unique point probability restriction."
        ),
        ClaimRelation.UNCLASSIFIED: "The logical relation has not been established.",
    }
    return CoherenceImplication("none", False, reasons[relation])


@dataclass(frozen=True)
class PriceDiagnostic:
    """A price-coherence diagnostic, never a verdict about Bayesian rationality."""

    status: str
    reason: str
    excess: float | None = None
    exceeds_tolerance: bool | None = None


def price_coherence_diagnostic(
    relation: ClaimRelation | str,
    price_a: float,
    price_b: float,
    *,
    relation_validated: bool = False,
    determinate_binary: bool = False,
    comparable_prices: bool = False,
    tolerance: float = 1e-9,
) -> PriceDiagnostic:
    """Calculate raw inequality excess only after explicit semantic and price validation.

    The caller must validate synchronized, fresh, YES-oriented normalized prices,
    common horizons and comparable conditions. Tolerance affects the flag, not excess;
    it handles numerical noise and is not a model of fees or transaction costs.
    """

    implication = probability_implication(relation)
    if not isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    if not relation_validated:
        return PriceDiagnostic("not_estimable", "Complete-rule relation audit is missing.")
    if not determinate_binary:
        return PriceDiagnostic("not_estimable", "Determinate binary payout mappings not validated.")
    if not implication.diagnostic_available:
        return PriceDiagnostic("not_estimable", implication.reason)
    if not comparable_prices:
        return PriceDiagnostic("not_estimable", "Comparable synchronized prices not validated.")
    if not all(isfinite(value) and 0 <= value <= 1 for value in (price_a, price_b)):
        return PriceDiagnostic("not_estimable", "Prices must be finite and normalized to [0, 1].")
    excesses = {
        ClaimRelation.EQUIVALENT: abs(price_a - price_b),
        ClaimRelation.SUBSET: max(0.0, price_a - price_b),
        ClaimRelation.SUPERSET: max(0.0, price_b - price_a),
        ClaimRelation.DISJOINT: max(0.0, price_a + price_b - 1),
        ClaimRelation.COMPLEMENT: abs(price_a + price_b - 1),
    }
    excess = excesses[ClaimRelation(relation)]
    return PriceDiagnostic(
        "estimated",
        "Conditional price diagnostic under a probability-price approximation; "
        "liquidity, spreads, fees, stale trading, risk preferences, market composition "
        "and limits to arbitrage may explain excess. Not a Bayesian violation.",
        excess,
        excess > tolerance,
    )


def _explicit_true(value: object) -> bool:
    """Parse only explicit affirmative flags, including CSV round trips."""

    return str(value).lower() == "true"


def case_price_diagnostics(
    cases: pd.DataFrame, observations: pd.DataFrame | None = None
) -> pd.DataFrame:
    """Evaluate separately validated observations; emit missing-evidence rows otherwise.

    Optional observations identify case_id, price_a/b, observed_at_a/b,
    comparable_prices and comparison_basis. Times must be timezone-aware and equal;
    the comparison basis must document freshness, orientation and market conditions.
    Daily resampled or forward-filled panel rows cannot certify these requirements.
    """

    columns = [
        "case_id",
        "claim_relation",
        "probability_coherence_implication",
        "observed_at_a",
        "observed_at_b",
        "price_a",
        "price_b",
        "comparison_basis",
        "status",
        "reason",
        "excess",
        "exceeds_tolerance",
    ]
    observations = pd.DataFrame() if observations is None else observations
    if not observations.empty:
        required = {
            "case_id",
            "price_a",
            "price_b",
            "observed_at_a",
            "observed_at_b",
            "comparable_prices",
            "comparison_basis",
        }
        if missing := required - set(observations.columns):
            raise ValueError(f"Missing coherence observation columns: {sorted(missing)}")
        if not observations.case_id.isin(cases.case_id).all():
            raise ValueError("Coherence observations refer to unaudited case IDs")
    records: list[dict[str, object]] = []
    for case in cases.to_dict(orient="records"):
        sample = (
            observations.loc[observations.case_id.eq(case["case_id"])]
            if not observations.empty
            else pd.DataFrame()
        )
        for observation in sample.to_dict(orient="records") or [{}]:
            timestamps = [
                pd.to_datetime(str(observation.get(f"observed_at_{side}", "")), errors="coerce")
                for side in ("a", "b")
            ]
            synchronized = (
                all(
                    isinstance(stamp, pd.Timestamp) and pd.notna(stamp) and stamp.tzinfo is not None
                    for stamp in timestamps
                )
                and timestamps[0] == timestamps[1]
            )
            basis = str(observation.get("comparison_basis", ""))
            comparable = (
                synchronized
                and _explicit_true(observation.get("comparable_prices"))
                and bool(basis.strip())
                and basis.lower() not in {"nan", "none"}
            )
            prices = [
                float(pd.to_numeric(str(observation.get(f"price_{side}", "")), errors="coerce"))
                for side in ("a", "b")
            ]
            relation = str(case.get("claim_relation", "unclassified"))
            diagnostic = price_coherence_diagnostic(
                relation,
                *prices,
                relation_validated=_explicit_true(case.get("claim_relation_validated")),
                determinate_binary=case.get("representation_status") == "determinate_binary",
                comparable_prices=comparable,
            )
            reason = diagnostic.reason
            if not observation:
                reason += " No separately validated synchronized price observations supplied."
            elif not comparable:
                reason += " Price timestamps/comparability evidence do not pass validation."
            records.append(
                {
                    "case_id": case["case_id"],
                    "claim_relation": relation,
                    "probability_coherence_implication": probability_implication(
                        relation
                    ).probability_restriction,
                    "observed_at_a": observation.get("observed_at_a", ""),
                    "observed_at_b": observation.get("observed_at_b", ""),
                    "price_a": prices[0],
                    "price_b": prices[1],
                    "comparison_basis": basis,
                    "status": diagnostic.status,
                    "reason": reason,
                    "excess": diagnostic.excess,
                    "exceeds_tolerance": diagnostic.exceeds_tolerance,
                }
            )
    return pd.DataFrame.from_records(records, columns=columns).sort_values(
        ["case_id", "observed_at_a", "observed_at_b"], kind="stable", ignore_index=True
    )


def panel_coherence_readiness(panel: pd.DataFrame) -> pd.DataFrame:
    """Report why legacy daily alignment does not establish coherence-test eligibility."""

    columns = ["underlying_event_id", "daily_rows", "status", "reason"]
    if panel.empty:
        return pd.DataFrame(columns=columns)
    result = (
        panel.groupby("underlying_event_id", sort=True).size().rename("daily_rows").reset_index()
    )
    result["status"] = "not_estimable"
    result["reason"] = (
        "Automated metadata matching is not a complete-rule relation audit. "
        "Daily resampling with up to seven-day forward fill lacks original quote times "
        "and freshness/comparability validation. Supply separately audited observations."
    )
    return result[columns]
