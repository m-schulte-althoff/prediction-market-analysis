"""Generate concise research documentation from completed analyses."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd


def _records(frame: pd.DataFrame) -> list[dict[str, object]]:
    """Convert pandas records to mappings with explicit string keys."""

    return [
        {str(key): value for key, value in record.items()}
        for record in frame.to_dict(orient="records")
    ]


def _value(record: dict[str, object], key: str) -> float:
    """Convert one model-table cell to a float."""

    return float(str(record[key]))


def coverage_table(contracts: pd.DataFrame) -> pd.DataFrame:
    """Summarize market counts, dates, and volume by platform."""

    return (
        contracts.groupby("platform", sort=True)
        .agg(
            contracts=("contract_id", "nunique"),
            first_open=("open_timestamp", "min"),
            last_resolution=("resolution_timestamp", "max"),
            resolved_outcome=("outcome", lambda values: int(values.isin(["yes", "no"]).sum())),
            median_volume=("volume", "median"),
            total_volume=("volume", "sum"),
            categories=("category", "nunique"),
        )
        .reset_index()
    )


def semantic_examples(contracts: pd.DataFrame) -> pd.DataFrame:
    """Return representative low/high-score contracts from both platforms."""

    examples: list[pd.DataFrame] = []
    for _, group in contracts.groupby("platform", sort=True):
        ordered = group.sort_values(["determinacy_score", "volume"], ascending=[True, False])
        examples.extend([ordered.head(2), ordered.tail(2)])
    columns = [
        "platform",
        "platform_contract_id",
        "question",
        "source_specificity",
        "temporal_specificity",
        "outcome_definition",
        "edge_completeness",
        "discretion_clarity",
        "determinacy_score",
        "rule_word_count",
    ]
    return pd.concat(examples, ignore_index=True)[columns]


def _model_record(models: pd.DataFrame, name: str) -> dict[str, object] | None:
    """Return one named model record when it was estimable."""

    if models.empty:
        return None
    rows = models.loc[models["model"] == name]
    return None if rows.empty else _records(rows)[0]


def _estimate(record: dict[str, object], uncertainty: str = "SE") -> str:
    """Format a coefficient with uncertainty and sample size."""

    return (
        f"{_value(record, 'coefficient'):.3f} ({uncertainty} "
        f"{_value(record, 'std_error'):.3f}, p={_value(record, 'p_value'):.3g}, "
        f"n={int(_value(record, 'n')):,})"
    )


def write_research_log(
    path: Path,
    models: pd.DataFrame,
    error_models: pd.DataFrame,
    matches: pd.DataFrame,
    matched_models: pd.DataFrame,
) -> None:
    """Record substantive specifications, including weakened and infeasible results."""

    baseline = _model_record(models, "main_composite")
    cohort = _model_record(models, "cohort_exposure_adjusted")
    within_kalshi = _model_record(models, "within_family_kalshi")
    within_poly = _model_record(models, "within_family_polymarket")
    counts = matches["match_label"].value_counts() if not matches.empty else pd.Series(dtype=int)
    lines = [
        "# Research Log",
        "",
        f"## {date.today().isoformat()} — sample and exposure audit",
        "",
        "- Removed sports before imposing the Polymarket volume cap using official fields plus a documented conservative taxonomy. This corrects contamination by tournament families.",
        "- Parsed mixed ISO timestamp precision explicitly; the prior coercion had erased Polymarket resolution timestamps.",
        "- Replaced scheduled duration with retrieval-capped observed exposure in the preferred volume specification and added opening-year cohorts.",
    ]
    if baseline is not None:
        lines.append(f"- Original-style baseline determinacy coefficient: {_estimate(baseline, 'HC3 SE')}.")
    if cohort is not None:
        lines.append(f"- Preferred exposure/cohort-adjusted coefficient: {_estimate(cohort, 'HC3 SE')}.")
    lines.extend(
        [
            "",
            f"## {date.today().isoformat()} — within-family diagnostic",
            "",
            "- Question: Does determinacy predict volume using only variation inside repeated Kalshi series or Polymarket events? This removes stable family popularity by demeaning outcomes and controls within family.",
        ]
    )
    for platform, record in (("Kalshi", within_kalshi), ("Polymarket", within_poly)):
        if record is not None:
            lines.append(f"- {platform}: {_estimate(record, 'family-clustered SE')}.")
    lines.append(
        "- Decision: Treat the determinacy–volume association as secondary and exploratory unless stronger within-family or fixed-window-volume evidence emerges. A weak/null within-family estimate is evidence about identification, not evidence that representations do not matter."
    )
    lines.extend(
        [
            "",
            f"## {date.today().isoformat()} — construct and case audit",
            "",
            "- Recast semantic determinacy as an intra-contract property and divergence as an inter-contract property; neither is a substitute for the other.",
            "- Require a counterfactual witness state and implied settlement on each side before calling a pair truth-condition divergent. Automated text distances remain candidate diagnostics only.",
            f"- Matching inventory: {int(counts.get('high_confidence', 0))} high-confidence, {int(counts.get('probable', 0))} probable, and {int(counts.get('rejected', 0))} rejected candidates retained for audit.",
        ]
    )
    if not matched_models.empty:
        lines.append(
            f"- Sparse matched-price diagnostic: {_estimate(_records(matched_models)[0], 'HC3 SE')}."
        )
    else:
        lines.append("- Matched-price regression remains infeasible; no average divergence claim is made.")
    if not error_models.empty:
        lines.append(
            f"- Kalshi last-trade error diagnostic: {_estimate(_records(error_models)[0], 'series-clustered SE')}; this is not a common-horizon accuracy test."
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_research_summary(
    path: Path,
    contracts: pd.DataFrame,
    models: pd.DataFrame,
    error_models: pd.DataFrame,
    matches: pd.DataFrame,
    panel_summary: pd.DataFrame,
    matched_models: pd.DataFrame,
    cases: pd.DataFrame,
) -> None:
    """Write the paper-oriented summary with bounded, critic-audited claims."""

    coverage = coverage_table(contracts)
    platform_descriptions = "; ".join(
        f"{record['platform']}: {int(_value(record, 'contracts')):,} contracts"
        for record in _records(coverage)
    )
    high_matches = matches.loc[matches["match_label"] == "high_confidence"]
    baseline = _model_record(models, "main_composite")
    cohort = _model_record(models, "cohort_exposure_adjusted")
    resolved = _model_record(models, "resolved_cohort_adjusted")
    within_kalshi = _model_record(models, "within_family_kalshi")
    within_poly = _model_record(models, "within_family_polymarket")
    qualitative = _model_record(models, "qualitative_contracts")
    quantitative = _model_record(models, "quantitative_contracts")
    ambiguity = _model_record(models, "direct_ambiguity_count")
    temporal_rows = models.loc[models["model"].str.startswith("temporal_")]
    first_open = contracts["open_timestamp"].min()
    last_resolution = contracts["resolution_timestamp"].max()

    result_lines: list[str] = []
    if baseline is not None:
        result_lines.append(
            f"- **Baseline association:** one within-platform SD more measured determinacy corresponds to {_estimate(baseline, 'HC3 SE')} SD in log volume."
        )
    if cohort is not None:
        result_lines.append(
            f"- **Preferred cohort/exposure specification:** replacing scheduled duration with observed exposure and adding opening-year controls gives {_estimate(cohort, 'HC3 SE')}."
        )
    if resolved is not None:
        result_lines.append(f"- **Resolved contracts only:** {_estimate(resolved, 'HC3 SE')}.")
    for label, model_record in (("Kalshi", within_kalshi), ("Polymarket", within_poly)):
        if model_record is not None:
            result_lines.append(
                f"- **Within-family {label}:** {_estimate(model_record, 'family-clustered SE')}. This estimand uses only families whose determinacy varies internally."
            )
    type_parts = []
    if qualitative is not None:
        type_parts.append(f"qualitative {_estimate(qualitative, 'SE')}")
    if quantitative is not None:
        type_parts.append(f"quantitative {_estimate(quantitative, 'SE')}")
    if type_parts:
        result_lines.append(f"- **Contract-type heterogeneity:** {'; '.join(type_parts)}.")
    if ambiguity is not None:
        result_lines.append(
            f"- **Direct ambiguity lexicon check:** one SD more flagged ambiguity terms corresponds to {_estimate(ambiguity, 'SE')} SD in log volume."
        )
    if not temporal_rows.empty:
        temporal_detail = "; ".join(
            f"{str(record['model']).removeprefix('temporal_').replace('_', ' ')} {_estimate(record)}"
            for record in _records(temporal_rows)
        )
        result_lines.append(
            f"- **Temporal replication split (July 1, 2025):** {temporal_detail}. This is a stability diagnostic, not a preregistered holdout test."
        )
    if not error_models.empty:
        result_lines.append(
            f"- **Forecast-error diagnostic:** {_estimate(_records(error_models)[0], 'series-clustered SE')}. The coefficient is not a fixed-horizon accuracy comparison and a null is not evidence of equivalence."
        )
    diagnostic_interpretation: list[str] = []
    if (
        qualitative is not None
        and quantitative is not None
        and _value(qualitative, "p_value") >= 0.05
        and _value(quantitative, "p_value") < 0.05
    ):
        diagnostic_interpretation.append(
            "- **Interpretation:** the inverse association is concentrated in quantitative-threshold contracts; the qualitative-contract estimate is not distinguishable from zero. This is more consistent with threshold-family composition than with a general ambiguity–activity effect."
        )
    if ambiguity is not None and _value(ambiguity, "coefficient") <= 0:
        diagnostic_interpretation.append(
            "- **Interpretation:** directly flagged ambiguous language is associated with less, not more, activity after controls, so the current metadata do not directly support the heterogeneous-interpretation mechanism."
        )
    if (
        within_kalshi is not None
        and within_poly is not None
        and _value(within_kalshi, "p_value") >= 0.05
        and _value(within_poly, "p_value") >= 0.05
    ):
        diagnostic_interpretation.append(
            "- **Interpretation:** neither platform has a detectable within-family determinacy coefficient. The pooled result is therefore primarily a between-family pattern."
        )
    temporal_lookup = {
        str(record["model"]): record for record in _records(temporal_rows)
    }
    early_kalshi = temporal_lookup.get("temporal_early_kalshi")
    early_poly = temporal_lookup.get("temporal_early_polymarket")
    late_kalshi = temporal_lookup.get("temporal_late_kalshi")
    late_poly = temporal_lookup.get("temporal_late_polymarket")
    if (
        early_kalshi is not None
        and early_poly is not None
        and late_kalshi is not None
        and late_poly is not None
        and _value(early_poly, "p_value") >= 0.05
        and _value(late_poly, "p_value") < 0.05
    ):
        diagnostic_interpretation.append(
            "- **Platform-time heterogeneity:** the inverse pattern is strong in early Kalshi but absent in early Polymarket, then weaker in later Kalshi and strong in later Polymarket. This crossover argues against a timeless platform-general law and points toward evolving contract-family composition or governance."
        )

    case_lines: list[str] = []
    for record in _records(cases):
        case_lines.append(
            f"- **{record['phenomenon']} — {record['mechanism']}.** Witness: {record['witness_state']} Implied settlements: A = {record['payout_a']}; B = {record['payout_b']}."
        )
    if not case_lines:
        case_lines.append("- Run `main.py anecdotes` to build the archived witness-state case matrix.")

    lines = [
        "# Same Future, Different Claim",
        "",
        "## 1. Research question and contribution",
        "",
        "How do prediction-market platforms constitute digitally tradable and institutionally resolvable claims from ostensibly the same public-world phenomenon, and what consequences follow for participation and apparent disagreement?",
        "",
        "The central contribution is upstream of aggregation: platform resolution architectures choose predicates, measurement conventions, temporal boundaries, evidence, exceptions, and fallback procedures. Markets with similar labels can therefore price non-equivalent digital claims. Apparent cross-market forecast disagreement can be rational disagreement about different state exposure.",
        "",
        "## 2. Construct architecture",
        "",
        "A contract is a possibly set-valued mapping from world histories to institutionally permissible settlements. **Semantic determinacy** is an intra-contract property: how uniquely a relevant world history maps to a settlement. **Semantic divergence** is an inter-contract property: whether two contracts about the same phenomenon map at least one plausible world history to different payouts or procedures.",
        "",
        "The constructs are orthogonal. Two precise contracts can diverge (network call versus inauguration); two identically vague contracts can have low determinacy but little between-contract divergence. Automated wording, number, source, stage, and deadline distances retrieve candidates but are not treated as validated semantic equivalence measures.",
        "",
        "## 3. Audited mechanism cases",
        "",
        *case_lines,
        "",
        "Every truth-condition divergence above has a witness state and predicted settlement on both sides. The suit case instead witnesses within-contract category indeterminacy. Exact archived rules and URLs are in `tables/representation-case-matrix.csv` and `REPRESENTATION_CASEBOOK.md`.",
        "",
        "## 4. Data and sample correction",
        "",
        f"The reproducible official-API sample contains {platform_descriptions}. Openings begin {first_open.date() if pd.notna(first_open) else 'unknown'}; the latest observed resolution is {last_resolution.date() if pd.notna(last_resolution) else 'unknown'}. Polymarket sports contracts are excluded before its high-volume cap using official sports fields plus a conservative documented taxonomy. Volume remains cumulative and is standardized within platform; this purposive sample is not population-representative.",
        "",
        f"The automated matcher retains {len(high_matches)} high-confidence metadata pairs, dominated by repeated families. Only {len(panel_summary)} pairs have aligned histories, all too sparse and homogeneous to test whether divergence predicts price wedges.",
        "",
        "## 5. Measurement and method",
        "",
        "The transparent determinacy proxy averages source specificity, temporal specificity, operational definition, edge-case completeness, and discretion clarity. Calendar years no longer count as quantitative thresholds. Leave-one-component-out models, direct ambiguity counts, and qualitative/quantitative splits expose score dependence.",
        "",
        "Volume models compare the original baseline with a preferred retrieval-capped exposure/opening-cohort specification, resolved-only samples, family-clustered uncertainty, family aggregation, and within-family demeaning. The within-family estimates remove stable Kalshi-series or Polymarket-event popularity but are supported by relatively few families with internal semantic variation.",
        "",
        "## 6. Empirical results",
        "",
        *result_lines,
        "",
        *diagnostic_interpretation,
        "",
        "The between-contract pattern is consistent with interpretive latitude increasing activity, but attention, salience, placement, and template composition remain plausible alternatives. Weak or null within-family results would sharply limit an ambiguity-causes-trading interpretation without weakening the directly demonstrated representational phenomenon.",
        "",
        "## 7. Information Systems storyline",
        "",
        "- **Phenomenon:** nearly identical market labels can expose traders to different platform-defined claims.",
        "- **Puzzle:** aggregation accounts often treat the proposition being priced as fixed before it enters the information system.",
        "- **Mechanism:** resolution architectures partition world histories through predicate selection, operationalization, boundary rules, adjudication, and fallback.",
        "- **Evidence:** witness-state cases demonstrate non-equivalence; systematic metadata document determinacy variation; volume associations supply secondary exploratory consequences.",
        "- **Contribution:** collective-intelligence systems govern the referents of aggregation, not only information processing about those referents.",
        "",
        "## 8. Best outputs",
        "",
        "- `tables/representation-case-matrix.csv`: exact rules, signatures, witness states, and implied settlements.",
        "- `REPRESENTATION_CASEBOOK.md`: plain-language explanations of the striking cases.",
        "- `figures/views-conceptual-schematic.svg`: platform-specific resolution architectures and distinct claims.",
        "- `tables/analysis-market-models.csv`: baseline, cohort/exposure, market-type, leave-one-out, and within-family estimates.",
        "- `figures/views-determinacy-volume.svg`: descriptive score–volume pattern; not a causal figure.",
        "",
        "## 9. Candidate abstract",
        "",
        "Prediction markets are commonly treated as information systems that aggregate beliefs about fixed future events. Yet platforms first constitute the claims whose probabilities they elicit. We distinguish semantic determinacy within a contract from semantic divergence between contracts and analyze official Kalshi and Polymarket metadata. Audited cases identify plausible world histories in which markets bearing similar labels settle differently because of event-stage, measurement, temporal, evidentiary, or fallback choices. A corrected non-sports sample and transparent text measures also show how determinacy covaries with cumulative trading activity, while exposure/cohort and within-family specifications reveal the limits of a causal ambiguity–activity interpretation. The study shifts attention from how collective-intelligence systems process information to how their resolution architectures govern the referents of aggregation.",
        "",
        "## 10. Next decisive tests",
        "",
        "- Human-code representation signatures and witness states for a stratified, phenomenon-diverse match sample with independent reliability checks.",
        "- Match public-world phenomena before comparing claims, so divergent deadlines or thresholds do not prevent candidate retrieval.",
        "- Acquire fixed first-30-day volume, common-horizon prices, spread, and volatility rather than relying on cumulative lifetime volume.",
        "- Expand cross-platform history coverage before estimating a divergence–price-wedge relationship.",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_research_status(
    path: Path, contracts: pd.DataFrame, models: pd.DataFrame, cases: pd.DataFrame
) -> None:
    """Write a one-page handoff of current evidence and decisions."""

    cohort = _model_record(models, "cohort_exposure_adjusted")
    within_kalshi = _model_record(models, "within_family_kalshi")
    within_poly = _model_record(models, "within_family_polymarket")
    lines = [
        "# Research Status",
        "",
        f"Updated {date.today().isoformat()}.",
        "",
        "## Current core",
        "",
        f"The strongest contribution is an audited account of how resolution architectures turn one public-world phenomenon into non-equivalent digital claims. The case matrix currently contains {len(cases)} mechanisms with exact rules and counterfactual witness states.",
        "",
        "## Current empirical package",
        "",
        f"The corrected non-sports metadata sample contains {len(contracts):,} contracts.",
    ]
    if cohort is not None:
        lines.append(f"- Preferred cohort/exposure-adjusted determinacy–volume estimate: {_estimate(cohort, 'HC3 SE')}.")
    if within_kalshi is not None:
        lines.append(f"- Within-family Kalshi estimate: {_estimate(within_kalshi, 'clustered SE')}.")
    if within_poly is not None:
        lines.append(f"- Within-family Polymarket estimate: {_estimate(within_poly, 'clustered SE')}.")
    qualitative = _model_record(models, "qualitative_contracts")
    quantitative = _model_record(models, "quantitative_contracts")
    if qualitative is not None and quantitative is not None:
        lines.append(
            f"- Contract-type split: qualitative {_estimate(qualitative)}; quantitative {_estimate(quantitative)}."
        )
    temporal_rows = models.loc[models["model"].str.startswith("temporal_")]
    if not temporal_rows.empty:
        detail = "; ".join(
            f"{str(record['model']).removeprefix('temporal_').replace('_', ' ')} "
            f"{_value(record, 'coefficient'):.3f}"
            for record in _records(temporal_rows)
        )
        lines.append(f"- Temporal/platform split: {detail}.")
    lines.extend(
        [
            "",
            "These volume results are exploratory consequences, not the theory’s sole support. The tiny aligned-price panel does not identify a divergence effect.",
            "",
            "## Locked decisions",
            "",
            "- Keep determinacy (within contract) separate from divergence (between contracts).",
            "- Require a witness state before labeling truth-condition divergence.",
            "- Keep automated text-distance scores as candidate diagnostics until validated coding exists.",
            "- Exclude sports before Polymarket’s high-volume cap and control cumulative-volume exposure/cohort.",
            "",
            "## Next decisive work",
            "",
            "Human-code a phenomenon-diverse match sample; acquire fixed-window volume and common-horizon prices; then test whether representation differences predict activity, spreads, volatility, or persistent price wedges.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
