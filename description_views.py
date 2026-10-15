"""Offline descriptive data atlas, using the study's existing measurement and audit gates."""

from __future__ import annotations

from html import escape
from pathlib import Path
from string import Template

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.ticker import PercentFormatter

from src.analysis import platform_profiles, prepare_market_analysis
from src.anecdotes import add_claim_relations
from views import PLATFORM_COLORS, _finish

TEMPLATE_PATH = Path(__file__).parent / "templates" / "data-descriptions.html"
COMPONENT_LABELS = {
    "source_specificity": "Authority / source cues",
    "temporal_specificity": "Date / time cues",
    "outcome_definition": "Definition / threshold cues",
    "edge_completeness": "Conditional / fallback cues",
    "discretion_clarity": "Discretion-term score (1 − penalty)",
}
EVIDENCE_LABELS = {
    "observed_settlement_divergence": "Observed payout difference",
    "observed_chronology": "Observed chronology; same payout",
    "observed_adjudication": "Observed adjudication; one contract",
    "hypothetical_rule_witness": "Hypothetical separating scenario",
}
OUTCOME_LABELS = {
    "none": "No recorded outcome",
    "platform_result": "Recorded platform result",
    "price_inferred_missing_status": "Endpoint inference; final status missing",
    "price_inferred_proposed": "Endpoint inference; proposed status",
    "price_inferred_resolved": "Endpoint inference; resolved status",
    "price_inferred_settled": "Endpoint inference; settled status",
    "intermediate_price_missing_status": "Intermediate price; status missing",
    "intermediate_price_resolved": "Intermediate price; resolved status",
}


def _table(frame: pd.DataFrame, caption: str) -> str:
    """Render escaped table cells with an accessible caption."""

    markup = frame.to_html(index=False, border=0, classes="data-table", na_rep="—")
    return (
        '<div class="table-scroll">'
        + markup.replace(">", f"><caption>{escape(caption)}</caption>", 1)
        + "</div>"
    )


def _chart(figure: Figure, path: Path, title: str, description: str) -> str:
    """Export a standalone SVG and embed the same accessible vector graphic."""

    _finish(figure, path)
    svg = path.read_text(encoding="utf-8")
    svg = svg[svg.index("<svg") :]
    identifier = path.stem
    svg = svg.replace('id="', f'id="{identifier}-')
    svg = svg.replace("url(#", f"url(#{identifier}-")
    svg = svg.replace('href="#', f'href="#{identifier}-')
    end = svg.index(">")
    svg = (
        svg[:end]
        + f' role="img" aria-labelledby="{identifier}-title {identifier}-desc">'
        + f'<title id="{identifier}-title">{escape(title)}</title>'
        + f'<desc id="{identifier}-desc">{escape(description)}</desc>'
        + svg[end + 1 :]
    )
    path.write_text(svg, encoding="utf-8")
    return svg


def _case_cards(cases: pd.DataFrame) -> str:
    """Expose scenarios only after revalidating the inputs within the audit's scope."""

    cards = []
    for row in cases.sort_values(["display_order", "case_id"]).to_dict("records"):
        valid = bool(row["claim_relation_validated"])
        kind = str(row["evidence_kind"])
        group = "observed" if kind.startswith("observed_") else "hypothetical"
        if not valid:
            group = "unreviewed"
        label = EVIDENCE_LABELS.get(kind, kind) if valid else "Re-audit required"
        body = "<p>Scenario and payout assertions withheld pending review of changed inputs.</p>"
        if valid:
            body = "".join(
                f"<dt>{heading}</dt><dd>{escape(str(row.get(field, '')))}</dd>"
                for heading, field in (
                    ("Scenario / event", "witness_state"),
                    ("A · qualifying condition", "signature_a"),
                    ("B · qualifying condition", "signature_b"),
                    ("A · settlement / scenario payout", "payout_a"),
                    ("B · settlement / scenario payout", "payout_b"),
                    ("Interpretation", "explanation"),
                    ("Audit boundary", "audit_note"),
                )
            )
            links = " · ".join(
                f'<a href="{escape(str(row[f"{side}_url"]), quote=True)}">'
                f"{escape(str(row[f'{side}_platform']))} "
                f"{escape(str(row[f'{side}_contract_id']))}</a>"
                for side in ("a", "b")
                if str(row.get(f"{side}_url", "")).startswith("https://")
            )
            body = f"<dl>{body}</dl><p>{links}</p>"
        cards.append(
            f'<details class="case" data-kind="{group}"><summary>'
            f'<span class="tag {group}">{escape(label)}</span>'
            f"<span>{escape(str(row['phenomenon']))}</span></summary>{body}</details>"
        )
    return "\n".join(cards)


def write_data_descriptions(
    path: Path, contracts: pd.DataFrame, cases: pd.DataFrame, normalization: pd.DataFrame
) -> None:
    """Build a reproducible standalone page and its underlying descriptive tables/figures."""

    if set(contracts.platform) != set(PLATFORM_COLORS):
        raise ValueError("The data atlas requires both Kalshi and Polymarket contract rows")
    if contracts.contract_id.duplicated().any():
        raise ValueError("Contract identifiers must be unique in the descriptive sample")
    scores = contracts[[*COMPONENT_LABELS, "determinacy_score"]]
    if ((scores < 0) | (scores > 1)).any().any():
        raise ValueError("Text components and specificity scores must be in [0, 1]")
    if (contracts.rule_word_count < 0).any():
        raise ValueError("Analyzed text length cannot be negative")
    counts = contracts.groupby("platform", sort=True).size()
    retained = normalization.loc[normalization.normalization_reason.eq("retained")]
    if not retained.groupby("platform").size().equals(counts):
        raise ValueError("Normalization ledger does not reconcile with the contract sample")

    path.parent.mkdir(parents=True, exist_ok=True)
    figure_dir, table_dir = path.parent / "figures", path.parent / "tables"
    table_dir.mkdir(exist_ok=True)
    analysis = prepare_market_analysis(contracts)
    profiles = platform_profiles(analysis)
    overall = profiles.loc[profiles.stratum.eq("all")].set_index("platform")
    if not overall.contracts.astype(int).equals(counts):
        raise ValueError("Analysis eligibility differs from the descriptive contract sample")
    cases = add_claim_relations(cases.fillna(""))
    platforms = list(PLATFORM_COLORS)
    groups = {platform: contracts.loc[contracts.platform.eq(platform)] for platform in platforms}
    tables: dict[str, pd.DataFrame] = {}
    figures: dict[str, str] = {}

    summary_rows = []
    for platform, group in groups.items():
        profile = overall.loc[platform]
        length = group.rule_word_count
        summary_rows.append(
            {
                "Platform": platform,
                "Contracts": f"{len(group):,}",
                "API families": f"{overall['families'][platform]:,.0f}",
                "Categories": str(group.category.nunique()),
                "Index mean": f"{profile.mean_determinacy:.3f}",
                "Median text words [IQR]": (
                    f"{length.median():.0f} "
                    f"[{length.quantile(0.25):.0f}–{length.quantile(0.75):.0f}]"
                ),
                "Threshold flag": f"{group.quantitative_threshold.mean():.1%}",
                "Top-five family share": f"{profile.top_five_family_share:.1%}",
            }
        )
    tables["overview"] = pd.DataFrame(summary_rows)
    attrition = normalization.groupby(["platform", "normalization_reason"], sort=True).size()
    tables["attrition"] = (
        attrition.rename("Rows")
        .reset_index()
        .rename(
            columns={
                "platform": "Platform",
                "normalization_reason": "Normalization disposition",
            }
        )
    )
    tables["components"] = (
        overall[list(COMPONENT_LABELS)]
        .rename(columns=COMPONENT_LABELS)
        .T.rename_axis("Literal component")
        .reset_index()
    )
    tables["strata"] = profiles[
        [
            "platform",
            "stratum",
            "contracts",
            "mean_determinacy",
            "mean_text_words",
        ]
    ].rename(
        columns={
            "platform": "Platform",
            "stratum": "Threshold stratum",
            "contracts": "Contracts",
            "mean_determinacy": "Mean index",
            "mean_text_words": "Mean text words",
        }
    )
    family_rows = []
    category_rows = []
    distribution_rows = []
    length_rows = []
    index_edges = np.linspace(0, 1, 21)
    length_edges = [0, 50, 100, 150, 200, 300, 500, np.inf]
    length_labels = ["0–49", "50–99", "100–149", "150–199", "200–299", "300–499", "500+"]
    for platform, group in groups.items():
        family = analysis.loc[analysis.platform.eq(platform)].groupby("family_id", sort=True).size()
        ordered = (
            family.rename("contracts")
            .rename_axis("family")
            .reset_index()
            .sort_values(["contracts", "family"], ascending=[False, True], kind="stable")
        )
        ordered["cumulative_share"] = ordered.contracts.cumsum() / len(group)
        for rank, (_, row) in enumerate(ordered.iterrows(), 1):
            family_rows.append(
                {
                    "platform": platform,
                    "rank": rank,
                    "family": row.family,
                    "contracts": int(row.contracts),
                    "cumulative_share": row.cumulative_share,
                }
            )
        for category, number in group.groupby("category", dropna=False).size().items():
            category_rows.append(
                {
                    "platform": platform,
                    "category": str(category),
                    "contracts": int(number),
                    "share": number / len(group),
                }
            )
        valid_scores = group.determinacy_score.dropna()
        hist, _ = np.histogram(valid_scores, bins=index_edges)
        for i, number in enumerate(hist):
            distribution_rows.append(
                {
                    "platform": platform,
                    "lower": index_edges[i],
                    "upper": index_edges[i + 1],
                    "contracts": int(number),
                    "share": number / len(valid_scores),
                }
            )
        valid_lengths = group.rule_word_count.dropna()
        hist, _ = np.histogram(valid_lengths, bins=length_edges)
        for label, number in zip(length_labels, hist, strict=True):
            length_rows.append(
                {
                    "platform": platform,
                    "words": label,
                    "contracts": int(number),
                    "share": number / len(valid_lengths),
                }
            )
    tables["families"] = pd.DataFrame(family_rows)
    tables["categories"] = pd.DataFrame(category_rows).sort_values(
        ["platform", "contracts", "category"], ascending=[True, False, True]
    )
    tables["distribution"] = pd.DataFrame(distribution_rows)
    tables["length"] = pd.DataFrame(length_rows)
    outcomes = (
        contracts.groupby(
            ["platform", "outcome_category", "outcome_evidence"], dropna=False, sort=True
        )
        .size()
        .rename("contracts")
        .reset_index()
    )
    outcomes["share"] = outcomes.contracts / outcomes.platform.map(counts)
    tables["outcomes"] = outcomes
    observed = cases.loc[
        cases.claim_relation_validated
        & cases.evidence_kind.isin(["observed_settlement_divergence", "observed_chronology"])
    ].sort_values(["display_order", "case_id"])
    tables["settlements"] = observed[
        [
            "case_id",
            "phenomenon",
            "evidence_kind",
            "a_platform",
            "b_platform",
            "observed_settlement_a",
            "observed_settlement_b",
        ]
    ]

    with plt.rc_context(
        {
            "font.family": "DejaVu Sans",
            "font.size": 10,
            "svg.fonttype": "none",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.spines.left": False,
            "axes.edgecolor": "#D8DEDC",
            "text.color": "#233D3C",
            "axes.labelcolor": "#536766",
            "xtick.color": "#536766",
            "ytick.color": "#233D3C",
            "figure.facecolor": "#FFFFFF",
            "axes.facecolor": "#FFFFFF",
        }
    ):
        fig, ax = plt.subplots(figsize=(7.1, 3.9))
        for offset, platform in zip([-0.13, 0.13], platforms, strict=True):
            values = overall.loc[platform, list(COMPONENT_LABELS)].astype(float)
            ax.scatter(
                values,
                np.arange(5) + offset,
                s=60,
                color=PLATFORM_COLORS[platform],
                label=platform,
                zorder=3,
            )
            for y, value in enumerate(values):
                ax.annotate(
                    f"{value:.2f}",
                    (value, y + offset),
                    xytext=(5, 0),
                    textcoords="offset points",
                    va="center",
                    fontsize=8,
                )
        ax.set(
            yticks=np.arange(5),
            yticklabels=list(COMPONENT_LABELS.values()),
            xlim=(-0.03, 1.13),
            xticks=[0, 0.25, 0.5, 0.75, 1],
            xlabel="Mean component score (0–1)",
        )
        ax.invert_yaxis()
        ax.grid(axis="x", alpha=0.18)
        ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, 1.18), ncols=2)
        figures["components"] = _chart(
            fig,
            figure_dir / "descriptions-components.svg",
            "Five literal rule-text components",
            "Mean scores by platform; exact values in the adjacent table.",
        )

        fig, ax = plt.subplots(figsize=(7.1, 3.9))
        for platform in platforms:
            sample = tables["distribution"].loc[tables["distribution"].platform.eq(platform)]
            ax.stairs(
                sample.share,
                index_edges,
                color=PLATFORM_COLORS[platform],
                linewidth=2,
                label=platform,
            )
        ax.set(
            xlim=(0, 1),
            ylim=(0, None),
            xlabel="Exploratory rule-text specificity index",
            ylabel="Share of platform contracts",
        )
        ax.yaxis.set_major_formatter(PercentFormatter(1))
        ax.grid(axis="y", alpha=0.18)
        ax.legend(frameon=False)
        figures["distribution"] = _chart(
            fig,
            figure_dir / "descriptions-distribution.svg",
            "Distribution of the exploratory text index",
            "Twenty fixed bins of width 0.05; shares use nonmissing scores within each platform.",
        )

        fig, ax = plt.subplots(figsize=(7.1, 3.9))
        for offset, platform in zip([-0.19, 0.19], platforms, strict=True):
            sample = tables["length"].loc[tables["length"].platform.eq(platform)]
            ax.bar(
                np.arange(7) + offset,
                sample.share,
                width=0.36,
                color=PLATFORM_COLORS[platform],
                label=platform,
            )
        ax.set(
            xticks=np.arange(7),
            xticklabels=length_labels,
            xlabel="Analyzed text length (words)",
            ylabel="Share of platform contracts",
            ylim=(0, None),
        )
        ax.yaxis.set_major_formatter(PercentFormatter(1))
        ax.grid(axis="y", alpha=0.18)
        ax.set_axisbelow(True)
        ax.legend(frameon=False)
        figures["length"] = _chart(
            fig,
            figure_dir / "descriptions-length.svg",
            "How much text defines a claim?",
            "Question, rules and source text combined; 500+ includes all long texts.",
        )

        fig, ax = plt.subplots(figsize=(7.1, 3.9))
        for platform in platforms:
            sample = tables["families"].loc[tables["families"].platform.eq(platform)].head(20)
            ax.plot(
                sample["rank"],
                sample.cumulative_share,
                color=PLATFORM_COLORS[platform],
                linewidth=2,
                label=platform,
            )
            fifth = sample.loc[sample["rank"].eq(5)]
            if not fifth.empty:
                share = float(fifth.iloc[0].cumulative_share)
                ax.scatter([5], [share], color=PLATFORM_COLORS[platform], zorder=3)
                ax.annotate(
                    f"Top 5: {share:.1%}",
                    (5, share),
                    xytext=(9, 7),
                    textcoords="offset points",
                    fontsize=9,
                )
        ax.set(
            xlim=(1, 20),
            ylim=(0, 1),
            xticks=[1, 5, 10, 15, 20],
            xlabel="Largest API families included (ranked within platform)",
            ylabel="Cumulative share of platform contracts",
        )
        ax.yaxis.set_major_formatter(PercentFormatter(1))
        ax.grid(alpha=0.18)
        ax.legend(frameon=False, loc="upper left")
        figures["families"] = _chart(
            fig,
            figure_dir / "descriptions-families.svg",
            "Contract concentration in API families",
            "Kalshi series and Polymarket events have different granularity. "
            "This does not rank platform diversity.",
        )

        fig, axes = plt.subplots(1, 2, figsize=(12, 4.2))
        for platform, ax in zip(platforms, axes, strict=True):
            sample = tables["categories"].loc[tables["categories"].platform.eq(platform)]
            shown = sample.head(5)[["category", "share"]].copy()
            if len(sample) > 5:
                shown.loc[len(shown)] = ["Remaining categories", sample.iloc[5:].share.sum()]
            category_positions = np.arange(len(shown))
            ax.barh(category_positions, shown.share, color=PLATFORM_COLORS[platform], height=0.57)
            for i, share in enumerate(shown.share):
                ax.text(share + 0.012, i, f"{share:.1%}", va="center", fontsize=9)
            ax.set(
                yticks=category_positions,
                yticklabels=shown.category,
                xlim=(0, 0.68),
                title=platform,
                xlabel="Share of platform contracts",
            )
            ax.xaxis.set_major_formatter(PercentFormatter(1))
            ax.invert_yaxis()
            ax.grid(axis="x", alpha=0.18)
            ax.set_axisbelow(True)
        fig.tight_layout(w_pad=3)
        figures["categories"] = _chart(
            fig,
            figure_dir / "descriptions-categories.svg",
            "Topics in the selected portfolios",
            "Five largest categories plus the remainder; "
            "native labels are not harmonized across platforms.",
        )

        fig, ax = plt.subplots(figsize=(8.6, 3.2))
        labels = []
        for i, observed_record in enumerate(observed.to_dict("records")):
            label = {
                "hilton-first-vs-advance": "Hilton · first place / advancement",
                "khamenei-death-allocation": "Khamenei · departure settlements",
                "minerals-observed-chronology": "Minerals · different milestones",
            }.get(str(observed_record["case_id"]), str(observed_record["phenomenon"]))
            labels.append(label)
            a = float(observed_record["observed_settlement_a"])
            b = float(observed_record["observed_settlement_b"])
            ax.plot([a, b], [i, i], color="#CFD8D5", linewidth=4, zorder=1)
            for offset, side, amount in [(-0.09, "a", a), (0.09, "b", b)]:
                platform = str(observed_record[f"{side}_platform"])
                ax.scatter(
                    [amount],
                    [i + offset],
                    color=PLATFORM_COLORS[platform],
                    s=70,
                    marker="o" if side == "a" else "D",
                    zorder=3,
                )
                ax.annotate(
                    f"{side.upper()}: ${amount:.2f}",
                    (amount, i + offset),
                    xytext=(0, -15 if side == "a" else 9),
                    textcoords="offset points",
                    ha="center",
                    fontsize=8,
                )
        ax.set(
            yticks=np.arange(len(labels)),
            yticklabels=labels,
            xlim=(-0.12, 1.12),
            xticks=[0, 0.25, 0.5, 0.75, 1],
            ylim=(-0.65, max(len(labels) - 0.35, 0.65)),
            xlabel="Recorded normalized contract settlement ($ per $1 maximum payout)",
        )
        ax.invert_yaxis()
        ax.grid(axis="x", alpha=0.18)
        figures["settlements"] = _chart(
            fig,
            figure_dir / "descriptions-settlements.svg",
            "Observed contract settlements",
            "Circles are contract A; diamonds are B. Blue is Kalshi, coral is Polymarket. "
            "Cases form a separate purposive evidence inventory.",
        )

    replacements = {f"{name}_chart": svg for name, svg in figures.items()}
    for name, table in tables.items():
        table.to_csv(table_dir / f"descriptions-{name}.csv", index=False, lineterminator="\n")
        display = table.copy()
        if name == "components":
            display[platforms] = display[platforms].map(lambda value: f"{value:.3f}")
        if name == "strata":
            display["Threshold stratum"] = display["Threshold stratum"].replace(
                {
                    "all": "Overall",
                    "no_threshold_flag": "No threshold flag",
                    "threshold_flag": "Threshold flag",
                }
            )
            display["Mean index"] = display["Mean index"].map(lambda value: f"{value:.3f}")
            display["Mean text words"] = display["Mean text words"].map(
                lambda value: f"{value:.1f}"
            )
        if "share" in display:
            display["share"] = display["share"].map(lambda value: f"{value:.1%}")
        if name == "outcomes":
            display["outcome_evidence"] = display["outcome_evidence"].map(
                lambda value: OUTCOME_LABELS.get(value, str(value))
            )
            display = display.rename(
                columns={
                    "platform": "Platform",
                    "outcome_category": "Outcome category",
                    "outcome_evidence": "Evidence basis",
                    "contracts": "Contracts",
                    "share": "Within-platform share",
                }
            )
        replacements[f"{name}_table"] = _table(display, f"{name.title()} · descriptive values")
    valid_cases = cases.loc[cases.claim_relation_validated]
    replacements.update(
        {
            "contracts": f"{len(contracts):,}",
            "kalshi_n": f"{counts['Kalshi']:,}",
            "polymarket_n": f"{counts['Polymarket']:,}",
            "cases_n": str(len(cases)),
            "observed_n": str(valid_cases.evidence_kind.str.startswith("observed_").sum()),
            "hypothetical_n": str(valid_cases.evidence_kind.eq("hypothetical_rule_witness").sum()),
            "snapshot": escape(
                ", ".join(sorted(contracts.snapshot_date.dropna().astype(str).unique()))
            ),
            "case_cards": _case_cards(cases),
            "missing_index": str(contracts.determinacy_score.isna().sum()),
            "missing_length": str(contracts.rule_word_count.isna().sum()),
        }
    )
    page = Template(TEMPLATE_PATH.read_text(encoding="utf-8")).substitute(replacements)
    path.write_text(page, encoding="utf-8")
