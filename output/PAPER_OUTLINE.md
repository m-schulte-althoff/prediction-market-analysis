# Same Future, Different Claim: How Prediction Markets Define What Counts

Working ICIS conference-paper outline. Lead with observable differences in contract rules, explain why these matter for collective intelligence, and use activity associations as a secondary result.

## 1. Introduction

- **Motivation:** similar market headlines invite readers to treat their displayed probabilities as forecasts of the same event. Yet finishing first and advancing to the next round are different bets.
- **Opening example:** a candidate who finishes second loses a first-place contract but wins an advancement contract under a top-two rule. A called election winner who never takes office likewise separates media-call and inauguration contracts.
- **Theoretical shortcoming:** aggregation-focused explanations leave the constitution of the priced claim in the background. Position this as an upstream complement; do not claim that prior research universally ignores contract design.
- **RQ:** How do prediction-market resolution architectures differentiate claims about the same public phenomenon, and how do determinacy and trading activity vary across the sampled market portfolios?
- **Methods:** official Kalshi/Polymarket metadata for 19,500 contracts, 6 purposively selected archived-rule cases, transparent rule-text measures, descriptive platform comparisons, and a small main-text set of exploratory volume estimates.
- **Contribution:** distinguish semantic differentiation as a design process, divergence between resulting claims, and determinacy within each claim. Explain why explicit rules can still price different state exposure.

## 2. Literature and conceptual framework

- **Prediction markets and collective intelligence:** connect information aggregation and forecast evaluation to the proposition the market actually prices.
- **IS representation and classification:** connect digital categories and operational definitions to what observable circumstances count as an outcome.
- **Platform governance and adjudication:** explain evidence authorities, time boundaries, exceptions, fallback procedures, and settlement methods as contract-design choices.
- **Constructs:** differentiation selects what/when/whose evidence counts; determinacy concerns one contract's mapping from a scenario to settlement; divergence concerns differences between two such mappings. A procedural difference alone need not imply a payout difference.
- **Core argument:** two precise contracts can disagree about what success means. Unclear category boundaries, such as ‘suit,’ present a separate interpretive problem.

Meehan and Zhang's [*Bayes Is Back* (2025)](https://doi.org/10.1215/00318108-11873775) studies updating within a given prior space `(S, π)` and a represented strongest evidence proposition. Non-contrastiveness holds the posterior fixed across learning situations with the same prior space and learned proposition; global evidential constancy also holds it fixed across states with that evidence. This invariance does not by itself single out conditionalization. Their distinction between accuracy in one learning situation and total expected accuracy across learning situations supports an argument about updating rules, not a test of platform design (supplied manuscript §§2, 4–5; [source audit](../docs/BAYES_SOURCE_AUDIT.md)).

**Our IS extension:** let `Ω` be relevant possible world histories, `e` represented evidence with positive prior probability, and `μ_e = P(· | e)` the posterior over histories. The platform specifies a settlement mapping. For a determinate binary contract, `r_c: Ω → {0,1}` and `Y_c = {ω: r_c(ω)=1}`. Applying the posterior gives `q_c(e) = E_{μ_e}[r_c] = P(Y_c | e)`. The platform defines the claim; evidence updates beliefs about worlds; traders value that claim and markets aggregate valuations into prices. These are analytically distinct functions, not a claim that platforms do Bayesian updating or that rules must chronologically precede all learning.

Thus `q_A − q_B = μ_e(Y_A \ Y_B) − μ_e(Y_B \ Y_A)`: identical world beliefs can justify different claim probabilities. Different sets need not have different probability mass; the claim is a possibility, not a necessary price gap. Validated equivalence, inclusion, disjointness and complementarity imply exact probability restrictions under a common distribution. A single witness establishes non-equivalence, not inclusion. Price analogues additionally assume a probability-price approximation and sufficiently comparable conditions.

**Determinacy remains intra-contract:** a nonempty set-valued mapping `R_c(ω) ⊆ {0,1}` can leave both payouts permissible at a borderline state. Uncertainty about which world obtains is epistemic; an unresolved institutional mapping concerns what counts as a payout in that world. The suit text alone does not select a garment-level payoff mapping; credible-reporting adjudication completes it. A unique claim event, and hence a point probability derived from that event, cannot simply be assumed. Positive posterior mass on unresolved states can make expected payout depend on completion; zero mass need not. A model of adjudication would add assumptions. Fractional tie/death payouts instead require `r_c: Ω → [0,1]`: expected payout is then not generally a YES-event probability. A fractional but specified payout is not itself indeterminacy.

- **Theoretical implication:** under shared beliefs and otherwise comparable pricing conditions, different payout mappings can have different expected payoffs. A price gap need not be a disagreement about the same event; the current study does not estimate that mechanism in prices.
- **Exhibit:** conceptual schematic plus the compact determinacy/divergence matrix in `../docs/CONSTRUCTS.md`. These literature streams are an outline for a sourced literature section, not a completed literature review.

## 3. Method

- **Data and selection:** immutable September 10, 2026 official-API snapshots for this reproduction; purposive Kalshi series and volume-selected Polymarket contracts, with sports excluded before its cap. Report platform counts and coverage from `tables/preprocessing-coverage.csv`.
- **Units:** contract for text profiles and activity; Kalshi series or Polymarket event for family structure; a contract pair for payout divergence; one contract for the suit category example. Family granularities differ across APIs.
- **Text measurement:** source, temporal, outcome-definition, edge-clause, and discretion proxies averaged on a 0–1 scale. Recognize ET in clock context. Scores describe archived textual specification, not a validated scale of all institutional determinacy.
- **Platform comparisons:** report raw components, text length, threshold-flag composition, and composite means inside each flag group. Since the flag enters the score, these strata reveal composition rather than independently validate the measure.
- **Case method:** preserve exact rules and links; specify a hypothetical scenario, the decisive qualifying condition, implied settlements, and the interpretation boundary. These cases show how divergence can occur, not its population frequency or realized financial impact.
- **Coherence method:** audit the entire archived mapping, including cancellation, ties and death allocation, before assigning a logical relation. Audits are fingerprint-bound to IDs and rule text. Overlap/non-nesting needs witnesses in both differences and the intersection; one separating state never proves inclusion. Separately validated fresh synchronized YES prices are required for any price diagnostic.
- **Retrieval:** retrieve shared phenomena before screening claim compatibility. First-place/advancement and departure/first-departure pairs remain useful cases while being excluded from high-confidence claim candidates.
- **Activity:** standardize log cumulative volume and determinacy within platform; control observed exposure, opening year, text length, category, and platform. Report the preferred association and one within-family diagnostic per platform; leave existing additional checks in supplementary tables.
- **Scope:** sparse matched histories cannot support a divergence–price-wedge estimate. No extensive new robustness program is needed for the descriptive mechanism contribution.

## 4. Results

- **4.1 Different portfolios of claims:** compare the component profiles and contract-type mix. Explain the conditional composite comparison using the table below; avoid a global platform-quality ranking.
- **4.2 Same recognizable issue, different payable claim:** use the primary and election cases as entry points, followed by Fed rounding, the minerals milestone, and the competing-leader departure condition.
- **4.3 What counts as a suit?:** separate within-contract category interpretation from between-contract differentiation. Authentic images and explicit dates need not define the clothing category.
- **Representation-aware implications:** the election and minerals cases support overlap without nesting; neither yields an extra marginal restriction. Fed nesting is unclassified; primary ties and leader death allocations prevent a globally binary reading. The suit mapping requires institutional completion. Current coherence tests are not estimable: the legacy panel supplies neither manual relation validation nor fresh synchronized quote evidence.
- **4.4 Trading activity across claim portfolios:** report the preferred volume association, contract-type estimates, and the within-family boundary. The evidence does not establish that ambiguity causes participation.

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

### Case exhibit: scenario → qualifying condition → settlement

- **2028 U.S. presidential winner** (cross-platform): Winning the news call and actually taking office are different milestones.
  Hypothetical scenario: All three networks call Rubio, but he dies or is disqualified before inauguration. A (Kalshi) = NO; B (Polymarket) = YES.
  Interpretation boundary: The scenario assumes all three calls occur before inauguration; it is not an observed election outcome.
- **September 2026 Federal Reserve decision** (cross-platform): Even numerical markets need a rule for assigning an unusual measurement to an answer bucket.
  Hypothetical scenario: The target-range upper bound falls by an unusual 12.5 bp. A (Kalshi) = NO under the literal exact-25-bp rule; B (Polymarket) = YES because 12.5 bp rounds up to the 25-bp bucket.
  Interpretation boundary: The witness isolates rounding under the archived literal Kalshi wording. Cancellation and no-statement fallbacks also differ, but are not tested by this scenario.
- **Donald Trump leaving office versus being the next leader out** (cross-platform): Leaving office at some point and being the first listed leader to leave are different bets.
  Hypothetical scenario: Before the deadline, Trump announces a non-term-limit resignation within the next year but stays in office through 2026. No listed leader leaves by December 31, 2026, 11:59 PM ET. A (Kalshi) = YES; B (Polymarket) = NO.
  Second scenario: Another listed leader permanently leaves first; Trump subsequently resigns and permanently leaves before 2027, without dying. A = YES; B = NO.
  Interpretation boundary: The primary witness separates announcement from actual departure. The second isolates competition with other leaders. Kalshi's death-allocation clause is an additional rule feature, not demonstrated by either witness.
- **U.S.–Ukraine minerals agreement** (within-platform across successive contracts): Saying 'we have a deal' and signing the deal are different milestones.
  Hypothetical scenario: On March 31, 2025 before 11:59 PM ET, both governments announce a deal explicitly involving Ukrainian rare earths. No qualifying mineral deal is signed, enacted, or formally adopted through April 30, 2025, 11:59 PM ET. A (Polymarket) = YES; B (Polymarket) = NO.
  Interpretation boundary: Successive Polymarket contracts also differ in dates, rare-earth versus mineral scope, and evidence sources. The witness specifies rare earths and both windows; this is not a synchronized cross-platform comparison.
- **Tom Steyer finishing first versus advancing in the California primary** (cross-platform; retrieved from systematic sample): A runner-up can lose the contest for first place and still qualify for the next round.
  Hypothetical scenario: Steyer finishes second without a tie in the June 2, 2026 primary and advances to the general election. A (Kalshi) = NO; B (Polymarket) = YES.
  Interpretation boundary: This is a hypothetical second-place scenario, not a claim about the observed primary result. Similar headlines retrieved the pair; different success conditions prevent a claim-equivalence label.
- **Zelenskyy wearing a suit** (within-contract): People can see the same clothing and still disagree about whether it counts as a suit.
  Hypothetical scenario: During May 22–June 30, 2025, authentic images are taken and released showing Zelenskyy in a blazer and nonmatching trousers, without a tie. Credible reports differ on whether this counts as a suit. A (Polymarket) = not fixed by garment criteria alone; depends on the credible-reporting adjudication; B (Hypothetical world state) = N/A—witness to within-contract indeterminacy.
  Interpretation boundary: The archived text specifies image authenticity and timing but no garment definition. It delegates to credible reporting; this case does not document an actual dispute or prove the final institutional outcome remains indeterminate.

Exact clauses and URLs: [casebook](REPRESENTATION_CASEBOOK.md).

### Compact activity exhibit

- Preferred exposure/cohort association: -0.129 (HC3 SE 0.009, p=2.49e-44, n=19,500) SD of log volume per one within-platform SD of the score.
- Within-family Kalshi: -0.077 (family-clustered SE 0.082, p=0.342, n=6,443). Uses one SD of residual score in internally varying families, so coefficient magnitude is not on the pooled score scale.
- Within-family Polymarket: 0.030 (family-clustered SE 0.027, p=0.265, n=1,048). Uses one SD of residual score in internally varying families, so coefficient magnitude is not on the pooled score scale.
- No threshold flag: -0.032 (HC3 SE 0.017, p=0.0625, n=7,725). Separate significance levels do not test whether the two coefficients differ.
- Threshold flag: -0.068 (HC3 SE 0.014, p=1.81e-06, n=11,775). Separate significance levels do not test whether the two coefficients differ.

- **Main exhibits:** (1) conceptual schematic; (2) sampled platform profile table/figure; (3) compact case matrix; (4) preferred activity estimate and within-family diagnostic. Keep the full model inventory in supplementary outputs.

## 5. Discussion and conclusion

- **Answer to the RQ:** platforms differentiate claims through success predicates, milestones, measurement buckets, time and evidence boundaries, and competing outcomes. The sampled portfolios also differ in their mix and textual specification.
- **Theoretical contribution:** collective-intelligence systems help define what information is aggregated about. Clear specification and equivalent claims are separate achievements.
- **Empirical contribution:** auditable ordinary scenarios connect the conceptual distinction to platform rules; component and composition profiles extend beyond isolated anecdotes; volume estimates show an associated portfolio pattern.
- **Design implications:** show ‘what must happen to pay Yes,’ relevant deadlines, measurement conventions, and evidence rules beside similar headlines. Flag first-place versus advancement and individual versus first departure when comparing probabilities. These are proposed implications, not evaluated interventions.
- **Boundaries:** purposive samples, API family granularity, a text proxy, hypothetical rule-based cases, and cumulative activity constrain generalization and causal claims. Keep this concise and tied to what the paper actually claims.
- **Focused extension:** the implemented coherence module makes tests on validated binary equivalence, nesting, disjointness or complementarity possible once fresh synchronized prices and comparable market conditions exist. Numerical excess is conditional on a probability-price approximation, not proof of Bayesian irrationality or a causal divergence effect.
- **Closing message:** before asking whose forecast is right, establish what would have to happen for each contract to pay.
