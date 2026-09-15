# Research Status

Updated 2026-09-14.

## Current core

The strongest contribution is an audited account of how resolution architectures turn one public-world phenomenon into non-equivalent digital claims. The case matrix currently contains 6 mechanisms with exact rules and counterfactual witness states.
Same posterior over world histories does not require equal probabilities for different payoff events: `q_c(e)=E_{μ_e}[r_c]`, equal to `P(Y_c|e)` for determinate binary contracts. Semantic indeterminacy leaves the written mapping incomplete; it is separate from uncertainty about worlds. This is our representation extension, not Meehan and Zhang's own market argument; see [source audit](../docs/BAYES_SOURCE_AUDIT.md).

**Representation-aware coherence:** indeterminate: 1; non_equivalent_unclassified: 3; overlap_non_nested: 2. 0 cases supply a validated binary marginal restriction. Not estimable / insufficient evidence for an actual price-coherence test.

Election and minerals rules support overlapping, non-nested events under the stated archived-rule model; this alone imposes no useful pairwise marginal restriction. Fed inclusion is unclassified. Primary ties and leader death allocations fall outside globally binary payouts; the suit case remains adjudicatively incomplete. These qualifications preserve the existing witness results. The legacy daily panel forward-fills prices for up to seven days and cannot certify synchronized fresh observations. See `tables/coherence-case-diagnostics.csv` and `tables/coherence-panel-readiness.csv` for explicit eligibility reasons. Numerical excess, where estimable, is a conditional price diagnostic; liquidity, fees, spreads, stale trading, risk preferences, market composition and limits to arbitrage prevent interpreting it as trader irrationality.

## Current empirical package

The corrected non-sports metadata sample contains 19,500 contracts.

| Sampled rule-text measure | Kalshi | Polymarket |
|---|---:|---:|
| Contracts | 12,251 | 7,249 |
| Mean determinacy proxy | 0.624 | 0.610 |
| Source specificity | 0.550 | 0.518 |
| Temporal specificity | 0.619 | 0.812 |
| Outcome definition | 0.678 | 0.501 |
| Edge-clause completeness | 0.273 | 0.409 |
| Discretion clarity | 0.997 | 0.811 |
| Threshold-flag share | 82.1% | 23.7% |
| Mean analyzed text length (words) | 100.5 | 157.8 |

| Determinacy proxy within text strata | Kalshi | Polymarket |
|---|---:|---:|
| No threshold flag | 0.548 (n=2,191) | 0.575 (n=5,534) |
| Threshold flag | 0.640 (n=10,060) | 0.724 (n=1,715) |

These are raw proxy means in purposive sampled portfolios. Threshold flags come from the text measure and also enter its outcome-definition component; the strata describe composition rather than supply an independent validation or causal adjustment. Longer text and a higher component score do not establish better forecasting or more equivalent claims.

**Composition reversal:** Kalshi has the higher overall composite mean, while Polymarket has the higher mean in both threshold-flag strata. The overall ranking depends on the mix of contracts; it is not a general ranking of platform clarity.

- **Kalshi family structure:** 120 families; the five largest account for 46.2% of sampled contracts. Between-family differences account for 95.8% of the score sum of squares; 48 families (6,443 contracts) vary internally.
- **Polymarket family structure:** 2,634 families; the five largest account for 2.6% of sampled contracts. Between-family differences account for 99.1% of the score sum of squares; 145 families (1,048 contracts) vary internally.
Family units follow the APIs: Kalshi series and Polymarket events. Their different granularity means concentration and variance shares describe each sample; they do not rank platform diversity.

- Preferred cohort/exposure-adjusted determinacy–volume estimate: -0.129 (HC3 SE 0.009, p=2.49e-44, n=19,500).
- Within-family Kalshi estimate: -0.077 (clustered SE 0.082, p=0.342, n=6,443).
- Within-family Polymarket estimate: 0.030 (clustered SE 0.027, p=0.265, n=1,048).
- Contract-type split: qualitative -0.032 (SE 0.017, p=0.0625, n=7,725); quantitative -0.068 (SE 0.014, p=1.81e-06, n=11,775).
- Temporal/platform split: early kalshi -0.187; early polymarket -0.044; late kalshi -0.079; late polymarket -0.129.

These volume results are exploratory consequences, not the theory’s sole support. The tiny aligned-price panel does not identify a divergence effect.

## Locked decisions

- Keep determinacy (within contract) separate from divergence (between contracts).
- Require a witness state before labeling truth-condition divergence.
- Require a complete-rule audit for a probability restriction; no inclusion inference from a headline or one witness. Neither platform is classified as more Bayesian or as violating global evidential constancy.
- Keep automated text-distance scores as candidate diagnostics until validated coding exists.
- Exclude sports before Polymarket’s high-volume cap and control cumulative-volume exposure/cohort.

## Conference-paper focus

Use PAPER_OUTLINE.md: platform profiles, audited payout contrasts, and secondary activity associations. Keep case explanations accessible and distinguish hypothetical scenarios from realized events. The empirical/theory critic feedback and implemented decisions are recorded in ../docs/CRITIC_REVIEW.md. Common-horizon price comparisons are a future extension.
