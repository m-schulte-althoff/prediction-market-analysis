"""Acquire and structure mechanism-rich representation cases."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import pandas as pd

from src.config import KALSHI_BASE_URL, POLYMARKET_GAMMA_URL, SampleConfig, dated_raw_path
from src.http_client import PublicApiClient
from src.io_utils import read_json, write_immutable_json

LOGGER = logging.getLogger(__name__)

POLYMARKET_EVENT_SLUGS = (
    "presidential-election-winner-2028",
    "fed-decision-in-september-762",
    "ukraine-agrees-to-give-trump-rare-earth-metals-before-april",
    "trump-x-ukraine-mineral-deal-signed-before-may",
    "will-zelenskyy-wear-a-suit-before-july",
)
KALSHI_EVENT_TICKERS = ("KXPRESPERSON-28", "KXFEDDECISION-26SEP")


def anecdote_snapshot_path(config: SampleConfig) -> Path:
    """Return the immutable official-rule snapshot used by the casebook."""

    return dated_raw_path("representation-cases", config.retrieval_date)


def download_anecdote_sources(
    config: SampleConfig, client: PublicApiClient
) -> dict[str, Any]:
    """Download or load exact official records for the pre-specified cases."""

    path = anecdote_snapshot_path(config)
    if path.exists():
        payload = read_json(path)
        if not isinstance(payload, dict):
            raise TypeError("Representation-case snapshot must contain a JSON object")
        LOGGER.info("Using cached representation-case snapshot: %s", path)
        return payload
    polymarket_events: dict[str, Any] = {}
    for slug in POLYMARKET_EVENT_SLUGS:
        response = client.get_json(f"{POLYMARKET_GAMMA_URL}/events", {"slug": slug})
        if not isinstance(response, list) or not response:
            raise RuntimeError(f"Polymarket event was not found: {slug}")
        polymarket_events[slug] = response[0]
    kalshi_events: dict[str, Any] = {}
    for ticker in KALSHI_EVENT_TICKERS:
        response = client.get_json(f"{KALSHI_BASE_URL}/events/{ticker}")
        if not isinstance(response, dict):
            raise TypeError(f"Kalshi event returned an unexpected payload: {ticker}")
        kalshi_events[ticker] = response
    payload = {
        "retrieved_at_date": config.retrieval_date.isoformat(),
        "polymarket_events": polymarket_events,
        "kalshi_events": kalshi_events,
    }
    write_immutable_json(path, payload)
    LOGGER.info("Saved official representation-case records to %s", path)
    return payload


def _polymarket_market(
    payload: dict[str, Any], event_slug: str, market_slug: str
) -> dict[str, Any]:
    """Extract one exact Polymarket market from an archived event."""

    events = payload.get("polymarket_events", {})
    event = events.get(event_slug, {}) if isinstance(events, dict) else {}
    markets = event.get("markets", []) if isinstance(event, dict) else []
    for market in markets:
        if isinstance(market, dict) and market.get("slug") == market_slug:
            return market
    raise KeyError(f"Polymarket market not found in case snapshot: {market_slug}")


def _kalshi_market(
    payload: dict[str, Any], event_ticker: str, market_ticker: str
) -> dict[str, Any]:
    """Extract one exact Kalshi market from an archived event."""

    events = payload.get("kalshi_events", {})
    event = events.get(event_ticker, {}) if isinstance(events, dict) else {}
    markets = event.get("markets", []) if isinstance(event, dict) else []
    for market in markets:
        if isinstance(market, dict) and market.get("ticker") == market_ticker:
            return market
    raise KeyError(f"Kalshi market not found in case snapshot: {market_ticker}")


def _contract_fields(platform: str, market: dict[str, Any]) -> dict[str, str]:
    """Normalize casebook identifiers, text, and official links."""

    if platform == "Kalshi":
        ticker = str(market.get("ticker") or "")
        rules = "\n".join(
            str(market.get(key) or "").strip()
            for key in ("rules_primary", "rules_secondary")
            if market.get(key)
        )
        return {
            "platform": platform,
            "contract_id": ticker,
            "question": str(market.get("title") or ""),
            "rule": rules,
            "url": f"https://kalshi.com/markets/{ticker.lower()}",
        }
    slug = str(market.get("slug") or "")
    return {
        "platform": platform,
        "contract_id": str(market.get("id") or slug),
        "question": str(market.get("question") or ""),
        "rule": str(market.get("description") or ""),
        "url": f"https://polymarket.com/event/{slug}",
    }


def _case(
    *,
    case_id: str,
    phenomenon: str,
    scope: str,
    mechanism: str,
    signature_a: str,
    signature_b: str,
    witness_state: str,
    payout_a: str,
    payout_b: str,
    contract_a: dict[str, str],
    contract_b: dict[str, str],
    retrieval_date: str,
    truth_condition_divergent: bool,
    determinacy_issue: bool,
    coder_confidence: str = "high",
) -> dict[str, object]:
    """Create one stable, auditable representation-case row."""

    record: dict[str, object] = {
        "case_id": case_id,
        "phenomenon": phenomenon,
        "scope": scope,
        "mechanism": mechanism,
        "signature_a": signature_a,
        "signature_b": signature_b,
        "witness_state": witness_state,
        "payout_a": payout_a,
        "payout_b": payout_b,
        "truth_condition_divergent": truth_condition_divergent,
        "determinacy_issue": determinacy_issue,
        "coder_confidence": coder_confidence,
        "retrieval_date": retrieval_date,
        "evidence_role": "mechanism case; not an average-effect estimate",
    }
    for side, contract in (("a", contract_a), ("b", contract_b)):
        for key, value in contract.items():
            record[f"{side}_{key}"] = value
    return record


def build_representation_case_matrix(
    payload: dict[str, Any], matches: pd.DataFrame | None = None
) -> pd.DataFrame:
    """Build manually coded signatures with counterfactual witness states."""

    retrieval_date = str(payload.get("retrieved_at_date") or "")
    election_a = _contract_fields(
        "Kalshi", _kalshi_market(payload, "KXPRESPERSON-28", "KXPRESPERSON-28-MRUB")
    )
    election_b = _contract_fields(
        "Polymarket",
        _polymarket_market(
            payload,
            "presidential-election-winner-2028",
            "will-marco-rubio-win-the-2028-us-presidential-election",
        ),
    )
    fed_a = _contract_fields(
        "Kalshi", _kalshi_market(payload, "KXFEDDECISION-26SEP", "KXFEDDECISION-26SEP-C25")
    )
    fed_b = _contract_fields(
        "Polymarket",
        _polymarket_market(
            payload,
            "fed-decision-in-september-762",
            "will-the-fed-decrease-interest-rates-by-25-bps-after-the-september-2026-meeting-586",
        ),
    )
    minerals_a = _contract_fields(
        "Polymarket",
        _polymarket_market(
            payload,
            "ukraine-agrees-to-give-trump-rare-earth-metals-before-april",
            "ukraine-agrees-to-give-trump-rare-earth-metals-before-april",
        ),
    )
    minerals_b = _contract_fields(
        "Polymarket",
        _polymarket_market(
            payload,
            "trump-x-ukraine-mineral-deal-signed-before-may",
            "trump-x-ukraine-mineral-deal-signed-before-may",
        ),
    )
    suit_a = _contract_fields(
        "Polymarket",
        _polymarket_market(
            payload,
            "will-zelenskyy-wear-a-suit-before-july",
            "will-zelenskyy-wear-a-suit-before-july",
        ),
    )
    within_state = {
        "platform": "Observed world state",
        "contract_id": "not-a-second-contract",
        "question": "Does borderline formal clothing count as a suit?",
        "rule": "No additional garment-level definition is supplied by the contract.",
        "url": "",
    }
    records = [
        _case(
            case_id="election-call-vs-inauguration",
            phenomenon="2028 U.S. presidential winner",
            scope="cross-platform",
            mechanism="predicate-stage and temporal divergence",
            signature_a="next person inaugurated for the term beginning in 2029",
            signature_b="candidate called winner by AP, Fox News, and NBC; inauguration fallback",
            witness_state=(
                "All three networks call Rubio, but he dies or is disqualified before "
                "inauguration."
            ),
            payout_a="NO",
            payout_b="YES",
            contract_a=election_a,
            contract_b=election_b,
            retrieval_date=retrieval_date,
            truth_condition_divergent=True,
            determinacy_issue=False,
        ),
        _case(
            case_id="fed-quantization-convention",
            phenomenon="September 2026 Federal Reserve decision",
            scope="cross-platform",
            mechanism="measurement, quantization, and fallback divergence",
            signature_a="exactly a 25 bp cut within a mutually exclusive bucket family",
            signature_b="upper-bound change rounded up to 25 bp increments; no-statement fallback",
            witness_state="The target-range upper bound falls by an unusual 12.5 bp.",
            payout_a="NO under the literal exact-25-bp rule",
            payout_b="YES because 12.5 bp rounds up to the 25-bp bucket",
            contract_a=fed_a,
            contract_b=fed_b,
            retrieval_date=retrieval_date,
            truth_condition_divergent=True,
            determinacy_issue=False,
        ),
        _case(
            case_id="minerals-agreement-vs-signature",
            phenomenon="U.S.–Ukraine minerals agreement",
            scope="within-platform across successive contracts",
            mechanism="milestone-stage divergence",
            signature_a="public announcement that a deal has been reached can qualify",
            signature_b=(
                "deal must be enacted, signed, or formally adopted; announcement alone fails"
            ),
            witness_state=(
                "Both governments announce an agreement, but no instrument is signed or adopted."
            ),
            payout_a="YES",
            payout_b="NO",
            contract_a=minerals_a,
            contract_b=minerals_b,
            retrieval_date=retrieval_date,
            truth_condition_divergent=True,
            determinacy_issue=False,
        ),
        _case(
            case_id="suit-category-boundary",
            phenomenon="Zelenskyy wearing a suit",
            scope="within-contract",
            mechanism="category-boundary indeterminacy",
            signature_a="photographed or videotaped wearing a suit; no garment definition",
            signature_b="borderline observed attire",
            witness_state="Zelenskyy wears a blazer and trousers that do not match, with no tie.",
            payout_a="YES or NO: the rule does not uniquely classify the attire",
            payout_b="N/A—witness to within-contract indeterminacy",
            contract_a=suit_a,
            contract_b=within_state,
            retrieval_date=retrieval_date,
            truth_condition_divergent=False,
            determinacy_issue=True,
        ),
    ]
    leader_case = _leader_departure_case(matches, retrieval_date)
    if leader_case is not None:
        records.append(leader_case)
    return pd.DataFrame.from_records(records).sort_values("case_id", kind="stable").reset_index(
        drop=True
    )


def _leader_departure_case(
    matches: pd.DataFrame | None, retrieval_date: str
) -> dict[str, object] | None:
    """Extract the strongest archived leader-departure witness from matched data."""

    if matches is None or matches.empty:
        return None
    sample = matches.loc[
        matches["kalshi_question"]
        .astype(str)
        .str.contains("Donald Trump out before 2027", regex=False)
    ]
    if sample.empty:
        return None
    row = sample.sort_values("match_confidence", ascending=False, kind="stable").iloc[0]
    a = {
        "platform": "Kalshi",
        "contract_id": str(row["kalshi_contract_id"]),
        "question": str(row["kalshi_question"]),
        "rule": str(row["kalshi_rule"]),
        "url": f"https://kalshi.com/markets/{str(row['kalshi_contract_id']).lower()}",
    }
    b = {
        "platform": "Polymarket",
        "contract_id": str(row["polymarket_contract_id"]),
        "question": str(row["polymarket_question"]),
        "rule": str(row["polymarket_rule"]),
        "url": "https://polymarket.com",
    }
    return _case(
        case_id="leader-announcement-vs-departure",
        phenomenon="Donald Trump leaving office before 2027",
        scope="cross-platform",
        mechanism="stage, edge-case, and settlement-codomain divergence",
        signature_a="departure announcement can qualify; death triggers price-based allocation",
        signature_b="only permanent cessation qualifies; announcement and caretaker status fail",
        witness_state=(
            "Trump announces a qualifying resignation date but remains in office past the deadline."
        ),
        payout_a="YES",
        payout_b="NO",
        contract_a=a,
        contract_b=b,
        retrieval_date=retrieval_date,
        truth_condition_divergent=True,
        determinacy_issue=False,
    )


def write_casebook(path: Path, cases: pd.DataFrame) -> None:
    """Write a concise narrative that keeps every striking case explainable."""

    lines = [
        "# Representation Casebook",
        "",
        "These cases establish mechanisms, not average effects. A divergence claim requires a "
        "plausible witness state for which the represented payouts differ.",
        "",
    ]
    for row in cases.to_dict(orient="records"):
        lines.extend(
            [
                f"## {row['phenomenon']}",
                "",
                f"- Scope: {row['scope']}",
                f"- Mechanism: {row['mechanism']}",
                f"- Representation A ({row['a_platform']}): {row['signature_a']}",
                f"- Representation B ({row['b_platform']}): {row['signature_b']}",
                f"- Witness state: {row['witness_state']}",
                f"- Implied settlements: A = {row['payout_a']}; B = {row['payout_b']}",
                f"- Exact archived rules: {row['a_rule']} || {row['b_rule']}",
                (
                    f"- Retrieval date: {row['retrieval_date']}; "
                    f"coder confidence: {row['coder_confidence']}"
                ),
                "",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
