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
    """Explain the forecast target and fractional payout with ordinary expected-value reasoning."""

    return [
        'Write r_c(ω) for the amount paid by contract c in a fully specified relevant history ω, normalized so that a full payout is one. A history includes the event facts and any required reference prices or authority decisions. Under a common probability distribution μ, the expected payout is:',
        '',
        '```text\nq_c = E_μ[r_c]\nq_A − q_B = E_μ[r_A − r_B]\n```',
        '',
        'If r_c can take only zero and one, q_c is the probability of the condition that pays one. With fractional amounts, q_c is an expected amount. For example, a 20% chance of receiving one dollar and a 30% chance of receiving 50 cents contribute 35 cents to expected payout. These probabilities are a synthetic illustration. A binary occurrence, such as departure from office, need not imply a binary settlement when the contract contains a fractional exception.',
        '',
        'This distinction concerns what is valued. Observed price p_c also reflects trading conditions, including liquidity, spreads, fees and risk preferences. Different payout mappings can have different expected values under common beliefs; a separating scenario alone does not establish that their expected values differ. The scenario may have zero probability, or differences elsewhere may offset it. The expected-value identity clarifies the comparison without identifying an empirical price effect.',
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
        ("Authority/source cue score", "source_specificity", ".3f"),
        ("Date/time cue score", "temporal_specificity", ".3f"),
        ("Definition/threshold cue score", "outcome_definition", ".3f"),
        ("Edge-clause cue score", "edge_completeness", ".3f"),
        ("Discretion-term score (1 − penalty)", "discretion_clarity", ".3f"),
        ("Threshold-flag share", "threshold_flag_share", ".1%"),
        ("Mean analyzed text length (words)", "mean_text_words", ".1f"),
    ):
        cells = [format(float(overall.loc[platform, column]), fmt) for platform in platforms]
        lines.append(f"| {label} | " + " | ".join(cells) + " |")
    lines.extend([
        "",
        "The five components are mean weighted cue scores, not frequencies of institutionally determinate rules. The discretion-term score is max(0, 1 − 0.25 × the number of distinct configured phrases); 0.811 does not mean 81.1% of rules lack a flag. The legacy column `determinacy_score` stores their exploratory mean, without independent human construct validation. The threshold flag contributes to that index, so stratification is descriptive. Measurement repairs and field-placement invariance are documented in the measurement note.",
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
    """Introduce each event before interpreting its audited conditions and evidence."""

    if cases.empty:
        return ["Case evidence unavailable."]
    audited = add_claim_relations(cases)
    priority = {"hilton-first-vs-advance": 0, "minerals-observed-chronology": 1, "khamenei-death-allocation": 2, "suit-adjudication-episode": 3}
    rows = sorted(_records(audited), key=lambda row: (priority.get(str(row["case_id"]), 9), str(row["case_id"])))
    narratives = {
        "hilton-first-vs-advance": "The Kalshi claim rewarded first place and allowed a proportional payout for exact ties. The Polymarket claim rewarded advancement, for which either of the top two positions qualified. Hilton's untied second place therefore produced NO and a recorded zero settlement on Kalshi, alongside resolved YES and a full unit payout on Polymarket. The common election result supports both outcomes because the contracts select different achievements.",
        "minerals-observed-chronology": "The earlier contract accepted a public announcement of an agreement by March 31. The later contract required signing or formal adoption by April 30 and excluded an announcement alone. These are successive milestones with different windows. The recorded YES outcomes show that such differences need not produce a realized split: an announcement can satisfy the earlier condition, and a subsequent signature can satisfy the later one.",
        "khamenei-death-allocation": "The Kalshi description covered departure before July 1, 2026 and qualifying announcements, but treated a death-only departure through a pre-death price or a committee's fair allocation. Its record reports a scalar settlement of $0.45. The Polymarket rule covered loss of the position or ability to perform its duties by June 30, 11:59 PM ET; its record shows resolved YES, corresponding to $1. Identifying the departure answers the event question, while valuing the Kalshi claim also requires the allocation rule and its reference inputs.",
        "suit-adjudication-episode": "The contract required authentic images or video taken and released within the stated window and named a consensus of credible reporting as its resolution source. The creator's July 1 update addressed whether that reporting criterion had been met. The recorded outcome is NO, corresponding to a zero payout, and the pinned protocol state corroborates it. The dated updates make the institutional application observable: the May 29 dispute acknowledgment preceded the June 24 appearance, while the July 1 clarification followed the window's close. The photograph alone cannot explain the whole dispute history.",
    }
    lines: list[str] = []
    for row in rows:
        observed = str(row.get("evidence_kind", "")).startswith("observed_") or str(row.get("scenario_status", "")).lower().startswith(("observed", "realized"))
        if observed_only and not observed:
            continue
        lines.extend([f"**{row['phenomenon']}.**", ""])
        if not bool(row.get("claim_relation_validated", False)):
            lines.extend(["Case-specific assertions are withheld pending source-version or changed-input review.", ""])
            continue
        lines.extend([str(row["witness_state"]), ""])
        narrative = narratives.get(str(row["case_id"]))
        if narrative and row.get("evidence_kind") in {"observed_settlement_divergence", "observed_chronology", "observed_adjudication"}:
            lines.extend([narrative, ""])
        elif row.get("b_contract_id") == "not-a-second-contract":
            lines.extend([f"The written condition is {row['signature_a']}. The recorded outcome is {row['payout_a']}. This is one contract with a named resolution procedure. {row.get('explanation', '')}", ""])
        else:
            basis = "The records show" if observed else "The hypothetical scenario implies"
            lines.extend([f"The {row['a_platform']} condition is {row['signature_a']}; the {row['b_platform']} condition is {row['signature_b']}. {basis} {row['a_platform']}: {row['payout_a']}; {row['b_platform']}: {row['payout_b']}. {row.get('explanation', '')}", ""])
        lines.extend([str(row.get("audit_note", "")), ""])
        links = "; ".join(f"[{row[f'{side}_platform']} {row[f'{side}_contract_id']}]({row[f'{side}_url']})" for side in ("a", "b") if str(row.get(f"{side}_url", "")).startswith("https://"))
        raw_sources = row.get("event_sources")
        sources = json.loads(raw_sources) if isinstance(raw_sources, str) and raw_sources else []
        links += "; " + "; ".join(f"[event source]({item['url']})" for item in sources) if sources else ""
        lines.extend([f"Source records: {links}.", ""])
    return lines or ["Observed cases require the explicitly versioned source bundle."]


def _opening_lines(cases: pd.DataFrame) -> list[str]:
    """Explain the primary system, claims and use consequence only after re-audit."""

    audited = add_claim_relations(cases) if not cases.empty else cases
    realized = audited.loc[audited.case_id.eq("hilton-first-vs-advance")] if not audited.empty else audited
    if not realized.empty and bool(realized.claim_relation_validated.all()):
        return [
            'On June 2, 2026, Steve Hilton finished second in California’s gubernatorial primary and advanced to the general election. California’s nonpartisan primary sends the two candidates with the most votes to the next round, so finishing first and advancing are different achievements. Kalshi listed a contract on whether Hilton would finish first; Polymarket listed one on whether he would advance. The archived Kalshi record shows NO and a zero settlement, while the Polymarket record shows resolved YES, corresponding to a full unit payout. The certified election result and both records therefore describe a consistent outcome: Hilton qualified without taking first place. [Certified results](https://elections.cdn.sos.ca.gov/sov/2026-primary/sov/06-sov-summary.pdf) and the [contract audit](REPRESENTATION_CASEBOOK.md) identify the event and the claims separately.',
            '',
            'The distinction matters when prices are used beyond the individual contract. If an analyst pooled these two prices as estimates of ‘Hilton’s primary prospects,’ the combined series would mix forecasts of first place with forecasts of advancing. Scoring both against a single outcome would likewise evaluate different targets as though they were the same forecast. Positions in the two contracts would not form an exact offset in the observed second-place outcome. These are consequences of their specified claims; the case does not show that traders or analysts actually made those mistakes.',
            '',
        ]
    return ["A forecast comparison requires a specified contractual target and source-supported payout evidence. Case-specific opening assertions are withheld until the required input audit is valid.", ""]


def literature_lines() -> list[str]:
    """Develop linked definitions and arguments from verified literature."""

    return [
        '### 2.1 From a public event to a forecast target',
        '',
        'A prediction-market contract ties a payment to a specified condition. In the familiar winner-take-all design, a YES position receives one unit when the condition is met and zero otherwise. Its probabilistic interpretation depends on that payment rule and on assumptions about trading and preferences. [Wolfers and Zitzewitz (2004)](https://doi.org/10.1257/0895330041371321) distinguish contract designs that elicit probabilities, means and medians, and discuss the difficulty of specifying and adjudicating the relevant conditions. The forecast target is therefore the condition selected by the contract, including the associated payment rule.',
        '',
        'Two contracts can refer to the same person and election while applying different predicates to that referent: finishing first, qualifying for a later round, being declared the winner, or taking office. Establishing a common referent is only the first step in comparing their targets. The rule also selects the achievement, time window, measurement convention, evidence source and exceptions. Throughout this paper, a rule-defined claim means the entitlement to payment produced by those conditions and the applicable resolution procedure.',
        '',
        'This is a longstanding problem of representation and semantic interoperability. [Wand and Weber (1993)](https://doi.org/10.1111/j.1365-2575.1993.tb00127.x) assess representational clarity through mappings between modeling constructs and what they represent. [Goh et al. (1999)](https://doi.org/10.1145/314516.314520) show why information exchanged across systems requires the assumptions that determine its interpretation. In the present setting, a shared event label provides less information than a complete statement of the claim. The difference can also be substantive: first-place and advancement contracts offer distinct entitlements, so a change of units or a more consistent label cannot make them identical.',
        '',
        'Recent prediction-market research makes these relationships explicit. [Gebele and Matthes (2026)](https://arxiv.org/html/2601.01706v1) model cross-platform event identity through resolution semantics and payoff regions. [Capponi, Gliozzo and Zhu (2026)](https://arxiv.org/html/2512.02436v3) develop a structured approach to discovering relations among contract texts and distinguish linguistic inference from relationships between settlements. These approaches make the object of comparison a contractual claim. The documentary audit developed here examines how qualifying conditions, fractional exceptions and authorized determination enter that object in particular observed cases.',
        '',
        '### 2.2 Payoff divergence and the amount being forecast',
        '',
        '**Payoff divergence** means that two contracts assign different normalized amounts to at least one explicitly described relevant scenario. The comparison holds the underlying facts fixed and states the information needed to apply each contract’s rules. A candidate who finishes second can receive zero under a first-place contract and one under an advancement contract. That scenario is a witness to non-equivalence: the two claims cannot be substituted for one another across the audited domain. Different wording alone is insufficient, and a witness to difference does not establish that either rule is ambiguous.',
        '',
        'The amount payable requires separate attention. A clear event condition may coexist with a tie provision, a price-based allocation or another exception that pays a fraction of the nominal unit. The distinction is important because the probability of an occurrence and the expected amount received are different quantities. A model restricted to zero-or-one settlements remains appropriate within that restriction; the restriction must be checked against the contract being analyzed.',
        '',
        *representation_bridge_lines(),
        '',
        '### 2.3 Written rules and institutional determination',
        '',
        '**Written-rule determinacy** asks whether a specified version of the rules fixes one payout when the stated scenario information is supplied. The information held fixed must be explicit. For a candidate finishing second without a tie, rank and qualification rules may each yield a definite answer while yielding different payouts. In another contract, knowing the physical occurrence may leave a required reference price or authority decision unresolved. Analysts must distinguish an unknown future fact, a missing input and a genuinely underdetermined criterion. The absence of an explicit definition is not sufficient to prove that multiple payouts remain permissible.',
        '',
        'A contract can specify who will decide a disputed question. Suppose the rule asks whether authentic images show a person wearing a suit and names a consensus of credible reporting as its resolution source. Knowing what the images depict does not itself establish what that reporting consensus will be. Once the relevant decision is supplied, the institution may record a unique payout. A need for later determination is therefore compatible with a definite eventual settlement. A stronger claim of institutional incompleteness would require showing that incompatible payouts remain permissible after all relevant procedural inputs are fixed.',
        '',
        'Information-systems research explains why this institutional layer belongs in the analysis. [Recker et al. (2021)](https://doi.org/10.25300/MISQ/2021/16027) describe conceptual models as mediating between represented and digitally enacted realities. [Eriksson and Öhlund (2024)](https://doi.org/10.17705/1jais.00845) examine constitutive rules that establish institutional entities and rights. Applied to prediction markets, this perspective directs attention to the entitlement created by the contract and to the authority recognized to settle it. The platform’s rules govern the payment right attached to a position; the external election result remains common to the compared venues.',
        '',
        'The temporal separation between occurrence and decision is also central to recent market research. [Wang (2026)](https://doi.org/10.1016/j.econlet.2026.113176) studies prices during disputes, when the underlying event has already occurred but the decision fixing the payoff is pending. [Nechepurenko (2026)](https://arxiv.org/html/2609.15368v1) distinguishes question rules, oracle adjudication and protocol settlement. Together these arguments show why an event date, a proposal, a recorded final outcome and a holder’s receipt are different observations. The present audit retains those distinctions when interpreting its evidence.',
        '',
        'The analysis consequently asks three related questions: what qualifies under the claim, how much is payable, and which institutional inputs remain to be supplied? These questions describe overlapping dimensions of a contract. A rank contract can also contain fractional tie payouts; a reporting criterion can also contain precise image and deadline conditions. They provide an organizing scheme for the audit without asserting an exhaustive semantic taxonomy or treating every clause as an independently identified causal mechanism.',
    ]


def reference_lines() -> list[str]:
    """List only works used in the manuscript, with exact preprint versions."""

    return [
        '- Capponi, A., Gliozzo, A., & Zhu, B. (2026). Agentic AI for Clustering, Relationship Discovery, and Semantic Trading in Prediction Markets. arXiv:2512.02436v3, 29 September; preprint, first version 2025. [Version](https://arxiv.org/html/2512.02436v3).',
        '- Eriksson, O., & Öhlund, S.-E. (2024). Digital Institutionalization: The Case of E-Prescribing. *Journal of the Association for Information Systems, 25*(3), 569–593. [DOI](https://doi.org/10.17705/1jais.00845).',
        '- Gebele, J., & Matthes, F. (2026). Semantic Non-Fungibility and Violations of the Law of One Price in Prediction Markets. arXiv:2601.01706v1, 5 January; preprint. [Version](https://arxiv.org/html/2601.01706v1).',
        '- Goh, C. H., Bressan, S., Madnick, S., & Siegel, M. (1999). Context Interchange: New Features and Formalisms for the Intelligent Integration of Information. *ACM Transactions on Information Systems, 17*(3), 270–293. [DOI](https://doi.org/10.1145/314516.314520).',
        '- Nechepurenko, M. (2026). Resolution Is Not Settlement, Part I: Oracle Adjudication and Semantic Governance on Polymarket. arXiv:2609.15368v1, 14 September; preprint. [Version](https://arxiv.org/html/2609.15368v1).',
        '- Recker, J., Lukyanenko, R., Jabbari Sabegh, M. A., Samuel, B. M., & Castellanos, A. (2021). From Representation to Mediation: A New Agenda for Conceptual Modeling Research in a Digital World. *MIS Quarterly, 45*(1), 269–300. [DOI](https://doi.org/10.25300/MISQ/2021/16027).',
        '- Wand, Y., & Weber, R. (1993). On the ontological expressiveness of information systems analysis and design grammars. *Information Systems Journal, 3*(4), 217–237. [DOI](https://doi.org/10.1111/j.1365-2575.1993.tb00127.x).',
        '- Wang, G. (2026). Do prediction markets price events or adjudication? Evidence from the disputed Polymarket markets. *Economics Letters, 268*, 113176. [DOI](https://doi.org/10.1016/j.econlet.2026.113176).',
        '- Wang, R. Y., & Strong, D. M. (1996). Beyond Accuracy: What Data Quality Means to Data Consumers. *Journal of Management Information Systems, 12*(4), 5–33. [DOI](https://doi.org/10.1080/07421222.1996.11518099).',
        '- Wolfers, J., & Zitzewitz, E. (2004). Prediction Markets. *Journal of Economic Perspectives, 18*(2), 107–126. [DOI](https://doi.org/10.1257/0895330041371321).',
    ]


def supplementary_model_lines(models: pd.DataFrame) -> list[str]:
    """Present final estimates with their actual covariance and confidence intervals."""

    lines = ["| Specification | Coefficient | 95% interval | Uncertainty | n |", "|---|---:|---:|---|---:|"]
    for name in ("cohort_exposure_adjusted", "cohort_exposure_adjusted_hc3", "within_family_kalshi", "within_family_polymarket"):
        row = _model_record(models, name)
        if row is not None:
            covariance = str(row.get("covariance", "family-clustered" if name != "cohort_exposure_adjusted_hc3" else "HC3"))
            lines.append(f"| {name} | {_value(row, 'coefficient'):.4f} | [{_value(row, 'ci_lower'):.4f}, {_value(row, 'ci_upper'):.4f}] | {covariance}; SE {_value(row, 'std_error'):.4f} | {int(_value(row, 'n')):,} |")
    lines.extend([
        "", "The preferred pooled coefficient uses one within-platform SD of the text index and standardized log cumulative volume. Its family clusters are qualified by platform. HC3 uses the same formula and rows as a covariance comparison. Within-family models use internally varying families and a different residual-score SD; their magnitudes are not directly comparable to the pooled coefficient.",
        "", "Volume selection, retrospective rules, family concentration and incomplete exposure metadata limit interpretation to these selected portfolios. Subgroup significance differences do not test heterogeneity.",
        "", "The current cycle's [independent reproduction](paper-revision/2026-10-15-01/scratch-empirics/reproduction-results.json) uses the final field-invariant features. Its top five families contribute 66.86% of focal sandwich variance. Omitting the largest family by row count (2,000 rows) gives β=−0.1199, family-clustered SE 0.0402 and 95% interval [−0.1986, −0.0411], n=17,500. This bounded diagnostic does not establish broad robustness or causality. The older 69.48% concentration belongs to the earlier frozen specification and is retained only as historical evidence. No further deletion grid was run.",
    ])
    return lines


def write_supplementary_results(path: Path, models: pd.DataFrame, error_models: pd.DataFrame, panel_summary: pd.DataFrame, matched_models: pd.DataFrame) -> None:
    """Keep activity, terminal-error and dormant panel evidence outside the main argument."""

    lines = [
        "# Supplementary analysis", "", "## Text measurement and portfolio context", "",
        "The [measurement note](MEASUREMENT_NOTE.md) retains the composite definition and repair history. [Component profiles](tables/analysis-platform-profiles.csv) and the [data atlas](descriptions-data.html) describe the selected portfolios. Components are mean weighted cue scores; the discretion-term score is max(0, 1 − 0.25 × distinct configured phrases), not a no-flag share. These lexical descriptions do not validate scenario-level determinacy.", "",
        "## Activity association", "", *supplementary_model_lines(models), "", "## Terminal-error diagnostic", "",
    ]
    if not error_models.empty:
        lines.append(_estimate(_records(error_models)[0], "family-clustered SE") + ". This last-trade Kalshi diagnostic lacks a common forecast horizon; a null is not equivalence.")
    else:
        lines.append("Not estimable on the available final analysis rows.")
    lines.extend(["", "## Dormant price panel", "", f"{len(panel_summary)} saved pair summaries remain. Matched-model rows: {len(matched_models)}. There are no qualifying synchronized-price observations. The retained `bad72f8883` cache and alternate `627b27c83f-interval-max` contain different pair inventories; the alternate third pair remains eligible, so prior three-to-two attrition was not caused by current eligibility.", "", "All existing model rows are retained in [analysis-market-models.csv](tables/analysis-market-models.csv), with formula, covariance, sample size and confidence intervals. These exploratory values are unadjusted for multiple comparisons. Figures of score–volume bins use unclustered descriptive mean intervals, separate from preferred family-clustered model inference."])
    _write_lines(path, lines)


def write_research_summary(path: Path, contracts: pd.DataFrame, models: pd.DataFrame, error_models: pd.DataFrame, matches: pd.DataFrame, panel_summary: pd.DataFrame, matched_models: pd.DataFrame, cases: pd.DataFrame, profiles: pd.DataFrame, coherence: pd.DataFrame) -> None:
    """Keep a concise evidence handoff aligned with the concept-led manuscript."""

    counts = matches.match_label.value_counts() if not matches.empty else pd.Series(dtype=int)
    lines = [
        "# Same Future, Different Claim", "", *_opening_lines(cases),
        "## Question and organizing concepts", "",
        "The paper audits what qualifies for payment, how much pays and which institutional inputs are still required. Payoff divergence is a difference in amounts in a specified relevant scenario. Written-rule determinacy asks whether the stated information and rule version fix one payout. The dimensions overlap and are not a validated taxonomy or an estimate of causal mechanisms.", "",
        "## Observed exhibits", "", *case_exhibit_lines(cases, observed_only=True),
        "Full sources and chronology: [casebook](REPRESENTATION_CASEBOOK.md). The new suit read is documented in [P2_OUTCOME.md](paper-revision/2026-10-15-01/P2_OUTCOME.md).", "",
        "## Interpretation and literature", "",
        "The contribution applies established contract-specification, representation and institutional-rule insights to linked observed records. The main manuscript engages Wolfers–Zitzewitz, Wand–Weber, Goh and colleagues, Recker and colleagues, Eriksson–Öhlund, and close semantic-alignment/adjudication work. The literature chapter explains their arguments; source-access qualifications are retained in the revision evidence record.", "",
        "## Selected-portfolio text context", "", *sample_limit_lines(contracts), "", *platform_profile_lines(profiles), "",
        f"Matching retains {int(counts.get('high_confidence', 0))} high-confidence candidates, {int(counts.get('probable', 0))} probable candidates and {int(counts.get('rejected', 0))} rejected rows. These retrieval labels do not establish payoff equivalence.", "",
        "## Supplementary estimates and limits", "", *supplementary_model_lines(models), "", *coherence_status_lines(cases, coherence), "",
        "Pooling/scoring one forecast target and exact offsetting each require a justified claim relation. Other comparisons and useful hedges can concern different claims. No prevalence, trader misunderstanding, manipulation, causal price effect or holder-cash-flow claim is established. See the [manuscript](PAPER_OUTLINE.md) and [supplement](SUPPLEMENTARY_ANALYSIS.md).",
    ]
    _write_lines(path, lines)


def write_research_status(path: Path, contracts: pd.DataFrame, models: pd.DataFrame, cases: pd.DataFrame, profiles: pd.DataFrame, coherence: pd.DataFrame) -> None:
    """Write the current revision handoff while retaining persistent history elsewhere."""

    lines = [
        "# Research Status", "", f"Updated {date.today().isoformat()} under approved cycle 2026-10-15-01, P1–P6.", "", *_opening_lines(cases),
        "## Main interpretation", "",
        "The documentary audit distinguishes qualifying conditions, payout amounts and required institutional inputs. The [observed exhibits](REPRESENTATION_CASEBOOK.md) are re-audited against their supplied fields before publication. The suit extension concerns one contract; it supplies no pairwise relation or demonstrated institutional incompleteness. Historical proposal/finality logs remain unavailable. The presidential interruption witness is withheld because governing-version coverage is incomplete.", "", *coherence_status_lines(cases, coherence),
        "## Sample and measurement", "", *sample_limit_lines(contracts), "", *platform_profile_lines(profiles),
        "## Supplementary association", "", *supplementary_model_lines(models),
        "## Approved scope and remaining evidence", "",
        "P1–P6 are approved in paper-revision/2026-10-15-01/APPROVED_PROMPT_PLAN.md, with the user's prose amendments. P2 adds one question's pinned protocol state and creator updates; the HTTP-403 historical-log limit is recorded in P2_OUTCOME.md. O1–O4, broader samples, price/comprehension studies and another critic round remain excluded. Source/version gaps limit exhaustive rule claims. Metadata endDate is an exposure/window proxy, not necessarily the operative rule deadline. New updates and sources never backdate the original snapshots.", "",
        "Manuscript: [PAPER_OUTLINE.md](PAPER_OUTLINE.md). Persistent research history is in research-log.md; cycle outcomes and validation are in paper-revision/2026-10-15-01/.",
    ]
    _write_lines(path, lines)


def write_paper_outline(path: Path, contracts: pd.DataFrame, models: pd.DataFrame, cases: pd.DataFrame, profiles: pd.DataFrame) -> None:
    """Write the approved concept-led manuscript after revalidating its main evidence."""

    audited = add_claim_relations(cases) if not cases.empty else cases
    required = {"hilton-first-vs-advance", "khamenei-death-allocation", "suit-adjudication-episode", "minerals-observed-chronology"}
    present = set(audited.case_id) if not audited.empty else set()
    if not required.issubset(present) or not bool(audited.loc[audited.case_id.isin(required), "claim_relation_validated"].all()):
        _write_lines(path, ["# Same Future, Different Claim", "", "The observed-case manuscript is withheld pending source-version or changed-input review of its required exhibits."])
        return
    qualifying = audited.loc[audited.case_id.isin(["hilton-first-vs-advance", "minerals-observed-chronology"])]
    amounts = audited.loc[audited.case_id.eq("khamenei-death-allocation")]
    adjudication = audited.loc[audited.case_id.eq("suit-adjudication-episode")]
    lines = [
        '# Same Future, Different Claim: How Prediction Markets Define What Counts',
        '',
        'Working manuscript; documentary audit with supplementary metadata analysis.',
        '',
        '## Abstract',
        '',
        'Prediction-market prices refer to contractual claims whose paying conditions can differ even when their questions concern the same public event. We examine how analysts can establish those conditions through a documentary audit of rules, event evidence and recorded outcomes. Hilton’s second-place primary result supports a zero settlement in a first-place contract and a full payout in an advancement contract. Khamenei’s departure contracts record 45 cents and YES, showing why a binary event or product label does not establish binary payout support. A suit-adjudication case links a reporting criterion to dated creator updates and a protocol-corroborated NO; successive minerals contracts illustrate different milestones with the same realized outcome. The findings organize comparability around qualifying conditions, payout amounts and remaining institutional inputs. They support an empirical diagnostic rather than estimates of prevalence or causal price effects.',
        '',
        '## 1. Introduction',
        '',
        *_opening_lines(audited),
        'Prediction-market prices can be interpreted as forecasts only in relation to what the positions pay for. The semantic step is easy to overlook because an event title is a convenient way to identify a market, whereas payment depends on more detailed rules. A contract can specify a different milestone, require a particular source to recognize it, or change the amount paid under an exception. Comparing prices as beliefs about one target therefore requires an account of those selections. Existing theories of contingent claims and semantic alignment supply the necessary concepts; the empirical question is how the relevant distinctions appear in linked records of real contracts and their outcomes.',
        '',
        'The issue extends beyond visibly different achievements. In the Khamenei departure episode, one Kalshi contract recorded a settlement of 45 cents while a related Polymarket contract recorded YES. The Kalshi data described the product as binary, yet its death provision permitted a price-based allocation. In the Zelenskyy clothing case, the published criterion referred to credible reporting, and the question creator later issued a clarification about whether that consensus had been reached. These cases direct attention to both the amount promised and the institutional input needed to settle a claim.',
        '',
        'We ask: **How can analysts establish what apparently comparable prediction-market contracts pay for, and what information is still required to determine settlement?** We address the question through a documentary audit linking identified contracts, available rule versions, event sources and recorded outcomes. Two cases contain observed payout differences; a single-contract adjudication case and a same-outcome milestone comparison help distinguish what the evidence can establish. A selected metadata portfolio provides descriptive context.',
        '',
        'The contribution is a comparative empirical account of qualifying conditions, payout amounts and institutional determination. It makes the interpretation of each exhibit explicit and shows where additional source information is needed before a stronger claim can be made. This supports a focused audit of forecast comparability. It does not estimate how often these distinctions arise, whether traders understand them, or how they affect prices.',
        '',
        '## 2. From public events to payable claims',
        '',
        *literature_lines(),
        '',
        '## 3. Audit design and evidence',
        '',
        '### 3.1 Documentary units and source roles',
        '',
        'Cases were selected purposively to examine contrasting contractual conditions and evidence types. The main units are two cross-platform contract pairs with different recorded payouts, one pair of successive contracts with the same recorded outcome, and one single-contract adjudication episode. We keep three source roles distinct: contract descriptions specify available rules; independent event sources establish the public occurrence; platform or protocol records establish the recorded outcome. A documented appearance, for example, is evidence that an event occurred, while a creator clarification is evidence about the resolution criterion being applied.',
        '',
        'For each exhibit, the audit retains stable identifiers, the supplied question and rule text, source versions, the scenario information used, and recorded or hypothetical payouts. Fingerprints bind assertions to those inputs; altered inputs withhold dependent claims until re-audit. A matching fingerprint establishes consistency with the audited files, rather than exhaustive governing-rule coverage. Series-level specifications and all historical clarifications are not reconstructed. The presidential death/interruption witness is consequently withheld because a current linked specification contains additional exceptions whose historical applicability is unverified. Remaining hypothetical scenarios are conditional applications of their stated archived question rules.',
        '',
        f"The case inventory contains {len(audited)} exhibits: four observed exhibits and {int(audited.evidence_kind.eq('hypothetical_rule_witness').sum())} proposed hypothetical scenarios. One presidential witness is withheld pending governing-version evidence. Exhibit counts refer to evidential displays, including shared contracts, rather than independent events or identified mechanisms.",
        '',
        'The suit extension is deliberately narrow. A public Polygon read verifies the adapter/question/condition linkage, the stored question text, the creator’s update list and the condition’s payout numerators at a pinned block. The stored updates supply two dated observations, including a dispute acknowledgment before the June 24 appearance. A historical-log query returned HTTP 403, so individual proposal rounds and the original final-resolution transaction were not reconstructed. Current protocol state, stored update timestamps, API closure time and holder receipts retain separate evidence roles. The [source bundle and acquisition record](paper-revision/2026-10-15-01/P2_OUTCOME.md) document those checks.',
        '',
        '### 3.2 Metadata context and supplementary analysis',
        '',
        'The historical portfolio combines high-volume Kalshi series with high-volume closed Polymarket markets. Its selection is purposive, and the historical Polymarket sports filter incorrectly excluded some non-sports records. Original request times and the rejected/overflow sample are unavailable. September 10 is a legacy label; three retained source updates are dated September 11. These limitations preclude a population or platform-quality ranking. Named cases recovered separately from the metadata portfolio are not treated as a random subsample of it.',
        '',
        'The automated text components record authority, time, definition/threshold, edge-clause and discretion-term cues. Their equal-weight mean is an exploratory specificity index, not a validated measure of whether a rule determines a payout in a scenario. Each component is a weighted cue score; the discretion component is not a no-flag frequency. The [measurement note](MEASUREMENT_NOTE.md), [component profiles](tables/analysis-platform-profiles.csv) and [data atlas](descriptions-data.html) provide the descriptive context. The case classifications are not inferred from these scores.',
        '',
        'Metadata time fields are also treated as proxies. In the named Khamenei Polymarket record, endDate is 27 hours 59 minutes earlier than the explicit Eastern Time deadline; in the two minerals records the difference is 15 hours 59 minutes. The operative dates and metadata values are retained separately in the [data-source note](../DATA_SOURCES.md). We do not interpret these metadata fields as proof of a complete semantic window or synchronized price observations.',
        '',
        'Activity and terminal-error analyses remain supplementary. The preferred activity specification adjusts for metadata exposure and opening cohorts, uses within-platform standardization and platform-qualified family clusters, and compares HC3 uncertainty on the same rows and formula. Volume selection, retrospective rules and incomplete exposure prevent a causal interpretation. No synchronized-price or common-horizon forecast-accuracy test is established by the retained panel.',
        '',
        f"The retained metadata portfolio contains {len(contracts):,} contracts: " + "; ".join(f"{platform}: {count:,}" for platform, count in contracts.groupby("platform").size().items()) + ". The case audit and this selected portfolio answer different questions.",
        '',
        '## 4. Findings',
        '',
        '### 4.1 What qualifies: achievements and milestones',
        '',
        'The first comparison concerns the event condition rewarded by the claim. A primary election can establish both a ranking and eligibility for the next round. An agreement can pass through an announcement and a later signature. The observed record distinguishes these conditions without implying that they must produce different settlements on every occasion.',
        '',
        *case_exhibit_lines(qualifying, observed_only=True),
        '### 4.2 How much pays: fractional exceptions',
        '',
        'A second distinction concerns the amount attached to a qualifying occurrence. Even after identifying the relevant departure, a price-referenced exception can change the settlement amount. This question overlaps with the first: the full rule must specify both which occurrence counts and which payment rule applies.',
        '',
        *case_exhibit_lines(amounts, observed_only=True),
        '### 4.3 What remains for institutional determination',
        '',
        'The final exhibit concerns a single contract with a specified reporting source. It separates the public appearance, the creator’s application of the reporting criterion, and the recorded institutional outcome. The added records help establish that sequence without identifying the rationale of every challenge.',
        '',
        *case_exhibit_lines(adjudication, observed_only=True),
        '### 4.4 Cross-case synthesis',
        '',
        '| Audit dimension | Unit and information held fixed | Observation | Supported inference |',
        '|---|---|---|---|',
        '| Qualifying achievement | Hilton pair; certified primary rank | NO/$0 and YES/$1 | Shared election facts support different claim outcomes. |',
        '| Milestone and time window | Successive minerals contracts; dated closure and signing records | YES/YES | Distinct conditions can coincide in the realized outcomes. |',
        '| Payout amount and exception | Khamenei pair; departure episode and recorded allocations | $0.45 and YES/$1 | Binary product metadata do not establish binary payout support. |',
        '| Authorized determination | One suit contract; question, creator updates and pinned protocol read | Reporting clarification and corroborated NO | The named reporting criterion has a documented institutional application; individual dispute causes remain unresolved. |',
        '',
        'The dimensions overlap. The rank cases also contain fractional tie clauses, while the suit question contains time and authenticity conditions. A hypothetical rounding witness addresses how a measurement enters a category; it is not another observed fractional settlement. The full [casebook](REPRESENTATION_CASEBOOK.md) and [case matrix](tables/representation-case-matrix.csv) preserve the source versions and surviving hypothetical scenarios. The presidential interruption witness is withheld. Metadata text scores and activity estimates remain in the [supplementary materials](SUPPLEMENTARY_ANALYSIS.md).',
        '',
        '## 5. Discussion and conclusion',
        '',
        '### 5.1 Forecast targets and the task of comparison',
        '',
        'Hilton’s second place shows why a common event record is insufficient to identify a common forecast target. The two recorded settlements are consistent with the election result because the claims reward different achievements. This applies the established role of contract specification to a concrete comparison problem. In the terms of [Wang and Strong (1996)](https://doi.org/10.1080/07421222.1996.11518099), fitness for a data consumer’s task involves interpretation and context as well as accuracy. A correctly recorded price can be unsuitable for a pooled forecast if the pooling operation silently changes the target.',
        '',
        'The implication depends on the task. Forecast pooling and scoring against one target require a justified correspondence between the claims and that target. Exact offsetting requires an appropriate relation between payouts across the relevant states. Broader hedging can use related claims without exact equivalence, and analysts can meaningfully compare the prices of different achievements. The audit therefore specifies the relation needed for a proposed use. It does not prohibit comparison whenever contracts differ.',
        '',
        'This task-specific interpretation connects the evidence to semantic-interoperability research. [Goh et al. (1999)](https://doi.org/10.1145/314516.314520) retain contextual assumptions when combining data. Prediction-market comparison additionally encounters deliberate differences in the entitlements being traded. The Hilton pair is not an error to eliminate by making the labels uniform. Preserving the difference tells an analyst which forecast or exposure each position provides.',
        '',
        '### 5.2 Payout support and the boundary of a binary abstraction',
        '',
        'Khamenei’s 45-cent settlement adds an issue that identifying the departure condition alone would miss. The recorded product-type label was binary, while the archived rule allowed a price-referenced allocation and the settlement was fractional. The relevant forecast quantity therefore depends on the exception’s amount and inputs. This is a concrete check on the applicability of a binary payoff model. It complements the explicitly binary scope of [Gebele and Matthes (2026)](https://arxiv.org/html/2601.01706v1) and the distinction between textual and settlement relations developed by [Capponi et al. (2026)](https://arxiv.org/html/2512.02436v3).',
        '',
        'The evidence supports auditing payout amounts alongside event conditions. It does not identify the counterfactual price of a contract without the exception, the probability traders assigned to the death scenario, or the reference-price choice that generated the allocation. Reported reimbursements further separate contract settlement from an individual account’s receipts. The expected-payout formulation accommodates those amounts, while the observed case supplies no new valuation theorem.',
        '',
        '### 5.3 Institutional determination and the scope of the evidence',
        '',
        'The suit case makes the role of an authorized determination more concrete. The question creator’s July 1 update addressed whether the named credible-reporting criterion had been satisfied. Its May 29 acknowledgment also establishes that the dispute history began before the June 24 photograph used to introduce the appearance. The observations support a documented relation among the criterion, creator communication and recorded outcome. They leave the reasons for the individual challenges unresolved.',
        '',
        'This distinction is consistent with [Eriksson and Öhlund’s (2024)](https://doi.org/10.17705/1jais.00845) account of rules governing institutional entities and rights, and with [Wang’s (2026)](https://doi.org/10.1016/j.econlet.2026.113176) separation of event occurrence from pending adjudication. [Nechepurenko (2026)](https://arxiv.org/html/2609.15368v1) provides the further distinction between adjudication stages and protocol settlement. Here, the added protocol read corroborates the recorded NO, but a complete historical trace is unavailable. A missing garment-level definition and a contested process do not prove that the institution lacked a determinate eventual outcome.',
        '',
        'Interfaces and research datasets could retain qualifying conditions, possible payout amounts and authoritative updates alongside prices. These are design proposals to be evaluated, rather than tested improvements in comprehension. A small prospective comparison could assess whether the same audit distinctions remain useful before outcomes are known. A reusable classification measure would require independent applications of complete rules to specified scenarios and explicit treatment of disagreement.',
        '',
        '### 5.4 Limitations and conclusion',
        '',
        'The exhibits demonstrate particular distinctions and cannot estimate their prevalence or economic magnitude. Their purposive selection, unequal deadlines and exceptions prevent isolating clause effects. Some rules are retrospective snapshots, historical governing versions remain incomplete, and the metadata portfolios have unresolved acquisition and selection gaps. The lexical measures describe text without validating semantic determinacy. Current protocol corroboration does not recover every historical stage or a holder’s cash flow. These limits rule out a platform ranking, an inference of manipulation and a general causal price or comprehension claim.',
        '',
        'The cases show why contract comparison requires attention to the achievement that qualifies, the amount payable and the institutional inputs needed to settle the claim. The audit keeps those questions distinct while tracing how they meet in observed records. Before using a market price as a forecast, specify the claim whose expected payout it represents under the relevant pricing assumptions.',
        '',
        '![Analytical decomposition from rule-defined claim and beliefs to expected payout and observed price](figures/views-conceptual-schematic.svg)',
        '',
        '*Figure 1. Analytical decomposition of the contract comparison. Qualifying conditions, payout amounts and required institutional decisions specify the claim. Expected payout and observed market price have separate roles; the arrows are not estimated causal effects.*',
        '',
        '## References',
        '',
        *reference_lines(),
    ]
    _write_lines(path, lines)


def write_claim_confidence(path: Path, models: pd.DataFrame, cases: pd.DataFrame, profiles: pd.DataFrame) -> None:
    """Regenerate the twenty original claim IDs with their approved dispositions."""

    preferred = _model_record(models, "cohort_exposure_adjusted")
    volume = "Not estimable" if preferred is None else f"β={_value(preferred, 'coefficient'):.4f}, family-clustered 95% CI [{_value(preferred, 'ci_lower'):.4f}, {_value(preferred, 'ci_upper'):.4f}], n={int(_value(preferred, 'n')):,}"
    dispositions = [
        (1, "First place versus advancement", "Hilton supplies archived NO/$0 versus resolved YES; supplementary Steyer second-place witness remains hypothetical. Source-scoped audit gates each case; historical governing coverage remains qualified."),
        (2, "Call versus inauguration", "WITHHELD: the presidential interruption witness requires governing-specification versions covering death and accelerated resolution."),
        (3, "Fed quantization", "12.5-bp counterfactual conditional on literal wording and other operative clauses; no realized unusual-rate case established."),
        (4, "Announcement versus signature", "Minerals chronology records YES/YES; separate YES/NO witness concerns dates, scope and milestones together."),
        (5, "Announcement versus first departure", "Trump witness remains hypothetical with competing leaders and death-price exception; no global binary relation."),
        (6, "Suit category and adjudication", "Creator updates acknowledge a May 29 dispute and a July 1 reporting-consensus clarification; pinned protocol state corroborates NO. Individual dispute reasons and a complete historical log chronology remain unverified."),
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
    lines = ["# Claim confidence and disposition", "", f"Updated {date.today().isoformat()} under approved cycle 2026-10-15-01, P1–P6. Claim IDs preserve the former overview; row counts denote exhibits rather than independent mechanisms.", "", "| ID | Claim | Current evidence and boundary |", "|---:|---|---|"]
    lines.extend(f"| {identifier} | {label} | {disposition} |" for identifier, label, disposition in dispositions)
    lines.extend(["", f"The generated case matrix contains {len(cases)} exhibits. Numerical profiles and covariance rows are regenerated from final data. Code tests establish parser/pipeline behavior; they supply no human construct reliability.", "", "Evidence: [casebook](REPRESENTATION_CASEBOOK.md), [model table](tables/analysis-market-models.csv), [profiles](tables/analysis-platform-profiles.csv), [supplementary analysis](SUPPLEMENTARY_ANALYSIS.md)."])
    _write_lines(path, lines)
