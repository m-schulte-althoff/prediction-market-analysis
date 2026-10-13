"""Acquire and structure mechanism-rich representation cases."""

from __future__ import annotations

import hashlib
import json
import logging
from contextlib import suppress
from pathlib import Path
from typing import Any

import pandas as pd

from src.coherence import ClaimRelation, probability_implication
from src.config import (
    KALSHI_BASE_URL,
    POLYMARKET_GAMMA_URL,
    SampleConfig,
    acquisition_metadata,
    dated_raw_path,
    require_current_acquisition_date,
    validate_snapshot_date,
)
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

# Manual audits of archived operative inputs, refreshed under approved P5.
# Fingerprints also bind questions, boundaries, scenario and settlement evidence.
# Overlap/non-nesting uses three existence witnesses, not an inclusion inference.
CLAIM_AUDITS: dict[str, tuple[str, ClaimRelation, str, str]] = {
    "election-call-vs-inauguration": (
        "ed80a81a468a895b4a4691adef7ca6c4e5fccc1d901821e43b6d1cab3772f567",
        ClaimRelation.OVERLAP_NON_NESTED,
        "determinate_binary",
        "Under the archived binary reading: Rubio called by all three sources but never "
        "inaugurated gives A=0,B=1. All three call another candidate, who is then unable to "
        "take office, and Rubio is inaugurated for the 2029 term gives A=1,B=0. "
        "Rubio called and inaugurated gives A=1,B=1. The inauguration fallback applies "
        "only absent a unanimous call by January 20, 2029. These existence witnesses "
        "establish overlap and both differences, not a marginal probability ordering.",
    ),
    "minerals-agreement-vs-signature": (
        "ed8daafb88abe332d9ec43d4b1510275cafbf5110d69bbafc83b0dab7a1e8cab",
        ClaimRelation.OVERLAP_NON_NESTED,
        "determinate_binary",
        "Both governments announce a rare-earth deal on March 31 but never formally adopt "
        "any mineral deal through April 30: A=1,B=0. No deal by March 31, then an officially "
        "documented rare-earth deal signed on April 15: A=0,B=1. A March 31 rare-earth "
        "announcement followed by an April 15 signature: A=1,B=1. All times fall within "
        "the respective ET windows, with official information and credible reporting in "
        "agreement. Distinct windows, mineral scope and authorities prevent nesting; "
        "these successive contracts are not a synchronized market pair.",
    ),
    "fed-quantization-convention": (
        "0c2a502e434a72bf76328a514317d9ab7bc00276cbf0bd7478337a0fa2dcb245",
        ClaimRelation.NON_EQUIVALENT_UNCLASSIFIED,
        "binary_reading_unvalidated",
        "The 12.5 bp witness proves non-equivalence conditional on literal Kalshi wording. "
        "The September 16 criterion and cancellation-to-no-change clause differ from the "
        "Polymarket upper-bound measurement, rounding and no-statement fallback through "
        "the next meeting. No full-state binary mapping or global inclusion is validated.",
    ),
    "primary-first-vs-advance": (
        "e0d99d66691402e4af6dda7592022c65b4b8a23dae77b43cd4cc30d0ca740937",
        ClaimRelation.NON_EQUIVALENT_UNCLASSIFIED,
        "non_binary_exceptions",
        "Second place without a tie establishes payout divergence. Kalshi pays 1/n in "
        "exact ties, ranks withdrawn/disqualified candidates remaining on the ballot, "
        "and pays NO for cancellation/postponement beyond expiration. Polymarket asks "
        "actual advancement, with a December 31 cutoff and official-results fallback. "
        "The full Kalshi mapping is not binary; no binary subset restriction is imposed.",
    ),
    "leader-announcement-vs-departure": (
        "2cb60221eadc28c2339c8d2d6e8ee1d7923185bbbd4d92c4daf44166fe96328b",
        ClaimRelation.NON_EQUIVALENT_UNCLASSIFIED,
        "non_binary_and_adjudicated_exceptions",
        "Announcement and competing-departure witnesses establish payout divergence. "
        "Kalshi's death-only clause uses the last traded price or committee fair allocation; "
        "it is not a binary mapping over all histories. Polymarket requires first permanent "
        "departure among the fixed leader list, excludes caretaker/temporary status, and "
        "has a December 31 ET fallback. No global binary superset restriction is justified.",
    ),
    "suit-category-boundary": (
        "4adc9d5061b96588dab2d6cdafc8ec5f7ea565739615b1e7537c4a91abb3d623",
        ClaimRelation.INDETERMINATE,
        "adjudicatively_incomplete",
        "Authenticity and May 22-June 30 image/release requirements fix evidence conditions, "
        "not the garment category. For the borderline attire witness, the text alone does "
        "not select a payout; credible-reporting adjudication completes the mapping. "
        "This is a within-contract illustration, not a second market or proof that "
        "an eventual institutional settlement is undefined.",
    ),
    "hilton-first-vs-advance": (
        "f7d08b8952136ae4a31ccf4c0725f6369f90d3b02a07c76f7641d9f608e7cc2f",
        ClaimRelation.NON_EQUIVALENT_UNCLASSIFIED,
        "non_binary_exceptions",
        "Archived first-place and advancement records plus certified second place establish "
        "realized 0/1 payout divergence. The full Kalshi rule also pays 1/n for exact ties, "
        "ranks withdrawn/disqualified candidates left on the ballot, excludes write-in winners "
        "without their own option, and pays NO if cancelled/postponed beyond expiration. "
        "Polymarket uses advancement, a December 31 cutoff and official-results fallback. "
        "No binary subset restriction follows from the realized contrast.",
    ),
    "khamenei-death-allocation": (
        "59572a858384dab769d2f60f4ac0bb6cae6cbd3df2b175dcdf02b026d96df09e",
        ClaimRelation.NON_EQUIVALENT_UNCLASSIFIED,
        "non_binary_and_adjudicated_exceptions",
        "Both archived and follow-up official records establish a normalized 0.45/1 contrast. "
        "Kalshi's ordinary departure/announcement criterion is overridden for death-only "
        "departure by a pre-death last-price allocation, with binding committee discretion "
        "if the price is unavailable, illogical or unfair. Polymarket covers resignation, "
        "detention, loss of position or inability to perform duties through its ET cutoff. "
        "The deadlines differ; the full payout mapping is fractional and adjudicated. "
        "The recorded settlement does not identify reference-price selection or account "
        "reimbursements. No global binary-event restriction is validated.",
    ),
    "suit-adjudication-episode": (
        "5930677751ed486dc7c8bb462c78a2fcf0751ca21ec321b4ba547ac7edcd7492",
        ClaimRelation.INDETERMINATE,
        "adjudicatively_incomplete",
        "The full rule fixes May 22–June 30 ET image-taking/release and authenticity conditions "
        "but supplies no garment-level definition of suit. It delegates to credible-reporting "
        "consensus. The June 24 appearance, repeated proposed/disputed states and final NO "
        "document institutional completion; they do not prove the complete-history payout "
        "function is undefined, independently classify the clothing, or measure ambiguity's "
        "economic effect. This is one contract, so no pairwise probability restriction applies.",
    ),
    "minerals-observed-chronology": (
        "0598420f1dd005161fc488579f3cf9c1cb169dc4ec8bb2cfb64f74a54a96bcd9",
        ClaimRelation.OVERLAP_NON_NESTED,
        "determinate_binary",
        "Full rules match the audited successive minerals witnesses: announcement-only "
        "March 31 agreement can give A=1,B=0; no March agreement and qualifying April signature "
        "can give A=0,B=1; both milestones can give A=1,B=1. Different windows, scopes and "
        "authorities prevent nesting. Observed outcomes are YES/YES; the April 30 signing "
        "and March 25/May 4 closure records are chronology, not a realized payout split "
        "or a synchronized market comparison.",
    ),
}

AUDIT_ASSERTION_FIELDS = (
    "signature_a", "signature_b", "witness_state", "payout_a", "payout_b",
    "secondary_witness_state", "secondary_payout_a", "secondary_payout_b",
    "truth_condition_divergent", "determinacy_issue", "scenario_status", "evidence_kind",
    "event_sources", "settlement_evidence", "chronology", "observed_settlement_a",
    "observed_settlement_b",
)


def case_assertion_fingerprint(row: dict[str, Any]) -> str:
    """Bind judgments to operative fields and scenario/settlement assertion inputs."""

    fields = sorted(
        {key for key in row if str(key).startswith(("a_", "b_"))}
        | set(AUDIT_ASSERTION_FIELDS)
    )
    payload: dict[str, str] = {}
    for key in fields:
        value = row.get(key, "")
        text = "" if value is None or (isinstance(value, float) and pd.isna(value)) else str(value)
        if key in {"observed_settlement_a", "observed_settlement_b"} and text:
            with suppress(ValueError):
                text = format(float(text), ".12g")
        payload[key] = " ".join(text.split())
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode()
    return hashlib.sha256(encoded).hexdigest()


def add_claim_relations(cases: pd.DataFrame) -> pd.DataFrame:
    """Attach manual representation audits only to their verified archived rule versions."""

    records: list[dict[str, object]] = []
    for row in cases.to_dict(orient="records"):
        inputs = {str(key): value for key, value in row.items()}
        fingerprint = case_assertion_fingerprint(inputs)
        audit = CLAIM_AUDITS.get(str(row["case_id"]))
        validated = audit is not None and fingerprint == audit[0]
        if audit is not None and validated:
            _, relation, status, basis = audit
            confidence = (
                "conditional on literal archived wording"
                if row["case_id"] == "fed-quantization-convention"
                else "high within stated archived-rule model; not a probability"
            )
        else:
            relation, status = ClaimRelation.UNCLASSIFIED, "unreviewed"
            basis = (
                "Operative inputs or asserted scenario/settlement evidence differ from the "
                "audited archive; manual review required. Dependent assertions withheld."
            )
            confidence = "unreviewed"
            for key in (
                "signature_a", "signature_b", "witness_state", "payout_a", "payout_b",
                "secondary_witness_state", "secondary_payout_a", "secondary_payout_b",
                "observed_settlement_a", "observed_settlement_b", "explanation", "audit_note",
            ):
                if key in row:
                    row[key] = "Withheld pending review of changed inputs."
            for key in ("truth_condition_divergent", "determinacy_issue"):
                if key in row:
                    row[key] = False
            row["scenario_status"] = "unreviewed; dependent scenario/settlement assertions withheld"
        implication = probability_implication(relation)
        applicable = (
            validated and status == "determinate_binary" and implication.diagnostic_available
        )
        records.append(
            {
                **{str(key): value for key, value in row.items()},
                "claim_relation": relation.value,
                "claim_relation_validated": validated,
                "audit_input_sha256": fingerprint,
                "claim_relation_confidence": confidence,
                "claim_relation_basis": basis,
                "representation_status": status,
                "probability_coherence_implication": implication.probability_restriction,
                "coherence_test_applicable": applicable,
                "coherence_test_reason": (
                    "Semantic gate only; independently validated synchronized prices "
                    "still required."
                    if applicable
                    else f"{status}: {implication.reason} {basis}"
                ),
            }
        )
    return pd.DataFrame.from_records(records)


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
        validate_snapshot_date(payload, config.retrieval_date, "representation-case")
        selection = payload.get("selection")
        expected_selection = {
            "polymarket_event_slugs": list(POLYMARKET_EVENT_SLUGS),
            "kalshi_event_tickers": list(KALSHI_EVENT_TICKERS),
        }
        if selection is not None and selection != expected_selection:
            raise ValueError("Representation-case cache selection differs from requested cases")
        LOGGER.info("Using cached representation-case snapshot: %s", path)
        return payload
    require_current_acquisition_date(path, config.retrieval_date)
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
        **acquisition_metadata(config.retrieval_date),
        "selection": {
            "polymarket_event_slugs": list(POLYMARKET_EVENT_SLUGS),
            "kalshi_event_tickers": list(KALSHI_EVENT_TICKERS),
        },
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
            "operative_inputs": json.dumps({
                key: market.get(key) for key in (
                    "custom_strike", "yes_sub_title", "early_close_condition", "open_time",
                    "close_time", "expiration_time", "series_settlement_sources", "market_type",
                    "notional_value_dollars", "result", "status", "settlement_value_dollars",
                    "settlement_ts",
                ) if key in market
            }, ensure_ascii=False, sort_keys=True),
        }
    slug = str(market.get("slug") or "")
    return {
        "platform": platform,
        "contract_id": str(market.get("id") or slug),
        "question": str(market.get("question") or ""),
        "rule": str(market.get("description") or ""),
        "url": f"https://polymarket.com/event/{slug}",
        "operative_inputs": json.dumps({
            key: market.get(key) for key in (
                "startDate", "endDate", "closedTime", "outcomes", "outcomePrices",
                "resolutionSource", "umaResolutionStatus", "umaResolutionStatuses", "closed",
            ) if key in market
        }, ensure_ascii=False, sort_keys=True),
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
    evidence_kind: str = "hypothetical_rule_witness",
    scenario_status: str = "hypothetical witness; archived rules, not a realized payout audit",
    event_sources: str = "",
    settlement_evidence: str = "",
    chronology: str = "",
    observed_settlement_a: str = "",
    observed_settlement_b: str = "",
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
        "scenario_status": scenario_status,
        "evidence_kind": evidence_kind,
        "event_sources": event_sources,
        "settlement_evidence": settlement_evidence,
        "chronology": chronology,
        "observed_settlement_a": observed_settlement_a,
        "observed_settlement_b": observed_settlement_b,
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
    payload: dict[str, Any], matches: pd.DataFrame | None = None,
    case_evidence: dict[str, Any] | None = None,
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
    if case_evidence is not None:
        observed = _observed_cases(case_evidence, retrieval_date)
        records = [row for row in records if row["case_id"] != "suit-category-boundary"]
        records.extend(observed)
    result = add_claim_relations(pd.DataFrame.from_records(records))
    priorities = {
        "hilton-first-vs-advance": 0, "khamenei-death-allocation": 1,
        "suit-adjudication-episode": 2, "minerals-observed-chronology": 3,
    }
    result["display_order"] = result["case_id"].map(priorities).fillna(4).astype(int)
    return result.sort_values(["display_order", "case_id"], kind="stable", ignore_index=True)


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
            "A runner-up can lose the contest for first place and still qualify for the next round."
        ),
        audit_note=(
            "This is a hypothetical second-place scenario, not a claim about the observed "
            "primary result. Similar headlines retrieved the pair; different success "
            "conditions prevent a claim-equivalence label."
        ),
    )


def load_case_evidence(path: Path) -> dict[str, Any]:
    """Read an explicitly selected versioned bundle and verify preserved source copies."""

    payload = read_json(path)
    if not isinstance(payload, dict) or payload.get("schema_version") != 1:
        raise ValueError("Case evidence requires a schema-version-1 JSON object")
    if not isinstance(payload.get("observed_cases"), dict):
        raise ValueError("Case evidence has no observed_cases mapping")
    for source in payload.get("source_versions", []):
        copy = path.parent / Path(source["preserved_path"]).name
        digest = hashlib.sha256(copy.read_bytes()).hexdigest()
        if digest != source["sha256"]:
            raise ValueError(f"Preserved case source hash differs: {copy}")
    return payload


def _settlement_evidence(platform: str, market: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    """Require recorded final status and aligned outcomes before assigning a settlement."""

    if platform == "Kalshi":
        if market.get("status") != "finalized":
            raise ValueError("Observed Kalshi case is not finalized")
        amount = float(market["settlement_value_dollars"])
        if not 0 <= amount <= 1:
            raise ValueError("Observed Kalshi settlement lies outside normalized payout range")
        result = market.get("result")
        if result not in {"yes", "no", "scalar"}:
            raise ValueError("Observed Kalshi result is unsupported")
        if result in {"yes", "no"} and amount != float(result == "yes"):
            raise ValueError("Kalshi result and settlement value disagree")
        evidence = {key: market.get(key) for key in (
            "ticker", "status", "result", "settlement_value_dollars", "settlement_ts"
        )}
    else:
        if market.get("closed") is not True or market.get("umaResolutionStatus") != "resolved":
            raise ValueError("Observed Polymarket case lacks recorded final resolution")
        outcomes = market.get("outcomes")
        prices = market.get("outcomePrices")
        outcomes = json.loads(outcomes) if isinstance(outcomes, str) else outcomes
        prices = json.loads(prices) if isinstance(prices, str) else prices
        if not isinstance(outcomes, list) or not isinstance(prices, list):
            raise ValueError("Observed Polymarket case requires aligned outcome vectors")
        labels = [str(value).casefold() for value in outcomes]
        if len(labels) != 2 or set(labels) != {"yes", "no"} or len(prices) != 2:
            raise ValueError("Observed Polymarket case requires exactly YES and NO")
        amounts = [float(value) for value in prices]
        if sorted(amounts) != [0.0, 1.0]:
            raise ValueError("Observed Polymarket case is not a final binary outcome vector")
        amount = amounts[labels.index("yes")]
        evidence = {key: market.get(key) for key in (
            "id", "closed", "umaResolutionStatus", "outcomes", "outcomePrices",
            "closedTime", "umaResolutionStatuses"
        )}
    return format(amount, ".12g"), evidence


def _observed_cases(payload: dict[str, Any], retrieval_date: str) -> list[dict[str, object]]:
    """Construct the four named P5 exhibits from exact preserved case records."""

    sources = payload["observed_cases"]
    records: list[dict[str, object]] = []
    for name in ("hilton", "khamenei", "suit", "minerals"):
        source = sources[name]
        platform_a = "Kalshi" if name in {"hilton", "khamenei"} else "Polymarket"
        a = _contract_fields(platform_a, source["a"])
        amount_a, evidence_a = _settlement_evidence(platform_a, source["a"])
        if name == "suit":
            b = {
                "platform": "Adjudication procedure", "contract_id": "not-a-second-contract",
                "question": "How is the garment category interpreted?",
                "rule": "The contract delegates to a consensus of credible reporting.",
                "url": "",
            }
            amount_b, evidence_b = "", dict[str, Any]()
        else:
            b = _contract_fields("Polymarket", source["b"])
            amount_b, evidence_b = _settlement_evidence("Polymarket", source["b"])
        settlement = json.dumps({
            "a": evidence_a, "b": evidence_b,
            "source_check": source["source_check"],
            "checked_at_utc": source.get("checked_at_utc"),
            "original_http_acquisition_time": payload.get("original_http_acquisition_time"),
            "boundary": (
                "Recorded contract outcomes; no token redemption or account cash-flow audit."
            ),
        }, ensure_ascii=False, sort_keys=True)
        common: dict[str, Any] = {
            "contract_a": a, "contract_b": b,
            "retrieval_date": (
                retrieval_date if name in {"hilton", "khamenei"}
                else "unrecorded for follow-up API responses preserved in the October review"
            ),
            "event_sources": json.dumps(
                source["event_sources"], ensure_ascii=False, sort_keys=True
            ),
            "settlement_evidence": settlement,
            "observed_settlement_a": amount_a, "observed_settlement_b": amount_b,
        }
        if name == "hilton":
            record = _case(
                case_id="hilton-first-vs-advance",
                phenomenon="Steve Hilton: first place versus advancing in the California primary",
                scope="cross-platform; archived realized settlement contrast",
                mechanism="rank versus qualification divergence",
                signature_a="first place in the primary; proportional payout for exact ties",
                signature_b="advance to the general election; the top two candidates qualify",
                witness_state=(
                    "Steve Hilton finished second in the June 2, 2026 California primary "
                    "and advanced to the general election. Certified results place Becerra "
                    "first (28.0%), Hilton second (24.6%) and Steyer third (22.8%)."
                ),
                payout_a="NO; recorded normalized settlement $0",
                payout_b="resolved YES; normalized payout $1",
                truth_condition_divergent=True, determinacy_issue=False,
                evidence_kind="observed_settlement_divergence",
                scenario_status="observed event and recorded final settlement contrast",
                chronology=(
                    "June 2, 2026: primary; June 10 20:05:30 UTC: Polymarket closure record; "
                    "July 11 00:39:59.561815 UTC: Kalshi settlement timestamp."
                ),
                explanation="Finishing second loses the first-place contract and wins advancement.",
                audit_note=(
                    "Both records are in the September-labelled sample and match the preserved "
                    "October follow-up on operative fields. They have different cutoff/fallback "
                    "conditions; exact ties make Kalshi's full payout mapping fractional. "
                    "This realized contrast establishes no price error or trader misunderstanding."
                ),
                **common,
            )
        elif name == "khamenei":
            record = _case(
                case_id="khamenei-death-allocation",
                phenomenon="Ali Khamenei departure: price-based death allocation versus YES",
                scope="cross-platform; archived realized fractional settlement contrast",
                mechanism="death-clause payout divergence",
                signature_a=(
                    "departure before July 1, 2026; qualifying announcement also covered; "
                    "death-only departure uses a pre-death price or committee fair allocation"
                ),
                signature_b=(
                    "loss of position or ability to perform duties by June 30, 2026, 11:59 PM ET"
                ),
                witness_state=(
                    "Following the February 28, 2026 attack, contemporaneous March 1 reporting "
                    "recorded Iranian state media confirming Khamenei's death. The compared "
                    "contracts recorded scalar 45-cent and resolved-YES settlements."
                ),
                payout_a="scalar; recorded normalized settlement $0.45",
                payout_b="resolved YES; normalized payout $1",
                truth_condition_divergent=True, determinacy_issue=False,
                evidence_kind="observed_settlement_divergence",
                scenario_status="observed departure episode and recorded final settlement contrast",
                chronology=(
                    "February 28, 2026: attack; March 1: contemporaneous confirmation report; "
                    "March 1 00:02:17 UTC: Polymarket closure record; "
                    "March 1 03:19:27.389859 UTC: Kalshi scalar-settlement timestamp."
                ),
                explanation=(
                    "Forecasting departure is insufficient to value a contract whose death "
                    "clause can pay a fraction of the unit payout."
                ),
                audit_note=(
                    "The deadlines and exceptions differ, so this is not a controlled clause "
                    "effect. Full Kalshi mapping includes announcement, ordinary departure, "
                    "price-based death allocation and binding committee discretion. The exact "
                    "reference-price selection was not audited. Reported reimbursements can "
                    "make account receipts differ from contract settlement; original linked "
                    "social posts were inaccessible. No binary-event restriction applies."
                ),
                **common,
            )
        elif name == "suit":
            record = _case(
                case_id="suit-adjudication-episode",
                phenomenon="Zelenskyy's clothing: appearance, proposals and final adjudication",
                scope="within-contract; documented adjudication episode",
                mechanism="category-boundary interpretation",
                signature_a=(
                    "authentic images/video taken and released May 22–June 30, 2025 ET; "
                    "wearing a suit; no garment-level definition"
                ),
                signature_b="credible-reporting consensus supplies the deciding interpretation",
                witness_state=(
                    "Zelenskyy appeared in the Netherlands on June 24, 2025, documented by "
                    "the Ukrainian presidency and its photograph. The official market record "
                    "preserves repeated proposal/dispute states and a final NO."
                ),
                payout_a="resolved NO; normalized payout $0",
                payout_b="N/A; this is one contract and its adjudication procedure",
                truth_condition_divergent=False, determinacy_issue=True,
                evidence_kind="observed_adjudication",
                scenario_status=(
                    "observed appearance, documented proposal/dispute sequence and final NO"
                ),
                chronology=(
                    "June 24, 2025: photographed appearance; June 30: rule window ends; "
                    "archived status history alternates proposed/disputed five times "
                    "(individual timestamps unavailable); July 9 00:30:39 UTC: closure record "
                    "with current resolved status and NO outcome."
                ),
                explanation=(
                    "The rules fix timing and image authenticity, while the deciding procedure "
                    "supplies the interpretation of the clothing category."
                ),
                audit_note=(
                    "The appearance source does not independently classify the clothing. "
                    "A dispute shows adjudication mattered; it establishes no manipulation, "
                    "trader consensus or causal ambiguity effect. Final institutional payout "
                    "is recorded despite incomplete written garment criteria. Closure is "
                    "not independently verified on-chain finality."
                ),
                **common,
            )
        else:
            record = _case(
                case_id="minerals-observed-chronology",
                phenomenon="U.S.–Ukraine minerals agreement: two YES resolutions across milestones",
                scope="within-platform across successive contracts; observed chronology",
                mechanism="milestone-stage divergence",
                signature_a="rare-earth agreement by March 31; public announcement qualifies",
                signature_b=(
                    "minerals agreement signed or formally adopted by April 30; "
                    "announcement alone fails"
                ),
                witness_state=(
                    "The March agreement contract records YES and March 25 closure. "
                    "The U.S. Treasury and Ukrainian ministry record an April 30, 2025 "
                    "signing; the later signed-deal contract records YES and May 4 closure."
                ),
                payout_a="resolved YES; normalized payout $1",
                payout_b="resolved YES; normalized payout $1",
                truth_condition_divergent=False, determinacy_issue=False,
                evidence_kind="observed_chronology",
                scenario_status=(
                    "observed chronology and two recorded YES outcomes; no realized split"
                ),
                chronology=(
                    "March 25, 2025 00:21:27 UTC: agreement-contract closure record; "
                    "April 30: official signing announcement; "
                    "May 4 01:10:41 UTC: signed-deal-contract closure record."
                ),
                explanation=(
                    "An agreement announcement and a signature are distinct milestones, "
                    "and both successive contracts can ultimately pay YES."
                ),
                audit_note=(
                    "Different windows, rare-earth/mineral scope and evidence authorities "
                    "prevent a controlled milestone comparison. The YES/YES chronology "
                    "does not instantiate the supplementary hypothetical YES/NO witness "
                    "and establishes no manipulation or erroneous March outcome."
                ),
                **common,
            )
        records.append(record)
    return records


def write_casebook(path: Path, cases: pd.DataFrame) -> None:
    """Write a concise narrative that keeps every striking case explainable."""

    cases = add_claim_relations(cases)
    lines = [
        "# Representation Casebook",
        "",
        "The leading exhibits separate recorded settlement contrasts, adjudication and "
        "observed chronology. Supplementary scenarios are explicitly hypothetical. "
        "These cases establish mechanisms and existence, not prevalence or average effects.",
        "A common distribution over scenarios can value different payout claims differently. "
        "The audit supplies no price result; scalar settlements and tie exceptions require "
        "the full payout mapping and cannot enter binary-event restrictions. "
        "See [constructs and source bridge](../docs/CONSTRUCTS.md).",
        "",
    ]
    ordered = cases.sort_values(["display_order", "case_id"], kind="stable") if (
        "display_order" in cases
    ) else cases.sort_values("case_id", kind="stable")
    supplementary_started = False
    for row in ordered.to_dict(orient="records"):
        hypothetical = row.get("evidence_kind", "hypothetical_rule_witness") == (
            "hypothetical_rule_witness"
        )
        if hypothetical and not supplementary_started:
            lines.extend(["## Supplementary hypothetical boundary scenarios", ""])
            supplementary_started = True
        lines.extend([f"### {row['phenomenon']}", ""])
        if str(row.get("claim_relation_validated", "")).casefold() != "true":
            lines.extend([
                "Scenario, implied payout and settlement assertions are withheld pending "
                "review of the changed operative inputs.",
                f"- Audit status: {row['claim_relation_basis']}",
                f"- Contract A: {row['a_contract_id']}; question: {row['a_question']}",
                f"- Contract B: {row['b_contract_id']}; question: {row['b_question']}",
                f"- Exact current input rules: {row['a_rule']} || {row['b_rule']}",
                "",
            ])
            continue
        lines.extend(
            [
                f"- Scope: {row['scope']}",
                f"- Evidence status: {row['scenario_status']}",
                f"- Mechanism: {row['mechanism']}",
                f"- Plain-language explanation: {row['explanation']}",
                f"- {'Hypothetical scenario' if hypothetical else 'Observed scenario'}: "
                f"{row['witness_state']}",
                f"- Qualifying condition A ({row['a_platform']}): {row['signature_a']}",
                f"- Qualifying condition B ({row['b_platform']}): {row['signature_b']}",
                f"- {'Implied payouts' if hypothetical else 'Recorded settlements'}: "
                f"A = {row['payout_a']}; B = {row['payout_b']}",
                f"- Contract identifiers: A = {row['a_contract_id']}; B = {row['b_contract_id']}",
                f"- Audit boundary: {row['audit_note']}",
                f"- Claim relation: {row['claim_relation']}; "
                f"representation: {row['representation_status']}",
                f"- Relation confidence: {row['claim_relation_confidence']}",
                f"- Complete-rule relation audit: {row['claim_relation_basis']}",
                f"- Probability implication: {row['probability_coherence_implication']}; "
                f"coherence test applicable (semantic gate): {row['coherence_test_applicable']}",
                f"- Sources: [A: {row['a_platform']}]({row['a_url']})"
                + (f"; [B: {row['b_platform']}]({row['b_url']})" if row["b_url"] else ""),
                f"- Exact archived rules: {row['a_rule']} || {row['b_rule']}",
                (
                    f"- Snapshot date label: {row['retrieval_date']}; "
                    f"coder confidence: {row['coder_confidence']}"
                ),
                "",
            ]
        )
        if row.get("chronology"):
            lines.extend([f"- Chronology: {row['chronology']}", ""])
        if row.get("event_sources"):
            for source in json.loads(str(row["event_sources"])):
                lines.append(
                    f"- Independent event source: [{source['basis']}]({source['url']}); "
                    f"{source['finding']}"
                )
            lines.append("")
        if row.get("settlement_evidence"):
            lines.extend([f"- Exact settlement evidence: {row['settlement_evidence']}", ""])
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
