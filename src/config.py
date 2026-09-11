"""Project paths and reproducible sampling configuration."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path

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


@dataclass(frozen=True)
class SampleConfig:
    """Parameters controlling the cached public-data sample."""

    retrieval_date: date = date.today()
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
