"""Command-line controller for the prediction-market study pipeline."""

from __future__ import annotations

import argparse
import logging
from dataclasses import replace
from datetime import date, datetime
from pathlib import Path

import pandas as pd

from src.analysis import (
    determinacy_bins,
    market_level_models,
    matched_model,
    prepare_market_analysis,
    terminal_error_model,
)
from src.anecdotes import (
    build_representation_case_matrix,
    download_anecdote_sources,
    write_casebook,
)
from src.config import (
    FIGURE_DIR,
    LOG_DIR,
    OUTPUT_DIR,
    PROCESSED_DIR,
    TABLE_DIR,
    SampleConfig,
    ensure_directories,
)
from src.http_client import PublicApiClient
from src.io_utils import read_json, write_csv
from src.kalshi import download_kalshi, kalshi_snapshot_path
from src.matching import match_contracts
from src.panel import build_matched_panel, download_matched_histories, summarize_matched_panel
from src.polymarket import download_polymarket, polymarket_snapshot_path
from src.preprocessing import build_contract_table
from src.reporting import (
    coverage_table,
    semantic_examples,
    write_research_log,
    write_research_status,
    write_research_summary,
)
from src.semantics import add_semantic_features
from views import (
    conceptual_schematic,
    determinacy_distribution,
    determinacy_volume_bins,
    divergence_disagreement,
    price_trajectories,
)

LOGGER = logging.getLogger(__name__)
CONTRACT_PATH = PROCESSED_DIR / "semantics-contracts.csv"
MATCH_PATH = PROCESSED_DIR / "matching-candidates.csv"
PANEL_PATH = PROCESSED_DIR / "panel-daily.csv"
PANEL_SUMMARY_PATH = PROCESSED_DIR / "panel-matched-summary.csv"
CASE_PATH = TABLE_DIR / "representation-case-matrix.csv"


def configure_logging() -> Path:
    """Configure console and timestamped file logging."""

    ensure_directories()
    path = LOG_DIR / f"pipeline-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.FileHandler(path, encoding="utf-8"), logging.StreamHandler()],
        force=True,
    )
    return path


def _read_frame(path: Path, date_columns: tuple[str, ...] = ()) -> pd.DataFrame:
    """Read a required processed table and restore selected UTC timestamps."""

    if not path.exists():
        raise FileNotFoundError(f"Required pipeline output is missing: {path}")
    columns = pd.read_csv(path, nrows=0).columns
    identifier_columns = {
        column: "string"
        for column in (
            "platform_contract_id",
            "platform_event_id",
            "kalshi_contract_id",
            "polymarket_contract_id",
        )
        if column in columns
    }
    frame = pd.read_csv(path, dtype=identifier_columns, low_memory=False)
    for column in date_columns:
        if column in frame:
            frame[column] = pd.to_datetime(
                frame[column], utc=True, errors="coerce", format="mixed"
            )
    return frame


def run_download(config: SampleConfig) -> None:
    """Download both immutable official-API snapshots."""

    client = PublicApiClient(timeout_seconds=config.request_timeout_seconds)
    kalshi = download_kalshi(config, client)
    polymarket = download_polymarket(config, client)
    LOGGER.info(
        "Download complete: %d Kalshi, %d Polymarket rows",
        len(kalshi.get("markets", [])),
        len(polymarket.get("markets", [])),
    )


def run_preprocess(config: SampleConfig) -> pd.DataFrame:
    """Normalize cached sources and compute transparent semantic measures."""

    kalshi_path = kalshi_snapshot_path(config)
    polymarket_path = polymarket_snapshot_path(config)
    if not kalshi_path.exists() or not polymarket_path.exists():
        run_download(config)
    kalshi_payload = read_json(kalshi_path)
    polymarket_payload = read_json(polymarket_path)
    if not isinstance(kalshi_payload, dict) or not isinstance(polymarket_payload, dict):
        raise TypeError("Raw platform snapshots must contain JSON objects")
    contracts = add_semantic_features(build_contract_table(kalshi_payload, polymarket_payload))
    write_csv(contracts, CONTRACT_PATH, ["platform", "contract_id"])
    write_csv(coverage_table(contracts), TABLE_DIR / "preprocessing-coverage.csv", ["platform"])
    write_csv(
        semantic_examples(contracts),
        TABLE_DIR / "semantics-component-examples.csv",
        ["platform", "determinacy_score", "platform_contract_id"],
    )
    LOGGER.info("Preprocessed %d contracts", len(contracts))
    return contracts


def run_match() -> pd.DataFrame:
    """Generate and export auditable cross-platform match candidates."""

    contracts = _read_frame(
        CONTRACT_PATH,
        ("open_timestamp", "close_timestamp", "resolution_timestamp"),
    )
    matches = match_contracts(contracts)
    write_csv(matches, MATCH_PATH, ["match_label", "match_confidence", "underlying_event_id"])
    high = matches.loc[matches["match_label"] == "high_confidence"].copy()
    write_csv(
        high,
        TABLE_DIR / "matching-high-confidence.csv",
        ["semantic_divergence", "match_confidence"],
    )
    representative = high.sort_values(
        ["semantic_divergence", "match_confidence"], ascending=False, kind="stable"
    ).head(20)
    columns = [
        "kalshi_question",
        "kalshi_rule",
        "polymarket_question",
        "polymarket_rule",
        "identified_semantic_difference",
        "phenomenon_similarity",
        "phenomenon_match_label",
        "lexical_similarity",
        "semantic_divergence",
        "match_confidence",
    ]
    write_csv(representative[columns], TABLE_DIR / "matching-representative-pairs.csv")
    LOGGER.info("Generated %d candidates, %d high-confidence", len(matches), len(high))
    return matches


def run_anecdotes(config: SampleConfig) -> pd.DataFrame:
    """Archive exact cited rules and build the witness-state casebook."""

    client = PublicApiClient(timeout_seconds=config.request_timeout_seconds)
    payload = download_anecdote_sources(config, client)
    matches = _read_frame(MATCH_PATH) if MATCH_PATH.exists() else None
    cases = build_representation_case_matrix(payload, matches)
    write_csv(cases, CASE_PATH, ["case_id"])
    write_casebook(OUTPUT_DIR / "REPRESENTATION_CASEBOOK.md", cases)
    LOGGER.info("Built %d audited representation cases", len(cases))
    return cases


def run_panel(config: SampleConfig) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Acquire and construct the cross-platform daily price panel."""

    matches = _read_frame(
        MATCH_PATH,
        (
            "kalshi_open_timestamp",
            "polymarket_open_timestamp",
            "kalshi_close_timestamp",
            "polymarket_close_timestamp",
        ),
    )
    client = PublicApiClient(timeout_seconds=config.request_timeout_seconds)
    payload = download_matched_histories(matches, config, client)
    panel = build_matched_panel(payload)
    summary = summarize_matched_panel(panel)
    write_csv(panel, PANEL_PATH, ["underlying_event_id", "timestamp"] if not panel.empty else None)
    write_csv(
        summary,
        PANEL_SUMMARY_PATH,
        ["semantic_divergence", "underlying_event_id"] if not summary.empty else None,
    )
    LOGGER.info("Built %d daily observations for %d matched events", len(panel), len(summary))
    return panel, summary


def run_analysis() -> None:
    """Estimate models and generate paper-like tables, figures, and narrative."""

    contracts = _read_frame(
        CONTRACT_PATH,
        ("open_timestamp", "close_timestamp", "resolution_timestamp"),
    )
    matches = _read_frame(MATCH_PATH)
    panel = _read_frame(PANEL_PATH, ("timestamp",)) if PANEL_PATH.exists() else pd.DataFrame()
    panel_summary = (
        _read_frame(PANEL_SUMMARY_PATH) if PANEL_SUMMARY_PATH.exists() else pd.DataFrame()
    )
    cases = _read_frame(CASE_PATH) if CASE_PATH.exists() else pd.DataFrame()
    analysis_frame = prepare_market_analysis(contracts)
    models = market_level_models(analysis_frame)
    bins = determinacy_bins(analysis_frame)
    matched_models = matched_model(panel_summary)
    error_models = terminal_error_model(analysis_frame)

    write_csv(models, TABLE_DIR / "analysis-market-models.csv", ["model"])
    write_csv(
        bins,
        TABLE_DIR / "analysis-determinacy-bins.csv",
        ["platform", "determinacy_group"],
    )
    write_csv(matched_models, TABLE_DIR / "analysis-matched-model.csv")
    write_csv(error_models, TABLE_DIR / "analysis-terminal-error.csv")
    conceptual_schematic(FIGURE_DIR / "views-conceptual-schematic.svg")
    determinacy_distribution(analysis_frame, FIGURE_DIR / "views-determinacy-distribution.svg")
    determinacy_volume_bins(bins, FIGURE_DIR / "views-determinacy-volume.svg")
    divergence_disagreement(panel_summary, FIGURE_DIR / "views-divergence-disagreement.svg")
    price_trajectories(panel, FIGURE_DIR / "views-matched-trajectories.svg")
    write_research_log(
        OUTPUT_DIR / "research-log.md", models, error_models, matches, matched_models
    )
    write_research_summary(
        OUTPUT_DIR / "RESEARCH_SUMMARY.md",
        contracts,
        models,
        error_models,
        matches,
        panel_summary,
        matched_models,
        cases,
    )
    write_research_status(OUTPUT_DIR / "RESEARCH_STATUS.md", contracts, models, cases)
    LOGGER.info("Analysis package written under %s", OUTPUT_DIR)


def run_all(config: SampleConfig) -> None:
    """Execute the complete cached pipeline."""

    run_download(config)
    run_preprocess(config)
    run_match()
    run_anecdotes(config)
    run_panel(config)
    run_analysis()


def parse_args() -> argparse.Namespace:
    """Parse command-oriented pipeline arguments."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command",
        choices=(
            "download",
            "preprocess",
            "semantics",
            "match",
            "anecdotes",
            "panel",
            "analyze",
            "all",
        ),
    )
    parser.add_argument("--retrieval-date", type=date.fromisoformat, default=date.today())
    parser.add_argument("--kalshi-series-limit", type=int, default=120)
    parser.add_argument("--polymarket-limit", type=int, default=8_000)
    parser.add_argument("--matched-panel-limit", type=int, default=12)
    return parser.parse_args()


def main() -> None:
    """Dispatch the requested pipeline stage."""

    arguments = parse_args()
    log_path = configure_logging()
    config = replace(
        SampleConfig(),
        retrieval_date=arguments.retrieval_date,
        kalshi_series_limit=arguments.kalshi_series_limit,
        polymarket_limit=arguments.polymarket_limit,
        matched_panel_limit=arguments.matched_panel_limit,
    )
    LOGGER.info("Starting %s; log=%s", arguments.command, log_path)
    if arguments.command == "download":
        run_download(config)
    elif arguments.command in {"preprocess", "semantics"}:
        run_preprocess(config)
    elif arguments.command == "match":
        run_match()
    elif arguments.command == "anecdotes":
        run_anecdotes(config)
    elif arguments.command == "panel":
        run_panel(config)
    elif arguments.command == "analyze":
        run_analysis()
    else:
        run_all(config)


if __name__ == "__main__":
    main()
