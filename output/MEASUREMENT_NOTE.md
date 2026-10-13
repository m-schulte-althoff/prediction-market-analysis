# Rule-text measurement correction

The fixed original sample has 19,500 rows. `determinacy_score` remains a legacy column name for an exploratory equal-weight rule-text specificity index; neither code tests nor agent family checks provide human construct validation.

| Specification | Kalshi mean | Polymarket mean | Changed scores versus original |
|---|---:|---:|---:|
| Original | 0.623620 | 0.610127 | 0 |
| Four frozen parser repairs | 0.620616 | 0.629620 | 4,136 |
| Final production with authority-field placement correction | 0.620616 | 0.656617 | 6,406 |

The four repairs recognize quoted YES phrases, percent units, whole-word tie clauses and actual deadline cues. They add definition cues to 2,353 Polymarket rows and percent threshold flags to 11 Kalshi and 79 Polymarket rows. The auditor's narrower quote-removal diagnostic is a distinct definition, not the adopted specification. Frozen row-level values reproduce exactly. Corrections eliminate the old composition reversal; no institutional quality ranking replaces it.

The final source component retains 0.75 authority/URL and 0.25 source-information weights, crediting recognized authority or URL information in the combined rule/source text irrespective of duplicate placement. It adds 0.25 to the source component and 0.05 to the composite for 3,914 Polymarket rows across 1,357 API event families. Its overlap with parser changes explains why total changed rows are not the sum of separate diagnostic counts. Source-bonus removal remains a weight sensitivity. The final four non-source components equal the frozen diagnostic on every row.

Twelve distinct affected families were inspected. A Federal Reserve nomination example demonstrates that a lexicon authority can be the event subject rather than the deciding source. This supports the literal-cue label and limits its institutional interpretation. Missing operative rules produce missing discretion/index values, but no current sample row lacks operative rules. Weights were not tuned to volume results.

Reader-facing components: authority/source cues; date/time cues; definition/threshold cues; conditional/fallback cues; absence of configured discretion terms when rules exist. Threshold flags contribute to the index, so within-flag profiles are descriptive. Final flags mark 10,071 Kalshi rows (82.2055%) and 1,794 Polymarket rows (24.7482%).

The preferred formula is `volume_z ~ determinacy_z + log_rule_length + log_observed_exposure + C(open_year) + C(platform) + C(category_group)`. On the final index, the coefficient is −0.124293, family-clustered SE 0.041064 and 95% interval [−0.204776, −0.043809], with n=19,500 and 2,754 qualified families. The same-formula HC3 comparison has the identical point estimate with SE 0.009349. See the regenerated model table for all final estimates. The parser-only review estimate was −0.129454; it must not be confused with final production.

Audit tables: [row-level comparison](tables/measurement-before-after.csv), [summary](tables/measurement-summary.csv), [feature variants and preferred models](tables/measurement-preferred-models.csv), [final departures](tables/measurement-final-departures.csv), [bounded family checks](tables/measurement-rule-family-checks.csv). No new scale validation, specification grid or dataset was authorized.
