# Data Sources

Retrieval date for the included empirical package: **2026-09-10**. All used sources are official, public, and unauthenticated. No third-party dataset enters the reported results.

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
- Fields used: market/condition/event identifiers; question; description; resolution source; opening/end/closure timestamps; outcomes and outcome prices; `volumeNum`; `liquidityNum`; CLOB token IDs; official `sportsMarketType` and `gameStartTime` flags.
- Selection: scan the descending-volume archive, exclude sports using official flags plus a conservative documented text taxonomy, and only then retain the first 8,000 non-sports rows. The included snapshot scanned 23,700 raw rows; binary `Yes`/`No` validation yields 7,249 usable contracts.
- Observed coverage: 7,249 usable non-sports binary contracts opened from 2020-10-09 onward; latest observed resolution 2026-09-10.
- Limitations: archived category/tag labels are absent for almost all rows, so analysis categories use a fixed question/rule keyword taxonomy. Sports detection is transparent but imperfect. `lastTradePrice` is not consistently YES-oriented for legacy AMM records and is deliberately excluded from forecast-error analysis. Sampling on volume makes the Polymarket portion unsuitable for population volume estimates.

### Audited representation cases

- Polymarket endpoint: `GET https://gamma-api.polymarket.com/events?slug=...` for the 2028 presidential winner, September 2026 Fed decision, two Ukraine-minerals markets, and Zelenskyy-suit market.
- Kalshi endpoint: `GET https://external-api.kalshi.com/trade-api/v2/events/{event_ticker}` for `KXPRESPERSON-28` and `KXFEDDECISION-26SEP`.
- Fields archived: event and contract identifiers, questions, complete rule descriptions, statuses, and timestamps returned by the official endpoints.
- Purpose: mechanism evidence only. A manually coded truth-condition divergence requires a plausible witness state and different implied settlements; these cases do not estimate population prevalence or average price effects.

### CLOB price history

- Documentation: <https://docs.polymarket.com/api-reference/markets/get-prices-history>
- Endpoint: `GET https://clob.polymarket.com/prices-history?market={yes_token_id}&interval=max`.
- Fields used: Unix timestamp `t` and YES-token price `p`.
- Limitation: explicit long start/end windows were rejected by the live API, so the supported compressed full-history mode is used. Only 3 of 11 accepted cross-platform pairs returned histories on both platforms. This sparse coverage is reported as a limitation, not silently dropped.

## Reproducibility and immutability

The September 14 representation-aware extension uses the same empirical archives. Relation audits cover the full returned descriptions and are bound to contract-ID/rule fingerprints; additional hypothetical states establish overlap/non-nesting for election and minerals cases. The primary and leader clauses expose fractional exceptions. These audits add neither realized settlement data nor observed trader beliefs.

The legacy panel resamples daily and forward-fills for up to seven days; it does not preserve original observation timestamps or verify trade freshness. The currently eligible subset has two pairs with nine daily rows each. `coherence-panel-readiness.csv` therefore marks both as insufficient evidence. Any future `data/processed/coherence-price-observations.csv` must separately document fresh synchronized, YES-oriented normalized observations and comparable conditions; no such observations are supplied in the current package.

Raw responses are saved as date-stamped UTF-8 JSON under `data/raw/`; matched histories are additionally content-addressed by the selected match IDs and acquisition mode. Existing raw snapshots are loaded rather than overwritten. `data/` is Git-ignored because API responses can be large and are reproducible from the public sources. Derived CSV files are deterministically sorted before writing.
