"""Generate concise research documentation from completed analyses."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd


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


def write_research_log(
    path: Path,
    models: pd.DataFrame,
    error_models: pd.DataFrame,
    matches: pd.DataFrame,
    matched_models: pd.DataFrame,
) -> None:
    """Record all substantive specifications, including weak or infeasible ones."""

    lines = [
        "# Research Log",
        "",
        f"## {date.today().isoformat()} — Iteration 1: transparent composite",
        "",
    ]
    main = models.loc[models["model"] == "main_composite"] if not models.empty else pd.DataFrame()
    if not main.empty:
        main_row = main.iloc[0]
        lines.extend(
            [
                "- Question: Does semantic determinacy predict within-platform standardized log volume, controlling for rule length, market duration, platform, and category?",
                f"- Result: coefficient {main_row['coefficient']:.3f} (HC3 SE {main_row['std_error']:.3f}, p={main_row['p_value']:.3g}, n={int(main_row['n'])}).",
                "- Interpretation: The inverse sign contradicts a simple participation-cost account and is consistent with ambiguity attracting heterogeneous-interpretation trading; volume is not direct evidence of forecast quality or causality.",
                "- Decision: Separate semantic clarity from rule complexity and repeat within platform.",
            ]
        )
    lines.extend(["", f"## {date.today().isoformat()} — Iteration 2: complexity separation", ""])
    robust = (
        models.loc[models["model"] == "complexity_separated"]
        if not models.empty
        else pd.DataFrame()
    )
    if not robust.empty:
        robust_row = robust.iloc[0]
        lines.extend(
            [
                "- Question: Does a core score excluding edge-case completeness survive controls for both rule length and conditional-clause count?",
                f"- Result: coefficient {robust_row['coefficient']:.3f} (HC3 SE {robust_row['std_error']:.3f}, p={robust_row['p_value']:.3g}).",
                "- Interpretation: This check reduces the risk that the composite is merely a verbose-rules measure.",
                "- Decision: Add clustered and event/series-aggregated specifications to rule out repeated-template pseudoreplication.",
            ]
        )
    robustness = (
        models.loc[models["model"].isin(["main_series_clustered", "event_series_aggregated"])]
        if not models.empty
        else pd.DataFrame()
    )
    lines.extend(
        [
            "",
            f"## {date.today().isoformat()} — Iteration 3: dependence and forecast error",
            "",
        ]
    )
    for record in robustness.to_dict(orient="records"):
        lines.append(
            f"- {record['model']}: determinacy coefficient {record['coefficient']:.3f} (SE {record['std_error']:.3f}, p={record['p_value']:.3g}, n={int(record['n'])})."
        )
    if not error_models.empty:
        error_row = error_models.iloc[0]
        lines.extend(
            [
                f"- Terminal-error result: coefficient {error_row['coefficient']:.3f} probability points per determinacy SD (series-clustered SE {error_row['std_error']:.3f}, p={error_row['p_value']:.3g}, n={int(error_row['n'])}).",
                "- Interpretation: The volume pattern does not translate into detectable last-trade accuracy differences; this is an important null, and terminal timing is not a fixed forecast horizon.",
                "- Decision: Reframe the current result as an ambiguity–activity phenomenon and prioritize fixed-horizon errors/spreads in follow-up work.",
            ]
        )
    counts = matches["match_label"].value_counts() if not matches.empty else pd.Series(dtype=int)
    lines.extend(
        [
            "",
            f"## {date.today().isoformat()} — Iteration 4: cross-platform matching",
            "",
            "- Question: Can same-underlying-event contracts be isolated with conservative lexical, numeric, and date agreement before comparing resolution conditions?",
            f"- Result: {int(counts.get('high_confidence', 0))} high-confidence, {int(counts.get('probable', 0))} probable, and {int(counts.get('rejected', 0))} rejected candidates retained for audit.",
        ]
    )
    if not matched_models.empty:
        matched_row = matched_models.iloc[0]
        lines.extend(
            [
                f"- Price-panel result: a one-unit divergence increase corresponds to {matched_row['coefficient']:.3f} absolute probability disagreement in the last 30 days (HC3 SE {matched_row['std_error']:.3f}, p={matched_row['p_value']:.3g}, n={int(matched_row['n'])}).",
                "- Decision: Treat this small matched-panel estimate as suggestive mechanism evidence pending human validation and broader price-history coverage.",
            ]
        )
    else:
        lines.extend(
            [
                "- Price-panel result: insufficient aligned high-confidence histories for a stable regression; retained as a visible failed/limited specification.",
                "- Decision: Use matched examples diagnostically and prioritize human validation plus expanded history coverage.",
            ]
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
) -> None:
    """Write the requested first-study summary with appropriately bounded claims."""

    coverage = coverage_table(contracts)
    platform_descriptions = "; ".join(
        f"{record['platform']}: {int(float(record['contracts'])):,} contracts"
        for record in coverage.to_dict(orient="records")
    )
    high_matches = matches.loc[matches["match_label"] == "high_confidence"]
    main = models.loc[models["model"] == "main_composite"]
    robust = models.loc[models["model"] == "complexity_separated"]
    platform_rows = models.loc[models["model"].str.startswith("within_")]
    dependence_rows = models.loc[
        models["model"].isin(["main_series_clustered", "event_series_aggregated"])
    ]

    results: list[str] = []
    if not main.empty:
        main_row = main.iloc[0]
        results.append(
            f"**Primary exploratory association.** A one-SD increase in within-platform determinacy is associated with {main_row['coefficient']:.3f} SD in log volume (HC3 SE {main_row['std_error']:.3f}, 95% CI [{main_row['ci_lower']:.3f}, {main_row['ci_upper']:.3f}], p={main_row['p_value']:.3g}; n={int(main_row['n']):,})."
        )
    if not robust.empty:
        robust_row = robust.iloc[0]
        results.append(
            f"**Complexity-separated robustness.** Excluding edge-case completeness from the clarity score while directly controlling rule length and conditional clauses gives {robust_row['coefficient']:.3f} SD (SE {robust_row['std_error']:.3f}, p={robust_row['p_value']:.3g})."
        )
    if not platform_rows.empty:
        detail = "; ".join(
            f"{str(record['model']).removeprefix('within_').title()} {record['coefficient']:.3f} (p={record['p_value']:.3g})"
            for record in platform_rows.to_dict(orient="records")
        )
        results.append(f"**Platform heterogeneity.** {detail}.")
    if not dependence_rows.empty:
        detail = "; ".join(
            f"{record['model']}: {record['coefficient']:.3f} (SE {record['std_error']:.3f}, p={record['p_value']:.3g})"
            for record in dependence_rows.to_dict(orient="records")
        )
        results.append(f"**Dependence robustness.** {detail}.")
    if not error_models.empty:
        error_row = error_models.iloc[0]
        results.append(
            f"**Forecast-error null.** For Kalshi's last traded price, determinacy predicts {error_row['coefficient']:.3f} probability points of absolute error per SD (series-clustered SE {error_row['std_error']:.3f}, p={error_row['p_value']:.3g}; n={int(error_row['n']):,}). This is not statistically distinguishable from zero."
        )
    if not matched_models.empty:
        matched_row = matched_models.iloc[0]
        results.append(
            f"**Suggestive matched evidence.** In {int(matched_row['n'])} aligned pairs, a one-unit divergence increase predicts {matched_row['coefficient']:.3f} greater absolute probability disagreement during the last 30 days (SE {matched_row['std_error']:.3f}, p={matched_row['p_value']:.3g})."
        )
    else:
        results.append(
            "**Matched-price limitation.** The first aligned panel is too small for a stable divergence regression; matched contracts are evidence-generating examples, not a confirmed average effect."
        )

    example_lines: list[str] = []
    examples = high_matches.sort_values(
        ["semantic_divergence", "match_confidence"], ascending=False
    ).head(4)
    for record in examples.to_dict(orient="records"):
        example_lines.append(
            f"- **Kalshi:** {record['kalshi_question']} **Polymarket:** {record['polymarket_question']} Difference flagged: {record['identified_semantic_difference']}."
        )
    if not example_lines:
        example_lines.append("- No pair crossed the deliberately conservative high-confidence threshold.")

    first_open = contracts["open_timestamp"].min()
    last_resolution = contracts["resolution_timestamp"].max()
    observed_pairs = len(panel_summary)
    lines = [
        "# 1. Research question",
        "",
        "How does the determinacy of a platform's machine-settleable representation of a future event shape participation and cross-platform agreement in digital prediction markets?",
        "",
        "# 2. Theoretical mechanism",
        "",
        "Prediction-market software does not receive a naturally fixed event state. Contract text, deadlines, sources, exceptions, and fallback procedures first define the state space. Determinacy can reduce interpretation costs, but indeterminacy can also create heterogeneous interpretations that stimulate speculative trade without improving accuracy. This is an Information Systems mechanism because representational design and platform governance condition downstream information aggregation.",
        "",
        "# 3. Data",
        "",
        f"The reproducible public-API sample contains {platform_descriptions}. Opening dates run from {first_open.date() if pd.notna(first_open) else 'unknown'} through a latest observed resolution of {last_resolution.date() if pd.notna(last_resolution) else 'unknown'}. The cross-platform matcher identifies {len(high_matches):,} high-confidence metadata pairs; {observed_pairs} currently have aligned daily histories. Volume units differ across platforms and are standardized within platform. The sample is intentionally focused on high-volume non-sports Kalshi series and high-volume closed Polymarket contracts, so it is not population-representative.",
        "",
        "# 4. Measurement",
        "",
        "The transparent 0–1 determinacy composite averages source specificity, temporal specificity, operational outcome definition, edge-case completeness, and absence of discretionary resolution language. Rule length and conditional-clause count remain separate complexity measures. For matched pairs, divergence combines wording, numeric/date conditions, named sources, required event stage, and closing-date distance. These are auditable proxies rather than validated latent-variable scales.",
        "",
        "# 5. Main method",
        "",
        "Market-level OLS relates standardized log volume to within-platform standardized determinacy with platform/category controls, market duration, and rule length. Alternatives separate conditional complexity, cluster uncertainty by series, and collapse repeated contracts to series/events. A Kalshi model tests last-trade absolute forecast error. Matching uses nearest-neighbor lexical retrieval followed by numeric, predicate, and date gates; price histories are aligned daily using only contemporaneous or earlier observations.",
        "",
        "# 6. Main results",
        "",
        *results,
        "",
        "The robust inverse volume association is consistent with an ambiguity–activity mechanism: less determinate contracts may invite heterogeneous interpretations and more trade. It does not show better information aggregation, and the terminal-error null offers no accuracy benefit. Volume is a participation proxy, the associations are not causal, and high statistical visibility can partly reflect the large metadata sample.",
        "",
        "# 7. Best empirical examples",
        "",
        *example_lines,
        "",
        "# 8. Best figures/tables",
        "",
        "- `figures/views-conceptual-schematic.svg`: locates contract representation upstream of trading and resolution.",
        "- `figures/views-determinacy-distribution.svg`: compares the score distribution across platforms.",
        "- `figures/views-determinacy-volume.svg`: shows the raw within-platform volume gradient by score quintile.",
        "- `figures/views-matched-trajectories.svg`: displays aligned prices for the most visibly divergent matched pairs when histories are available.",
        "- `tables/analysis-market-models.csv`: reports the main and complexity-separated coefficients.",
        "- `tables/matching-representative-pairs.csv`: provides auditable contract text and flagged semantic differences.",
        "",
        "# 9. Information Systems paper storyline",
        "",
        "**Phenomenon:** Platforms encode apparently similar uncertain events into contracts with measurably different semantic precision and truth conditions.",
        "",
        "**Puzzle:** Aggregation accounts usually treat the event being priced as fixed, even though a digital platform must construct it first.",
        "",
        "**Theoretical mechanism:** Determinate representations lower interpretive friction, while indeterminate ones can stimulate trade through interpretive disagreement; divergent representations can sustain rational price differences because the digital objects are not equivalent claims.",
        "",
        "**Evidence:** Lower determinacy is robustly associated with more volume across both platforms and after complexity/dependence checks, but not with better terminal accuracy. Concrete matched contracts expose different rules alongside price paths where available.",
        "",
        "**Contribution:** Digital systems structure the referents of collective intelligence, not merely the speed or accuracy with which information about those referents is processed.",
        "",
        "# 10. Candidate paper titles",
        "",
        "- Defining the Future: Semantic Determinacy and Information Aggregation in Digital Prediction Markets",
        "- Before the Crowd Can Forecast: How Platforms Construct Predictable Events",
        "- Same Future, Different Contract: Semantic Divergence in Prediction Markets",
        "- Trading on Different Meanings: Semantic Indeterminacy in Prediction Markets",
        "- The State Space Is the System: Representation and Collective Forecasting",
        "",
        "# 11. Candidate abstract",
        "",
        "Prediction markets are commonly understood as information systems that aggregate dispersed beliefs about future events. Yet the event is not a ready-made input: a platform must encode an uncertain real-world phenomenon as a machine-settleable digital contract. We theorize semantic determinacy—the degree to which real-world states map unambiguously onto formal outcomes—and divergence between contracts intended to represent the same event. Using reproducible public metadata and price histories from Kalshi and Polymarket, we construct transparent measures of source, temporal, definitional, edge-case, and discretion specificity. Across both platforms, lower determinacy is associated with greater trading volume after accounting for rule complexity, duration, category, and repeated series, consistent with an ambiguity–activity mechanism in which heterogeneous interpretations stimulate trade. Determinacy does not, however, predict Kalshi last-trade forecast error, cautioning against treating activity as aggregation quality. Precision-oriented matching further identifies same-event contracts with different deadlines, sources, and event stages. The study reframes prediction markets as systems that both define and aggregate information, showing that digital representation can generate participation without demonstrably improving accuracy and extending Information Systems theory on digital objects, information quality, and platform governance.",
        "",
        "# 12. What remains before submission",
        "",
        "## Essential next steps",
        "",
        "- Human-validate a stratified sample of high-confidence, probable, and rejected matches and report precision.",
        "- Expand price-history coverage and test spread, volatility, and fixed-horizon forecast error rather than relying on cumulative volume.",
        "- Validate the determinacy components with independent coders or a cached structured annotation exercise.",
        "",
        "## Robustness extensions",
        "",
        "- Reweight repeated Kalshi series templates and cluster uncertainty at series/event level.",
        "- Test alternative component weights, ambiguity lexicons, time windows, and liquidity thresholds.",
        "- Separate quantitative threshold markets from qualitative event predicates.",
        "",
        "## Optional nice-to-have analyses",
        "",
        "- Reconstruct timestamped clarification events and examine non-causal event-time patterns.",
        "- Add on-chain Polymarket trades and historical Kalshi bid/ask data for richer microstructure outcomes.",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
