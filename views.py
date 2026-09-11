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


def _finish(figure: Figure, path: Path) -> None:
    """Save a tightly bounded vector graphic and close its figure."""

    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, format=path.suffix.removeprefix("."), bbox_inches="tight")
    plt.close(figure)


def conceptual_schematic(path: Path) -> None:
    """Draw the study's digital-representation mechanism."""

    figure, axis = plt.subplots(figsize=(11, 2.8))
    axis.set_xlim(0, 1)
    axis.set_ylim(0, 1)
    axis.axis("off")
    labels = [
        "Uncertain\nreal-world event",
        "Platform contract\nsemantic representation",
        "Participant\ninterpretation",
        "Trading and\ninformation aggregation",
        "Formal\nresolution",
    ]
    positions = np.linspace(0.08, 0.92, len(labels))
    for index, (position, label) in enumerate(zip(positions, labels, strict=True)):
        color = "#E7EEF5" if index != 1 else "#F6D8AE"
        axis.text(
            position,
            0.55,
            label,
            ha="center",
            va="center",
            fontsize=10,
            bbox={"boxstyle": "round,pad=0.65", "facecolor": color, "edgecolor": "#333333"},
        )
        if index < len(labels) - 1:
            axis.annotate(
                "",
                xy=(positions[index + 1] - 0.085, 0.55),
                xytext=(position + 0.085, 0.55),
                arrowprops={"arrowstyle": "->", "color": "#555555", "lw": 1.5},
            )
    axis.text(
        positions[1],
        0.12,
        "Semantic determinacy shapes the state space about which beliefs can aggregate",
        ha="center",
        fontsize=9,
        color="#7A3E00",
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
            group["determinacy_quintile"],
            group["mean_volume_z"],
            yerr=1.96 * group["se_volume_z"].fillna(0),
            marker="o",
            capsize=3,
            label=platform,
            color=PLATFORM_COLORS.get(str(platform)),
        )
    axis.axhline(0, color="#777777", linewidth=0.8)
    axis.set(
        xlabel="Semantic determinacy quintile (within platform)",
        ylabel="Mean standardized log volume (95% CI)",
        xticks=range(1, 6),
    )
    axis.legend(frameon=False)
    axis.grid(alpha=0.2)
    _finish(figure, path)


def divergence_disagreement(summary: pd.DataFrame, path: Path) -> None:
    """Plot near-close price disagreement against semantic divergence."""

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
        return
    ranking = (
        panel.groupby("underlying_event_id", sort=True)
        .agg(max_disagreement=("disagreement", "max"), observations=("timestamp", "size"))
        .query("observations >= 5")
        .sort_values("max_disagreement", ascending=False)
        .head(maximum_events)
    )
    if ranking.empty:
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
    axis.plot(
        group["timestamp"], group["polymarket_price"], label="Polymarket", color="#D1495B"
    )
    title = _wrap_question(str(group["kalshi_question"].iloc[0]))
    axis.set(title=title, ylabel="YES probability", ylim=(-0.03, 1.03))
    axis.grid(alpha=0.2)
    axis.legend(frameon=False, ncol=2, loc="best")
