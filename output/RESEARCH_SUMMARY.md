# Same Future, Different Claim

## 1. Research question and contribution

How do prediction-market platforms constitute digitally tradable and institutionally resolvable claims from ostensibly the same public-world phenomenon, and what consequences follow for participation and apparent disagreement?

The central contribution is upstream of aggregation: platform resolution architectures choose predicates, measurement conventions, temporal boundaries, evidence, exceptions, and fallback procedures. Markets with similar labels can therefore price non-equivalent digital claims. Apparent cross-market forecast disagreement can be rational disagreement about different state exposure.

## 2. Construct architecture

A contract is a possibly set-valued mapping from world histories to institutionally permissible settlements. **Semantic determinacy** is an intra-contract property: how uniquely a relevant world history maps to a settlement. **Semantic divergence** is an inter-contract property: whether two contracts about the same phenomenon map at least one plausible world history to different payouts or procedures.

The constructs are orthogonal. Two precise contracts can diverge (network call versus inauguration); two identically vague contracts can have low determinacy but little between-contract divergence. Automated wording, number, source, stage, and deadline distances retrieve candidates but are not treated as validated semantic equivalence measures.

## 3. Audited mechanism cases

- **2028 U.S. presidential winner — predicate-stage and temporal divergence.** Witness: All three networks call Rubio, but he dies or is disqualified before inauguration. Implied settlements: A = NO; B = YES.
- **September 2026 Federal Reserve decision — measurement, quantization, and fallback divergence.** Witness: The target-range upper bound falls by an unusual 12.5 bp. Implied settlements: A = NO under the literal exact-25-bp rule; B = YES because 12.5 bp rounds up to the 25-bp bucket.
- **Donald Trump leaving office before 2027 — stage, edge-case, and settlement-codomain divergence.** Witness: Trump announces a qualifying resignation date but remains in office past the deadline. Implied settlements: A = YES; B = NO.
- **U.S.–Ukraine minerals agreement — milestone-stage divergence.** Witness: Both governments announce an agreement, but no instrument is signed or adopted. Implied settlements: A = YES; B = NO.
- **Zelenskyy wearing a suit — category-boundary indeterminacy.** Witness: Zelenskyy wears a blazer and trousers that do not match, with no tie. Implied settlements: A = YES or NO: the rule does not uniquely classify the attire; B = N/A—witness to within-contract indeterminacy.

Every truth-condition divergence above has a witness state and predicted settlement on both sides. The suit case instead witnesses within-contract category indeterminacy. Exact archived rules and URLs are in `tables/representation-case-matrix.csv` and `REPRESENTATION_CASEBOOK.md`.

## 4. Data and sample correction

The reproducible official-API sample contains Kalshi: 12,251 contracts; Polymarket: 7,249 contracts. Openings begin 2020-10-09; the latest observed resolution is 2026-09-10. Polymarket sports contracts are excluded before its high-volume cap using official sports fields plus a conservative documented taxonomy. Volume remains cumulative and is standardized within platform; this purposive sample is not population-representative.

The automated matcher retains 15 high-confidence metadata pairs, dominated by repeated families. Only 2 pairs have aligned histories, all too sparse and homogeneous to test whether divergence predicts price wedges.

## 5. Measurement and method

The transparent determinacy proxy averages source specificity, temporal specificity, operational definition, edge-case completeness, and discretion clarity. Calendar years no longer count as quantitative thresholds. Leave-one-component-out models, direct ambiguity counts, and qualitative/quantitative splits expose score dependence.

Volume models compare the original baseline with a preferred retrieval-capped exposure/opening-cohort specification, resolved-only samples, family-clustered uncertainty, family aggregation, and within-family demeaning. The within-family estimates remove stable Kalshi-series or Polymarket-event popularity but are supported by relatively few families with internal semantic variation.

## 6. Empirical results

- **Baseline association:** one within-platform SD more measured determinacy corresponds to -0.160 (HC3 SE 0.009, p=7.27e-67, n=19,500) SD in log volume.
- **Preferred cohort/exposure specification:** replacing scheduled duration with observed exposure and adding opening-year controls gives -0.115 (HC3 SE 0.009, p=2.16e-35, n=19,500).
- **Resolved contracts only:** -0.107 (HC3 SE 0.009, p=1.48e-29, n=18,312).
- **Within-family Kalshi:** -0.035 (family-clustered SE 0.066, p=0.597, n=6,443). This estimand uses only families whose determinacy varies internally.
- **Within-family Polymarket:** 0.031 (family-clustered SE 0.027, p=0.262, n=1,043). This estimand uses only families whose determinacy varies internally.
- **Contract-type heterogeneity:** qualitative -0.023 (SE 0.018, p=0.198, n=7,725); quantitative -0.049 (SE 0.014, p=0.00048, n=11,775).
- **Direct ambiguity lexicon check:** one SD more flagged ambiguity terms corresponds to -0.024 (SE 0.011, p=0.0372, n=19,500) SD in log volume.
- **Temporal replication split (July 1, 2025):** early kalshi -0.179 (SE 0.024, p=3.48e-14, n=3,295); early polymarket -0.021 (SE 0.035, p=0.538, n=2,189); late kalshi -0.068 (SE 0.011, p=2.74e-09, n=7,784); late polymarket -0.134 (SE 0.019, p=2.9e-12, n=5,060). This is a stability diagnostic, not a preregistered holdout test.
- **Forecast-error diagnostic:** 0.011 (series-clustered SE 0.007, p=0.146, n=10,400). The coefficient is not a fixed-horizon accuracy comparison and a null is not evidence of equivalence.

- **Interpretation:** the inverse association is concentrated in quantitative-threshold contracts; the qualitative-contract estimate is not distinguishable from zero. This is more consistent with threshold-family composition than with a general ambiguity–activity effect.
- **Interpretation:** directly flagged ambiguous language is associated with less, not more, activity after controls, so the current metadata do not directly support the heterogeneous-interpretation mechanism.
- **Interpretation:** neither platform has a detectable within-family determinacy coefficient. The pooled result is therefore primarily a between-family pattern.
- **Platform-time heterogeneity:** the inverse pattern is strong in early Kalshi but absent in early Polymarket, then weaker in later Kalshi and strong in later Polymarket. This crossover argues against a timeless platform-general law and points toward evolving contract-family composition or governance.

The between-contract pattern is consistent with interpretive latitude increasing activity, but attention, salience, placement, and template composition remain plausible alternatives. Weak or null within-family results would sharply limit an ambiguity-causes-trading interpretation without weakening the directly demonstrated representational phenomenon.

## 7. Information Systems storyline

- **Phenomenon:** nearly identical market labels can expose traders to different platform-defined claims.
- **Puzzle:** aggregation accounts often treat the proposition being priced as fixed before it enters the information system.
- **Mechanism:** resolution architectures partition world histories through predicate selection, operationalization, boundary rules, adjudication, and fallback.
- **Evidence:** witness-state cases demonstrate non-equivalence; systematic metadata document determinacy variation; volume associations supply secondary exploratory consequences.
- **Contribution:** collective-intelligence systems govern the referents of aggregation, not only information processing about those referents.

## 8. Best outputs

- `tables/representation-case-matrix.csv`: exact rules, signatures, witness states, and implied settlements.
- `REPRESENTATION_CASEBOOK.md`: plain-language explanations of the striking cases.
- `figures/views-conceptual-schematic.svg`: platform-specific resolution architectures and distinct claims.
- `tables/analysis-market-models.csv`: baseline, cohort/exposure, market-type, leave-one-out, and within-family estimates.
- `figures/views-determinacy-volume.svg`: descriptive score–volume pattern; not a causal figure.

## 9. Candidate abstract

Prediction markets are commonly treated as information systems that aggregate beliefs about fixed future events. Yet platforms first constitute the claims whose probabilities they elicit. We distinguish semantic determinacy within a contract from semantic divergence between contracts and analyze official Kalshi and Polymarket metadata. Audited cases identify plausible world histories in which markets bearing similar labels settle differently because of event-stage, measurement, temporal, evidentiary, or fallback choices. A corrected non-sports sample and transparent text measures also show how determinacy covaries with cumulative trading activity, while exposure/cohort and within-family specifications reveal the limits of a causal ambiguity–activity interpretation. The study shifts attention from how collective-intelligence systems process information to how their resolution architectures govern the referents of aggregation.

## 10. Next decisive tests

- Human-code representation signatures and witness states for a stratified, phenomenon-diverse match sample with independent reliability checks.
- Match public-world phenomena before comparing claims, so divergent deadlines or thresholds do not prevent candidate retrieval.
- Acquire fixed first-30-day volume, common-horizon prices, spread, and volatility rather than relying on cumulative lifetime volume.
- Expand cross-platform history coverage before estimating a divergence–price-wedge relationship.
