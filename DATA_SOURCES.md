# Data Sources

Legacy snapshot date label for the included metadata package: **2026-09-10**. Original HTTP acquisition timestamps are unavailable. Three Polymarket source updates fall on September 11; this date inconsistency is unresolved. Metadata and price archives use official public unauthenticated APIs. Named cases additionally use certified election results and independent event reporting preserved during review.

## Kalshi

### Series catalog

- Documentation: <https://docs.kalshi.com/api-reference/market/get-series-list>
- Endpoint: `GET https://external-api.kalshi.com/trade-api/v2/series?include_volume=true`
- Fields used: `ticker`, `title`, `category`, `volume_fp`, `settlement_sources` (`name`, `url`).
- Selection: the 120 highest-total-volume series in the pre-specified AI, Business, Companies, Economics, Elections, Health, Politics, Science and Technology, Social, Transportation, and World categories.
- Limitation: selection is purposive and conditions market-level coverage on series popularity. Recurring weather, asset-price, sports, entertainment, and mention-count series are excluded to avoid domination by near-identical templates.

### Live and historical market metadata

- Live documentation: <https://docs.kalshi.com/api-reference/market/get-markets>
- Historical documentation: <https://docs.kalshi.com/api-reference/historical/get-historical-markets>
- Endpoints: `GET /markets?series_ticker=...` and `GET /historical/markets?series_ticker=...`.
- Fields used: contract/event identifiers; title; primary/secondary rules; early-close condition; creation/open/close/settlement timestamps; result; volume; liquidity; open interest; last traded YES price; status.
- Observed coverage: 12,251 usable contracts opened from 2021-06-30 onward; latest observed resolution 2026-09-10. The combined raw response contains 12,253 rows before minimal question validation/deduplication.
- Limitation: each selected series is capped at 1,000 records per live/archive tier. Historical metadata reflect the platform's state at retrieval and may contain retrospective rule corrections.

### Historical partition cutoff

- Documentation: <https://docs.kalshi.com/api-reference/historical/get-historical-cutoff-timestamps>
- Endpoint: `GET /historical/cutoff`.
- Field used: `market_settled_ts` to route candlestick requests.
- Observed cutoff: 2026-07-12T00:00:00Z.

### Market candlesticks

- Live documentation: <https://docs.kalshi.com/api-reference/market/get-market-candlesticks>
- Historical documentation: <https://docs.kalshi.com/api-reference/historical/get-historical-market-candlesticks>
- Endpoints: live series/market candlesticks or historical market candlesticks, selected from the cutoff.
- Fields used: `end_period_ts`, trade `price.close_dollars`, YES bid/ask `close_dollars`, and `volume_fp` at daily resolution. When a daily trade close is absent, the contemporaneous YES bid–ask midpoint is used.
- Limitation: empty/no-trade candles and API archival coverage reduce usable overlap. Candlesticks were requested only for accepted pairs.

## Polymarket

### Gamma market metadata

- Documentation: <https://docs.polymarket.com/api-reference/markets/list-markets-keyset-pagination>
- Endpoint: `GET https://gamma-api.polymarket.com/markets/keyset`.
- Query: `closed=true`, ordered by `volumeNum` descending, with opaque cursor pagination.
- Fields used: market/condition/event identifiers; question; description; resolution source; opening/end/closure timestamps; outcomes and outcome prices; `volumeNum`; `liquidityNum`; CLOB token IDs; official `sportsMarketType`, `gameStartTime`, and available category/tag fields.
- Selection: historically scan the descending-volume archive and retain 8,000 rows after a flawed sports filter. That filter wrongly used `gameStartTime` alone, excluding identifiable non-sports minerals (521607) and suit (546814) records. The wrapper reports 23,700 scanned rows, but the rejected/overflow ledger is absent. The 15,700 arithmetic difference is not an established sports count. Exactly two supported `Yes`/`No` outcomes yield 7,249 rows. The corrected substantive classifier is used for future acquisition and preserves the current retained IDs; alternate snapshots are not silently unioned into the primary sample.
- Observed coverage: 7,249 usable supported-binary-label contracts from the historically filtered portfolio opened from 2020-10-09 onward; latest observed resolution 2026-09-10.
- Limitations: archived category/tag labels are absent for almost all rows, so analysis categories use a fixed question/rule keyword taxonomy. Sports detection is transparent but imperfect. `lastTradePrice` is not consistently YES-oriented for legacy AMM records and is deliberately excluded from forecast-error analysis. Sampling on volume makes the Polymarket portion unsuitable for population volume estimates.

### Audited representation cases

- Polymarket endpoint: `GET https://gamma-api.polymarket.com/events?slug=...` for the 2028 presidential winner, September 2026 Fed decision, two Ukraine-minerals markets, and Zelenskyy-suit market.
- Kalshi endpoint: `GET https://external-api.kalshi.com/trade-api/v2/events/{event_ticker}` for `KXPRESPERSON-28` and `KXFEDDECISION-26SEP`.
- Fields archived: event and contract identifiers, questions, rule descriptions, statuses, and timestamps returned by the official endpoints. These are complete returned fields, not a reconstruction of all historical governing specifications or updates.
- Purpose: documentary case evidence. A manually coded payoff divergence requires a specified witness scenario and different implied settlements within the audited source scope; these cases do not estimate population prevalence or average price effects.

### CLOB price history

- Documentation: <https://docs.polymarket.com/api-reference/markets/get-prices-history>
- Endpoint: `GET https://clob.polymarket.com/prices-history?market={yes_token_id}&interval=max`.
- Fields used: Unix timestamp `t` and YES-token price `p`.
- Limitation: explicit long start/end windows were rejected by the live API, so the supported compressed full-history mode is used. Only 3 of 11 accepted cross-platform pairs returned histories on both platforms. This sparse coverage is reported as a limitation, not silently dropped.

## Approved revision: evidence and provenance

The metadata normalization ledger reconciles 12,253 Kalshi rows to 12,251 (two missing titles) and 8,000 Polymarket rows to 7,249 (751 unsupported outcome-label rows). Acquisition exclusions and normalization attrition are distinct. The full rejected scan and tier overflow records cannot be reconstructed.

Outcome fields distinguish evidence. Kalshi has recorded YES/NO outcomes and six scalar settlements. Polymarket endpoint prices remain price-inferred labels: 15 have `proposed` status, 38 lack status, and two have `settled` status. Only supported endpoints with `resolved`/`settled` status enter the qualified binary outcome field; 53 nonfinal/missing-status endpoints remain in `price_inferred_outcome`. Ten intermediate-price cases remain separate. A final-status endpoint vector does not substitute for a recorded payout field, token-redemption audit or account receipts. YES-token IDs follow exact supported outcome ordering; malformed vectors are explicit missing evidence.

Exposure is metadata elapsed time to the minimum of close, resolution and snapshot-label midnight, with clipping reported rather than concealed. The audit records 65 negative pre-clipping Kalshi intervals: 38 scheduled future openings with zero volume and 27 same-day openings with positive volume. All 52 Polymarket close-before-open intervals have positive volume. An end-of-day convention would change 1,115 Kalshi and three Polymarket exposures; the retained convention remains an explicitly labelled proxy. No evidence establishes that all archived rule versions preceded trading.

### Versioned real cases

The approved [2026-10-15-01 source bundle](output/paper-revision/2026-10-15-01/case-evidence/case-source-bundle.json) preserves the bounded observed-case inputs and source roles, including the newly verified suit records. It retains the older source files byte-for-byte. Original September-labelled records and separately acquired October checks remain distinct; no missing HTTP timestamp is invented.

- **Hilton:** Kalshi `KXCAGOVPRIMARY1ST-26JUN02-1ST-SHIL` and Gamma `825460` record NO/$0 versus resolved YES. Supplied API question/rule fields match restored metadata and dated follow-up records; exhaustive historical governing-specification coverage is unverified. The [certified California result](https://elections.cdn.sos.ca.gov/sov/2026-primary/sov/06-sov-summary.pdf) records second place and top-two advancement. No redemption transaction or pre-trading rule-version audit was performed.
- **Khamenei:** Kalshi `KXKHAMENEIOUT-AKHA-26JUL01` records scalar settlement `0.4500`; Gamma `661699` records resolved YES. Supplied API operative fields match archived/current versions. Different deadlines and the Kalshi price-based death allocation prevent a controlled clause-effect interpretation. [AP death reporting](https://apnews.com/article/5b13b69b708c4ed38e8f95f5fb41a597) and [contemporaneous reporting on the carve-out/reimbursements](https://cointelegraph.com/news/kalshi-founder-khamenei-market-carveout) are independent episode sources. Original linked social posts were inaccessible. Reference-price selection and individual account receipts are unverified; reimbursements can affect cash returns independently of contract settlement.
- **Suit:** Gamma `546814` and the preserved market-page sequence show proposals, disputes and final NO. A [dated Ukrainian presidency account](https://www.president.gov.ua/en/news/vidbulasya-audiyenciya-prezidenta-ukrayini-v-korolya-niderla-98637) records the June 24, 2025 appearance. A bounded public Polygon read now verifies the question/condition linkage, stored creator updates and current condition payout `[0,1]` (NO). The May 29 update acknowledges a dispute before the June 24 photograph; the July 1 update says the named credible-reporting consensus has not confirmed a suit. This is a single-contract exhibit. The audit does not independently classify the clothing or attribute individual challenges to that photograph.
- **Minerals:** Gamma `521607` and `532897` ultimately record YES/YES, with March 25 and May 4 closure fields around the [April 30 signing announcement](https://home.treasury.gov/news/press-releases/sb0126). Closure is a lifecycle record, not a complete settlement timestamp. The distinct announcement-versus-signature YES/NO scenario remains hypothetical; the observed chronology does not instantiate it.

Case assertions and relation labels are bound to all supplied input fields, including questions, source fields, rules, windows, exceptions and explicitly linked new evidence. Mutation fails closed pending re-audit; hash agreement does not certify exhaustive governing coverage. Raw Kalshi series metadata retain `contract_url` and `terms_url`; the unresolved gap is the contents and historical applicability of those linked specifications. Current PDFs contain additional death, accelerated-call and announcement provisions and are not silently substituted for historical versions. The presidential death/interruption witness is withheld. Minerals' binary label is conditional on its archived question-rule model, with platform fallbacks uncertified. Single-contract suit evidence has no pairwise relation. Fractional payout mappings cannot enter binary-event coherence restrictions.

### Named rule deadlines versus metadata timestamps

The explicit deadlines use Eastern Time. `America/New_York` is on daylight-saving time (UTC−04:00) on all three dates. The UTC conversions below were checked with Python's `zoneinfo`; the difference is the operative deadline minus Gamma `endDate`. These meanings are retained separately. No bulk deadline parser, metadata replacement or new price-window analysis was added.

| Gamma market | Metadata `endDate` (UTC) | Written-rule deadline (ET) | Rule deadline (UTC) | Difference |
|---|---|---|---|---|
| 661699, Khamenei | 2026-06-30 00:00 | 2026-06-30 23:59 EDT | 2026-07-01 03:59 | 27h59m |
| 521607, March minerals | 2025-03-31 12:00 | 2025-03-31 23:59 EDT | 2025-04-01 03:59 | 15h59m |
| 532897, April minerals | 2025-04-30 12:00 | 2025-04-30 23:59 EDT | 2025-05-01 03:59 | 15h59m |

### Bounded suit protocol evidence

The [P2 acquisition record](output/paper-revision/2026-10-15-01/P2_OUTCOME.md) preserves raw responses, decoded fields, hashes, the exact adapter/request identifiers and access failures. At Polygon block 95,596,076 (`0x9751daf09ba364fc77858fc7921c00198e38523d2f3c2c3f66ee5057d4b94b4a`, 2026-10-15 21:24:02 UTC), the recorded adapter's question and CTF condition link uniquely and the payout numerators are `[0,1]`. The creator's two stored updates carry May 29 and July 1 timestamps. The adapter's stored July 5 request time is the current remaining request, not an initialization timestamp or a complete history of rounds.

A historical `eth_getLogs` query returned HTTP 403, triggering the approved stop rule. No final-resolution transaction/log index or full proposal/reset chronology was recovered. Current protocol state corroborates NO without proving the exact historical finality time, individual dispute reasons or holder receipts. The attempt used $0, five supporting documents and 23 RPC calls for one question; no wallet or price data were added.

### Dormant panel

The explicitly retained version is `matched-price-histories-2026-09-10-bad72f8883-interval-max.json`. The alternate `627b27c83f-interval-max` version has a third pair that remains candidate-eligible; prior three-to-two differences are version differences, not current eligibility attrition. Current selected-ID cache `03e62f0936` is absent and must not trigger a fresh historical download.

Original intraday observations are clipped to the supported aligned window before aggregation. Daily bucket as-of times, source timestamps and fill ages are preserved, and all rows remain ineligible for synchronized-price tests. The old panel included August 19 rows beyond its August 18 cutoff and after-midnight source observations on the cutoff day. The corrected output no longer includes out-of-window sources. Candidate predicate/window checks and cutoff routing are documented in the approved cycle's audit outputs.

### Immutable caches and safe regeneration

Raw JSON snapshots are never rewritten. New current-date acquisitions record actual UTC `acquired_at_utc` plus requested date and selection metadata. Reuse validates recorded parameters, including the Kalshi per-tier cap. Compatible legacy caches remain readable without invented fields. A missing historical/future-date cache fails before any network call, for metadata, anecdotes and histories alike. An explicit absent history archive also fails clearly. Derived CSV files are deterministically sorted.

The approved old manuscripts, tables, figures, memory and source code are copied under `output/paper-revision/2026-10-12-01/pre-revision/`; `IMPLEMENTATION_BASELINE.json` records SHA-256 hashes. `analyze` updates generated summaries but preserves `output/research-log.md`. Original alternate source archives and unsuccessful analyses remain available. Literature access levels and the missing original Bayesian PDF are documented separately in the preserved theory review and updated source audit.
