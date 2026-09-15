"""Paper-oriented tables and figures."""

from __future__ import annotations

import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure

PLATFORM_COLORS = {"Kalshi": "#335C81", "Polymarket": "#D1495B"}


def platform_rule_profiles(profiles: pd.DataFrame, path: Path) -> None:
    """Compare raw rule components and show how portfolio mix affects the composite."""

    figure, axes = plt.subplots(1, 2, figsize=(12, 4.8))
    components = [
        "source_specificity",
        "temporal_specificity",
        "outcome_definition",
        "edge_completeness",
        "discretion_clarity",
    ]
    strata = ["all", "no_threshold_flag", "threshold_flag"]
    for platform, group in profiles.groupby("platform", sort=True):
        overall = group.loc[group.stratum == "all"].iloc[0]
        axes[0].plot(
            [overall[component] for component in components],
            np.arange(5),
            "o-",
            label=platform,
            color=PLATFORM_COLORS.get(str(platform)),
        )
        ordered = group.set_index("stratum").reindex(strata)
        axes[1].plot(
            np.arange(3),
            ordered.mean_determinacy,
            "o-",
            label=platform,
            color=PLATFORM_COLORS.get(str(platform)),
        )
    axes[0].set(
        yticks=np.arange(5),
        yticklabels=["Source", "Time", "Outcome definition", "Edge clauses", "Discretion"],
        xlim=(0, 1.05),
        xlabel="Mean component proxy (0–1)",
        title="Different dimensions of rule specification",
    )
    axes[0].invert_yaxis()
    axes[1].set(
        xticks=np.arange(3),
        xticklabels=["Overall", "No threshold\nflag", "Threshold\nflag"],
        ylim=(0, 1),
        ylabel="Mean determinacy proxy (0–1)",
        title="Compare the composite within contract types",
    )
    for axis in axes:
        axis.grid(alpha=0.2)
        axis.legend(frameon=False)
    figure.text(
        0.5,
        0.01,
        "Purposive sampled portfolios; threshold flags are text proxies, "
        "not validated contract types.",
        ha="center",
        fontsize=9,
    )
    figure.tight_layout(rect=(0, 0.05, 1, 1))
    _finish(figure, path)


def _finish(figure: Figure, path: Path) -> None:
    """Save a tightly bounded vector graphic and close its figure."""

    path.parent.mkdir(parents=True, exist_ok=True)
    # Stable SVG identifiers and no wall-clock metadata make regenerated figures reproducible.
    with plt.rc_context({"svg.hashsalt": path.name}):
        figure.savefig(
            path,
            format=path.suffix.removeprefix("."),
            bbox_inches="tight",
            metadata={"Date": None} if path.suffix.lower() == ".svg" else None,
        )
    plt.close(figure)
    if path.suffix.lower() == ".svg":
        lines = path.read_text(encoding="utf-8").splitlines()
        normalized = "\n".join(line.rstrip() for line in lines)
        path.write_text(normalized + "\n", encoding="utf-8")


def conceptual_schematic(path: Path) -> None:
    """Separate institutional claim definition, world-belief updating and market pricing."""

    figure, axis = plt.subplots(figsize=(14, 5.3))
    axis.set_xlim(0, 1)
    axis.set_ylim(0, 1)
    axis.axis("off")
    nodes = [
        (0.09, 0.78, "Possible world\nhistories $\\Omega$", "#E7EEF5"),
        (0.30, 0.78, "Platform $c$\nresolution architecture", "#DDEAF4"),
        (
            0.54,
            0.78,
            "Settlement mapping $r_c$\nbinary event $Y_c$\nor incomplete $R_c$",
            "#F5DFE2",
        ),
        (0.09, 0.30, "Trader evidence $e$", "#E7EEF5"),
        (
            0.30,
            0.30,
            "Bayesian updating\nover world histories\n$\\mu_e=P(\\cdot\\mid e)$",
            "#DDEAF4",
        ),
        (0.54, 0.30, "Claim valuation\n$q_c=E_{\\mu_e}[r_c]$", "#F3F0E8"),
        (0.76, 0.30, "Market\naggregation", "#F3F0E8"),
        (0.94, 0.30, "Observed\nprice $p_c$", "#F3F0E8"),
    ]
    for x_value, y_value, label, color in nodes:
        axis.text(
            x_value,
            y_value,
            label,
            ha="center",
            va="center",
            fontsize=10,
            bbox={"boxstyle": "round,pad=0.65", "facecolor": color, "edgecolor": "#333333"},
        )
    arrows = [
        ((0.16, 0.78), (0.21, 0.78)),
        ((0.40, 0.78), (0.44, 0.78)),
        ((0.17, 0.30), (0.21, 0.30)),
        ((0.40, 0.30), (0.46, 0.30)),
        ((0.54, 0.65), (0.54, 0.40)),
        ((0.62, 0.30), (0.71, 0.30)),
        ((0.82, 0.30), (0.90, 0.30)),
    ]
    for start, end in arrows:
        axis.annotate(
            "",
            xy=end,
            xytext=start,
            arrowprops={"arrowstyle": "->", "color": "#555555", "lw": 1.5},
        )
    axis.text(
        0.80,
        0.78,
        "Same posterior over worlds\n+ different payoff events\n"
        "can yield different claim probabilities",
        ha="center",
        va="center",
        fontsize=10,
        color="#7A3E00",
    )
    axis.text(
        0.50,
        0.02,
        "A point claim valuation requires a sufficiently complete mapping. "
        "Equating price with probability requires additional assumptions.",
        ha="center",
        fontsize=9,
        color="#444444",
    )
    _finish(figure, path)


def determinacy_distribution(contracts: pd.DataFrame, path: Path) -> None:
    """Plot determinacy distributions by platform."""

    figure, axis = plt.subplots(figsize=(7.5, 4.8))
    bins = np.linspace(0, 1, 22)
    for platform, group in contracts.groupby("platform", sort=True):
        axis.hist(
            group["determinacy_score"],
            bins=bins.tolist(),
            alpha=0.55,
            density=True,
            label=f"{platform} (n={len(group):,})",
            color=PLATFORM_COLORS.get(str(platform)),
        )
    axis.set(xlabel="Semantic determinacy score", ylabel="Density")
    axis.legend(frameon=False)
    axis.grid(axis="y", alpha=0.2)
    _finish(figure, path)


def determinacy_volume_bins(bins: pd.DataFrame, path: Path) -> None:
    """Plot mean within-platform volume by determinacy quintile."""

    figure, axis = plt.subplots(figsize=(7.5, 4.8))
    for platform, group in bins.groupby("platform", sort=True):
        axis.errorbar(
            group["determinacy_group"],
            group["mean_volume_z"],
            yerr=1.96 * group["se_volume_z"].fillna(0),
            marker="o",
            capsize=3,
            label=platform,
            color=PLATFORM_COLORS.get(str(platform)),
        )
    axis.axhline(0, color="#777777", linewidth=0.8)
    axis.set(
        xlabel="Tie-preserving determinacy quantile group (within platform)",
        ylabel="Mean standardized log volume (95% CI)",
        xticks=range(1, int(bins["determinacy_group"].max()) + 1),
    )
    axis.legend(frameon=False)
    axis.grid(alpha=0.2)
    _finish(figure, path)


def divergence_disagreement(summary: pd.DataFrame, path: Path) -> None:
    """Plot near-close price disagreement against semantic divergence."""

    if summary.empty:
        path.unlink(missing_ok=True)
        return
    sample = summary.dropna(subset=["semantic_divergence", "mean_disagreement_30d"])
    if len(sample) < 6 or sample["semantic_divergence"].nunique() < 3:
        if path.exists():
            path.unlink()
        return
    figure, axis = plt.subplots(figsize=(7.5, 4.8))
    axis.scatter(
        sample["semantic_divergence"],
        sample["mean_disagreement_30d"],
        s=42,
        color="#5B4B8A",
        alpha=0.8,
    )
    if len(sample) >= 3 and sample["semantic_divergence"].nunique() > 1:
        coefficients = np.polyfit(
            sample["semantic_divergence"], sample["mean_disagreement_30d"], deg=1
        )
        x_values = np.linspace(
            sample["semantic_divergence"].min(), sample["semantic_divergence"].max()
        )
        axis.plot(x_values, np.polyval(coefficients, x_values), color="#D1495B")
    axis.set(
        xlabel="Semantic divergence",
        ylabel="Mean absolute probability disagreement, last 30 days",
    )
    axis.grid(alpha=0.2)
    _finish(figure, path)


def _wrap_question(value: str, width: int = 48) -> str:
    """Wrap a question for compact subplot titles."""

    return textwrap.fill(value, width=width, max_lines=2, placeholder=" …")


def price_trajectories(panel: pd.DataFrame, path: Path, maximum_events: int = 4) -> None:
    """Plot revealing paired price paths close to resolution."""

    if panel.empty:
        path.unlink(missing_ok=True)
        return
    ranking = (
        panel.groupby("underlying_event_id", sort=True)
        .agg(max_disagreement=("disagreement", "max"), observations=("timestamp", "size"))
        .query("observations >= 5")
        .sort_values("max_disagreement", ascending=False)
        .head(maximum_events)
    )
    if ranking.empty:
        path.unlink(missing_ok=True)
        return
    figure, axes = plt.subplots(len(ranking), 1, figsize=(9, 3.2 * len(ranking)), squeeze=False)
    for axis, event_id in zip(axes[:, 0], ranking.index, strict=True):
        group = panel.loc[panel["underlying_event_id"] == event_id].sort_values("timestamp")
        group = group.loc[group["days_to_close"].between(0, 180)]
        _plot_pair(axis, group)
    figure.tight_layout()
    _finish(figure, path)


def _plot_pair(axis: Axes, group: pd.DataFrame) -> None:
    """Plot one aligned matched pair on an existing axis."""

    axis.plot(group["timestamp"], group["kalshi_price"], label="Kalshi", color="#335C81")
    axis.plot(group["timestamp"], group["polymarket_price"], label="Polymarket", color="#D1495B")
    title = _wrap_question(str(group["kalshi_question"].iloc[0]))
    axis.set(title=title, ylabel="YES probability", ylim=(-0.03, 1.03))
    axis.grid(alpha=0.2)
    axis.legend(frameon=False, ncol=2, loc="best")
