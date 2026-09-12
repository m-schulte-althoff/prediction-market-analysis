# Same Future, Different Claim

## 1. Research question and contribution

How do prediction-market resolution architectures differentiate claims about the same public phenomenon, and how do determinacy and trading activity vary across the sampled market portfolios?

The central contribution is upstream of aggregation: platform resolution architectures choose predicates, measurement conventions, temporal boundaries, evidence, exceptions, and fallback procedures. Markets with similar labels can therefore price non-equivalent digital claims. Apparent cross-market forecast disagreement can be rational disagreement about different state exposure.

## 2. Construct architecture

**Semantic differentiation** is the process of selecting what counts, when it counts, and whose evidence counts. **Divergence** describes differences between the resulting claims; **determinacy** describes clarity within one claim. More explicit contracts need not be equivalent contracts.

A contract is a possibly set-valued mapping from world histories to institutionally permissible settlements. **Semantic determinacy** is an intra-contract property: how uniquely a relevant world history maps to a settlement. **Semantic divergence** is an inter-contract property: whether two contracts about the same phenomenon map at least one plausible world history to different payouts or procedures.

The constructs are orthogonal. Two precise contracts can diverge (network call versus inauguration); two identically vague contracts can have low determinacy but little between-contract divergence. Automated wording, number, source, stage, and deadline distances retrieve candidates but are not treated as validated semantic equivalence measures.

## 3. Audited mechanism cases

- **2028 U.S. presidential winner — predicate-stage and temporal divergence.** Winning the news call and actually taking office are different milestones. Scope: cross-platform. Hypothetical witness: All three networks call Rubio, but he dies or is disqualified before inauguration. Implied settlements: Kalshi = NO; Polymarket = YES.
- **September 2026 Federal Reserve decision — measurement-bucket divergence (rounding).** Even numerical markets need a rule for assigning an unusual measurement to an answer bucket. Scope: cross-platform. Hypothetical witness: The target-range upper bound falls by an unusual 12.5 bp. Implied settlements: Kalshi = NO under the literal exact-25-bp rule; Polymarket = YES because 12.5 bp rounds up to the 25-bp bucket.
- **Donald Trump leaving office versus being the next leader out — departure-stage and competing-leader divergence.** Leaving office at some point and being the first listed leader to leave are different bets. Scope: cross-platform. Hypothetical witness: Before the deadline, Trump announces a non-term-limit resignation within the next year but stays in office through 2026. No listed leader leaves by December 31, 2026, 11:59 PM ET. Implied settlements: Kalshi = YES; Polymarket = NO.
  Additional witness: Another listed leader permanently leaves first; Trump subsequently resigns and permanently leaves before 2027, without dying. A = YES; B = NO.
- **U.S.–Ukraine minerals agreement — milestone-stage divergence.** Saying 'we have a deal' and signing the deal are different milestones. Scope: within-platform across successive contracts. Hypothetical witness: On March 31, 2025 before 11:59 PM ET, both governments announce a deal explicitly involving Ukrainian rare earths. No qualifying mineral deal is signed, enacted, or formally adopted through April 30, 2025, 11:59 PM ET. Implied settlements: Polymarket = YES; Polymarket = NO.
- **Tom Steyer finishing first versus advancing in the California primary — rank versus qualification divergence.** A runner-up can lose the contest for first place and still qualify for the next round. Scope: cross-platform; retrieved from systematic sample. Hypothetical witness: Steyer finishes second without a tie in the June 2, 2026 primary and advances to the general election. Implied settlements: Kalshi = NO; Polymarket = YES.
- **Zelenskyy wearing a suit — category-boundary indeterminacy.** People can see the same clothing and still disagree about whether it counts as a suit. Scope: within-contract. Hypothetical witness: During May 22–June 30, 2025, authentic images are taken and released showing Zelenskyy in a blazer and nonmatching trousers, without a tie. Credible reports differ on whether this counts as a suit. Implied settlements: Polymarket = not fixed by garment criteria alone; depends on the credible-reporting adjudication; Hypothetical world state = N/A—witness to within-contract indeterminacy.

The archived rules are observed evidence; these scenarios are hypothetical, not records of realized settlements. Payout-divergence cases specify outcomes on both sides. The suit case illustrates an unspecified category boundary with an adjudication procedure. Exact rules, source links, and case-specific audit boundaries are in `tables/representation-case-matrix.csv` and `REPRESENTATION_CASEBOOK.md`.

## 4. Data and sample correction

The reproducible official-API sample contains Kalshi: 12,251 contracts; Polymarket: 7,249 contracts. Openings begin 2020-10-09; the latest observed resolution is 2026-09-10. Polymarket sports contracts are excluded before its high-volume cap using official sports fields plus a conservative documented taxonomy. Volume remains cumulative and is standardized within platform; this purposive sample is not population-representative.

The automated matcher retains 11 high-confidence metadata pairs, dominated by repeated families. Only 2 pairs have aligned histories, all too sparse and homogeneous to test whether divergence predicts price wedges.

## 5. Measurement and method

The transparent determinacy proxy averages source specificity, temporal specificity, operational definition, edge-case completeness, and discretion clarity. Calendar years no longer count as quantitative thresholds. Leave-one-component-out models, direct ambiguity counts, and qualitative/quantitative splits expose score dependence.

Volume models compare the original baseline with a preferred retrieval-capped exposure/opening-cohort specification, resolved-only samples, family-clustered uncertainty, family aggregation, and within-family demeaning. The within-family estimates remove stable Kalshi-series or Polymarket-event popularity but are supported by relatively few families with internal semantic variation.

## 6. Empirical results

### Sampled platform rule profiles

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

### Secondary trading-activity evidence

- **Preferred cohort/exposure specification:** replacing scheduled duration with observed exposure and adding opening-year controls gives -0.129 (HC3 SE 0.009, p=2.49e-44, n=19,500).
- **Within-family Kalshi:** -0.077 (family-clustered SE 0.082, p=0.342, n=6,443). This estimand uses only families whose determinacy varies internally.
- **Within-family Polymarket:** 0.030 (family-clustered SE 0.027, p=0.265, n=1,048). This estimand uses only families whose determinacy varies internally.
- **Contract-type estimates:** no threshold flag -0.032 (SE 0.017, p=0.0625, n=7,725); threshold flag -0.068 (SE 0.014, p=1.81e-06, n=11,775).

- **Contract-type interpretation:** the threshold-flag estimate is negative and distinguishable from zero; the no-flag estimate is not. These separate significance tests do not establish that the two coefficients differ.
- **Lexicon interpretation:** the coefficient for words such as ‘deal’ and ‘agreement’ is nonpositive. These are text flags, not observations of traders interpreting a contract differently.
- **Family interpretation:** neither platform has a detectable within-family coefficient. Read the pooled association alongside the strong concentration of score variation between families. Within-family coefficients use one SD of the varying-family residual score and are not directly comparable in magnitude to the pooled coefficient.
- **Platform-time diagnostic:** the period-specific estimates vary. These exploratory splits do not isolate a change in platform governance or establish a difference by comparing significance levels.

Trading activity varies across portfolios of differently specified claims; the available associations do not isolate an effect of ambiguity itself. The paper's central result is the documented difference in what contracts require for a payout.

## 7. Information Systems storyline

- **Phenomenon:** nearly identical market labels can expose traders to different platform-defined claims.
- **Puzzle:** aggregation accounts often treat the proposition being priced as fixed before it enters the information system.
- **Mechanism:** resolution architectures partition world histories through predicate selection, operationalization, boundary rules, adjudication, and fallback.
- **Evidence:** witness-state cases demonstrate non-equivalence; systematic metadata document determinacy variation; volume associations supply secondary exploratory consequences.
- **Contribution:** collective-intelligence systems govern the referents of aggregation, not only information processing about those referents.
- **Memorable finding:** a second-place finish can lose a first-place contract and win an advancement contract. Clear resolution rules can still define different claims.

## 8. Best outputs

- `tables/representation-case-matrix.csv`: exact rules, signatures, witness states, and implied settlements.
- `REPRESENTATION_CASEBOOK.md`: plain-language explanations of the striking cases.
- `PAPER_OUTLINE.md`: five-section ICIS paper outline, with current estimates and exhibits.
- `tables/analysis-platform-profiles.csv` and `figures/views-platform-rule-profiles.svg`: component differences, contract mix, and conditional score comparisons.
- `figures/views-conceptual-schematic.svg`: platform-specific resolution architectures and distinct claims.
- `tables/analysis-market-models.csv`: baseline, cohort/exposure, market-type, leave-one-out, and within-family estimates.
- `figures/views-determinacy-volume.svg`: descriptive score–volume pattern; not a causal figure.

## 9. Candidate abstract

Prediction markets aggregate beliefs about claims that their platforms first define. We distinguish semantic differentiation through contract design, determinacy within a contract, and divergence between contracts. Official Kalshi and Polymarket metadata reveal different profiles of rule specification and contract composition. Archived-rule cases show how finishing first versus advancing, media calls versus inauguration, numerical rounding, qualifying announcements, and competing departures can imply different payouts under the same hypothetical scenario. A separate clothing-category case illustrates interpretive latitude within a written rule. Exploratory volume associations describe activity across claim portfolios. The study explains how collective-intelligence systems govern what counts as the event being forecast, making explicit specification and cross-market comparability separate design concerns.

## 10. Conference-paper scope

- Lead with understandable rule contrasts, the multidimensional platform profiles, and contract-composition patterns.
- Use the preferred volume association and within-family diagnostic as secondary evidence; keep remaining checks in the tables and research log.
- Audit the quoted case clauses when preparing the submission. Independent coding is a useful extension, not a reason to suspend the current mechanism paper.
- Reserve common-horizon prices on manually checked claims for a subsequent test of the price-wedge implication.

## 11. Supplementary diagnostics

- **Baseline association:** one within-platform SD more measured determinacy corresponds to -0.178 (HC3 SE 0.009, p=1.22e-82, n=19,500) SD in log volume.
- **Resolved contracts only:** -0.122 (HC3 SE 0.009, p=2.02e-38, n=18,312).
- **Direct ambiguity lexicon check:** one SD more flagged ambiguity terms corresponds to -0.024 (SE 0.011, p=0.0372, n=19,500) SD in log volume.
- **Temporal replication split (July 1, 2025):** early kalshi -0.187 (SE 0.023, p=1.36e-15, n=3,295); early polymarket -0.044 (SE 0.034, p=0.187, n=2,189); late kalshi -0.079 (SE 0.011, p=3.54e-12, n=7,784); late polymarket -0.129 (SE 0.019, p=2.21e-11, n=5,060). This is a stability diagnostic, not a preregistered holdout test.
- **Forecast-error diagnostic:** 0.013 (series-clustered SE 0.009, p=0.137, n=10,400). The coefficient is not a fixed-horizon accuracy comparison and a null is not evidence of equivalence.
