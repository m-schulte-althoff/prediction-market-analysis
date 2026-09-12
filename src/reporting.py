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


def platform_profile_lines(profiles: pd.DataFrame) -> list[str]:
    """Render reproducible sample comparisons without treating proxies as platform quality."""

    if profiles.empty:
        return ["Platform rule profiles are unavailable for this run."]
    overall = profiles.loc[profiles.stratum == "all"].set_index("platform")
    platforms = sorted(overall.index.astype(str))
    lines = [
        "| Sampled rule-text measure | " + " | ".join(platforms) + " |",
        "|---|" + "---:|" * len(platforms),
    ]
    for label, column, format_spec in (
        ("Contracts", "contracts", ",.0f"),
        ("Mean determinacy proxy", "mean_determinacy", ".3f"),
        ("Source specificity", "source_specificity", ".3f"),
        ("Temporal specificity", "temporal_specificity", ".3f"),
        ("Outcome definition", "outcome_definition", ".3f"),
        ("Edge-clause completeness", "edge_completeness", ".3f"),
        ("Discretion clarity", "discretion_clarity", ".3f"),
        ("Threshold-flag share", "threshold_flag_share", ".1%"),
        ("Mean analyzed text length (words)", "mean_text_words", ".1f"),
    ):
        cells = [
            format(float(overall.loc[platform, column]), format_spec) for platform in platforms
        ]
        lines.append(f"| {label} | " + " | ".join(cells) + " |")
    lines.extend(
        [
            "",
            "| Determinacy proxy within text strata | " + " | ".join(platforms) + " |",
            "|---|" + "---:|" * len(platforms),
        ]
    )
    by_type = profiles.set_index(["platform", "stratum"])
    for label, stratum in (
        ("No threshold flag", "no_threshold_flag"),
        ("Threshold flag", "threshold_flag"),
    ):
        cells = []
        for platform in platforms:
            key = (platform, stratum)
            if key in by_type.index:
                row = by_type.loc[key]
                cells.append(f"{row['mean_determinacy']:.3f} (n={row['contracts']:,.0f})")
            else:
                cells.append("unavailable")
        lines.append(f"| {label} | " + " | ".join(cells) + " |")
    lines.extend(
        [
            "",
            "These are raw proxy means in purposive sampled portfolios. Threshold flags come from the text measure and also enter its outcome-definition component; the strata describe composition rather than supply an independent validation or causal adjustment. Longer text and a higher component score do not establish better forecasting or more equivalent claims.",
        ]
    )
    if all(
        (platform, stratum) in by_type.index
        for platform in ("Kalshi", "Polymarket")
        for stratum in ("all", "no_threshold_flag", "threshold_flag")
    ):
        gaps = [
            float(
                float(str(by_type.loc[("Kalshi", stratum), "mean_determinacy"]))
                - float(str(by_type.loc[("Polymarket", stratum), "mean_determinacy"]))
            )
            for stratum in ("all", "no_threshold_flag", "threshold_flag")
        ]
        if gaps[0] * gaps[1] < 0 and gaps[0] * gaps[2] < 0:
            overall_leader = "Kalshi" if gaps[0] > 0 else "Polymarket"
            within_leader = "Polymarket" if gaps[0] > 0 else "Kalshi"
            lines.extend(
                [
                    "",
                    f"**Composition reversal:** {overall_leader} has the higher overall composite mean, while {within_leader} has the higher mean in both threshold-flag strata. The overall ranking depends on the mix of contracts; it is not a general ranking of platform clarity.",
                ]
            )
    lines.append("")
    for platform in platforms:
        row = overall.loc[platform]
        share = float(row["between_family_variance_share"])
        variance = f"{share:.1%}" if pd.notna(share) else "undefined (constant scores)"
        lines.append(
            f"- **{platform} family structure:** {row['families']:,.0f} families; the five largest account for {row['top_five_family_share']:.1%} of sampled contracts. Between-family differences account for {variance} of the score sum of squares; {row['varying_families']:,.0f} families ({row['contracts_in_varying_families']:,.0f} contracts) vary internally."
        )
    lines.append(
        "Family units follow the APIs: Kalshi series and Polymarket events. Their different granularity means concentration and variance shares describe each sample; they do not rank platform diversity."
    )
    return lines


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
        lines.append(
            f"- Original-style baseline determinacy coefficient: {_estimate(baseline, 'HC3 SE')}."
        )
    if cohort is not None:
        lines.append(
            f"- Preferred exposure/cohort-adjusted coefficient: {_estimate(cohort, 'HC3 SE')}."
        )
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
        lines.append(
            "- Matched-price regression remains infeasible; no average divergence claim is made."
        )
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
    profiles: pd.DataFrame,
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
        type_parts.append(f"no threshold flag {_estimate(qualitative, 'SE')}")
    if quantitative is not None:
        type_parts.append(f"threshold flag {_estimate(quantitative, 'SE')}")
    if type_parts:
        result_lines.append(f"- **Contract-type estimates:** {'; '.join(type_parts)}.")
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
            "- **Contract-type interpretation:** the threshold-flag estimate is negative and distinguishable from zero; the no-flag estimate is not. These separate significance tests do not establish that the two coefficients differ."
        )
    if ambiguity is not None and _value(ambiguity, "coefficient") <= 0:
        diagnostic_interpretation.append(
            "- **Lexicon interpretation:** the coefficient for words such as ‘deal’ and ‘agreement’ is nonpositive. These are text flags, not observations of traders interpreting a contract differently."
        )
    if (
        within_kalshi is not None
        and within_poly is not None
        and _value(within_kalshi, "p_value") >= 0.05
        and _value(within_poly, "p_value") >= 0.05
    ):
        diagnostic_interpretation.append(
            "- **Family interpretation:** neither platform has a detectable within-family coefficient. Read the pooled association alongside the strong concentration of score variation between families. Within-family coefficients use one SD of the varying-family residual score and are not directly comparable in magnitude to the pooled coefficient."
        )
    temporal_lookup = {str(record["model"]): record for record in _records(temporal_rows)}
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
            "- **Platform-time diagnostic:** the period-specific estimates vary. These exploratory splits do not isolate a change in platform governance or establish a difference by comparing significance levels."
        )

    case_lines: list[str] = []
    for record in _records(cases):
        case_lines.append(
            f"- **{record['phenomenon']} — {record['mechanism']}.** {record.get('explanation', '')} Scope: {record['scope']}. Hypothetical witness: {record['witness_state']} Implied settlements: {record['a_platform']} = {record['payout_a']}; {record['b_platform']} = {record['payout_b']}."
        )
        secondary = record.get("secondary_witness_state")
        if isinstance(secondary, str) and secondary:
            case_lines.append(
                f"  Additional witness: {secondary} A = {record['secondary_payout_a']}; B = {record['secondary_payout_b']}."
            )
    if not case_lines:
        case_lines.append(
            "- Run `main.py anecdotes` to build the archived witness-state case matrix."
        )
    main_result_lines = [
        line
        for line in result_lines
        if any(
            label in line
            for label in (
                "Preferred cohort/exposure",
                "Within-family",
                "Contract-type estimates",
            )
        )
    ]
    supplementary_lines = [line for line in result_lines if line not in main_result_lines]

    lines = [
        "# Same Future, Different Claim",
        "",
        "## 1. Research question and contribution",
        "",
        "How do prediction-market resolution architectures differentiate claims about the same public phenomenon, and how do determinacy and trading activity vary across the sampled market portfolios?",
        "",
        "The central contribution is upstream of aggregation: platform resolution architectures choose predicates, measurement conventions, temporal boundaries, evidence, exceptions, and fallback procedures. Markets with similar labels can therefore price non-equivalent digital claims. Apparent cross-market forecast disagreement can be rational disagreement about different state exposure.",
        "",
        "## 2. Construct architecture",
        "",
        "**Semantic differentiation** is the process of selecting what counts, when it counts, and whose evidence counts. **Divergence** describes differences between the resulting claims; **determinacy** describes clarity within one claim. More explicit contracts need not be equivalent contracts.",
        "",
        "A contract is a possibly set-valued mapping from world histories to institutionally permissible settlements. **Semantic determinacy** is an intra-contract property: how uniquely a relevant world history maps to a settlement. **Semantic divergence** is an inter-contract property: whether two contracts about the same phenomenon map at least one plausible world history to different payouts or procedures.",
        "",
        "The constructs are orthogonal. Two precise contracts can diverge (network call versus inauguration); two identically vague contracts can have low determinacy but little between-contract divergence. Automated wording, number, source, stage, and deadline distances retrieve candidates but are not treated as validated semantic equivalence measures.",
        "",
        "## 3. Audited mechanism cases",
        "",
        *case_lines,
        "",
        "The archived rules are observed evidence; these scenarios are hypothetical, not records of realized settlements. Payout-divergence cases specify outcomes on both sides. The suit case illustrates an unspecified category boundary with an adjudication procedure. Exact rules, source links, and case-specific audit boundaries are in `tables/representation-case-matrix.csv` and `REPRESENTATION_CASEBOOK.md`.",
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
        "### Sampled platform rule profiles",
        "",
        *platform_profile_lines(profiles),
        "",
        "### Secondary trading-activity evidence",
        "",
        *main_result_lines,
        "",
        *diagnostic_interpretation,
        "",
        "Trading activity varies across portfolios of differently specified claims; the available associations do not isolate an effect of ambiguity itself. The paper's central result is the documented difference in what contracts require for a payout.",
        "",
        "## 7. Information Systems storyline",
        "",
        "- **Phenomenon:** nearly identical market labels can expose traders to different platform-defined claims.",
        "- **Puzzle:** aggregation accounts often treat the proposition being priced as fixed before it enters the information system.",
        "- **Mechanism:** resolution architectures partition world histories through predicate selection, operationalization, boundary rules, adjudication, and fallback.",
        "- **Evidence:** witness-state cases demonstrate non-equivalence; systematic metadata document determinacy variation; volume associations supply secondary exploratory consequences.",
        "- **Contribution:** collective-intelligence systems govern the referents of aggregation, not only information processing about those referents.",
        "- **Memorable finding:** a second-place finish can lose a first-place contract and win an advancement contract. Clear resolution rules can still define different claims.",
        "",
        "## 8. Best outputs",
        "",
        "- `tables/representation-case-matrix.csv`: exact rules, signatures, witness states, and implied settlements.",
        "- `REPRESENTATION_CASEBOOK.md`: plain-language explanations of the striking cases.",
        "- `PAPER_OUTLINE.md`: five-section ICIS paper outline, with current estimates and exhibits.",
        "- `tables/analysis-platform-profiles.csv` and `figures/views-platform-rule-profiles.svg`: component differences, contract mix, and conditional score comparisons.",
        "- `figures/views-conceptual-schematic.svg`: platform-specific resolution architectures and distinct claims.",
        "- `tables/analysis-market-models.csv`: baseline, cohort/exposure, market-type, leave-one-out, and within-family estimates.",
        "- `figures/views-determinacy-volume.svg`: descriptive score–volume pattern; not a causal figure.",
        "",
        "## 9. Candidate abstract",
        "",
        "Prediction markets aggregate beliefs about claims that their platforms first define. We distinguish semantic differentiation through contract design, determinacy within a contract, and divergence between contracts. Official Kalshi and Polymarket metadata reveal different profiles of rule specification and contract composition. Archived-rule cases show how finishing first versus advancing, media calls versus inauguration, numerical rounding, qualifying announcements, and competing departures can imply different payouts under the same hypothetical scenario. A separate clothing-category case illustrates interpretive latitude within a written rule. Exploratory volume associations describe activity across claim portfolios. The study explains how collective-intelligence systems govern what counts as the event being forecast, making explicit specification and cross-market comparability separate design concerns.",
        "",
        "## 10. Conference-paper scope",
        "",
        "- Lead with understandable rule contrasts, the multidimensional platform profiles, and contract-composition patterns.",
        "- Use the preferred volume association and within-family diagnostic as secondary evidence; keep remaining checks in the tables and research log.",
        "- Audit the quoted case clauses when preparing the submission. Independent coding is a useful extension, not a reason to suspend the current mechanism paper.",
        "- Reserve common-horizon prices on manually checked claims for a subsequent test of the price-wedge implication.",
        "",
        "## 11. Supplementary diagnostics",
        "",
        *supplementary_lines,
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_research_status(
    path: Path,
    contracts: pd.DataFrame,
    models: pd.DataFrame,
    cases: pd.DataFrame,
    profiles: pd.DataFrame,
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
        "",
        *platform_profile_lines(profiles),
        "",
    ]
    if cohort is not None:
        lines.append(
            f"- Preferred cohort/exposure-adjusted determinacy–volume estimate: {_estimate(cohort, 'HC3 SE')}."
        )
    if within_kalshi is not None:
        lines.append(
            f"- Within-family Kalshi estimate: {_estimate(within_kalshi, 'clustered SE')}."
        )
    if within_poly is not None:
        lines.append(
            f"- Within-family Polymarket estimate: {_estimate(within_poly, 'clustered SE')}."
        )
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
            "## Conference-paper focus",
            "",
            "Use PAPER_OUTLINE.md: platform profiles, audited payout contrasts, and secondary activity associations. Keep case explanations accessible and distinguish hypothetical scenarios from realized events. The empirical/theory critic feedback and implemented decisions are recorded in ../docs/CRITIC_REVIEW.md. Common-horizon price comparisons are a future extension.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_paper_outline(
    path: Path,
    contracts: pd.DataFrame,
    models: pd.DataFrame,
    cases: pd.DataFrame,
    profiles: pd.DataFrame,
) -> None:
    """Generate a five-part ICIS outline tied to the current evidence and exhibits."""

    cohort = _model_record(models, "cohort_exposure_adjusted")
    case_count = len(cases)
    lines = [
        "# Same Future, Different Claim: How Prediction Markets Define What Counts",
        "",
        "Working ICIS conference-paper outline. Lead with observable differences in contract rules, explain why these matter for collective intelligence, and use activity associations as a secondary result.",
        "",
        "## 1. Introduction",
        "",
        "- **Motivation:** similar market headlines invite readers to treat their displayed probabilities as forecasts of the same event. Yet finishing first and advancing to the next round are different bets.",
        "- **Opening example:** a candidate who finishes second loses a first-place contract but wins an advancement contract under a top-two rule. A called election winner who never takes office likewise separates media-call and inauguration contracts.",
        "- **Theoretical shortcoming:** aggregation-focused explanations leave the constitution of the priced claim in the background. Position this as an upstream complement; do not claim that prior research universally ignores contract design.",
        "- **RQ:** How do prediction-market resolution architectures differentiate claims about the same public phenomenon, and how do determinacy and trading activity vary across the sampled market portfolios?",
        f"- **Methods:** official Kalshi/Polymarket metadata for {len(contracts):,} contracts, {case_count} purposively selected archived-rule cases, transparent rule-text measures, descriptive platform comparisons, and a small main-text set of exploratory volume estimates.",
        "- **Contribution:** distinguish semantic differentiation as a design process, divergence between resulting claims, and determinacy within each claim. Explain why explicit rules can still price different state exposure.",
        "",
        "## 2. Literature and conceptual framework",
        "",
        "- **Prediction markets and collective intelligence:** connect information aggregation and forecast evaluation to the proposition the market actually prices.",
        "- **IS representation and classification:** connect digital categories and operational definitions to what observable circumstances count as an outcome.",
        "- **Platform governance and adjudication:** explain evidence authorities, time boundaries, exceptions, fallback procedures, and settlement methods as contract-design choices.",
        "- **Constructs:** differentiation selects what/when/whose evidence counts; determinacy concerns one contract's mapping from a scenario to settlement; divergence concerns differences between two such mappings. A procedural difference alone need not imply a payout difference.",
        "- **Core argument:** two precise contracts can disagree about what success means. Unclear category boundaries, such as ‘suit,’ present a separate interpretive problem.",
        "- **Theoretical implication:** under shared beliefs and otherwise comparable pricing conditions, different payout mappings can have different expected payoffs. A price gap need not be a disagreement about the same event; the current study does not estimate that mechanism in prices.",
        "- **Exhibit:** conceptual schematic plus the compact determinacy/divergence matrix in `../docs/CONSTRUCTS.md`. These literature streams are an outline for a sourced literature section, not a completed literature review.",
        "",
        "## 3. Method",
        "",
        "- **Data and selection:** immutable September 10, 2026 official-API snapshots for this reproduction; purposive Kalshi series and volume-selected Polymarket contracts, with sports excluded before its cap. Report platform counts and coverage from `tables/preprocessing-coverage.csv`.",
        "- **Units:** contract for text profiles and activity; Kalshi series or Polymarket event for family structure; a contract pair for payout divergence; one contract for the suit category example. Family granularities differ across APIs.",
        "- **Text measurement:** source, temporal, outcome-definition, edge-clause, and discretion proxies averaged on a 0–1 scale. Recognize ET in clock context. Scores describe archived textual specification, not a validated scale of all institutional determinacy.",
        "- **Platform comparisons:** report raw components, text length, threshold-flag composition, and composite means inside each flag group. Since the flag enters the score, these strata reveal composition rather than independently validate the measure.",
        "- **Case method:** preserve exact rules and links; specify a hypothetical scenario, the decisive qualifying condition, implied settlements, and the interpretation boundary. These cases show how divergence can occur, not its population frequency or realized financial impact.",
        "- **Retrieval:** retrieve shared phenomena before screening claim compatibility. First-place/advancement and departure/first-departure pairs remain useful cases while being excluded from high-confidence claim candidates.",
        "- **Activity:** standardize log cumulative volume and determinacy within platform; control observed exposure, opening year, text length, category, and platform. Report the preferred association and one within-family diagnostic per platform; leave existing additional checks in supplementary tables.",
        "- **Scope:** sparse matched histories cannot support a divergence–price-wedge estimate. No extensive new robustness program is needed for the descriptive mechanism contribution.",
        "",
        "## 4. Results",
        "",
        "- **4.1 Different portfolios of claims:** compare the component profiles and contract-type mix. Explain the conditional composite comparison using the table below; avoid a global platform-quality ranking.",
        "- **4.2 Same recognizable issue, different payable claim:** use the primary and election cases as entry points, followed by Fed rounding, the minerals milestone, and the competing-leader departure condition.",
        "- **4.3 What counts as a suit?:** separate within-contract category interpretation from between-contract differentiation. Authentic images and explicit dates need not define the clothing category.",
        "- **4.4 Trading activity across claim portfolios:** report the preferred volume association, contract-type estimates, and the within-family boundary. The evidence does not establish that ambiguity causes participation.",
        "",
        *platform_profile_lines(profiles),
        "",
        "### Case exhibit: scenario → qualifying condition → settlement",
        "",
    ]
    for record in _records(cases):
        lines.extend(
            [
                f"- **{record['phenomenon']}** ({record['scope']}): {record.get('explanation', '')}",
                f"  Hypothetical scenario: {record['witness_state']} A ({record['a_platform']}) = {record['payout_a']}; B ({record['b_platform']}) = {record['payout_b']}.",
            ]
        )
        secondary = record.get("secondary_witness_state")
        if isinstance(secondary, str) and secondary:
            lines.append(
                f"  Second scenario: {secondary} A = {record['secondary_payout_a']}; B = {record['secondary_payout_b']}."
            )
        lines.append(f"  Interpretation boundary: {record.get('audit_note', '')}")
    lines.extend(
        [
            "",
            "Exact clauses and URLs: [casebook](REPRESENTATION_CASEBOOK.md).",
            "",
            "### Compact activity exhibit",
            "",
        ]
    )
    if cohort is not None:
        lines.append(
            f"- Preferred exposure/cohort association: {_estimate(cohort, 'HC3 SE')} SD of log volume per one within-platform SD of the score."
        )
    for platform in ("Kalshi", "Polymarket"):
        model_record = _model_record(models, f"within_family_{platform.lower()}")
        if model_record is not None:
            lines.append(
                f"- Within-family {platform}: {_estimate(model_record, 'family-clustered SE')}. Uses one SD of residual score in internally varying families, so coefficient magnitude is not on the pooled score scale."
            )
    for name, label in (
        ("qualitative_contracts", "No threshold flag"),
        ("quantitative_contracts", "Threshold flag"),
    ):
        model_record = _model_record(models, name)
        if model_record is not None:
            lines.append(
                f"- {label}: {_estimate(model_record, 'HC3 SE')}. Separate significance levels do not test whether the two coefficients differ."
            )
    lines.extend(
        [
            "",
            "- **Main exhibits:** (1) conceptual schematic; (2) sampled platform profile table/figure; (3) compact case matrix; (4) preferred activity estimate and within-family diagnostic. Keep the full model inventory in supplementary outputs.",
            "",
            "## 5. Discussion and conclusion",
            "",
            "- **Answer to the RQ:** platforms differentiate claims through success predicates, milestones, measurement buckets, time and evidence boundaries, and competing outcomes. The sampled portfolios also differ in their mix and textual specification.",
            "- **Theoretical contribution:** collective-intelligence systems help define what information is aggregated about. Clear specification and equivalent claims are separate achievements.",
            "- **Empirical contribution:** auditable ordinary scenarios connect the conceptual distinction to platform rules; component and composition profiles extend beyond isolated anecdotes; volume estimates show an associated portfolio pattern.",
            "- **Design implications:** show ‘what must happen to pay Yes,’ relevant deadlines, measurement conventions, and evidence rules beside similar headlines. Flag first-place versus advancement and individual versus first departure when comparing probabilities. These are proposed implications, not evaluated interventions.",
            "- **Boundaries:** purposive samples, API family granularity, a text proxy, hypothetical rule-based cases, and cumulative activity constrain generalization and causal claims. Keep this concise and tied to what the paper actually claims.",
            "- **Focused extension:** manually verify a phenomenon-diverse pair sample with common-horizon prices to test when payout differences explain apparent forecast disagreement.",
            "- **Closing message:** before asking whose forecast is right, establish what would have to happen for each contract to pay.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
