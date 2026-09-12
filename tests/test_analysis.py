"""Tests for market-level specifications and aggregation robustness."""

import numpy as np
import pandas as pd

from src.analysis import (
    determinacy_bins,
    market_level_models,
    platform_profiles,
    prepare_market_analysis,
    terminal_error_model,
)


def test_platform_profiles_preserve_composition_reversal_and_family_variation() -> None:
    """Unequal type mixes can reverse pooled rankings despite both conditional rankings."""

    records = []
    for platform, types in (
        ("Kalshi", [(0, 1, 0.2), (1, 9, 0.7)]),
        ("Polymarket", [(0, 9, 0.3), (1, 1, 0.8)]),
    ):
        for flag, count, score in types:
            for _ in range(count):
                records.append(
                    {
                        "platform": platform,
                        "quantitative_threshold": flag,
                        "determinacy_score": score,
                        "family_id": f"{platform}-{flag}",
                        "rule_word_count": 100,
                        **{
                            component: score
                            for component in (
                                "source_specificity",
                                "temporal_specificity",
                                "outcome_definition",
                                "edge_completeness",
                                "discretion_clarity",
                            )
                        },
                    }
                )
    result = platform_profiles(pd.DataFrame(records)).set_index(["platform", "stratum"])
    assert (
        float(str(result.loc[("Kalshi", "all"), "mean_determinacy"]))
        > float(str(result.loc[("Polymarket", "all"), "mean_determinacy"]))
    )
    for stratum in ("no_threshold_flag", "threshold_flag"):
        assert (
            float(str(result.loc[("Kalshi", stratum), "mean_determinacy"]))
            < float(str(result.loc[("Polymarket", stratum), "mean_determinacy"]))
        )
    assert result.loc[("Kalshi", "all"), "between_family_variance_share"] == 1
    assert result.loc[("Kalshi", "all"), "varying_families"] == 0
    assert result.loc[("Kalshi", "all"), "threshold_flag_share"] == 0.9


def test_platform_profiles_do_not_treat_constant_scores_as_explained_variance() -> None:
    """A portfolio with no score variation has no defined variance decomposition."""

    frame = prepare_market_analysis(_analysis_fixture())
    frame["determinacy_score"] = 0.5
    profiles = platform_profiles(frame)
    assert profiles.between_family_variance_share.isna().all()


def _analysis_fixture() -> pd.DataFrame:
    """Build two platforms with known inverse determinacy-volume gradients."""

    records: list[dict[str, object]] = []
    for platform in ("Kalshi", "Polymarket"):
        for index in range(40):
            family_index = index // 2 if index < 30 else 15 + index - 30
            determinacy = 0.25 + index / 80
            volume = float(np.exp(10 - 3 * determinacy + (index % 3) * 0.03))
            outcome = "yes" if index % 2 else "no"
            terminal_price = (
                0.75 + 0.002 * (index % 5) if outcome == "yes" else 0.15 + 0.002 * (index % 5)
            )
            terminal_error = abs(terminal_price - (1.0 if outcome == "yes" else 0.0))
            records.append(
                {
                    "platform": platform,
                    "series": f"{platform}-{family_index}",
                    "platform_event_id": f"{platform}-event-{family_index}",
                    "contract_id": f"{platform}-{index}",
                    "category": "Politics",
                    "volume": volume,
                    "log_volume": np.log1p(volume),
                    "determinacy_score": determinacy,
                    "source_specificity": determinacy,
                    "temporal_specificity": determinacy,
                    "outcome_definition": determinacy,
                    "discretion_clarity": determinacy,
                    "rule_word_count": 50 + index,
                    "conditional_clauses": index % 4,
                    "market_duration_days": 30 + index,
                    "observed_exposure_days": 25 + index,
                    "open_timestamp": pd.Timestamp(f"202{index % 3}-01-01", tz="UTC"),
                    "resolution_timestamp": pd.Timestamp(f"202{4 + index % 3}-12-31", tz="UTC"),
                    "edge_completeness": determinacy,
                    "ambiguous_terms": float(index % 2),
                    "quantitative_threshold": float(index % 2),
                    "outcome": outcome,
                    "terminal_price": terminal_price if platform == "Kalshi" else np.nan,
                    "terminal_abs_error": terminal_error if platform == "Kalshi" else np.nan,
                }
            )
    return pd.DataFrame.from_records(records)


def test_market_models_include_dependence_robust_specifications() -> None:
    """Main, platform, cluster, and collapsed-unit models all execute."""

    prepared = prepare_market_analysis(_analysis_fixture())
    models = market_level_models(prepared)

    assert {
        "main_composite",
        "within_kalshi",
        "within_polymarket",
        "main_series_clustered",
        "family_aggregated",
        "cohort_exposure_adjusted",
        "within_family_kalshi",
        "within_family_polymarket",
    }.issubset(set(models["model"]))
    assert models.loc[models["model"] == "main_composite", "coefficient"].iloc[0] < 0


def test_terminal_error_model_runs_on_resolved_kalshi_rows() -> None:
    """The Kalshi-only outcome uses traded interior prices and clustered uncertainty."""

    prepared = prepare_market_analysis(_analysis_fixture())
    result = terminal_error_model(prepared)

    assert result.iloc[0]["model"] == "kalshi_terminal_error"
    assert result.iloc[0]["n"] == 40


def test_determinacy_groups_do_not_arbitrarily_split_tied_scores() -> None:
    """Tie-preserving quantiles may return fewer than five honest groups."""

    frame = pd.DataFrame(
        {
            "platform": ["Kalshi"] * 10,
            "determinacy_score": [0.2] * 5 + [0.8] * 5,
            "volume_z": np.linspace(-1, 1, 10),
        }
    )

    result = determinacy_bins(frame)

    assert result["n"].sum() == 10
    assert len(result) < 5
