# Independent data audit — 2026-10-15-01

## Verdict and scope

**The checked stored records reconcile with the central sample counts, text profiles and case-outcome contrasts. No new central numerical discrepancy or critical defect was identified.** The newly quantified issue is that Gamma `endDate` is not necessarily the operative rule deadline (D1). Historical selection/as-of provenance and the distinction between final-status outcome vectors and protocol settlement remain disclosed evidence boundaries (D2–D3), not newly discovered errors.

This is a bounded audit of baseline `32231e50323a8fc56a0613a10e455c66a22cee05`, branch `main`. I inspected the manuscript, research log, construct/decision records, acquisition and normalization code, semantic scoring, matching, panel construction, case construction and relevant reporting/model code. I did not read other reviewer reports, change canonical data/code/prose, run the canonical pipeline, acquire a new dataset or make paid calls. Fifty selected primary data/table/code/manuscript hashes agree with this cycle's `BASELINE.json`; all eleven source-copy hashes in the observed-case bundle also match. These checks establish preservation relative to the recorded baselines, not the authenticity or acquisition time of the original HTTP responses.

Independent checks used Python's standard-library CSV/JSON readers and arithmetic. Machine-readable results are in [scratch-data-audit/reconciliation.json](scratch-data-audit/reconciliation.json). An earlier `uv run --no-sync --offline` inventory failed because the sandbox blocked the default uv cache; its escalated retry was aborted without producing an inventory. Subsequent standard-library checks succeeded. No model refit, parser rerun or full pipeline reproduction is claimed.

## Source-to-sample lineage and attrition

| Stage | Independently checked result | Interpretation |
|---|---|---|
| Local raw inventory | Nine JSON files; all lack `acquired_at_utc` and carry the legacy September 10 label | Separate source versions; do not union them or infer a common acquisition instant |
| Main Kalshi snapshot | `kalshi-markets-s120-2026-09-10.json`: 12,253 rows, no duplicate ticker; exactly two questions of length ≤4 | Ledger retains 12,251; no additional unexplained normalization loss |
| Kalshi selection | Wrapper records 120 series, selected categories and 1,000 rows per live/archive tier | Selection conditions on series volume; original tier overflow and complete catalog selection cannot be reconstructed from this package |
| Main Polymarket snapshot | `polymarket-nonsports-markets-v2-n8000-2026-09-10.json`: 8,000 rows, no duplicate ID; all have one embedded event | No observed ambiguity from choosing `events[0]` in this snapshot |
| Polymarket normalization | Exactly 751 raw IDs absent from normalized data have unsupported outcome labels; 709 are `Up`/`Down`; remaining labels are other non-YES/NO pairs | Deliberate supported-label restriction, not proof those markets are nonbinary or invalid |
| Polymarket acquisition | Wrapper reports 23,700 scanned and 8,000 retained | The arithmetic remainder 15,700 has no recoverable rejection/overflow decomposition; it must not be called a sports count |
| Retained table | 19,500 rows and 19,500 unique platform-qualified `contract_id` values | 12,251 Kalshi + 7,249 Polymarket |
| Phenomenon retrieval | 36,753 candidate rows and unique pairs = 12,251 × 3; no dangling contract references | 11 high-confidence, 368 probable, 36,374 rejected; retrieval labels do not establish claim equivalence |
| Retained price panel | 14 rows, two pairs, unique pair–timestamp keys; all 14 explicitly ineligible for synchronized-price tests | Stored `bad72f8883` version; do not interpret a missing test as zero incoherence |

The raw Kalshi snapshot contains 1,364 event identifiers but 120 series families. Polymarket has 2,634 event identifiers and 2,626 series strings; its analytical families correctly use event IDs rather than the potentially coarser strings (`src/analysis.py:63–70`). These platform family units are substantively different. All 8,000 raw Polymarket records have one embedded event, so the first-event mapping creates no observed many-to-many join in this package. There is no observed duplicate inflation in the retained contract, candidate-pair or panel keys checked here.

Candidate construction is a directed nearest-neighbour retrieval, not an independent event census (`src/matching.py:127–215`). One high-confidence candidate is “6 times” versus “6+ times” for Fed cuts. The stored `comparison_status=metadata_candidate_requires_rule_audit` is therefore material. No claim-equivalence certification is warranted from the label alone. The panel archive's default selection hash is not an acquisition license; the explicit preserved version and documented absence of the current default archive should remain visible.

## Central descriptive and outcome reconciliation

All following text-profile values were independently averaged from `data/processed/semantics-contracts.csv` and agree with `analysis-platform-profiles.csv` and the manuscript's rounding.

| Measure | Kalshi | Polymarket |
|---|---:|---:|
| Exploratory specificity index | 0.6206156232 | 0.6566171886 |
| Authority/source component | 0.5501591707 | 0.6532970065 |
| Date/time component | 0.6049832667 | 0.7978824665 |
| Definition/threshold component | 0.6786874541 | 0.6170630432 |
| Edge-clause component | 0.2719418823 | 0.4038350117 |
| Absence-of-discretion-term component | 0.9973063423 | 0.8110084150 |
| Threshold-flag share | 82.2055% | 24.7482% |
| Mean analyzed words | 100.4653 | 157.7881 |
| Top-five family share | 46.1758% | 2.5521% |
| Varying families / rows | 43 / 6,345 | 85 / 519 |

All 19,500 stored composite scores equal the arithmetic mean of their five stored components within `1e-12`. This checks arithmetic, not the validity of the lexical parsers or weights. `src/semantics.py:139–214` concatenates question, rules and source text; source scoring rewards explicit authorities/URLs, temporal scoring rewards dates/times/zones/deadline cues, the definition score includes a threshold bonus and ambiguity penalties, the edge component counts configured terms/conditionals, and discretion clarity penalizes configured discretion phrases. The equally weighted mean is not an empirical measure of whether complete rules fix a payout in a specified state. The manuscript correctly calls it exploratory specificity and acknowledges absent independent human validation.

No retained row lacks operative rule text, volume, opening timestamp or closing timestamp. Kalshi lacks 1,172 resolution timestamps and has 1,178 missing binary outcomes: the additional six are scalar settlements, not missing outcomes of the same kind. Its outcome ledger reconciles 11,073 recorded binary outcomes, six scalars and 1,172 without a recorded result. Polymarket has 7,186 qualified final-status endpoint labels, 53 endpoints without supported final status (15 proposed, 38 missing), and ten intermediate vectors. Thus 63 rows lack a qualified binary `outcome`. Endpoint inference uses 0.99/0.01 thresholds (`src/preprocessing.py:224–244`); it is distinct from the exact 0/1 vectors required for the named observed cases (`src/anecdotes.py:782–801`).

All acquisition timestamps are missing. Three raw Polymarket `updatedAt` fields are September 11 (`4339036`, `4339037`, `4339038`), agreeing with the disclosed label inconsistency. Negative elapsed exposures reconcile to 65 Kalshi and 52 Polymarket rows. The ledger separates 38 future scheduled zero-volume openings, 27 same-day positive-volume Kalshi openings, and 52 positive-volume Polymarket close-before-open cases. UTC parsing and seconds/86,400 arithmetic are explicit; date-only midnight and clipping remain conventions, not trading-time observations.

The preferred supplementary table reports coefficient −0.1242927593, clustered SE 0.0410637834, CI [−0.2047762959, −0.0438092227], n=19,500, 2,754 families. HC3 has the identical coefficient/formula/n with SE 0.0093489001. These stored numbers match the research log and code's covariance-only comparison (`src/analysis.py:19–22, 200–209`); I did not independently refit them. Standardization is within platform, rows have equal OLS weight, and families enter the covariance rather than equal-family weighting. Family clustering does not resolve purposive volume selection, exposure measurement or retrospective rule measurement. The terminal-error table has n=10,400; its coefficient was not refit and it is not a common-horizon accuracy evaluation.

## Case records and evidential reach

| Case | Checked preserved fields | What remains unchecked |
|---|---|---|
| Hilton | Kalshi finalized `no`, `settlement_value_dollars=0.0000`; Gamma 825460 resolved with YES/NO vector 1/0. Both records' selected operative/outcome fields equal the main raw snapshot. Settlement/closure dates agree with the displayed chronology. | Certified vote percentages were not re-extracted from the external PDF in this audit; no redemption or pre-trading version audit |
| Khamenei | Kalshi finalized `scalar`, `0.4500`; Gamma 661699 resolved 1/0. Selected operative/outcome fields equal the main raw snapshot. Recorded timestamps agree with the displayed chronology. | Independent death report not reverified; reference-price selection, reimbursements, account cash flows and causal clause attribution unverified |
| Suit | Gamma 546814 resolved 0/1; status list contains five proposed/disputed pairs; closure July 9, 2025, 00:30:39 UTC | No timestamps for the individual pairs; no independent garment classification, complete oracle trace or on-chain finality check |
| Minerals | Gamma 521607 and 532897 resolved 1/0; March 25 and May 4 closure records | No independently verified March qualifying announcement or complete settlement timeline in this audit; YES/YES is not the hypothetical YES/NO witness |

Suit and the March minerals contract are absent from the main raw metadata sample; the later minerals contract is present and its selected operative fields agree. Their separately versioned case evidence therefore cannot be represented as a random or complete subsample of the 19,500 rows. The manuscript preserves this distinction. The retained case bundle supplies seven distinct contract records across four observed exhibits; these are not seven independent empirical replications. The remaining five rule witnesses remain hypothetical.

The Polymarket fields establish a resolved institutional outcome and exact endpoint vector; the source does not contain a separately recorded `settlement_value_dollars` analogous to Kalshi. This supports the paper's qualified outcome comparison, not independently audited cash payment to each holder. Fractional Kalshi clauses also prevent global binary subset/coherence restrictions. No current panel row supplies synchronized price evidence.

## Findings

### D1 — Metadata end dates differ from operative rule deadlines

- **Severity / evidence:** minor for the current case-led paper; observed source-field discrepancy, newly quantified here. Broader impact unverified.
- **Location:** `src/preprocessing.py:260–262` maps Gamma `endDate` to `close_timestamp`; `_finalize:312–323` uses its minimum with resolution/snapshot times for exposure. `src/matching.py:148–155` uses it for deadline screening; `src/panel.py:102–105` uses normalized closes for overlap. Exact records: case bundle `observed_cases.khamenei.b`, `minerals.a`, `minerals.b`, columns `description`, `endDate`.
- **Expected versus observed:** an operative “June 30, 2026, 11:59 PM ET” cutoff is July 1, 03:59 UTC under daylight saving time; market 661699 instead has `endDate=2026-06-30T00:00:00Z`, 27h59m earlier. Markets 521607 and 532897 have noon-UTC metadata ends, each 15h59m earlier than their explicit March 31/April 30 23:59 ET rule deadlines. These are differences in field meaning, not UTC conversion errors in the code.
- **Affected sample / consequence:** 661699 and 532897 are retained; 521607 is a separate case record. Early resolution makes the Khamenei example's exposure minimum precede either deadline. The later minerals contract closes May 4, so its metadata-based exposure terminates before its stated rule window. The paper's case descriptions use operative clauses correctly; no observed case-payout conclusion changes. Population prevalence and model sensitivity are unchecked.
- **Minimal remedy:** preserve the metadata proxy and its label; explicitly distinguish it from semantic deadlines wherever it drives comparability or pre-deadline price analysis. For the named cases, record both timestamps without bulk date extraction. Any future price-window test must audit operative deadlines manually. If such tests remain absent, a short clarification is sufficient; no replacement sample or model grid is needed.

### D2 — Historical sample and as-of status remain unrecoverable

- **Severity / evidence:** major limit on population/as-of claims; observed missing provenance, already disclosed. Not a new defect in the narrowed paper.
- **Location:** main raw wrappers (`retrieved_at_date`, missing `acquired_at_utc`, `selection.raw_rows_scanned`); `src/kalshi.py:49–65, 102–129`; `src/polymarket.py:91–115`; manuscript lines 128–134; `DATA_SOURCES.md` acquisition/provenance sections.
- **Expected versus observed:** a reproducible contemporaneous sampling frame would need request times, rejected IDs/reasons, tier pagination/overflow and the selection catalog. The package supplies retained snapshots and settings, but not that complete frame. Three raw updates postdate the label. Exact case rules as they appeared before trading cannot be inferred from a later metadata response.
- **Consequence / uncertainty:** selected-portfolio description and observed archived-rule contrasts survive; population incidence, platform rankings and temporal causal interpretations are not identified. The size/direction of historical selection bias is unknown.
- **Minimal remedy:** retain the current explicit restrictions and fixed IDs. Do not reconstruct historical acquisition with current API responses. A new purposive sample would not repair this package's historical provenance. New rule-version evidence should be added only for the small realized-case set if pursued under rank 2 below.

### D3 — Current case evidence stops short of a protocol settlement chronology

- **Severity / evidence:** minor for current qualified claims; observed absence of stronger evidence, already disclosed. Actual protocol timing is unverified.
- **Location:** `src/anecdotes.py:764–801, 942–957`; case bundle `umaResolutionStatus`, `umaResolutionStatuses`, `outcomePrices`, `closedTime`; manuscript lines 59, 72–74, 80–86.
- **Expected versus observed:** ordered proposal/dispute/finality claims would require timestamped request, proposal, dispute, oracle and condition-resolution records. The suit archive has an undated status list plus current resolved status; `closedTime` is a lifecycle record. The API vector alone does not audit token redemption or holder cash receipts.
- **Consequence / uncertainty:** retain the observed outcome/dispute statements, but do not infer five independently timed arbitration rounds, a specific settlement delay, manipulation or account payout from these fields. No contradiction in the currently qualified wording was found.
- **Minimal remedy:** either keep this boundary or add the single-contract protocol trace below. Positive trace agreement strengthens provenance, not the causal claim; mismatch requires repairing the chronology and outcome wording; failed linkage leaves the current qualified case rather than a fabricated timeline.

## Ranked additional-data options — smallest useful additions

These are recommendations, not collection authorization. The bounded web check verified relevant primary documentation/source code, not the historical completeness or free availability of a case-level query. Both options add observations from outside the repository; neither is exogenous variation in the causal-inference sense. Merely recoding the existing case bundle is not new data.

| Rank | Concrete dataset, unit and linkage | Marginal scientific value | Availability, provenance and cost | Minimum collection and stop rule |
|---|---|---|---|---|
| **1** | **Timestamped protocol lifecycle for suit market 546814 only.** One row per request/proposal/dispute/oracle/condition-resolution event. Join held `questionID=0x0bf7a42b24b91417c1c1976cf99d153ac046f7bffd66c934291c94ddb742b743` and `conditionId=0x655e5ca101c466b6293aa15e06173b78b293221803d56e35551f708cd82eb352`; verify chain, adapter/version and request key rather than joining by title. | Directly replaces the weakest timing inference: what was proposed, challenged and finalized, and when. Adds an institutional process observation without a price study or new metadata sample. Does not establish an objectively correct garment classification or manipulation. | Polymarket's [official event-linkage code/documentation](https://github.com/Polymarket/go-market-events/blob/main/README.md) maps disputes through ancillary-data/question IDs and condition resolution through condition IDs. Its [adapter interface](https://github.com/Polymarket/uma-ctf-adapter/blob/main/src/interfaces/IUmaCtfAdapter.sol) specifies initialization/resolution events. Read-only logs require no transaction fees; historical public-RPC limits, archival coverage and exact deployed version are untested. No paid provider is assumed. | One contract, initialization through first verified final condition resolution, with June–July 2025 events the immediate focus. Preserve chain ID, address, pinned ABI/version, block/hash, transaction hash, log index, block time, raw logs and decoding. Cap feasibility work at two hours; stop on nonunique linkage, missing required history or paid-access requirement. Do not extend to wallet redemptions or all markets. |
| **2** | **Pre-outcome operative-rule versions for the Hilton and Khamenei pairs, maximum four contracts.** Unit = versioned source document/initialization or clarification record with its publication/block time, source role and text hash. Link exact platform IDs and compare to the held archived rules. | Addresses whether the realized contrasts were specified before the relevant event/trading, rather than merely visible afterward. This would support an ex-ante contract-design interpretation. Unchanged versions strengthen that narrow interpretation; material edits require restricting the claim to the verified period/version. | The [official adapter implementation](https://github.com/Polymarket/uma-ctf-adapter/blob/main/src/UmaCtfAdapter.sol) initializes questions with ancillary data and emits it; the actual historical deployment and any clarification mechanism must be checked. Existing Kalshi historical responses expose later stored rules, not a verified version history. Availability of dated primary Kalshi rule versions is **unconfirmed**; current endpoints cannot establish it. Mostly documentary work, no paid calls assumed. | Start with the Hilton pair; retain only independently dated primary versions preceding the June 2, 2026 event and relevant market opening. Expand to Khamenei only if the same retrieval works. Reuse initialization logs obtained for rank 1 where relevant; do not build a general version scraper. Stop after two hours if no primary pre-outcome Kalshi version can be located. Report missingness rather than substitute an undated copy. |

**Recommendation:** pursue rank 1 only if one small new dataset is approved. It is the clearest incremental evidential gain for the current adjudication case. Rank 2 has high conceptual value but uncertain two-platform coverage; treat it as a bounded feasibility task, not a prerequisite for finishing the current paper. Neither requires replacing the fixed historical sample.

**No-new-data alternative:** retain the archived-rule/outcome formulation; make the source-role boundary explicit for every exhibit; keep the suit sequence undated and minerals YES/YES separate from its hypothetical witness. An optional complete within-family listing of the already held California candidate contracts, applying the already held certified result, is recoding existing evidence. It can make case selection transparent but does not add an external dataset, independent validation or population prevalence.

## Check disposition

- **Checked:** stored raw inventory/selection wrappers; raw identifier duplication; normalization losses and label composition; retained keys and missing fields; family/event cardinalities; arithmetic profile means/components/threshold shares/concentration/varying families; candidate counts and references; panel key counts/eligibility; selected raw-to-case field agreement; eleven source-copy hashes and fifty baseline hashes; scalar versus endpoint-vector evidence; named timestamp fields and three explicit ET deadline conversions.
- **Unavailable or unrun:** original HTTP acquisition logs and rejected/overflow scan; independently dated pre-trading rules; fresh external event-source verification; full PDF vote re-extraction; independent lexical parser rerun; original frozen before/after score reproduction; model refits/covariance replication; full history-to-panel reconstruction; exhaustive match semantics; on-chain events/redemptions; account reimbursements/cash flows; human construct validation; full test/static-check suite.
- **Not applicable to current claims:** causal treatment-effect identification, population prevalence estimation, platform rationality ranking, a synchronized-price coherence result, and a TeX/PDF manuscript build.

Skipped full pipeline/model and blockchain reproduction; the stored-record reconciliation is not an end-to-end certification. Remaining risk is overextending archived selected evidence into contemporaneous, population, price-effect or account-payment claims.
