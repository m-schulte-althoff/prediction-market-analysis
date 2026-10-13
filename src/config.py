"""Project paths and reproducible sampling configuration."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
OUTPUT_DIR = PROJECT_ROOT / "output"
TABLE_DIR = OUTPUT_DIR / "tables"
FIGURE_DIR = OUTPUT_DIR / "figures"
DIAGNOSTIC_DIR = OUTPUT_DIR / "diagnostics"
LOG_DIR = PROJECT_ROOT / "logs"

KALSHI_BASE_URL = "https://external-api.kalshi.com/trade-api/v2"
POLYMARKET_GAMMA_URL = "https://gamma-api.polymarket.com"
POLYMARKET_CLOB_URL = "https://clob.polymarket.com"

# Semantic ambiguity is most defensible for these non-sports domains. Recurring
# weather and asset-price markets are excluded because contract counts would
# otherwise overwhelm the sample with near-identical templates.
KALSHI_CATEGORIES = (
    "AI",
    "Business",
    "Companies",
    "Economics",
    "Elections",
    "Health",
    "Politics",
    "Science and Technology",
    "Social",
    "Transportation",
    "World",
)


def utc_now() -> datetime:
    """Return the actual acquisition clock in UTC, independent of local timezone."""

    return datetime.now(UTC)


def utc_today() -> date:
    """Return the current UTC date used for new immutable snapshot labels."""

    return utc_now().date()


@dataclass(frozen=True)
class SampleConfig:
    """Parameters controlling the cached public-data sample."""

    retrieval_date: date = field(default_factory=utc_today)
    kalshi_series_limit: int = 120
    kalshi_markets_per_series: int = 1_000
    polymarket_limit: int = 8_000
    polymarket_page_size: int = 100
    matched_panel_limit: int = 12
    request_timeout_seconds: int = 45


def ensure_directories() -> None:
    """Create writable derived-data, output, and log directories."""

    for path in (
        RAW_DIR,
        PROCESSED_DIR,
        TABLE_DIR,
        FIGURE_DIR,
        DIAGNOSTIC_DIR,
        LOG_DIR,
    ):
        path.mkdir(parents=True, exist_ok=True)


def dated_raw_path(source: str, retrieval_date: date) -> Path:
    """Return the immutable snapshot path for a source and retrieval date."""

    return RAW_DIR / f"{source}-{retrieval_date.isoformat()}.json"


def require_current_acquisition_date(path: Path, retrieval_date: date) -> None:
    """Reject a missing dated cache before responses could receive a false date."""

    today = utc_today()
    if retrieval_date < today:
        raise FileNotFoundError(
            f"Historical snapshot is absent: {path}. Requested snapshot date "
            f"{retrieval_date.isoformat()} cannot be recreated with current API responses; "
            "restore the original archive or explicitly request today's UTC date."
        )
    if retrieval_date > today:
        raise ValueError(
            f"Snapshot date {retrieval_date.isoformat()} is in the future; "
            f"new API responses require today's UTC date {today.isoformat()}."
        )


def acquisition_metadata(retrieval_date: date) -> dict[str, str]:
    """Record the requested label separately from actual UTC acquisition completion."""

    return {
        "retrieved_at_date": retrieval_date.isoformat(),
        "acquired_at_utc": utc_now().isoformat(),
    }


def validate_snapshot_date(
    payload: dict[str, Any], retrieval_date: date, source: str
) -> None:
    """Check a recorded date while preserving legacy snapshots with no timestamp."""

    recorded_date = payload.get("retrieved_at_date")
    if recorded_date is not None and recorded_date != retrieval_date.isoformat():
        raise ValueError(
            f"{source} snapshot date {recorded_date!r} does not match requested date "
            f"{retrieval_date.isoformat()!r}."
        )
