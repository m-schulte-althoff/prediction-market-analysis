# Research Log

## 2026-09-11 — sample and exposure audit

- Removed sports before imposing the Polymarket volume cap using official fields plus a documented conservative taxonomy. This corrects contamination by tournament families.
- Parsed mixed ISO timestamp precision explicitly; the prior coercion had erased Polymarket resolution timestamps.
- Replaced scheduled duration with retrieval-capped observed exposure in the preferred volume specification and added opening-year cohorts.
- Original-style baseline determinacy coefficient: -0.160 (HC3 SE 0.009, p=7.27e-67, n=19,500).
- Preferred exposure/cohort-adjusted coefficient: -0.115 (HC3 SE 0.009, p=2.16e-35, n=19,500).

## 2026-09-11 — within-family diagnostic

- Question: Does determinacy predict volume using only variation inside repeated Kalshi series or Polymarket events? This removes stable family popularity by demeaning outcomes and controls within family.
- Kalshi: -0.035 (family-clustered SE 0.066, p=0.597, n=6,443).
- Polymarket: 0.031 (family-clustered SE 0.027, p=0.262, n=1,043).
- Decision: Treat the determinacy–volume association as secondary and exploratory unless stronger within-family or fixed-window-volume evidence emerges. A weak/null within-family estimate is evidence about identification, not evidence that representations do not matter.

## 2026-09-11 — construct and case audit

- Recast semantic determinacy as an intra-contract property and divergence as an inter-contract property; neither is a substitute for the other.
- Require a counterfactual witness state and implied settlement on each side before calling a pair truth-condition divergent. Automated text distances remain candidate diagnostics only.
- Matching inventory: 15 high-confidence, 364 probable, and 36374 rejected candidates retained for audit.
- Matched-price regression remains infeasible; no average divergence claim is made.
- Kalshi last-trade error diagnostic: 0.011 (series-clustered SE 0.007, p=0.146, n=10,400); this is not a common-horizon accuracy test.
