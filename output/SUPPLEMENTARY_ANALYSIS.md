# Supplementary analysis

## Text measurement and portfolio context

The [measurement note](MEASUREMENT_NOTE.md) retains the composite definition and repair history. [Component profiles](tables/analysis-platform-profiles.csv) and the [data atlas](descriptions-data.html) describe the selected portfolios. Components are mean weighted cue scores; the discretion-term score is max(0, 1 − 0.25 × distinct configured phrases), not a no-flag share. These lexical descriptions do not validate scenario-level determinacy.

## Activity association

| Specification | Coefficient | 95% interval | Uncertainty | n |
|---|---:|---:|---|---:|
| cohort_exposure_adjusted | -0.1243 | [-0.2048, -0.0438] | cluster; SE 0.0411 | 19,500 |
| cohort_exposure_adjusted_hc3 | -0.1243 | [-0.1426, -0.1060] | HC3; SE 0.0093 | 19,500 |
| within_family_kalshi | -0.0753 | [-0.2366, 0.0861] | cluster; SE 0.0823 | 6,345 |
| within_family_polymarket | -0.0445 | [-0.1218, 0.0327] | cluster; SE 0.0394 | 519 |

The preferred pooled coefficient uses one within-platform SD of the text index and standardized log cumulative volume. Its family clusters are qualified by platform. HC3 uses the same formula and rows as a covariance comparison. Within-family models use internally varying families and a different residual-score SD; their magnitudes are not directly comparable to the pooled coefficient.

Volume selection, retrospective rules, family concentration and incomplete exposure metadata limit interpretation to these selected portfolios. Subgroup significance differences do not test heterogeneity.

The current cycle's [independent reproduction](paper-revision/2026-10-15-01/scratch-empirics/reproduction-results.json) uses the final field-invariant features. Its top five families contribute 66.86% of focal sandwich variance. Omitting the largest family by row count (2,000 rows) gives β=−0.1199, family-clustered SE 0.0402 and 95% interval [−0.1986, −0.0411], n=17,500. This bounded diagnostic does not establish broad robustness or causality. The older 69.48% concentration belongs to the earlier frozen specification and is retained only as historical evidence. No further deletion grid was run.

## Terminal-error diagnostic

0.016 (family-clustered SE 0.008, p=0.0643, n=10,400). This last-trade Kalshi diagnostic lacks a common forecast horizon; a null is not equivalence.

## Dormant price panel

2 saved pair summaries remain. Matched-model rows: 0. There are no qualifying synchronized-price observations. The retained `bad72f8883` cache and alternate `627b27c83f-interval-max` contain different pair inventories; the alternate third pair remains eligible, so prior three-to-two attrition was not caused by current eligibility.

All existing model rows are retained in [analysis-market-models.csv](tables/analysis-market-models.csv), with formula, covariance, sample size and confidence intervals. These exploratory values are unadjusted for multiple comparisons. Figures of score–volume bins use unclustered descriptive mean intervals, separate from preferred family-clustered model inference.
