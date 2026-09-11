"""Lean empirical analyses for iterative mechanism discovery."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


def _zscore(series: pd.Series) -> pd.Series:
    """Standardize a series while avoiding division by zero."""

    standard_deviation = series.std(ddof=0)
    if pd.isna(standard_deviation) or standard_deviation == 0:
        return pd.Series(0.0, index=series.index)
    return (series - series.mean()) / standard_deviation


def prepare_market_analysis(contracts: pd.DataFrame) -> pd.DataFrame:
    """Construct pre-specified analysis variables and coarse control groups."""

    frame = contracts.loc[
        contracts["volume"].notna()
        & (contracts["volume"] >= 0)
        & contracts["determinacy_score"].notna()
    ].copy()
    frame["volume_z"] = frame.groupby("platform", observed=True)["log_volume"].transform(_zscore)
    frame["determinacy_z"] = frame.groupby("platform", observed=True)[
        "determinacy_score"
    ].transform(_zscore)
    frame["core_determinacy"] = frame[
        [
            "source_specificity",
            "temporal_specificity",
            "outcome_definition",
            "discretion_clarity",
        ]
    ].mean(axis=1)
    frame["core_determinacy_z"] = frame.groupby("platform", observed=True)[
        "core_determinacy"
    ].transform(_zscore)
    frame["log_rule_length"] = np.log1p(frame["rule_word_count"])
    frame["log_duration"] = np.log1p(frame["market_duration_days"].clip(lower=0).fillna(0))
    category_counts = frame["category"].value_counts()
    frame["category_group"] = frame["category"].where(
        frame["category"].map(category_counts) >= 30, "Other"
    )
    return frame


def _model_row(
    name: str, model: Any, term: str, clusters: int | None = None
) -> dict[str, object]:
    """Extract the focal coefficient and fit statistics from an OLS result."""

    return {
        "model": name,
        "term": term,
        "coefficient": float(model.params[term]),
        "std_error": float(model.bse[term]),
        "p_value": float(model.pvalues[term]),
        "ci_lower": float(model.conf_int().loc[term, 0]),
        "ci_upper": float(model.conf_int().loc[term, 1]),
        "n": int(model.nobs),
        "r_squared": float(model.rsquared),
        "clusters": clusters,
    }


def market_level_models(frame: pd.DataFrame) -> pd.DataFrame:
    """Estimate main and obvious-alternative volume specifications with HC3 errors."""

    specifications = [
        (
            "main_composite",
            "volume_z ~ determinacy_z + log_rule_length + log_duration + "
            "C(platform) + C(category_group)",
            "determinacy_z",
        ),
        (
            "complexity_separated",
            "volume_z ~ core_determinacy_z + log_rule_length + conditional_clauses + "
            "log_duration + C(platform) + C(category_group)",
            "core_determinacy_z",
        ),
        (
            "within_kalshi",
            "volume_z ~ determinacy_z + log_rule_length + log_duration + C(category_group)",
            "determinacy_z",
        ),
        (
            "within_polymarket",
            "volume_z ~ determinacy_z + log_rule_length + log_duration + C(category_group)",
            "determinacy_z",
        ),
    ]
    records: list[dict[str, object]] = []
    for name, formula, term in specifications:
        sample = frame
        if name == "within_kalshi":
            sample = frame.loc[frame["platform"] == "Kalshi"]
        elif name == "within_polymarket":
            sample = frame.loc[frame["platform"] == "Polymarket"]
        if len(sample) < 30 or sample[term].nunique() < 2:
            continue
        model = smf.ols(formula, data=sample).fit(cov_type="HC3")
        records.append(_model_row(name, model, term))
    cluster_formula = (
        "volume_z ~ determinacy_z + log_rule_length + log_duration + "
        "C(platform) + C(category_group)"
    )
    clustered_sample = frame.loc[frame["series"].astype(str).str.len() > 0]
    if len(clustered_sample) >= 30 and clustered_sample["series"].nunique() >= 10:
        clustered = smf.ols(cluster_formula, data=clustered_sample).fit(
            cov_type="cluster", cov_kwds={"groups": clustered_sample["series"]}
        )
        records.append(
            _model_row(
                "main_series_clustered",
                clustered,
                "determinacy_z",
                int(clustered_sample["series"].nunique()),
            )
        )
    aggregated = _aggregate_events(frame)
    if len(aggregated) >= 30 and aggregated["determinacy_z"].nunique() >= 2:
        aggregate_model = smf.ols(
            "volume_z ~ determinacy_z + log_rule_length + log_duration + "
            "C(platform) + C(category_group)",
            data=aggregated,
        ).fit(cov_type="HC3")
        records.append(_model_row("event_series_aggregated", aggregate_model, "determinacy_z"))
    return pd.DataFrame.from_records(records)


def _aggregate_events(frame: pd.DataFrame) -> pd.DataFrame:
    """Collapse repeated contracts to Kalshi series and Polymarket event units."""

    sample = frame.loc[frame["series"].astype(str).str.len() > 0].copy()
    aggregated = (
        sample.groupby(["platform", "series"], sort=True, observed=True)
        .agg(
            total_volume=("volume", "sum"),
            determinacy_score=("determinacy_score", "mean"),
            rule_word_count=("rule_word_count", "mean"),
            market_duration_days=("market_duration_days", "mean"),
            category_group=("category_group", "first"),
        )
        .reset_index()
    )
    aggregated["log_volume"] = np.log1p(aggregated["total_volume"].clip(lower=0))
    aggregated["volume_z"] = aggregated.groupby("platform", observed=True)[
        "log_volume"
    ].transform(_zscore)
    aggregated["determinacy_z"] = aggregated.groupby("platform", observed=True)[
        "determinacy_score"
    ].transform(_zscore)
    aggregated["log_rule_length"] = np.log1p(aggregated["rule_word_count"])
    aggregated["log_duration"] = np.log1p(
        aggregated["market_duration_days"].clip(lower=0).fillna(0)
    )
    return aggregated


def terminal_error_model(frame: pd.DataFrame) -> pd.DataFrame:
    """Test Kalshi last-trade absolute forecast error with series-clustered errors."""

    sample = frame.loc[
        (frame["platform"] == "Kalshi")
        & (frame["volume"] > 0)
        & frame["terminal_price"].between(0.01, 0.99)
        & frame["terminal_abs_error"].notna()
        & (frame["series"].astype(str).str.len() > 0)
    ].copy()
    if len(sample) < 30 or sample["series"].nunique() < 10:
        return pd.DataFrame()
    model = smf.ols(
        "terminal_abs_error ~ determinacy_z + log_rule_length + log_duration + "
        "C(category_group)",
        data=sample,
    ).fit(cov_type="cluster", cov_kwds={"groups": sample["series"]})
    return pd.DataFrame.from_records(
        [
            _model_row(
                "kalshi_terminal_error",
                model,
                "determinacy_z",
                int(sample["series"].nunique()),
            )
        ]
    )


def determinacy_bins(frame: pd.DataFrame) -> pd.DataFrame:
    """Summarize standardized trading volume across within-platform score quintiles."""

    records: list[dict[str, object]] = []
    for platform, group in frame.groupby("platform", sort=True):
        ranks = group["determinacy_score"].rank(method="first")
        bins = pd.qcut(ranks, q=min(5, len(group)), labels=False, duplicates="drop")
        for bin_value, subset in group.groupby(bins, observed=True):
            standard_error = subset["volume_z"].std() / np.sqrt(len(subset))
            records.append(
                {
                    "platform": platform,
                    "determinacy_quintile": int(bin_value) + 1,
                    "mean_determinacy": subset["determinacy_score"].mean(),
                    "mean_volume_z": subset["volume_z"].mean(),
                    "se_volume_z": standard_error,
                    "n": len(subset),
                }
            )
    return pd.DataFrame.from_records(records)


def matched_model(summary: pd.DataFrame) -> pd.DataFrame:
    """Estimate the exploratory divergence-disagreement association."""

    if summary.empty:
        return pd.DataFrame()
    sample = summary.dropna(subset=["mean_disagreement_30d", "semantic_divergence"])
    if len(sample) < 6 or sample["semantic_divergence"].nunique() < 2:
        return pd.DataFrame()
    model = smf.ols(
        "mean_disagreement_30d ~ semantic_divergence + match_confidence", data=sample
    ).fit(cov_type="HC3")
    return pd.DataFrame.from_records([_model_row("matched_30d", model, "semantic_divergence")])
