# Research Log

## 2026-09-14 — sample and exposure audit

- Removed sports before imposing the Polymarket volume cap using official fields plus a documented conservative taxonomy. This corrects contamination by tournament families.
- Parsed mixed ISO timestamp precision explicitly; the prior coercion had erased Polymarket resolution timestamps.
- Replaced scheduled duration with retrieval-capped observed exposure in the preferred volume specification and added opening-year cohorts.
- Original-style baseline determinacy coefficient: -0.178 (HC3 SE 0.009, p=1.22e-82, n=19,500).
- Preferred exposure/cohort-adjusted coefficient: -0.129 (HC3 SE 0.009, p=2.49e-44, n=19,500).

## 2026-09-14 — within-family diagnostic

- Question: Does determinacy predict volume using only variation inside repeated Kalshi series or Polymarket events? This removes stable family popularity by demeaning outcomes and controls within family.
- Kalshi: -0.077 (family-clustered SE 0.082, p=0.342, n=6,443).
- Polymarket: 0.030 (family-clustered SE 0.027, p=0.265, n=1,048).
- Decision: Treat the determinacy–volume association as secondary and exploratory unless stronger within-family or fixed-window-volume evidence emerges. A weak/null within-family estimate is evidence about identification, not evidence that representations do not matter.

## 2026-09-14 — construct and case audit

- Recast semantic determinacy as an intra-contract property and divergence as an inter-contract property; neither is a substitute for the other.
- Require a counterfactual witness state and implied settlement on each side before calling a pair truth-condition divergent. Automated text distances remain candidate diagnostics only.
- Added the representation-aware bridge: a common Bayesian posterior over histories can assign different probabilities to platform-defined payoff events. Keep rule constitution separate from updating and semantic indeterminacy separate from uncertainty over worlds.
- Audited full case descriptions for logical relations, including fractional tie/death payouts. Relation labels are bound to rule/ID fingerprints. Existing daily price fills are not synchronized quote evidence; coherence outputs report explicit eligibility gates without adding a general price-effect claim.
- Matching inventory: 11 high-confidence, 368 probable, and 36374 rejected candidates retained for audit.
- Matched-price regression remains infeasible; no average divergence claim is made.
- Kalshi last-trade error diagnostic: 0.013 (series-clustered SE 0.009, p=0.137, n=10,400); this is not a common-horizon accuracy test.

## 2026-10-13 — Approved P1–P7 implementation

- User reviewed/approved the existing revision plan. Captured APPROVED_PROMPT_PLAN.md, created paper-revision/2026-10-12-01 and archived old manuscripts, outputs, memory, sources and original processed data under pre-revision/ with hashes. Original raw files remain unchanged.
- Preserved the historical 19,500 IDs. Repaired gameStartTime-only sports inference for future acquisition; the full rejected scan/overflow split is unrecoverable. The earlier claim of a fully corrected non-sports sample is superseded. Added explicit normalization, outcome-status, scalar-payout and exposure ledgers rather than silently reconstructing excluded records.
- Missing historical/future-date metadata, anecdote and history caches now fail before network access. New records carry actual UTC acquisition times; legacy acquisition times remain unknown. Reused the named bad72f8883 history only; its repaired 14-row/two-pair panel preserves bounded original source times and still supplies no eligible synchronized-price test. The alternate third pair remains metadata-eligible.
- Reproduced the frozen four-parser correction exactly: 4,136 changed scores, means 0.620616/0.629620. Added the separately approved authority-field placement invariance: final means 0.620616/0.656617. Withdrawn the composition reversal and platform-ranking claim. Twelve inspected families verify lexical behavior, with a recorded event-subject authority false positive; no scale or human inter-coder validation is claimed.
- Refit the exact preferred formula with platform-qualified family covariance: coefficient −0.124293, clustered SE 0.041064 and 95% CI [−0.204776, −0.043809], n=19,500 and 2,754 families. HC3 uses identical rows/formula/point estimate, SE 0.009349. Existing within-family fits are −0.0753 (Kalshi, n=6,345) and −0.0445 (Polymarket, n=519), both intervals include zero on their distinct residual-score scale. Activity and terminal-error diagnostics remain supplementary. Frozen influence/deletion checks are retained as original-specification evidence, not new final-feature checks.
- Main cases now verify Hilton NO/$0 versus YES/$1, Khamenei scalar $0.45 versus YES/$1, suit adjudication/final NO, and minerals YES/YES chronology. Nine exhibits represent seven mechanism labels; five scenarios are supplementary counterfactuals. Complete-input fingerprints block stale witness/payout assertions, including generated documents. No redemption/account cash-flow or manipulation inference was added.
- Rebuilt the theoretical passage around payoff divergence, conditional written-rule determinacy and ordinary expected payout. The earlier Meehan–Zhang extension/global-constancy framing is withdrawn; source audit and prior decisions remain history. Literature comparisons retain partial-access and preprint qualifications.
- Validation: cached preprocess→match→anecdotes→explicit panel→analyze succeeded; 116 focused tests, ruff and mypy passed. Initial integration caught two obsolete fingerprint fixtures and one test variable type conflict; stronger complete-input tests resolved them. Static checking now targets installed Python 3.12 stubs and excludes archives/scratch; no dependency was added. Markdown/local links and vector previews checked. Persistent log entries survive analyze. Remaining source/sampling/measurement/price limitations are in the revision summary; optional O1–O4 were not executed.

## 2026-10-15 — Approved P1–P6 and prose amendments

- Captured the approved disk plan and the user's richer-prose amendments, preserved the implementation baseline including the user's atlas additions, and created branch `paper-revision/2026-10-15-01`. No new critic round, merge or publication.
- Narrowed rule claims to supplied fields/linked evidence. Current specification PDFs contain additional exceptions but do not establish historical applicability. Withheld the presidential death/interruption witness; retained the observed payout contrasts and qualified minerals' question-rule binary model. Source hashes certify consistency, not exhaustive coverage. Raw series URLs remain available.
- P2 added one bounded public Polygon observation: exact adapter/question/condition and ancillary-question hashes verify; pinned block 95,596,076 corroborates payout [0,1] (NO). Creator updates acknowledge a May 29, 2025 dispute and say on July 1 that credible-reporting consensus has not confirmed a suit. The May 29 acknowledgment predates the June 24 photograph, so no whole-history photograph attribution survives. Stored July 5 request time is not initialization. Historical log access returned HTTP 403; collection stopped with no original final-resolution transaction or individual dispute rationale. Cost $0, five supporting documents, 23 RPC calls; no wallet/price extension.
- Preserved a failed linkage check: padded address encoding initially failed the condition assertion; packed encoding then verified the archived condition. No inference was published from the failed attempt. Initial suit fingerprint integration also exposed an empty-field difference between direct dictionaries and CSV-shaped rows; canonical empty operative-input fields resolved it. The new evidence and event-first prose were explicitly re-audited and their previous/current hashes recorded.
- Rewrote the manuscript as connected scientific prose, with a fuller top-two-primary motivation, linked theoretical definitions, three overlapping findings questions and literature-derived discussion consequences. Source-access notes moved to LITERATURE_USAGE.md. The casebook retains full supplied rules and hypothetical exhibits; main findings start with each event. Expected payout remains distinct from observed price. Expanded source documentation and updated constructs, weighted-score labels and atlas captions.
- Recorded actual ET/UTC rule deadlines separately from Gamma metadata timestamps. No input reconstruction or model change. The current review's final-feature omission remains −0.119878 (n=17,500) and focal top-five variance concentration 66.86%; the earlier 69.48% belongs to a frozen specification. Activity, repair history and composite interpretation remain supplementary.
- Cached anecdotes → analyze → describe regenerated the outputs. The affected 57 tests passed, including changed-protocol-evidence withholding through the full manuscript and atlas safeguards; ruff and mypy passed. Initial integration exposed synthetic fixtures missing the newly used platform fields and pandas scalar typing; both were corrected. Final preservation, numeric tolerance, local-link and vector-preview results are recorded in this cycle's IMPLEMENTATION_VALIDATION files. Optional O1–O4 remain excluded.
