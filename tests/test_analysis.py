"""Tests for market-level specifications and aggregation robustness."""

import numpy as np
import pandas as pd

from src.analysis import market_level_models, prepare_market_analysis, terminal_error_model


def _analysis_fixture() -> pd.DataFrame:
    """Build two platforms with known inverse determinacy-volume gradients."""

    records: list[dict[str, object]] = []
    for platform in ("Kalshi", "Polymarket"):
        for index in range(40):
            determinacy = 0.25 + index / 80
            volume = float(np.exp(10 - 3 * determinacy + (index % 3) * 0.03))
            outcome = "yes" if index % 2 else "no"
            terminal_price = (
                0.75 + 0.002 * (index % 5)
                if outcome == "yes"
                else 0.15 + 0.002 * (index % 5)
            )
            terminal_error = abs(terminal_price - (1.0 if outcome == "yes" else 0.0))
            records.append(
                {
                    "platform": platform,
                    "series": f"{platform}-{index}",
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
        "event_series_aggregated",
    }.issubset(set(models["model"]))
    assert models.loc[models["model"] == "main_composite", "coefficient"].iloc[0] < 0


def test_terminal_error_model_runs_on_resolved_kalshi_rows() -> None:
    """The Kalshi-only outcome uses traded interior prices and clustered uncertainty."""

    prepared = prepare_market_analysis(_analysis_fixture())
    result = terminal_error_model(prepared)

    assert result.iloc[0]["model"] == "kalshi_terminal_error"
    assert result.iloc[0]["n"] == 40
