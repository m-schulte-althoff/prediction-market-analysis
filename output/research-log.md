# Research Log

## 2026-09-10 — Iteration 1: transparent composite

- Question: Does semantic determinacy predict within-platform standardized log volume, controlling for rule length, market duration, platform, and category?
- Result: coefficient -0.130 (HC3 SE 0.010, p=2.16e-37, n=15914).
- Interpretation: The inverse sign contradicts a simple participation-cost account and is consistent with ambiguity attracting heterogeneous-interpretation trading; volume is not direct evidence of forecast quality or causality.
- Decision: Separate semantic clarity from rule complexity and repeat within platform.

## 2026-09-10 — Iteration 2: complexity separation

- Question: Does a core score excluding edge-case completeness survive controls for both rule length and conditional-clause count?
- Result: coefficient -0.195 (HC3 SE 0.012, p=3.33e-62).
- Interpretation: This check reduces the risk that the composite is merely a verbose-rules measure.
- Decision: Add clustered and event/series-aggregated specifications to rule out repeated-template pseudoreplication.

## 2026-09-10 — Iteration 3: dependence and forecast error

- main_series_clustered: determinacy coefficient -0.130 (SE 0.061, p=0.033, n=15914).
- event_series_aggregated: determinacy coefficient -0.103 (SE 0.039, p=0.00749, n=1366).
- Terminal-error result: coefficient 0.006 probability points per determinacy SD (series-clustered SE 0.006, p=0.318, n=10400).
- Interpretation: The volume pattern does not translate into detectable last-trade accuracy differences; this is an important null, and terminal timing is not a fixed forecast horizon.
- Decision: Reframe the current result as an ambiguity–activity phenomenon and prioritize fixed-horizon errors/spreads in follow-up work.

## 2026-09-10 — Iteration 4: cross-platform matching

- Question: Can same-underlying-event contracts be isolated with conservative lexical, numeric, and date agreement before comparing resolution conditions?
- Result: 11 high-confidence, 154 probable, and 36588 rejected candidates retained for audit.
- Price-panel result: insufficient aligned high-confidence histories for a stable regression; retained as a visible failed/limited specification.
- Decision: Use matched examples diagnostically and prioritize human validation plus expanded history coverage.
