# Independent data audit — restored-data follow-up

Updated **2026-10-13**, cycle `2026-10-12-01`, baseline `d9b73ce415a65581938549bb5d9f4193d6675f8a`, branch `main`. This replaces the current cycle's audit; its previous version remains in `before-data-followup-2026-10-13/DATA_AUDIT_REVIEW.md`. D1–D8 retain their identities; D9 is new. No code, original data, manuscript, research memory, or canonical analytical output was changed.

## Assessment

**Source-level reproduction now succeeds.** The exact configured raw snapshots reproduce all 19,500 contracts and 38 columns, the central coverage/profile/bin tables, all 36,753 candidate rows and 34 columns, all six case rows, and the stored 18-row price panel and two summaries. Equality includes documented CSV whitespace serialization and numerical tolerance; it is not a claim of independently validated source truth.

Restoration resolves the missing-input and unexplained normalization-loss portions of D1. It also establishes actual defects previously demonstrated only synthetically: quotation formatting changes the platform composite ordering; the sports classifier rejects plainly non-sports markets; price-coded outcomes include proposed or undocumented resolution states; some exposure intervals are invalid; and the stored price panel uses post-close and forward-filled observations. The six case fingerprints and raw-to-case reproduction pass. None of these checks establishes an observed cross-platform settlement split or an estimable price-coherence effect.

The most consequential new selection finding is **D9**: `gameStartTime` is populated for non-sports contracts, including two mechanism-case contracts, yet the classifier treats it as sufficient proof of sports. The full 23,700-row scan was never preserved. **23,700 − 8,000 = 15,700 is not an observed sports-exclusion count.**

## Scope, versions, and audit artifacts

Read `INSTRUCTIONS.md`, `DATA_FOLLOWUP_PACKET.md`, the assigned reviewer instructions, and only this role's prior report. Inspected acquisition, preprocessing, semantic scoring, matching, panel, analysis, case and serialization code, applicable documentation and primary tables. No other reviewer report, revision plan, or voice profile was read. Applied the paper-revision review boundary and Ponytail guidance. No downloads, API calls, `main.py` stages, branch changes, commits, model searches, or manuscript edits were performed.

All follow-up scratch evidence is under `output/paper-revision/2026-10-12-01/scratch-data-audit-followup/`:

- `audit_restored.py`, `audit-results.json`: snapshot inventory/hashes, row lineage, descriptives, family construction, missingness, settlement cross-tabs, timing, alternate-snapshot overlap, history versions and theoretical-text provenance.
- `normalization-ledger.csv`: all 20,253 configured raw market records with retained/excluded reasons and stable IDs.
- `matching_case_checks.py`, `matching-case-results.json`: complete candidate, case, panel and panel-summary reproduction, with assert-based reconciliation.
- `measurement_checks.py`, `parser-prevalence.json`: isolated quotation, percentage and `tie` checks with exact input/term definitions.
- `alternate-poly-exclusions.csv`, `kalshi-settlement-records.csv`, `polymarket-settlement-records.csv`, platform timing-exception CSVs, `terminal-attrition.json`, and rebuilt tables/panels provide row-level evidence.

The configured inputs for `--retrieval-date 2026-09-10` and defaults are:

| File under `data/raw/` | Role and records | SHA-256 |
|---|---|---|
| `kalshi-markets-s120-2026-09-10.json` | Exact configured input; 12,253 markets, 120 selected series | `5bf5b537d3d1ef627f0b4ba6bc5ddc0ed73f63d651fa9f4b6bc98d01d975d062` |
| `polymarket-nonsports-markets-v2-n8000-2026-09-10.json` | Exact configured input; 8,000 markets; metadata says 23,700 scanned | Full digest in `audit-results.json:inventory` |
| `kalshi-markets-2026-09-10.json` | Older filename, byte-identical to configured Kalshi file | Same digest as above |
| `polymarket-markets-2026-09-10.json` | Alternate 100-row sample, despite selection metadata `limit=8000` | Recorded in inventory; not a replacement input |
| `polymarket-markets-n8000-2026-09-10.json` | Alternate 8,000-row volume sample before current sports filtering | Recorded in inventory; not the 23,700-row scan |

All archives label retrieval date 2026-09-10. None supplies verified HTTP acquisition timestamps or the complete catalog/page-response ledger. Source timestamps show a material date inconsistency in the configured Polymarket archive (D2). Filesystem restoration times do not establish acquisition times.

`data/processed/bayes-source-text.txt` is now present: **158,895 bytes**, SHA-256 `287566a90aba44b960c3bc3a8e202703eb495007282c7fa36bb17ca867402e31`; markers `PDF PAGE 1` through `PDF PAGE 43` are sequential. Its title/authors and “Forthcoming in The Philosophical Review” heading agree with the version described in `docs/BAYES_SOURCE_AUDIT.md`. `input/` and the cited original PDF remain absent, and no extraction manifest or source-PDF checksum was found. Text availability is resolved; exact PDF/extraction provenance remains unverified. This is a provenance check, not a new theory review. Hashes use original bytes, not newline-normalized text.

## Source-to-sample lineage and attrition

| Stage / unit | Reconciled counts | Explanation and limits |
|---|---:|---|
| Kalshi catalog selection | 120 archived selected series | Selected rows obey the documented category list and descending-volume order; full eligible catalog absent, so top-120 completeness unverified |
| Kalshi stored markets → normalized | 12,253 → 12,251 | Exactly two null titles: `KXLLM1-26AUG31-MOON`, `KXLLM1-26OCT31-MOON`; zero stored duplicate IDs |
| Polymarket scan → saved selection | Reported 23,700 → observed 8,000 unique rows | Rejected scan rows and last-page overflow not stored; 15,700 combines unrecovered selection components |
| Polymarket saved → normalized | 8,000 → 7,249 | Exactly 751 non-Yes/No outcome vectors; 709 are `[Up, Down]`; all 751 have two outcomes. No sports recheck, duplicate or short-question losses |
| Combined → volume analysis | 19,500 → 19,500 | Every normalized row has nonnegative volume and a score |
| Outcome-coded subset | 19,500 → 18,312 | 11,073 Kalshi official yes/no results + 7,239 Polymarket price-derived outcomes; status caveats in D6 |
| Resolution-time subset | 19,500 → 18,328 | All 7,249 Polymarket and 11,079 Kalshi rows; 1,172 missing Kalshi settlement times. Six Kalshi scalar results + ten uncoded Polymarket price outcomes explain the 16-row excess over the outcome subset |
| Family aggregation | 19,500 → 2,754 | 120 Kalshi series + 2,634 Polymarket events; no contract-ID fallback and no multiple embedded-event membership |
| Internally varying families | 7,491 contracts / 193 families | Kalshi 6,443 / 48; Polymarket 1,048 / 145 |
| Kalshi terminal-error sample | 12,251 → 11,681 → 11,338 → 10,400 | Sequentially require positive volume, price in [.01,.99], and binary outcome; series requirement loses zero additional rows |
| Candidate retrieval | 12,251 × 3 = 36,753 | Exactly 11 high-confidence, 368 probable, 36,374 rejected; complete regeneration agrees |
| Current accepted pair set | 11 pairs | All IDs unique on both sides; all join to contracts; five obvious phenomenon groupings, not 11 independent events |
| Older `627b27c83f-interval-max` histories | 11 archived pairs → 3 with both histories → 30 rebuilt daily rows | Collins, Donalds, Fishback; ten rows each |
| Stored panel's `bad72f8883-interval-max` histories | 12 archived pairs → 2 with both histories → 18 daily rows | Collins and Fishback; nine rows each; exactly reproduces stored panel |
| Representation case construction | Six cases → six matching exported rows | Full raw-to-case equality and current fingerprints pass |
| Price-coherence estimates | Zero | Separate validated observation file remains absent; non-estimable status remains appropriate |

The three-to-two history change is a **cache/selection-version change**, not removal of Donalds by current match eligibility: `match:KXGOVFLNOMR-26-BD:704474` remains high-confidence. The current accepted set hashes to `03e62f0936`; its expected raw history filename is absent. Old “3 of 11” coverage and current “2 of 12 cached selections / 18 rows” describe different versions and must be labeled accordingly.

## Descriptive reconciliation and joins

The following now reproduce from configured raw records, rather than merely agreeing across published aggregates:

| Statistic | Kalshi | Polymarket |
|---|---:|---:|
| Contracts | 12,251 | 7,249 |
| Mean composite | .6236197861 | .6101274659 |
| No-threshold / threshold counts | 2,191 / 10,060 | 5,534 / 1,715 |
| No-threshold / threshold score means | .5483304427 / .6400172962 | .5747444886 / .7243020408 |
| Families | 120 | 2,634 |
| Top-five family contract share | .4617582238 | .0255207615 |
| Between-family score variance share | .9575461403 | .9912911378 |
| Native-unit volume total | 4,472,151,114.36 | 29,464,980,788.63854 |
| Median volume | 7,898.25 | 1,036,617.204053 |

All columns in two coverage rows, six profile rows and nine determinacy-bin rows agree at `1e-10` numerical tolerance. Every component mean and weighted stratum/bin identity agrees. Raw-to-contract comparison agrees for all 38 columns after applying `io_utils.write_csv`'s per-line trailing-whitespace normalization; 1,742 raw rule strings differ only by this documented serialization. Numeric contract and full candidate comparisons use `1e-12` tolerances. No material content discrepancy is hidden by this comparison.

Family joins have no missing keys, fallback IDs or row multiplication. All 8,000 saved Polymarket records contain exactly one embedded event. Kalshi has 1,364 distinct platform events but uses the broader 120 series as analysis families. For example, `KXAAAGASD` contains 2,000 contracts; the top-five Kalshi families cover 46.18% of the sample. Polymarket's largest family, event `114242`, contains 57 “US strikes Iran by...?” contracts; Eurovision 2025/2026 and a Dutch-coalition event are other large families. These are substantively recognizable groupings, but series and events are different aggregation units. A pair's `underlying_event_id` identifies two contracts, not an independent common event.

All 36,753 candidate pairs are unique; every Kalshi contract has three candidates; 938 distinct Polymarket contracts are used. Candidate text, IDs, numeric diagnostics, labels, rankings and metadata reproduce. This verifies implementation/lineage, not match equivalence or recall.

Missingness is now measured: neither platform has missing question, rule, opening, closing, volume or final exposure values. Kalshi has no missing source-name strings; Polymarket has **6,150/7,249** missing `resolution_source` strings, 6,878 missing liquidity values and 353 missing open-interest values. Polymarket terminal prices are deliberately missing in all 7,249 rows. The score's source-field bonus thus compares differently populated API fields: Kalshi series authority names versus Polymarket market/event source strings. Source-field absence is not independently established absence of an authority in the operative rules.

## Findings and minimal corrections

### D1 — Restored sample reproduces; original selection ledger remains incomplete

**Major; changed / partially resolved, open; observed.** Exact locations: `src/kalshi.py:select_series,_series_markets,download_kalshi`; `src/polymarket.py:download_polymarket`; `src/preprocessing.py:_finalize`; configured files above; `DATA_SOURCES.md` selection/reproduction sections.

**Resolved:** source files exist; all 19,500 analysis rows, normalization losses, family counts and major outputs reconcile. The previous statement that source-level reproduction was unavailable is superseded.

**Open:** Kalshi stores only the selected catalog, merges live/archive variants before saving, and preserves neither tier identity nor page cursors. The 2,000 rows in `KXAAAGASD` are consistent with both 1,000-row tier caps binding under current downloader logic, but additional unseen markets cannot be counted. Polymarket preserves selected rows and `raw_rows_scanned`, not rejected rows or final-page overflow. Its alternative 8,000-row archive overlaps the current sample in exactly 2,985 IDs; its other 5,015 rows are all flagged by the current classifier. That recovers partial **classifier evidence**, not the full historical scan or a certified exact subset of its rejected row occurrences. The older 100-row file overlaps in 45 retained and 55 flagged rows.

Under current code **and the additional assumption** that the original scan used the current 100-row page size, overflow is 0–99 and classifier-rejected row occurrences would be 15,601–15,700. Page size is not stored in snapshot selection metadata; these are conditional bounds, not reconstructed counts. Moreover, “classifier-rejected” cannot be equated with true sports (D9).

**Smallest correction:** retain these original inputs and hashes, export the recovered row/reason ledger, distinguish supported Yes/No filtering from nonbinary filtering, and document irrecoverable acquisition stages. Future snapshots should preserve actual acquisition time, page/overflow counts and rejected IDs/reasons, and version all selection parameters. Do not claim a corrected historical top-8,000 sample from the partial older archive. If selection is later changed, version the resulting sample separately.

### D2 — Retrieval label conflicts with observed source-update dates

**Major; changed / open; observed code defect and actual archive inconsistency; actual HTTP time unverified.** Locations: downloader `retrieved_at_date` assignments in `src/{kalshi,polymarket,anecdotes,panel}.py`; `main.py:run_preprocess`; configured Polymarket records `4339036`, `4339037`, `4339038`; `audit-results.json:source_dates`.

The date argument still labels newly downloaded responses without recording a clock timestamp, and a missing historical cache still triggers acquisition. Prior fake-client proof remains applicable to unchanged code. The restored archive now supplies an actual inconsistency: three retained LAPTOP-FDV markets have `updatedAt=2026-09-11T01:57:35.284473Z`, although the wrapper says 2026-09-10. Their closure times are September 10 at 22:01:09, 22:01:10 and 23:27:24 UTC. These values are incompatible with treating the wrapper as a verified September 10 UTC acquisition cutoff, assuming source timestamp semantics are truthful. They do not establish deliberate misdating, the precise HTTP retrieval time, or that every row was fetched on September 11.

**Smallest correction:** separate requested snapshot label from actual retrieval timestamp; historical cache misses must fail rather than silently acquire fresh rows under an old label. Preserve original source timestamps and state the present uncertainty. A new response must receive a new version. Exposure sensitivities should not pretend that an unverified date label is a precise bound.

### D3 — Formatting artifacts materially affect observed composite profiles

**Major; changed / open; observed in the restored sample.** Locations: `src/semantics.py:DEFINITION_TERMS,QUANTITATIVE_THRESHOLD_PATTERN,EDGE_TERMS,_contains_count,semantic_features`; `analysis-platform-profiles.csv`; `measurement_checks.py` and `parser-prevalence.json`.

The inputs are exactly **question + rules + resolution_source**, with empty strings preserved. Isolated removal of straight/curly quotation characters while preserving the existing definition-phrase inventory changes **1,846 Polymarket scores and zero Kalshi scores**. Mean Polymarket composite rises from .6101274659 to **.6278518416**, exceeding Kalshi's unchanged .6236197861. The prior report's unknown ranking sensitivity is therefore resolved: even this narrow formatting diagnostic reverses the aggregate ordering. This is not a fully validated replacement measure or an inference about every component/stratum/model.

A separate percent-symbol equivalence diagnostic finds **11 Kalshi and 79 Polymarket** records whose threshold flag becomes true after `%` is expressed as `percent`. A focused false-`tie` check finds **120 Kalshi and 428 Polymarket** records containing the substring without whole-token `tie`, `ties` or `tied`; removing that false hit changes edge-completeness in **111 and 294** records after the cap. These are actual sample effects, not extrapolations from the prior synthetic examples.

The quotation diagnostic does **not** add a new bare `resolve to yes if` phrase. A repair that recognizes `resolve(s) to YES if` without the existing `will resolve` requirement also broadens grammar and may correctly affect additional rows; it must not be described as the same isolated punctuation test. The earlier broad singular-only substring count is not used: genuine `ties`/`tied` occurrences are retained.

**Smallest correction:** define the bounded parser repair and test quote equivalence, numeric-percent equivalence and unrelated-substring controls; recompute the same archived sample's existing outputs once. Update the profile interpretation because the raw ranking is demonstrably parser-sensitive. Empirical refits and combined-repair sensitivity are assigned to the empirical reviewer; this audit does not choose a repair by significance.

### D4 — Current panel contains post-close observations; historical coverage mixes cache versions

**Minor for the current no-price-effect manuscript; major prerequisite for reuse. Changed / open; observed.** Locations: `src/panel.py:download_matched_histories,build_matched_panel,summarize_matched_panel`; `main.py:run_analysis`; both interval-max archives; `data/processed/panel-{daily,matched-summary}.csv`; `DATA_SOURCES.md` historical coverage.

The exact stored panel comes from `bad72f8883-interval-max`, with 12 archived selections, two usable pairs and 18 rows. The other cache has 11 selections, three usable pairs and 30 rows. Donalds was omitted from the stored panel's archive selection, not rejected by the current matching table. The current selected-set cache `matched-price-histories-2026-09-10-03e62f0936-interval-max.json` does not exist. Running the acquisition stage would consequently seek a new cache, whereas replaying the stored artifacts succeeds.

For both stored pairs the aligned end is **2026-08-18 00:00 UTC**, yet daily rows span August 11–19. Each August 19 row has `days_to_close=-1`; both are included in all-time disagreement summaries. The August 18 rows also contain Polymarket observations after the aligned cutoff even though their daily labels equal the cutoff. All **18** Polymarket row labels precede the intraday observations they summarize. Four Kalshi values are forward-filled (August 18 and 19 in each pair); the final row's underlying candle time is August 17 at 04:00 UTC, **44 hours earlier**. Kalshi's seven directly observed daily rows per pair are likewise labeled at midnight before their 04:00 observation timestamps. A date-label clip alone would therefore leave invalid as-of data.

**Staleness distinction:** the older `627b27c83f` cache contains divergence/confidence values that differ from the current matcher. The two retained rows' metadata in the actual stored-panel cache agrees with current values. The previous suspicion of stale metadata in the current retained panel is not observed; original observation freshness and broad cache-key weakness remain real concerns. Candle endpoint routing still uses close time despite `market_settled_ts` cutoff semantics; actual routing loss was not established here.

**Smallest correction:** label cache versions and their true denominators; clip using original observation timestamps, preserve observation/fill times and use an explicit end-of-day convention before retaining these exhibits. Validate cached metadata against current inputs. Keep coherence `not_estimable`; no synchronization or trade-freshness claim follows from reconstruction.

### D5 — Reproducible candidate labels still do not establish common payouts

**Minor under the paper's candidate-only interpretation; open; observed.** Locations: `src/matching.py:_predicate_difference,_label_match`; accepted rows `match:GOVPARTYNJ-25-D:551137`, `match:GOVPARTYNJ-25-R:551143`, and the three current `RATECUTCOUNT-24DEC31-{T0,T2,T4}` pairs.

Full candidate regeneration and joins pass. Operative-rule inspection preserves the substantive concern: New Jersey Kalshi contracts concern a party representative being inaugurated, while Polymarket concerns a named candidate winning with call/certification conditions. A candidate winning but not taking office, or a same-party replacement, separates payouts. The rate-cut contracts also use “in 2024” versus “by the December meeting”; the close-metadata gap does not encode this rule-window distinction. The high-confidence filter recognizes only a few predicate contrasts.

**Smallest correction:** retain “candidate” terminology and manually adjudicate the 11 pairs before any claim-equivalent price comparison. Keep pair IDs distinct from the five underlying phenomenon groupings (Texas Senate nomination, Florida governor nomination, State of the Union attendance, 2024 rate cuts, New Jersey governor election). Existing lexical retrieval can remain; no broad classifier or new research is necessary for this correction.

### D6 — Actual outcome-coded sample mixes final, proposed and undocumented statuses

**Minor; changed / partly resolved, open; observed.** Locations: `src/preprocessing.py:normalize_polymarket,normalize_kalshi`; outcome-subset logic in `src/analysis.py`; platform settlement-record CSVs.

The prior multi-outcome acceptance risk is **latent in this sample**: all 7,249 retained Polymarket records have exactly two Yes/No outcomes and two prices; 7,248 have two token IDs and one has none (`222641`, EIP-1559). All are closed. Thus the earlier injected open-market example is not observed contamination. All 751 excluded rows also have exactly two outcomes; the restriction is supported Yes/No ordering, not binary versus nonbinary.

| Polymarket `umaResolutionStatus` | Price-coded YES | Price-coded NO | Uncoded | Total |
|---|---:|---:|---:|---:|
| resolved | 1,806 | 5,378 | 9 | 7,193 |
| proposed | 3 | 12 | 0 | 15 |
| settled | 0 | 2 | 0 | 2 |
| absent | 23 | 15 | 1 | 39 |
| **Total** | **1,832** | **5,407** | **10** | **7,249** |

Of the 7,239 price-coded outcomes, **15 remain proposed and 38 lack this status field**; the two `settled` values need documented interpretation. Absence is not proof of nonresolution. Nine uncoded rows are `resolved` with `[0.5,0.5]` prices; the tenth, `35976`, is a legacy Biden inauguration market with [.986241…, .013758…] and no status field. Neither the price vector alone nor `closedTime` is a universal final-payout certificate.

Kalshi's 11,073 binary outcomes all have finalized status and matching 0/1 settlement values. Six additional finalized rows have explicit scalar payouts: `.02, .25, .29, .45, .51, .63`. IDs include `KXELECTIONMOVNJGOV-25-MSHE-B1.5`, four `KXKHAMENEIOUT-*` contracts, and `KXLEADERSOUT-27JAN01-AKHAIRA`; all are listed in scratch. The other 1,172 rows are active (1,016), closed (46), inactive (76), or initialized (34), with no result/settlement time. The six scalar plus ten uncoded Polymarket rows exactly explain the outcome/timestamp sample difference. These scalar records establish archived fractional settlement metadata, not a realized cross-platform divergence mechanism.

**Smallest correction:** call the existing restriction “binary outcome-coded,” report this status table, retain fractional outcomes explicitly and validate lengths/order/token alignment at normalization. A final-status-only diagnostic may be informative but should not silently redefine the sample or classify missing legacy status as proven unresolved.

### D7 — Midnight truncation and invalid end dates produce observed zero exposures

**Minor; changed / open; observed.** Locations: `src/preprocessing.py:_finalize`; `src/analysis.py:prepare_market_analysis`; timing-exception CSVs.

No normalized row has a missing final exposure. However, **65 Kalshi intervals are negative before clipping**: 27 active markets opened during September 10, have positive volume, and are assigned zero exposure by the midnight cutoff; another 38 have later scheduled openings and zero volume. The latter are legitimate prospective schedules, not proof of a bad acquisition date. There are 74 Kalshi zero exposures overall.

**52 Polymarket rows have `endDate` before `startDate`**, positive volume and zero clipped exposure; their duration becomes missing. Example: `1007260`, “Will Russia capture all of Pokrovsk by February 28?”, opens December 23, 2025 but carries September 30, 2025 as `endDate`; its closure is February 27, 2026. Choosing this stale metadata endpoint over closure produces a negative 84.92-day interval and then a zero control value.

Replacing the midnight bound with the next midnight changes **1,115 Kalshi and three Polymarket** exposures, by at most one day. This is a sensitivity convention, not a recovered retrieval timestamp. It does not repair the 52 reversed-date Polymarket records. Sixteen-row outcome/timing sample differences are explained in D6 and do not themselves show a timestamp parser defect; parsing remains UTC with mixed timestamp formats.

**Smallest correction:** separate scheduled-not-yet-open, invalid interval and genuine zero exposure; document or repair demonstrated stale endpoint cases under a fixed rule, preserve original fields, and run the bounded timing sensitivity on the existing specification. Model consequences belong to the empirical follow-up. Do not impute a precise historical acquisition time.

### D8 — Current raw cases validate; stale witness publication remains a latent regeneration defect

**Minor; open, current-source check resolved; observed unchanged code behavior, no current sample failure.** Locations: `src/anecdotes.py:add_claim_relations`, fixed witness/payout construction, and report-generation callers.

All six cases now regenerate from the restored dedicated snapshots/current match table with exact equality across 38 exported columns, and their current audit fingerprints pass. There is no observed raw-rule mismatch in the present exhibits.

The prior mutation test still describes unchanged code: a changed rule invalidates `claim_relation_validated` but preserves fixed witness prose, asserted payouts and `truth_condition_divergent`; question changes are omitted from the fingerprint. Thus passing present fingerprints resolves the present source-availability concern, not the regeneration guard defect.

**Smallest correction:** bind operative questions and rules to the audit identity and invalidate dependent witness/payout publication when it fails. Preserve the current exhibits unless a substantive re-audit finds a problem. No new claim-equivalence or realized-settlement evidence was manufactured by the successful reconstruction.

### D9 — `gameStartTime` rejects demonstrably non-sports contracts

**Major; new / open; observed.** Locations: `src/taxonomy.py:is_polymarket_sports`; current acquisition and normalization callers; alternate `polymarket-markets-n8000-2026-09-10.json`; `alternate-poly-exclusions.csv`; dedicated `representation-cases-2026-09-10.json`.

The sports test returns true immediately for any nonempty `gameStartTime`. The older 8,000-row sample contains 5,015 classifier-positive rows absent from the current selected IDs; 213 of those have a game-start value but neither `sportsMarketType` nor a matching sports-taxonomy term. The 213 are **not** a manually verified false-positive total: the subgroup also contains real sports questions such as Liverpool matches.

Small representative checks establish at least seven clear non-sports exclusions attributable solely to this field:

| ID | Archived question/topic | Volume in alternate archive |
|---|---|---:|
| `502571` | Trump launches a coin before election | 76,899,060.60 |
| `504642` | Israel–Hamas ceasefire in 2024 | 3,950,958.94 |
| `506202` | US government shutdown | 53,500,373.74 |
| `510319` | Trump ends Ukraine war in first 90 days | 56,491,984.30 |
| `512598` | Trump declassifies Epstein list in first 100 days | 2,048,179.03 |
| `521607` | Ukraine agrees to Trump mineral deal before April | 7,079,947.24 |
| `546814` | Zelenskyy wears a suit before July | 242,231,180.27 |

All seven have empty `sportsMarketType`, no configured sports-text hit, a populated `gameStartTime`, and no ID in the current selected snapshot. The last two also appear in the independently archived mechanism cases. This shows the classifier removes some of the substantive phenomena the paper studies. It does not imply that purposively selected cases must belong to the metadata sample; their separate sampling is legitimate when explicit.

**Consequence:** “first 8,000 non-sports markets” is stronger than the implemented and observed selection permits. The effect is differential selection, not random missingness, and the full excluded population cannot be reconstructed. Native volume figures above identify substantial archived markets, not population totals or model effects.

**Smallest correction:** stop treating `gameStartTime` alone as sufficient sports evidence; use the already available sports-type/text evidence with representative regression checks, and explicitly describe remaining classifier limitations. Audit the recoverable rows and preserve the original selected sample for measurement before/after comparisons. Any broadened or corrected sample must be separately versioned; a fresh complete top-8,000 collection is outside this follow-up. Successful repair of these examples narrows the known defect, but cannot certify all 15,700 unretained row occurrences or establish full classifier precision/recall.

## Interpretation, validation and priorities

The mechanical score structure described in the prior audit is unchanged: five equally weighted components; threshold status enters the outcome component directly; discretion terms can penalize two components; length affects opportunity for term hits. Empty text's default score is .25, but no current row has an empty rule. The legacy pair-divergence formula remains a lexical/numeric/source/stage/deadline diagnostic, distinct from the six manually adjudicated witness cases. Reproduction certifies those calculations, not construct validity.

The restored archives support retrospective rule descriptions, sampled-portfolio composition and exploratory volume associations. They do not establish pre-trading treatments: raw metadata include cumulative volume, late outcomes and rule corrections. Neither native volume comparability, calendar-period splits nor family clustering converts this purposive sample into population or causal evidence.

**Validation performed:** pure imports, immutable JSON/CSV reads, complete raw-to-contract/table reproduction, full candidate re-execution, raw-to-case reconstruction, both history-version reconstructions, exact current panel/summary comparisons, assert-based unit/count checks, status and missingness cross-tabs, bounded parser diagnostics, representative source/rule/selection checks. The audit commands used `PYTHONDONTWRITEBYTECODE=1` and scratch-local `uv --cache-dir ... run --no-project --no-managed-python --no-python-downloads --no-config python3 -B`; matching also bounded BLAS threads. Initial diagnostics were corrected for the existing CSV serializer's trailing-whitespace rule, empty-string numeric parsing, byte-preserving hashes, and the distinction between whole-token `tie` and legitimate `ties/tied`; final recorded reconciliation assertions pass. No project code was patched to obtain equality. The earlier report's 50-test result is historical, not a new suite run.

**Still unavailable:** actual HTTP acquisition timestamps and original request logs; full eligible Kalshi catalog/tier variants; Polymarket scan rejections/overflow; exact original PDF/extraction chain; independently verified settlement payouts beyond API metadata; exhaustive classifier or matching validation; synchronized fresh prices. No external market collection or broad research was needed. Model coefficient/covariance refits are the empirical reviewer's assignment and were not duplicated here.

Priorities are **D1/D2/D9** for honest sample/provenance definitions and selection safeguards, **D3** for measured parser repair and revised profile interpretation, **D6/D7** for outcome/exposure definitions, and **D4/D5/D8** for safe retention or reuse of exploratory/case artifacts. The source-level replication barrier is resolved; the ranking, selection and timing limitations are now evidence-backed rather than hypothetical.

Skipped: new downloads, theory reassessment, model refits, exhaustive manual coding and broad test reruns. Risk: exact reproduction does not validate the sports filter, acquisition cutoff, outcome labels, or semantic construct; the complete corrected historical selection is unrecoverable from these files alone.
