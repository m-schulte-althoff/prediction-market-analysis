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
    r"touchdown|quarterback|playoffs?|regular season|"
    r"club world cup|world cup qualifier"
    r")\b",
    re.IGNORECASE,
)
SPORTS_FILTER_VERSION = "substantive-sports-v3"
SPORTS_CATEGORY_PATTERN = re.compile(r"\b(?:sports?|esports?)\b", re.IGNORECASE)
SPORTS_GAME_PATTERN = re.compile(r"\b(?:epl|cfb|cbb|ucl)\s+(?:game|match)\b", re.IGNORECASE)


def _text(value: object) -> str:
    """Normalize a nullable API value for taxonomy checks."""

    return str(value or "").strip()


def classify_polymarket_sports(row: dict[str, Any]) -> tuple[bool, str]:
    """Return a sports decision and its observable, substantive reason."""

    if row.get("sportsMarketType"):
        return True, "sports_market_type"
    events = row.get("events")
    event = events[0] if isinstance(events, list) and events and isinstance(events[0], dict) else {}
    categories = [_text(row.get("category")), _text(event.get("category"))]
    for source in (row, event):
        tags = source.get("tags", [])
        if isinstance(tags, list):
            categories.extend(
                _text(tag.get("label")) for tag in tags if isinstance(tag, dict)
            )
    if any(SPORTS_CATEGORY_PATTERN.search(category) for category in categories):
        return True, "sports_category_or_tag"
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
    match = SPORTS_PATTERN.search(text)
    if match:
        return True, f"sports_text:{match.group(0).lower()}"
    game_match = SPORTS_GAME_PATTERN.search(text)
    if game_match:
        return True, f"sports_game_phrase:{game_match.group(0).lower()}"
    if row.get("gameStartTime"):
        return False, "game_start_time_without_sports_evidence"
    return False, "no_substantive_sports_evidence"


def is_polymarket_sports(row: dict[str, Any]) -> bool:
    """Flag sports without treating an event timestamp as a sport label."""

    return classify_polymarket_sports(row)[0]
