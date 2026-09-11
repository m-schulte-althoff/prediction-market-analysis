"""Lean empirical analyses for iterative mechanism discovery."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

DETERMINACY_COMPONENTS = (
    "source_specificity",
    "temporal_specificity",
    "outcome_definition",
    "edge_completeness",
    "discretion_clarity",
)
TEMPORAL_REPLICATION_CUTOFF = pd.Timestamp("2025-07-01", tz="UTC")


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
    exposure = frame.get("observed_exposure_days", frame["market_duration_days"])
    frame["log_observed_exposure"] = np.log1p(exposure.clip(lower=0).fillna(0))
    open_timestamp = pd.to_datetime(frame["open_timestamp"], utc=True, errors="coerce")
    frame["open_year"] = open_timestamp.dt.year.astype("Int64").astype(str)
    frame["analysis_family"] = np.where(
        frame["platform"].eq("Kalshi"),
        frame["series"].astype(str),
        frame.get("platform_event_id", frame["series"]).astype(str),
    )
    missing_family = frame["analysis_family"].isin(("", "nan", "None", "<NA>"))
    frame.loc[missing_family, "analysis_family"] = frame.loc[missing_family, "contract_id"]
    frame["family_id"] = frame["platform"] + ":" + frame["analysis_family"]
    frame["family_contracts"] = frame.groupby("family_id", observed=True)[
        "contract_id"
    ].transform("size")
    family_mean = frame.groupby("family_id", observed=True)["determinacy_score"].transform("mean")
    frame["determinacy_within"] = frame["determinacy_score"] - family_mean
    frame["determinacy_between"] = family_mean
    frame["determinacy_within_z"] = frame.groupby("platform", observed=True)[
        "determinacy_within"
    ].transform(_zscore)
    frame["determinacy_between_z"] = frame.groupby("platform", observed=True)[
        "determinacy_between"
    ].transform(_zscore)
    frame["ambiguous_terms_z"] = frame.groupby("platform", observed=True)[
        "ambiguous_terms"
    ].transform(_zscore)
    for omitted in DETERMINACY_COMPONENTS:
        retained = [component for component in DETERMINACY_COMPONENTS if component != omitted]
        column = f"determinacy_without_{omitted}_z"
        score = frame[retained].mean(axis=1)
        frame[column] = score.groupby(frame["platform"], observed=True).transform(_zscore)
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
            "cohort_exposure_adjusted",
            "volume_z ~ determinacy_z + log_rule_length + log_observed_exposure + "
            "C(open_year) + C(platform) + C(category_group)",
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
    resolved = frame.loc[frame["outcome"].isin(("yes", "no"))]
    if len(resolved) >= 30 and resolved["determinacy_z"].nunique() >= 2:
        model = smf.ols(
            "volume_z ~ determinacy_z + log_rule_length + log_observed_exposure + "
            "C(open_year) + C(platform) + C(category_group)",
            data=resolved,
        ).fit(cov_type="HC3")
        records.append(_model_row("resolved_cohort_adjusted", model, "determinacy_z"))
    for market_type, value in (("qualitative", 0.0), ("quantitative", 1.0)):
        sample = frame.loc[frame["quantitative_threshold"].eq(value)]
        if len(sample) < 30 or sample["determinacy_z"].nunique() < 2:
            continue
        model = smf.ols(
            "volume_z ~ determinacy_z + log_rule_length + log_observed_exposure + "
            "C(open_year) + C(platform) + C(category_group)",
            data=sample,
        ).fit(cov_type="HC3")
        records.append(_model_row(f"{market_type}_contracts", model, "determinacy_z"))
    resolution_time = pd.to_datetime(
        frame["resolution_timestamp"], utc=True, errors="coerce", format="mixed"
    )
    for period, period_mask in (
        ("early", resolution_time < TEMPORAL_REPLICATION_CUTOFF),
        ("late", resolution_time >= TEMPORAL_REPLICATION_CUTOFF),
    ):
        for platform in ("Kalshi", "Polymarket"):
            sample = frame.loc[period_mask & frame["platform"].eq(platform)]
            if len(sample) < 30 or sample["determinacy_z"].nunique() < 2:
                continue
            model = smf.ols(
                "volume_z ~ determinacy_z + log_rule_length + log_observed_exposure + "
                "C(open_year) + C(category_group)",
                data=sample,
            ).fit(cov_type="HC3")
            records.append(
                _model_row(f"temporal_{period}_{platform.lower()}", model, "determinacy_z")
            )
    ambiguity_model = smf.ols(
        "volume_z ~ ambiguous_terms_z + log_rule_length + log_observed_exposure + "
        "C(open_year) + C(platform) + C(category_group)",
        data=frame,
    ).fit(cov_type="HC3")
    records.append(_model_row("direct_ambiguity_count", ambiguity_model, "ambiguous_terms_z"))
    for omitted in DETERMINACY_COMPONENTS:
        term = f"determinacy_without_{omitted}_z"
        model = smf.ols(
            f"volume_z ~ {term} + log_rule_length + log_observed_exposure + "
            "C(open_year) + C(platform) + C(category_group)",
            data=frame,
        ).fit(cov_type="HC3")
        records.append(_model_row(f"leave_out_{omitted}", model, term))
    cluster_formula = (
        "volume_z ~ determinacy_z + log_rule_length + log_duration + "
        "C(platform) + C(category_group)"
    )
    clustered_sample = frame.loc[frame["analysis_family"].astype(str).str.len() > 0]
    if len(clustered_sample) >= 30 and clustered_sample["family_id"].nunique() >= 10:
        clustered = smf.ols(cluster_formula, data=clustered_sample).fit(
            cov_type="cluster", cov_kwds={"groups": clustered_sample["family_id"]}
        )
        records.append(
            _model_row(
                "main_series_clustered",
                clustered,
                "determinacy_z",
                int(clustered_sample["family_id"].nunique()),
            )
        )
    records.extend(_within_family_models(frame))
    aggregated = _aggregate_families(frame)
    if len(aggregated) >= 30 and aggregated["determinacy_z"].nunique() >= 2:
        aggregate_model = smf.ols(
            "volume_z ~ determinacy_z + log_rule_length + log_observed_exposure + "
            "log_contract_count + C(platform) + C(category_group)",
            data=aggregated,
        ).fit(cov_type="HC3")
        records.append(_model_row("family_aggregated", aggregate_model, "determinacy_z"))
    return pd.DataFrame.from_records(records)


def _within_family_models(frame: pd.DataFrame) -> list[dict[str, object]]:
    """Estimate determinacy effects using only variation within repeated families."""

    records: list[dict[str, object]] = []
    for platform in ("Kalshi", "Polymarket"):
        repeated = (frame["platform"] == platform) & (frame["family_contracts"] >= 2)
        sample = frame.loc[repeated].copy()
        varying = sample.groupby("family_id", observed=True)["determinacy_score"].transform(
            "nunique"
        )
        sample = sample.loc[varying >= 2].copy()
        clusters = int(sample["family_id"].nunique())
        if len(sample) < 30 or clusters < 10:
            continue
        for column in ("volume_z", "log_rule_length", "log_observed_exposure"):
            sample[f"{column}_within"] = sample[column] - sample.groupby(
                "family_id", observed=True
            )[column].transform("mean")
        sample["determinacy_within_z"] = _zscore(sample["determinacy_within"])
        model = smf.ols(
            "volume_z_within ~ determinacy_within_z + log_rule_length_within + "
            "log_observed_exposure_within - 1",
            data=sample,
        ).fit(cov_type="cluster", cov_kwds={"groups": sample["family_id"]})
        records.append(
            _model_row(
                f"within_family_{platform.lower()}",
                model,
                "determinacy_within_z",
                clusters,
            )
        )
    return records


def _aggregate_families(frame: pd.DataFrame) -> pd.DataFrame:
    """Collapse repeated contracts to explicitly labeled template/event families."""

    aggregated = (
        frame.groupby(["platform", "family_id"], sort=True, observed=True)
        .agg(
            total_volume=("volume", "sum"),
            contract_count=("contract_id", "size"),
            determinacy_score=("determinacy_score", "mean"),
            rule_word_count=("rule_word_count", "mean"),
            market_duration_days=("market_duration_days", "mean"),
            observed_exposure_days=("observed_exposure_days", "mean"),
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
    aggregated["log_observed_exposure"] = np.log1p(
        aggregated["observed_exposure_days"].clip(lower=0).fillna(0)
    )
    aggregated["log_contract_count"] = np.log1p(aggregated["contract_count"])
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
        bins = pd.qcut(
            group["determinacy_score"], q=min(5, len(group)), labels=False, duplicates="drop"
        )
        for bin_value, subset in group.groupby(bins, observed=True):
            standard_error = subset["volume_z"].std() / np.sqrt(len(subset))
            records.append(
                {
                    "platform": platform,
                    "determinacy_group": int(bin_value) + 1,
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
