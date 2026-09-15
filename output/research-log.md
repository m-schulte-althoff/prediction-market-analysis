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
