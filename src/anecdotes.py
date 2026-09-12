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


def download_anecdote_sources(config: SampleConfig, client: PublicApiClient) -> dict[str, Any]:
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
    explanation: str = "",
    audit_note: str = "",
    secondary_witness_state: str = "",
    secondary_payout_a: str = "",
    secondary_payout_b: str = "",
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
        "scenario_status": "hypothetical witness; archived rules, not a realized payout audit",
        "explanation": explanation,
        "audit_note": audit_note,
        "secondary_witness_state": secondary_witness_state,
        "secondary_payout_a": secondary_payout_a,
        "secondary_payout_b": secondary_payout_b,
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
        "platform": "Hypothetical world state",
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
                "All three networks call Rubio, but he dies or is disqualified before inauguration."
            ),
            payout_a="NO",
            payout_b="YES",
            contract_a=election_a,
            contract_b=election_b,
            retrieval_date=retrieval_date,
            truth_condition_divergent=True,
            determinacy_issue=False,
            explanation=(
                "Winning the news call and actually taking office are different milestones."
            ),
            audit_note=(
                "The scenario assumes all three calls occur before inauguration; "
                "it is not an observed election outcome."
            ),
        ),
        _case(
            case_id="fed-quantization-convention",
            phenomenon="September 2026 Federal Reserve decision",
            scope="cross-platform",
            mechanism="measurement-bucket divergence (rounding)",
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
            explanation=(
                "Even numerical markets need a rule for assigning an unusual measurement "
                "to an answer bucket."
            ),
            audit_note=(
                "The witness isolates rounding under the archived literal Kalshi wording. "
                "Cancellation and no-statement fallbacks also differ, "
                "but are not tested by this scenario."
            ),
            coder_confidence="conditional on literal archived Kalshi rule",
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
                "On March 31, 2025 before 11:59 PM ET, both governments announce a deal "
                "explicitly involving Ukrainian rare earths. No qualifying mineral deal is "
                "signed, enacted, or formally adopted through April 30, 2025, 11:59 PM ET."
            ),
            payout_a="YES",
            payout_b="NO",
            contract_a=minerals_a,
            contract_b=minerals_b,
            retrieval_date=retrieval_date,
            truth_condition_divergent=True,
            determinacy_issue=False,
            explanation="Saying 'we have a deal' and signing the deal are different milestones.",
            audit_note=(
                "Successive Polymarket contracts also differ in dates, rare-earth versus "
                "mineral scope, and evidence sources. The witness specifies rare earths "
                "and both windows; this is not a synchronized cross-platform comparison."
            ),
        ),
        _case(
            case_id="suit-category-boundary",
            phenomenon="Zelenskyy wearing a suit",
            scope="within-contract",
            mechanism="category-boundary indeterminacy",
            signature_a="photographed or videotaped wearing a suit; no garment definition",
            signature_b="hypothetical borderline attire with differing descriptions",
            witness_state=(
                "During May 22–June 30, 2025, authentic images are taken and released showing "
                "Zelenskyy in a blazer and nonmatching trousers, without a tie. Credible reports "
                "differ on whether this counts as a suit."
            ),
            payout_a=(
                "not fixed by garment criteria alone; "
                "depends on the credible-reporting adjudication"
            ),
            payout_b="N/A—witness to within-contract indeterminacy",
            contract_a=suit_a,
            contract_b=within_state,
            retrieval_date=retrieval_date,
            truth_condition_divergent=False,
            determinacy_issue=True,
            explanation=(
                "People can see the same clothing and still disagree "
                "about whether it counts as a suit."
            ),
            audit_note=(
                "The archived text specifies image authenticity and timing but no garment "
                "definition. It delegates to credible reporting; this case does not document "
                "an actual dispute or prove the final institutional outcome remains indeterminate."
            ),
            coder_confidence=(
                "high for missing garment definition; institutional settlement not inferred"
            ),
        ),
    ]
    leader_case = _leader_departure_case(matches, retrieval_date)
    if leader_case is not None:
        records.append(leader_case)
    primary_case = _primary_advancement_case(matches, retrieval_date)
    if primary_case is not None:
        records.append(primary_case)
    return (
        pd.DataFrame.from_records(records)
        .sort_values("case_id", kind="stable")
        .reset_index(drop=True)
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
        "url": f"https://external-api.kalshi.com/trade-api/v2/markets/{row['kalshi_ticker']}",
    }
    b = {
        "platform": "Polymarket",
        "contract_id": str(row["polymarket_contract_id"]),
        "question": str(row["polymarket_question"]),
        "rule": str(row["polymarket_rule"]),
        "url": f"https://gamma-api.polymarket.com/markets/{row['polymarket_id']}",
    }
    return _case(
        case_id="leader-announcement-vs-departure",
        phenomenon="Donald Trump leaving office versus being the next leader out",
        scope="cross-platform",
        mechanism="departure-stage and competing-leader divergence",
        signature_a="departure announcement can qualify; death triggers price-based allocation",
        signature_b=(
            "Trump must be FIRST among listed leaders to permanently cease office; "
            "announcement and caretaker status fail"
        ),
        witness_state=(
            "Before the deadline, Trump announces a non-term-limit resignation within the "
            "next year but stays in office through 2026. No listed leader leaves by "
            "December 31, 2026, 11:59 PM ET."
        ),
        payout_a="YES",
        payout_b="NO",
        contract_a=a,
        contract_b=b,
        retrieval_date=retrieval_date,
        truth_condition_divergent=True,
        determinacy_issue=False,
        explanation=(
            "Leaving office at some point and being the first listed leader "
            "to leave are different bets."
        ),
        audit_note=(
            "The primary witness separates announcement from actual departure. The second "
            "isolates competition with other leaders. Kalshi's death-allocation clause is "
            "an additional rule feature, not demonstrated by either witness."
        ),
        secondary_witness_state=(
            "Another listed leader permanently leaves first; Trump subsequently resigns "
            "and permanently leaves before 2027, without dying."
        ),
        secondary_payout_a="YES",
        secondary_payout_b="NO",
    )


def _primary_advancement_case(
    matches: pd.DataFrame | None, retrieval_date: str
) -> dict[str, object] | None:
    """Extract an everyday rank-versus-qualification witness from systematic candidates."""

    if matches is None or matches.empty:
        return None
    sample = matches.loc[
        matches.kalshi_contract_id.eq("kalshi:KXCAGOVPRIMARY1ST-26JUN02-1ST-TSTE")
        & matches.polymarket_contract_id.eq("polymarket:825450")
    ]
    if sample.empty:
        return None
    row = sample.iloc[0]
    contracts = {}
    for prefix, platform in (("kalshi", "Kalshi"), ("polymarket", "Polymarket")):
        identifier = row[f"{prefix}_contract_id"]
        url = (
            f"https://external-api.kalshi.com/trade-api/v2/markets/{row['kalshi_ticker']}"
            if prefix == "kalshi"
            else f"https://gamma-api.polymarket.com/markets/{row['polymarket_id']}"
        )
        contracts[prefix] = {
            "platform": platform,
            "contract_id": str(identifier),
            "question": str(row[f"{prefix}_question"]),
            "rule": str(row[f"{prefix}_rule"]),
            "url": url,
        }
    return _case(
        case_id="primary-first-vs-advance",
        phenomenon="Tom Steyer finishing first versus advancing in the California primary",
        scope="cross-platform; retrieved from systematic sample",
        mechanism="rank versus qualification divergence",
        signature_a="must finish first in the California gubernatorial primary",
        signature_b="must advance to the general election; top two candidates qualify",
        witness_state=(
            "Steyer finishes second without a tie in the June 2, 2026 primary "
            "and advances to the general election."
        ),
        payout_a="NO",
        payout_b="YES",
        contract_a=contracts["kalshi"],
        contract_b=contracts["polymarket"],
        retrieval_date=retrieval_date,
        truth_condition_divergent=True,
        determinacy_issue=False,
        explanation=(
            "A runner-up can lose the contest for first place "
            "and still qualify for the next round."
        ),
        audit_note=(
            "This is a hypothetical second-place scenario, not a claim about the observed "
            "primary result. Similar headlines retrieved the pair; different success "
            "conditions prevent a claim-equivalence label."
        ),
    )


def write_casebook(path: Path, cases: pd.DataFrame) -> None:
    """Write a concise narrative that keeps every striking case explainable."""

    lines = [
        "# Representation Casebook",
        "",
        "These cases establish mechanisms, not average effects. A divergence claim requires a "
        "plausible witness state for which the represented payouts differ.",
        "The rules are archived observations; the witness scenarios are hypothetical. "
        "The suit case instead illustrates the limits of the written category definition.",
        "",
    ]
    for row in cases.to_dict(orient="records"):
        lines.extend(
            [
                f"## {row['phenomenon']}",
                "",
                f"- Scope: {row['scope']}",
                f"- Mechanism: {row['mechanism']}",
                f"- Plain-language explanation: {row['explanation']}",
                f"- Representation A ({row['a_platform']}): {row['signature_a']}",
                f"- Representation B ({row['b_platform']}): {row['signature_b']}",
                f"- Witness state: {row['witness_state']}",
                f"- Implied settlements: A = {row['payout_a']}; B = {row['payout_b']}",
                f"- Audit boundary: {row['audit_note']}",
                f"- Sources: [A: {row['a_platform']}]({row['a_url']})"
                + (f"; [B: {row['b_platform']}]({row['b_url']})" if row["b_url"] else ""),
                f"- Exact archived rules: {row['a_rule']} || {row['b_rule']}",
                (
                    f"- Retrieval date: {row['retrieval_date']}; "
                    f"coder confidence: {row['coder_confidence']}"
                ),
                "",
            ]
        )
        if row["secondary_witness_state"]:
            lines.extend(
                [
                    f"- Additional witness: {row['secondary_witness_state']}",
                    f"- Additional implied settlements: A = {row['secondary_payout_a']}; "
                    f"B = {row['secondary_payout_b']}",
                    "",
                ]
            )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
