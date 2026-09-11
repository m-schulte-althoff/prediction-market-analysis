"""Shared, auditable sample-taxonomy rules."""

from __future__ import annotations

import re
from typing import Any

SPORTS_PATTERN = re.compile(
    r"\b(?:"
    r"nba|wnba|nfl|nhl|mlb|mls|ncaa|ufc|fifa|uefa|"
    r"super bowl|stanley cup|world series|champions league|premier league|"
    r"la liga|bundesliga|serie a|liga mx|copa america|"
    r"basketball|baseball|american football|soccer|ice hockey|tennis|golf|"
    r"cricket|rugby|boxing|formula ?1|grand prix|olympic|"
    r"touchdown|quarterback|playoffs?|regular season|tournament|"
    r"club world cup|world cup qualifier"
    r")\b",
    re.IGNORECASE,
)


def _text(value: object) -> str:
    """Normalize a nullable API value for taxonomy checks."""

    return str(value or "").strip()


def is_polymarket_sports(row: dict[str, Any]) -> bool:
    """Flag sports using official fields plus a conservative text taxonomy."""

    if row.get("sportsMarketType") or row.get("gameStartTime"):
        return True
    events = row.get("events")
    event = events[0] if isinstance(events, list) and events and isinstance(events[0], dict) else {}
    text = " ".join(
        _text(value)
        for value in (
            row.get("question"),
            row.get("description"),
            row.get("slug"),
            event.get("title"),
            event.get("description"),
            event.get("slug"),
            event.get("ticker"),
        )
    )
    return bool(SPORTS_PATTERN.search(text))
