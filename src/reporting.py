"""Generate the approved case-led manuscript and bounded supplementary evidence."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pandas as pd

from src.anecdotes import add_claim_relations


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


def _write_lines(path: Path, lines: list[str]) -> None:
    """Write a deterministic UTF-8 research document."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def representation_bridge_lines() -> list[str]:
    """Explain normalized expected payout without claiming a new updating theory."""

    return [
        "The rules define which outcomes pay. Traders use evidence to assess those outcomes, and trading produces market prices. These functions can develop together over time.",
        "",
        "With a common distribution `μ` over relevant histories, the value of a specified normalized payout is `q_c = E_μ[r_c]`. Thus `q_A − q_B = E_μ[r_A − r_B]`. The identity holds for any common probability distribution. Different payout mappings can have different expected values, although non-equivalence alone does not guarantee a value difference.",
        "",
        "For binary payouts, expected payout equals the probability of the paying event. Fractional settlement requires the payout amount: a 20% chance of a full dollar and a 30% chance of 50 cents give an expected payout of 35 cents. This is a synthetic illustration.",
        "",
        "Where rules delegate interpretation, valuation can include expectations about how a later decision will be made. A rule may leave a clothing category unspecified while the institution ultimately records a definite settlement. Price-based clauses require past-price inputs in the modeled history. The formal qualifications and binary-event restrictions are in [constructs](../docs/CONSTRUCTS.md).",
    ]


def coherence_status_lines(cases: pd.DataFrame, diagnostics: pd.DataFrame) -> list[str]:
    """Report semantic and observation eligibility separately from realized cases."""

    applicable = int(cases.coherence_test_applicable.sum()) if not cases.empty else 0
    estimated = int(diagnostics.status.eq("estimated").sum()) if not diagnostics.empty else 0
    return [
        f"The case inventory contains {len(cases)} exhibits; {applicable} supply a validated binary marginal restriction. {estimated} observation-level price diagnostics are estimable.",
        "",
        "The saved price histories are a dormant diagnostic panel. Original observations are clipped to the supported window before aggregation, and source timestamps and fill ages are retained. Daily labels and forward fills do not certify fresh synchronized quotes. No general divergence–price effect, trader misunderstanding, or forecast-accuracy advantage is established. Missing excess values mean insufficient evidence.",
    ]


def platform_profile_lines(profiles: pd.DataFrame) -> list[str]:
    """Render literal text components as descriptions of selected portfolios."""

    if profiles.empty:
        return ["Platform text profiles unavailable."]
    overall = profiles.loc[profiles.stratum.eq("all")].set_index("platform")
    platforms = sorted(overall.index.astype(str))
    lines = [
        "| Sampled text feature | " + " | ".join(platforms) + " |",
        "|---|" + "---:|" * len(platforms),
    ]
    for label, column, fmt in (
        ("Contracts", "contracts", ",.0f"),
        ("Exploratory rule-text specificity index", "mean_determinacy", ".3f"),
        ("Authority/source cues", "source_specificity", ".3f"),
        ("Date/time cues", "temporal_specificity", ".3f"),
        ("Definition/threshold cues", "outcome_definition", ".3f"),
        ("Edge-clause cues", "edge_completeness", ".3f"),
        ("Absence of flagged discretion terms", "discretion_clarity", ".3f"),
        ("Threshold-flag share", "threshold_flag_share", ".1%"),
        ("Mean analyzed text length (words)", "mean_text_words", ".1f"),
    ):
        cells = [format(float(overall.loc[platform, column]), fmt) for platform in platforms]
        lines.append(f"| {label} | " + " | ".join(cells) + " |")
    lines.extend([
        "",
        "Literal cues describe the retained portfolios. The legacy column `determinacy_score` stores an exploratory text index; it has no independent human construct validation. The threshold flag contributes to that index, so stratification is descriptive. Corrected parsing eliminates the previously reported composition reversal. Final field-placement invariance is documented separately from the frozen four-repair diagnostic in the measurement note.",
        "",
    ])
    for platform in platforms:
        row = overall.loc[platform]
        lines.append(f"- {platform}: {row['families']:,.0f} API families; top five contain {row['top_five_family_share']:.1%} of rows; {row['varying_families']:,.0f} families ({row['contracts_in_varying_families']:,.0f} rows) vary internally in the index.")
    lines.append("Kalshi series and Polymarket events have different granularity. Their family counts and concentration do not rank platform diversity.")
    return lines


def sample_limit_lines(contracts: pd.DataFrame) -> list[str]:
    """State the fixed sample's provenance and unrecoverable selection boundaries."""

    counts = contracts.groupby("platform").size()
    description = "; ".join(f"{platform}: {count:,}" for platform, count in counts.items())
    return [
        f"The fixed historical sample contains {len(contracts):,} contracts ({description}). Raw normalization reconciles 12,253 Kalshi rows minus two missing titles and 8,000 retained Polymarket rows minus 751 unsupported outcome-label rows. Raw snapshots remain unchanged.",
        "",
        "Kalshi coverage selects 120 high-volume series and caps each acquisition tier. Polymarket coverage selects high-volume closed markets using a flawed historical sports filter. `gameStartTime` wrongly flagged named minerals and suit markets as sports. The classifier is repaired for future acquisition; omitted historical records are not restored by that repair. The 23,700 scanned minus 8,000 retained difference is 15,700, with no established sports/overflow split. These portfolios are purposive, use different category/family schemes, and support no population ranking.",
        "",
        "September 10 is the legacy snapshot label, not a verified HTTP acquisition timestamp. Three Polymarket source updates fall on September 11; the discrepancy remains unresolved. Missing historical caches now fail before network access. Date-only retrieval boundaries and metadata elapsed time are exposure proxies. The audit separates scheduled future openings, positive-volume same-day openings and close-before-open records; neither clipping nor alternate date conventions establishes that rules preceded trading.",
        "",
        "Outcome provenance separates Kalshi recorded binary results and scalar settlements from Polymarket final-status endpoint prices and unresolved price inference. Fifteen proposed-status and 38 missing-status endpoint records are qualified separately; two `settled` statuses count as recorded final status. Six Kalshi scalar settlements and ten Polymarket intermediate-price cases remain separate categories. See [data sources](../DATA_SOURCES.md) and the sample audit tables for the exact ledger.",
    ]


def case_exhibit_lines(cases: pd.DataFrame, *, observed_only: bool = False) -> list[str]:
    """Render only assertions that remain bound to verified operative inputs."""

    if cases.empty:
        return ["Case evidence unavailable."]
    cases = add_claim_relations(cases)
    priority = {"hilton-first-vs-advance": 0, "khamenei-death-allocation": 1, "suit-adjudication-episode": 2, "minerals-observed-chronology": 3}
    rows = sorted(_records(cases), key=lambda row: (priority.get(str(row["case_id"]), 9), str(row["case_id"])))
    lines: list[str] = []
    for row in rows:
        observed = str(row.get("evidence_kind", "")).startswith("observed_") or str(row.get("scenario_status", "")).lower().startswith(("observed", "realized"))
        if observed_only and not observed:
            continue
        lines.extend([f"### {row['phenomenon']}", ""])
        if not bool(row.get("claim_relation_validated", False)):
            lines.extend(["Operative inputs require re-audit; payout and witness assertions are withheld.", ""])
            continue
        lines.extend([
            f"- **Evidence:** {row['scenario_status']}",
            f"- **Scenario:** {row['witness_state']}",
            f"- **Qualifying condition:** A — {row['signature_a']}; B — {row['signature_b']}.",
            f"- **{'Settlement' if observed else 'Hypothetical payout'}:** A — {row['payout_a']}; B — {row['payout_b']}.",
            f"- **Implication:** {row.get('explanation', '')}",
            f"- **Boundary:** {row.get('audit_note', '')}",
            "- **Contracts:** " + "; ".join(
                f"[{row[f'{side}_contract_id']}]({row[f'{side}_url']})"
                for side in ("a", "b")
                if str(row.get(f"{side}_url", "")).startswith("https://")
            ) + ".",
        ])
        if observed:
            lines.append(f"- **Chronology:** {row.get('chronology', '')}")
            sources = json.loads(str(row.get("event_sources", "[]")))
            for source in sources:
                lines.append(f"- **Independent event evidence:** [{source['finding']}]({source['url']}).")
        lines.append("")
    if not lines:
        lines.append("Observed cases require the explicitly versioned case-evidence bundle.")
    lines.extend(["Full operative text, source versions, outcome evidence and chronology: [casebook](REPRESENTATION_CASEBOOK.md) and [case matrix](tables/representation-case-matrix.csv).", ""])
    return lines


def _opening_lines(cases: pd.DataFrame) -> list[str]:
    """Use an actual opening contrast only when its complete-input audit is valid."""

    audited = add_claim_relations(cases) if not cases.empty else cases
    realized = audited.loc[audited.case_id.astype(str).str.contains("hilton")] if not audited.empty else audited
    if not realized.empty and bool(realized.claim_relation_validated.all()):
        return ["Steve Hilton finished second in California's June 2, 2026 gubernatorial primary and advanced under the top-two rule. The archived first-place Kalshi contract settled NO/$0; the Polymarket advancement contract recorded resolved YES. The result concerns one election, yet the contracts reward different achievements.", ""]
    return ["Apparently similar prediction-market questions can specify different payouts. The empirical comparison requires complete archived rules and independently supported event and settlement records.", ""]


def literature_lines() -> list[str]:
    """Position the diagnostic contribution against the verified review source map."""

    return [
        "[Wolfers and Zitzewitz (2004)](https://doi.org/10.1257/0895330041371321) already discuss payoff design, clear specification and adjudication. [Wand and Weber (1993)](https://doi.org/10.1111/j.1365-2575.1993.tb00127.x) relate representational clarity to interpretation mappings. [Eriksson and Öhlund (2024)](https://doi.org/10.17705/1jais.00845) show how constitutive rules create digitally represented institutional entities and rights. Here the observable objects are contract clauses and settlements; published text does not identify designers' motives.",
        "",
        "[Gebele and Matthes (2026)](https://arxiv.org/abs/2601.01706) directly study resolution semantics, payoff regions and cross-platform comparison. [Capponi, Gliozzo and Zhu (2025)](https://arxiv.org/abs/2512.02436) develop automated relationship discovery. Their preprints supply close comparisons; their empirical performance is not independently replicated here. This paper's diagnostic contribution is the joined audit of separating scenarios, fractional settlement and delegated interpretation. It makes no priority claim for payoff mappings or event-equivalence checks.",
        "",
        "[Wang (2026)](https://doi.org/10.1016/j.econlet.2026.113176) examines event occurrence versus pending adjudication; the review accessed an abstract, highlights and section passages, rather than the complete paywalled article. [Nechepurenko (2026)](https://arxiv.org/abs/2609.15368) distinguishes proposals, disputes, oracle settlement and adapter completion in a recent preprint. These distinctions guide the case chronology and prevent treating closure timestamps as a full settlement history. The Rezaei Sanjabi working paper remains an abstract-only lead; its empirical findings are not adopted.",
    ]


def reference_lines() -> list[str]:
    """Supply the bounded verified bibliography without inventing inaccessible details."""

    return [
        "- Wolfers, J., & Zitzewitz, E. (2004). Prediction Markets. *Journal of Economic Perspectives, 18*(2), 107–126. [DOI](https://doi.org/10.1257/0895330041371321).",
        "- Wand, Y., & Weber, R. (1993). On the ontological expressiveness of information systems analysis and design grammars. *Information Systems Journal*. [DOI](https://doi.org/10.1111/j.1365-2575.1993.tb00127.x).",
        "- Eriksson, O., & Öhlund, A. (2024). Digital Institutionalization: The Case of E-Prescribing. *Journal of the Association for Information Systems*. [DOI](https://doi.org/10.17705/1jais.00845).",
        "- Gebele, J., & Matthes, F. (2026). Semantic Non-Fungibility and Violations of the Law of One Price in Prediction Markets. arXiv:2601.01706v1, preprint. [Version](https://arxiv.org/html/2601.01706v1).",
        "- Wang, G. (2026). Do prediction markets price events or adjudication? Evidence from the disputed Polymarket markets. *Economics Letters, 268*, 113176. [DOI](https://doi.org/10.1016/j.econlet.2026.113176). Review access was partial.",
        "- Nechepurenko, M. (2026). Resolution Is Not Settlement, Part I: Oracle Adjudication and Semantic Governance on Polymarket. arXiv:2609.15368v1, preprint. [Version](https://arxiv.org/html/2609.15368v1).",
        "- Capponi, A., Gliozzo, A., & Zhu, B. (2025). Semantic Trading: Agentic AI for Clustering and Relationship Discovery in Prediction Markets. arXiv:2512.02436v1, preprint. [Version](https://arxiv.org/html/2512.02436v1).",
    ]


def supplementary_model_lines(models: pd.DataFrame) -> list[str]:
    """Present final estimates with their actual covariance and confidence intervals."""

    lines = ["| Specification | Coefficient | 95% interval | Uncertainty | n |", "|---|---:|---:|---|---:|"]
    for name in ("cohort_exposure_adjusted", "cohort_exposure_adjusted_hc3", "within_family_kalshi", "within_family_polymarket"):
        row = _model_record(models, name)
        if row is not None:
            covariance = str(row.get("covariance", "family-clustered" if name != "cohort_exposure_adjusted_hc3" else "HC3"))
            lines.append(f"| {name} | {_value(row, 'coefficient'):.4f} | [{_value(row, 'ci_lower'):.4f}, {_value(row, 'ci_upper'):.4f}] | {covariance}; SE {_value(row, 'std_error'):.4f} | {int(_value(row, 'n')):,} |")
    lines.extend(["", "The preferred pooled coefficient uses one within-platform SD of the text index and standardized log cumulative volume. Its family clusters are qualified by platform. HC3 uses the same formula and rows as a covariance comparison. Within-family models use internally varying families and a different residual-score SD; their magnitudes are not directly comparable to the pooled coefficient.", "", "Volume selection, retrospective rules, family concentration and incomplete exposure metadata limit interpretation to these selected portfolios. Subgroup significance differences do not test heterogeneity. The frozen review's top-five families contribute 69.48% of focal sandwich variance; its bounded largest-family deletion remains negative. Those checks concern the archived and frozen repaired specifications, rather than certifying the final field-invariant index. No new deletion grid was run."])
    return lines


def write_supplementary_results(path: Path, models: pd.DataFrame, error_models: pd.DataFrame, panel_summary: pd.DataFrame, matched_models: pd.DataFrame) -> None:
    """Keep activity, terminal-error and dormant panel evidence outside the main argument."""

    lines = ["# Supplementary analysis", "", *supplementary_model_lines(models), "", "## Terminal-error diagnostic", ""]
    if not error_models.empty:
        lines.append(_estimate(_records(error_models)[0], "family-clustered SE") + ". This last-trade Kalshi diagnostic lacks a common forecast horizon; a null is not equivalence.")
    else:
        lines.append("Not estimable on the available final analysis rows.")
    lines.extend(["", "## Dormant price panel", "", f"{len(panel_summary)} saved pair summaries remain. Matched-model rows: {len(matched_models)}. There are no qualifying synchronized-price observations. The retained `bad72f8883` cache and alternate `627b27c83f-interval-max` contain different pair inventories; the alternate third pair remains eligible, so prior three-to-two attrition was not caused by current eligibility.", "", "All existing model rows are retained in [analysis-market-models.csv](tables/analysis-market-models.csv), with formula, covariance, sample size and confidence intervals. These exploratory values are unadjusted for multiple comparisons. Figures of score–volume bins use unclustered descriptive mean intervals, separate from preferred family-clustered model inference."])
    _write_lines(path, lines)


def write_research_summary(path: Path, contracts: pd.DataFrame, models: pd.DataFrame, error_models: pd.DataFrame, matches: pd.DataFrame, panel_summary: pd.DataFrame, matched_models: pd.DataFrame, cases: pd.DataFrame, profiles: pd.DataFrame, coherence: pd.DataFrame) -> None:
    """Generate a case-led summary synchronized with the approved outline."""

    counts = matches.match_label.value_counts() if not matches.empty else pd.Series(dtype=int)
    lines = ["# Same Future, Different Claim", "", *_opening_lines(cases), "## Question and evidence", "", "When do apparently similar market questions expose traders to different settlements, and when does written text leave a scenario to later interpretation? The main evidence joins realized settlements, documented adjudication and exact rule comparisons. It establishes case-level distinctions; it does not estimate their prevalence or effects on prices.", "", *case_exhibit_lines(cases, observed_only=True), "## Concepts and compact payout explanation", "", "**Payoff divergence** occurs when two contracts pay differently in an explicitly specified relevant scenario. **Written-rule determinacy** concerns whether a specified rule version and stated information determine one payout. Different procedures require a separating payout scenario before they establish divergence. Adjudication can supply the later institutional decision.", "", *representation_bridge_lines(), "", "## Position in the literature", "", *literature_lines(), "", "## Sampled text context", "", *sample_limit_lines(contracts), "", *platform_profile_lines(profiles), "", f"Automated matching retains {int(counts.get('high_confidence', 0))} high-confidence candidates, {int(counts.get('probable', 0))} probable candidates and {int(counts.get('rejected', 0))} rejected rows. The manually audited candidate predicates/windows are documented separately; retrieval confidence alone does not establish complete-rule equivalence.", "", "## Supplementary empirical checks", "", *supplementary_model_lines(models), "", *coherence_status_lines(cases, coherence), "", "Activity estimates, terminal-error diagnostics and dormant panel details: [supplementary analysis](SUPPLEMENTARY_ANALYSIS.md).", "", "## Implications and limits", "", "Contract comparison and offsetting positions require the same paying condition and amount. Forecast evaluation must identify the milestone being predicted. Interfaces could show those conditions beside prices; that intervention remains untested. Account cash returns can include reimbursements, so the Khamenei contract settlement is distinguished from trader-level receipts. The suit dispute shows that adjudication matters without proving manipulation or a causal ambiguity effect.", "", "The incremental contribution is an empirical diagnostic of comparability, extending established attention to contract specification with linked payout and chronology evidence. The composite platform-ranking and composition-reversal claims are withdrawn. Case evidence survives this correction."]
    _write_lines(path, lines)


def write_research_status(path: Path, contracts: pd.DataFrame, models: pd.DataFrame, cases: pd.DataFrame, profiles: pd.DataFrame, coherence: pd.DataFrame) -> None:
    """Write a current handoff while preserving research history elsewhere."""

    lines = ["# Research Status", "", f"Updated {date.today().isoformat()} after approved P1–P7 implementation.", "", *_opening_lines(cases), *coherence_status_lines(cases, coherence), "", "## Current sample and measurement", "", *sample_limit_lines(contracts), "", *platform_profile_lines(profiles), "", "## Supplementary association", "", *supplementary_model_lines(models), "", "## Locked scope", "", "Use the case-led PAPER_OUTLINE.md and documented casebook. Keep payoff divergence distinct from written-rule determinacy. Treat text features as portfolio context and volume as supplementary. No replacement historical sample, new activity design, synchronized price collection, comprehension study or new critic round was authorized. Missing historical caches fail closed. Research-log entries survive regeneration; cycle approval, archives and validation are in paper-revision/2026-10-12-01/."]
    _write_lines(path, lines)


def write_paper_outline(path: Path, contracts: pd.DataFrame, models: pd.DataFrame, cases: pd.DataFrame, profiles: pd.DataFrame) -> None:
    """Generate the approved five-section working conference-paper outline."""

    lines = ["# Same Future, Different Claim: How Prediction Markets Define What Counts", "", "Working ICIS conference-paper outline, revised under approved P1–P7. Main evidence: observed settlements and adjudication; sampled literal text features provide context. Activity estimates are supplementary.", "", "## 1. Introduction", "", *_opening_lines(cases), "- **Research question:** When do apparently similar prediction-market questions expose traders to different settlements, and when do written rules leave a scenario to later interpretation?", "- **Puzzle:** the market headline identifies a public phenomenon; operative clauses select an achievement, deadline, evidence source, exception and payout amount. Comparisons of displayed prices depend on those selections.", "- **Contribution:** a diagnostic account grounded in linked event/rule/settlement records. It distinguishes ordinary achievement conditions, fractional exceptions and delegated interpretation; it estimates no causal price mechanism or trader-comprehension effect.", "", "## 2. Literature and constructs", "", *literature_lines(), "", "**Payoff divergence** requires an explicitly specified scenario with different payouts. **Written-rule determinacy** asks whether the rule version uniquely determines the payout given the information held fixed. A complete eventual adjudication and an incomplete written garment criterion are compatible. Semantic differentiation describes observed rule dimensions; motives and design processes require additional evidence.", "", *representation_bridge_lines(), "", "## 3. Method", "", "- **Case audit:** bind assertions to complete operative inputs, stable platform identifiers and source versions. For realized splits, verify both contract settlements and an independent event source. Separate observed events, observed settlements, dispute chronology and hypothetical payout witnesses. Changed operative inputs block stale assertions pending re-audit.", "- **Sample and provenance:** freeze the historical 19,500 rows for before/after measurement comparison. Report flawed historical selection and absent acquisition timestamps. Preserve raw data and distinguish normalization attrition from acquisition exclusions.", "- **Text features:** report authority, date/time, definition/threshold, edge-clause and discretion-term cues literally. The legacy composite is exploratory. Four bounded parser repairs and field-placement invariance are documented; no human inter-coder validation is claimed.", "- **Supplementary methods:** use the exact exposure/opening-cohort formula with platform-qualified family clusters. Compare HC3 on identical rows; retain existing within-family diagnostics with their distinct scale. Daily price alignment supplies no synchronized-price test.", "", "## 4. Results", "", *case_exhibit_lines(cases, observed_only=True), "### Sampled text context", "", *platform_profile_lines(profiles), "", "The minerals chronology records YES/YES in successive contracts and does not instantiate the separate announcement-versus-signature counterfactual. President-elect interruption, Fed quantization and Trump announcement/first-departure scenarios remain supplementary witnesses with their rule qualifications. Exhibit counts refer to cases rather than independent mechanisms.", "", "Main exhibits: (1) Hilton settlement contrast; (2) Khamenei fractional settlement; (3) suit adjudication chronology; (4) literal text profile and compact payout schematic. Full rules and supplementary witnesses are in the casebook. All volume/terminal-error tables and their uncertainty belong in [supplementary analysis](SUPPLEMENTARY_ANALYSIS.md).", "", "## 5. Discussion and conclusion", "", "Contract prices are comparable only after the paying conditions and amounts have been established. Hilton demonstrates an ordinary milestone distinction; Khamenei demonstrates a special price-based exception; the suit episode demonstrates institutional completion of a disputed category. The cases make established specification concerns concrete through auditable linked records.", "", "For comparison and hedging, show what qualifies and how much pays. For forecast evaluation, identify the achievement being evaluated. For adjudication, retain proposal/dispute/final-outcome chronology. Interface recommendations remain proposals.", "", "Purposive volume selection, flawed historical filtering, missing acquisition records, retrospective rule snapshots, unvalidated text indices and limited synchronized price evidence constrain generalization. Account reimbursements and contract payouts are separate. No platform ranking, manipulation inference or causal effect follows from these exhibits.", "", "Before comparing forecasts, establish what would have to happen for each contract to pay.", "", "## Appendix: sample and provenance note", "", *sample_limit_lines(contracts), "", "## References", "", *reference_lines(), "", "The linked citations in section 2 are the verified review source map. Recent preprints, partial article access and abstract-only leads retain their stated evidence levels. The former Bayesian source audit is preserved as history; the elementary expected-payout identity supplies no new updating theorem."]
    _write_lines(path, lines)


def write_claim_confidence(path: Path, models: pd.DataFrame, cases: pd.DataFrame, profiles: pd.DataFrame) -> None:
    """Regenerate the twenty original claim IDs with their approved dispositions."""

    preferred = _model_record(models, "cohort_exposure_adjusted")
    volume = "Not estimable" if preferred is None else f"β={_value(preferred, 'coefficient'):.4f}, family-clustered 95% CI [{_value(preferred, 'ci_lower'):.4f}, {_value(preferred, 'ci_upper'):.4f}], n={int(_value(preferred, 'n')):,}"
    dispositions = [
        (1, "First place versus advancement", "Hilton supplies archived NO/$0 versus resolved YES; supplementary Steyer second-place witness remains hypothetical. Complete-rule audit gates each case."),
        (2, "Call versus inauguration", "Bounded counterfactual; overlapping/non-nested under the archived model; no realized split or global ordering estimated."),
        (3, "Fed quantization", "12.5-bp counterfactual conditional on literal wording and other operative clauses; no realized unusual-rate case established."),
        (4, "Announcement versus signature", "Minerals chronology records YES/YES; separate YES/NO witness concerns dates, scope and milestones together."),
        (5, "Announcement versus first departure", "Trump witness remains hypothetical with competing leaders and death-price exception; no global binary relation."),
        (6, "Suit category and adjudication", "Observed appearance, proposed/disputed sequence and final NO support adjudication relevance; no manipulation or causal ambiguity inference."),
        (7, "Portfolio text descriptions", "Corrected literal components describe selected rule text; independent human scale validation is absent."),
        (8, "Composition reversal", "WITHDRAWN: bounded parser corrections eliminate the old overall/within-stratum reversal; no replacement institutional ranking."),
        (9, "Threshold and family composition", "Corrected flag shares and API-family descriptions are sample context; granularity differs between platforms."),
        (10, "Pooled activity association", volume + "; supplementary selected-portfolio association."),
        (11, "Within-family identification", "Existing diagnostics retain a residual-score SD distinct from the pooled scale; inspect final model table rather than reusing old values."),
        (12, "Subgroup activity estimates", "Exploratory supplementary coefficients; different significance levels do not establish heterogeneity."),
        (13, "Temporal activity stability", "Existing period models are exploratory descriptions; no preregistered holdout or new interaction grid."),
        (14, "Terminal-error association", "Supplementary Kalshi last-trade diagnostic lacks a common horizon; no accuracy advantage or equivalence established."),
        (15, "Generalization and cause", "Volume-selected, retrospective portfolios and family concentration prevent causal or market-wide interpretation."),
        (16, "Expected-payout identity", "Elementary background under any common distribution; fractional amounts matter. Khamenei separately records 45c versus YES, with differing deadlines and possible reimbursements."),
        (17, "Interface comparability", "Untested proposal to display qualifying conditions and payout amounts; no behavioral effect measured."),
        (18, "Logical probability restrictions", "Mathematical background for complete determinate binary relations; fractional/adjudicated exceptions require qualifications."),
        (19, "Written-rule determinacy", "Conditional on stated scenario information and rule version. Later adjudication may define one eventual outcome."),
        (20, "Observed price-coherence test", "Not estimable: no qualifying synchronized-price observations; missing excess is insufficient evidence."),
    ]
    audited = add_claim_relations(cases) if not cases.empty else cases
    required_cases = {
        1: "hilton-first-vs-advance", 2: "election-call-vs-inauguration",
        3: "fed-quantization-convention", 4: "minerals-observed-chronology",
        5: "leader-announcement-vs-departure", 6: "suit-adjudication-episode",
        16: "khamenei-death-allocation",
    }
    for index, (identifier, label, _disposition) in enumerate(dispositions):
        if identifier in required_cases:
            selected = audited.loc[audited.case_id.eq(required_cases[identifier])] if not audited.empty else audited
            if selected.empty or not bool(selected.claim_relation_validated.all()):
                dispositions[index] = (identifier, label, "Case assertion withheld: verified operative inputs are unavailable or changed; re-audit required.")
    lines = ["# Claim confidence and disposition", "", f"Updated {date.today().isoformat()} under approved P1–P7. Claim IDs preserve the former overview; row counts denote exhibits rather than independent mechanisms.", "", "| ID | Claim | Current evidence and boundary |", "|---:|---|---|"]
    lines.extend(f"| {identifier} | {label} | {disposition} |" for identifier, label, disposition in dispositions)
    lines.extend(["", f"The generated case matrix contains {len(cases)} exhibits. Numerical profiles and covariance rows are regenerated from final data. Code tests establish parser/pipeline behavior; they supply no human construct reliability.", "", "Evidence: [casebook](REPRESENTATION_CASEBOOK.md), [model table](tables/analysis-market-models.csv), [profiles](tables/analysis-platform-profiles.csv), [supplementary analysis](SUPPLEMENTARY_ANALYSIS.md)."])
    _write_lines(path, lines)
