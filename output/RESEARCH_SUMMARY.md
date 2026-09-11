# 1. Research question

How does the determinacy of a platform's machine-settleable representation of a future event shape participation and cross-platform agreement in digital prediction markets?

# 2. Theoretical mechanism

Prediction-market software does not receive a naturally fixed event state. Contract text, deadlines, sources, exceptions, and fallback procedures first define the state space. Determinacy can reduce interpretation costs, but indeterminacy can also create heterogeneous interpretations that stimulate speculative trade without improving accuracy. This is an Information Systems mechanism because representational design and platform governance condition downstream information aggregation.

# 3. Data

The reproducible public-API sample contains Kalshi: 12,251 contracts; Polymarket: 3,663 contracts. Opening dates run from 2021-06-30 through a latest observed resolution of 2026-09-10. The cross-platform matcher identifies 11 high-confidence metadata pairs; 3 currently have aligned daily histories. Volume units differ across platforms and are standardized within platform. The sample is intentionally focused on high-volume non-sports Kalshi series and high-volume closed Polymarket contracts, so it is not population-representative.

# 4. Measurement

The transparent 0–1 determinacy composite averages source specificity, temporal specificity, operational outcome definition, edge-case completeness, and absence of discretionary resolution language. Rule length and conditional-clause count remain separate complexity measures. For matched pairs, divergence combines wording, numeric/date conditions, named sources, required event stage, and closing-date distance. These are auditable proxies rather than validated latent-variable scales.

# 5. Main method

Market-level OLS relates standardized log volume to within-platform standardized determinacy with platform/category controls, market duration, and rule length. Alternatives separate conditional complexity, cluster uncertainty by series, and collapse repeated contracts to series/events. A Kalshi model tests last-trade absolute forecast error. Matching uses nearest-neighbor lexical retrieval followed by numeric, predicate, and date gates; price histories are aligned daily using only contemporaneous or earlier observations.

# 6. Main results

**Primary exploratory association.** A one-SD increase in within-platform determinacy is associated with -0.130 SD in log volume (HC3 SE 0.010, 95% CI [-0.150, -0.110], p=2.16e-37; n=15,914).
**Complexity-separated robustness.** Excluding edge-case completeness from the clarity score while directly controlling rule length and conditional clauses gives -0.195 SD (SE 0.012, p=3.33e-62).
**Platform heterogeneity.** Kalshi -0.126 (p=2.25e-27); Polymarket -0.144 (p=1.53e-11).
**Dependence robustness.** main_series_clustered: -0.130 (SE 0.061, p=0.033); event_series_aggregated: -0.103 (SE 0.039, p=0.00749).
**Forecast-error null.** For Kalshi's last traded price, determinacy predicts 0.006 probability points of absolute error per SD (series-clustered SE 0.006, p=0.318; n=10,400). This is not statistically distinguishable from zero.
**Matched-price limitation.** The first aligned panel is too small for a stable divergence regression; matched contracts are evidence-generating examples, not a confirmed average effect.

The robust inverse volume association is consistent with an ambiguity–activity mechanism: less determinate contracts may invite heterogeneous interpretations and more trade. It does not show better information aggregation, and the terminal-error null offers no accuracy benefit. Volume is a participation proxy, the associations are not causal, and high statistical visibility can partly reflect the large metadata sample.

# 7. Best empirical examples

- **Kalshi:** Donald Trump out before 2027? **Polymarket:** Will Donald Trump be the next leader out before 2027? Difference flagged: announcement can qualify on Kalshi but not alone on Polymarket; death treatment is explicit on only one platform; numeric/date conditions differ; named resolution sources differ; required event stage differs.
- **Kalshi:** Will Luiz Inácio Lula da Silva leave President of Brazil before Jan 1, 2027? **Polymarket:** Will Luiz Inácio Lula da Silva be the next leader out before 2027? Difference flagged: announcement can qualify on Kalshi but not alone on Polymarket; death treatment is explicit on only one platform; numeric/date conditions differ; named resolution sources differ; required event stage differs.
- **Kalshi:** Will the Fed cut rates 4 times? **Polymarket:** Will Fed cut interest rates 4 times in 2024? Difference flagged: one contract records a rule correction; numeric/date conditions differ; named resolution sources differ; required event stage differs.
- **Kalshi:** Will the Fed cut rates 5 times? **Polymarket:** Will Fed cut interest rates 5 times in 2024? Difference flagged: one contract records a rule correction; numeric/date conditions differ; named resolution sources differ; required event stage differs.

# 8. Best figures/tables

- `figures/views-conceptual-schematic.svg`: locates contract representation upstream of trading and resolution.
- `figures/views-determinacy-distribution.svg`: compares the score distribution across platforms.
- `figures/views-determinacy-volume.svg`: shows the raw within-platform volume gradient by score quintile.
- `figures/views-matched-trajectories.svg`: displays aligned prices for the most visibly divergent matched pairs when histories are available.
- `tables/analysis-market-models.csv`: reports the main and complexity-separated coefficients.
- `tables/matching-representative-pairs.csv`: provides auditable contract text and flagged semantic differences.

# 9. Information Systems paper storyline

**Phenomenon:** Platforms encode apparently similar uncertain events into contracts with measurably different semantic precision and truth conditions.

**Puzzle:** Aggregation accounts usually treat the event being priced as fixed, even though a digital platform must construct it first.

**Theoretical mechanism:** Determinate representations lower interpretive friction, while indeterminate ones can stimulate trade through interpretive disagreement; divergent representations can sustain rational price differences because the digital objects are not equivalent claims.

**Evidence:** Lower determinacy is robustly associated with more volume across both platforms and after complexity/dependence checks, but not with better terminal accuracy. Concrete matched contracts expose different rules alongside price paths where available.

**Contribution:** Digital systems structure the referents of collective intelligence, not merely the speed or accuracy with which information about those referents is processed.

# 10. Candidate paper titles

- Defining the Future: Semantic Determinacy and Information Aggregation in Digital Prediction Markets
- Before the Crowd Can Forecast: How Platforms Construct Predictable Events
- Same Future, Different Contract: Semantic Divergence in Prediction Markets
- Trading on Different Meanings: Semantic Indeterminacy in Prediction Markets
- The State Space Is the System: Representation and Collective Forecasting

# 11. Candidate abstract

Prediction markets are commonly understood as information systems that aggregate dispersed beliefs about future events. Yet the event is not a ready-made input: a platform must encode an uncertain real-world phenomenon as a machine-settleable digital contract. We theorize semantic determinacy—the degree to which real-world states map unambiguously onto formal outcomes—and divergence between contracts intended to represent the same event. Using reproducible public metadata and price histories from Kalshi and Polymarket, we construct transparent measures of source, temporal, definitional, edge-case, and discretion specificity. Across both platforms, lower determinacy is associated with greater trading volume after accounting for rule complexity, duration, category, and repeated series, consistent with an ambiguity–activity mechanism in which heterogeneous interpretations stimulate trade. Determinacy does not, however, predict Kalshi last-trade forecast error, cautioning against treating activity as aggregation quality. Precision-oriented matching further identifies same-event contracts with different deadlines, sources, and event stages. The study reframes prediction markets as systems that both define and aggregate information, showing that digital representation can generate participation without demonstrably improving accuracy and extending Information Systems theory on digital objects, information quality, and platform governance.

# 12. What remains before submission

## Essential next steps

- Human-validate a stratified sample of high-confidence, probable, and rejected matches and report precision.
- Expand price-history coverage and test spread, volatility, and fixed-horizon forecast error rather than relying on cumulative volume.
- Validate the determinacy components with independent coders or a cached structured annotation exercise.

## Robustness extensions

- Reweight repeated Kalshi series templates and cluster uncertainty at series/event level.
- Test alternative component weights, ambiguity lexicons, time windows, and liquidity thresholds.
- Separate quantitative threshold markets from qualitative event predicates.

## Optional nice-to-have analyses

- Reconstruct timestamped clarification events and examine non-causal event-time patterns.
- Add on-chain Polymarket trades and historical Kalshi bid/ask data for richer microstructure outcomes.
