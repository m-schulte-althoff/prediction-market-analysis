# Same Future, Different Claim: How Prediction Markets Define What Counts

Working ICIS conference-paper outline, revised under approved P1–P7. Main evidence: observed settlements and adjudication; sampled literal text features provide context. Activity estimates are supplementary.

## 1. Introduction

Steve Hilton finished second in California's June 2, 2026 gubernatorial primary and advanced under the top-two rule. The archived first-place Kalshi contract settled NO/$0; the Polymarket advancement contract recorded resolved YES. The result concerns one election, yet the contracts reward different achievements.

- **Research question:** When do apparently similar prediction-market questions expose traders to different settlements, and when do written rules leave a scenario to later interpretation?
- **Puzzle:** the market headline identifies a public phenomenon; operative clauses select an achievement, deadline, evidence source, exception and payout amount. Comparisons of displayed prices depend on those selections.
- **Contribution:** a diagnostic account grounded in linked event/rule/settlement records. It distinguishes ordinary achievement conditions, fractional exceptions and delegated interpretation; it estimates no causal price mechanism or trader-comprehension effect.

## 2. Literature and constructs

[Wolfers and Zitzewitz (2004)](https://doi.org/10.1257/0895330041371321) already discuss payoff design, clear specification and adjudication. [Wand and Weber (1993)](https://doi.org/10.1111/j.1365-2575.1993.tb00127.x) relate representational clarity to interpretation mappings. [Eriksson and Öhlund (2024)](https://doi.org/10.17705/1jais.00845) show how constitutive rules create digitally represented institutional entities and rights. Here the observable objects are contract clauses and settlements; published text does not identify designers' motives.

[Gebele and Matthes (2026)](https://arxiv.org/abs/2601.01706) directly study resolution semantics, payoff regions and cross-platform comparison. [Capponi, Gliozzo and Zhu (2025)](https://arxiv.org/abs/2512.02436) develop automated relationship discovery. Their preprints supply close comparisons; their empirical performance is not independently replicated here. This paper's diagnostic contribution is the joined audit of separating scenarios, fractional settlement and delegated interpretation. It makes no priority claim for payoff mappings or event-equivalence checks.

[Wang (2026)](https://doi.org/10.1016/j.econlet.2026.113176) examines event occurrence versus pending adjudication; the review accessed an abstract, highlights and section passages, rather than the complete paywalled article. [Nechepurenko (2026)](https://arxiv.org/abs/2609.15368) distinguishes proposals, disputes, oracle settlement and adapter completion in a recent preprint. These distinctions guide the case chronology and prevent treating closure timestamps as a full settlement history. The Rezaei Sanjabi working paper remains an abstract-only lead; its empirical findings are not adopted.

**Payoff divergence** requires an explicitly specified scenario with different payouts. **Written-rule determinacy** asks whether the rule version uniquely determines the payout given the information held fixed. A complete eventual adjudication and an incomplete written garment criterion are compatible. Semantic differentiation describes observed rule dimensions; motives and design processes require additional evidence.

The rules define which outcomes pay. Traders use evidence to assess those outcomes, and trading produces market prices. These functions can develop together over time.

With a common distribution `μ` over relevant histories, the value of a specified normalized payout is `q_c = E_μ[r_c]`. Thus `q_A − q_B = E_μ[r_A − r_B]`. The identity holds for any common probability distribution. Different payout mappings can have different expected values, although non-equivalence alone does not guarantee a value difference.

For binary payouts, expected payout equals the probability of the paying event. Fractional settlement requires the payout amount: a 20% chance of a full dollar and a 30% chance of 50 cents give an expected payout of 35 cents. This is a synthetic illustration.

Where rules delegate interpretation, valuation can include expectations about how a later decision will be made. A rule may leave a clothing category unspecified while the institution ultimately records a definite settlement. Price-based clauses require past-price inputs in the modeled history. The formal qualifications and binary-event restrictions are in [constructs](../docs/CONSTRUCTS.md).

## 3. Method

- **Case audit:** bind assertions to complete operative inputs, stable platform identifiers and source versions. For realized splits, verify both contract settlements and an independent event source. Separate observed events, observed settlements, dispute chronology and hypothetical payout witnesses. Changed operative inputs block stale assertions pending re-audit.
- **Sample and provenance:** freeze the historical 19,500 rows for before/after measurement comparison. Report flawed historical selection and absent acquisition timestamps. Preserve raw data and distinguish normalization attrition from acquisition exclusions.
- **Text features:** report authority, date/time, definition/threshold, edge-clause and discretion-term cues literally. The legacy composite is exploratory. Four bounded parser repairs and field-placement invariance are documented; no human inter-coder validation is claimed.
- **Supplementary methods:** use the exact exposure/opening-cohort formula with platform-qualified family clusters. Compare HC3 on identical rows; retain existing within-family diagnostics with their distinct scale. Daily price alignment supplies no synchronized-price test.

## 4. Results

### Steve Hilton: first place versus advancing in the California primary

- **Evidence:** observed event and recorded final settlement contrast
- **Scenario:** Steve Hilton finished second in the June 2, 2026 California primary and advanced to the general election. Certified results place Becerra first (28.0%), Hilton second (24.6%) and Steyer third (22.8%).
- **Qualifying condition:** A — first place in the primary; proportional payout for exact ties; B — advance to the general election; the top two candidates qualify.
- **Settlement:** A — NO; recorded normalized settlement $0; B — resolved YES; normalized payout $1.
- **Implication:** Finishing second loses the first-place contract and wins advancement.
- **Boundary:** Both records are in the September-labelled sample and match the preserved October follow-up on operative fields. They have different cutoff/fallback conditions; exact ties make Kalshi's full payout mapping fractional. This realized contrast establishes no price error or trader misunderstanding.
- **Contracts:** [KXCAGOVPRIMARY1ST-26JUN02-1ST-SHIL](https://kalshi.com/markets/kxcagovprimary1st-26jun02-1st-shil); [825460](https://polymarket.com/event/will-steve-hilton-get-the-first-or-second-most-votes-in-the-2026-california-governor-primary-election).
- **Chronology:** June 2, 2026: primary; June 10 20:05:30 UTC: Polymarket closure record; July 11 00:39:59.561815 UTC: Kalshi settlement timestamp.
- **Independent event evidence:** [June 2, 2026 primary: Becerra 28.0%, Hilton 24.6%, Steyer 22.8%; Hilton second.](https://elections.cdn.sos.ca.gov/sov/2026-primary/sov/06-sov-summary.pdf).

### Ali Khamenei departure: price-based death allocation versus YES

- **Evidence:** observed departure episode and recorded final settlement contrast
- **Scenario:** Following the February 28, 2026 attack, contemporaneous March 1 reporting recorded Iranian state media confirming Khamenei's death. The compared contracts recorded scalar 45-cent and resolved-YES settlements.
- **Qualifying condition:** A — departure before July 1, 2026; qualifying announcement also covered; death-only departure uses a pre-death price or committee fair allocation; B — loss of position or ability to perform duties by June 30, 2026, 11:59 PM ET.
- **Settlement:** A — scalar; recorded normalized settlement $0.45; B — resolved YES; normalized payout $1.
- **Implication:** Forecasting departure is insufficient to value a contract whose death clause can pay a fraction of the unit payout.
- **Boundary:** The deadlines and exceptions differ, so this is not a controlled clause effect. Full Kalshi mapping includes announcement, ordinary departure, price-based death allocation and binding committee discretion. The exact reference-price selection was not audited. Reported reimbursements can make account receipts differ from contract settlement; original linked social posts were inaccessible. No binary-event restriction applies.
- **Contracts:** [KXKHAMENEIOUT-AKHA-26JUL01](https://kalshi.com/markets/kxkhameneiout-akha-26jul01); [661699](https://polymarket.com/event/khamenei-out-as-supreme-leader-of-iran-by-june-30-747).
- **Chronology:** February 28, 2026: attack; March 1: contemporaneous confirmation report; March 1 00:02:17 UTC: Polymarket closure record; March 1 03:19:27.389859 UTC: Kalshi scalar-settlement timestamp.
- **Independent event evidence:** [Iranian state media confirmed Khamenei's death following the February 28 attack.](https://apnews.com/article/5b13b69b708c4ed38e8f95f5fb41a597).
- **Independent event evidence:** [Reported price-based death settlement and fee/entry-cost reimbursements; original linked social posts returned 403.](https://cointelegraph.com/news/kalshi-founder-khamenei-market-carveout).

### Zelenskyy's clothing: appearance, proposals and final adjudication

- **Evidence:** observed appearance, documented proposal/dispute sequence and final NO
- **Scenario:** Zelenskyy appeared in the Netherlands on June 24, 2025, documented by the Ukrainian presidency and its photograph. The official market record preserves repeated proposal/dispute states and a final NO.
- **Qualifying condition:** A — authentic images/video taken and released May 22–June 30, 2025 ET; wearing a suit; no garment-level definition; B — credible-reporting consensus supplies the deciding interpretation.
- **Settlement:** A — resolved NO; normalized payout $0; B — N/A; this is one contract and its adjudication procedure.
- **Implication:** The rules fix timing and image authenticity, while the deciding procedure supplies the interpretation of the clothing category.
- **Boundary:** The appearance source does not independently classify the clothing. A dispute shows adjudication mattered; it establishes no manipulation, trader consensus or causal ambiguity effect. Final institutional payout is recorded despite incomplete written garment criteria. Closure is not independently verified on-chain finality.
- **Contracts:** [546814](https://polymarket.com/event/will-zelenskyy-wear-a-suit-before-july).
- **Chronology:** June 24, 2025: photographed appearance; June 30: rule window ends; archived status history alternates proposed/disputed five times (individual timestamps unavailable); July 9 00:30:39 UTC: closure record with current resolved status and NO outcome.
- **Independent event evidence:** [Zelenskyy appeared in the Netherlands on June 24, 2025; no independent clothing classification is supplied.](https://www.president.gov.ua/en/news/vidbulasya-audiyenciya-prezidenta-ukrayini-v-korolya-niderla-98637).

### U.S.–Ukraine minerals agreement: two YES resolutions across milestones

- **Evidence:** observed chronology and two recorded YES outcomes; no realized split
- **Scenario:** The March agreement contract records YES and March 25 closure. The U.S. Treasury and Ukrainian ministry record an April 30, 2025 signing; the later signed-deal contract records YES and May 4 closure.
- **Qualifying condition:** A — rare-earth agreement by March 31; public announcement qualifies; B — minerals agreement signed or formally adopted by April 30; announcement alone fails.
- **Settlement:** A — resolved YES; normalized payout $1; B — resolved YES; normalized payout $1.
- **Implication:** An agreement announcement and a signature are distinct milestones, and both successive contracts can ultimately pay YES.
- **Boundary:** Different windows, rare-earth/mineral scope and evidence authorities prevent a controlled milestone comparison. The YES/YES chronology does not instantiate the supplementary hypothetical YES/NO witness and establishes no manipulation or erroneous March outcome.
- **Contracts:** [521607](https://polymarket.com/event/ukraine-agrees-to-give-trump-rare-earth-metals-before-april); [532897](https://polymarket.com/event/trump-x-ukraine-mineral-deal-signed-before-may).
- **Chronology:** March 25, 2025 00:21:27 UTC: agreement-contract closure record; April 30: official signing announcement; May 4 01:10:41 UTC: signed-deal-contract closure record.
- **Independent event evidence:** [Reconstruction investment fund agreement signed April 30, 2025.](https://home.treasury.gov/news/press-releases/sb0126).
- **Independent event evidence:** [Independently records the April 30, 2025 signing date.](https://me.gov.ua/News/Detail/91af98f8-9ae6-49ba-99ae-adb847fe493a?lang=en-GB).

Full operative text, source versions, outcome evidence and chronology: [casebook](REPRESENTATION_CASEBOOK.md) and [case matrix](tables/representation-case-matrix.csv).

### Sampled text context

| Sampled text feature | Kalshi | Polymarket |
|---|---:|---:|
| Contracts | 12,251 | 7,249 |
| Exploratory rule-text specificity index | 0.621 | 0.657 |
| Authority/source cues | 0.550 | 0.653 |
| Date/time cues | 0.605 | 0.798 |
| Definition/threshold cues | 0.679 | 0.617 |
| Edge-clause cues | 0.272 | 0.404 |
| Absence of flagged discretion terms | 0.997 | 0.811 |
| Threshold-flag share | 82.2% | 24.7% |
| Mean analyzed text length (words) | 100.5 | 157.8 |

Literal cues describe the retained portfolios. The legacy column `determinacy_score` stores an exploratory text index; it has no independent human construct validation. The threshold flag contributes to that index, so stratification is descriptive. Corrected parsing eliminates the previously reported composition reversal. Final field-placement invariance is documented separately from the frozen four-repair diagnostic in the measurement note.

- Kalshi: 120 API families; top five contain 46.2% of rows; 43 families (6,345 rows) vary internally in the index.
- Polymarket: 2,634 API families; top five contain 2.6% of rows; 85 families (519 rows) vary internally in the index.
Kalshi series and Polymarket events have different granularity. Their family counts and concentration do not rank platform diversity.

The minerals chronology records YES/YES in successive contracts and does not instantiate the separate announcement-versus-signature counterfactual. President-elect interruption, Fed quantization and Trump announcement/first-departure scenarios remain supplementary witnesses with their rule qualifications. Exhibit counts refer to cases rather than independent mechanisms.

Main exhibits: (1) Hilton settlement contrast; (2) Khamenei fractional settlement; (3) suit adjudication chronology; (4) literal text profile and compact payout schematic. Full rules and supplementary witnesses are in the casebook. All volume/terminal-error tables and their uncertainty belong in [supplementary analysis](SUPPLEMENTARY_ANALYSIS.md).

## 5. Discussion and conclusion

Contract prices are comparable only after the paying conditions and amounts have been established. Hilton demonstrates an ordinary milestone distinction; Khamenei demonstrates a special price-based exception; the suit episode demonstrates institutional completion of a disputed category. The cases make established specification concerns concrete through auditable linked records.

For comparison and hedging, show what qualifies and how much pays. For forecast evaluation, identify the achievement being evaluated. For adjudication, retain proposal/dispute/final-outcome chronology. Interface recommendations remain proposals.

Purposive volume selection, flawed historical filtering, missing acquisition records, retrospective rule snapshots, unvalidated text indices and limited synchronized price evidence constrain generalization. Account reimbursements and contract payouts are separate. No platform ranking, manipulation inference or causal effect follows from these exhibits.

Before comparing forecasts, establish what would have to happen for each contract to pay.

## Appendix: sample and provenance note

The fixed historical sample contains 19,500 contracts (Kalshi: 12,251; Polymarket: 7,249). Raw normalization reconciles 12,253 Kalshi rows minus two missing titles and 8,000 retained Polymarket rows minus 751 unsupported outcome-label rows. Raw snapshots remain unchanged.

Kalshi coverage selects 120 high-volume series and caps each acquisition tier. Polymarket coverage selects high-volume closed markets using a flawed historical sports filter. `gameStartTime` wrongly flagged named minerals and suit markets as sports. The classifier is repaired for future acquisition; omitted historical records are not restored by that repair. The 23,700 scanned minus 8,000 retained difference is 15,700, with no established sports/overflow split. These portfolios are purposive, use different category/family schemes, and support no population ranking.

September 10 is the legacy snapshot label, not a verified HTTP acquisition timestamp. Three Polymarket source updates fall on September 11; the discrepancy remains unresolved. Missing historical caches now fail before network access. Date-only retrieval boundaries and metadata elapsed time are exposure proxies. The audit separates scheduled future openings, positive-volume same-day openings and close-before-open records; neither clipping nor alternate date conventions establishes that rules preceded trading.

Outcome provenance separates Kalshi recorded binary results and scalar settlements from Polymarket final-status endpoint prices and unresolved price inference. Fifteen proposed-status and 38 missing-status endpoint records are qualified separately; two `settled` statuses count as recorded final status. Six Kalshi scalar settlements and ten Polymarket intermediate-price cases remain separate categories. See [data sources](../DATA_SOURCES.md) and the sample audit tables for the exact ledger.

## References

- Wolfers, J., & Zitzewitz, E. (2004). Prediction Markets. *Journal of Economic Perspectives, 18*(2), 107–126. [DOI](https://doi.org/10.1257/0895330041371321).
- Wand, Y., & Weber, R. (1993). On the ontological expressiveness of information systems analysis and design grammars. *Information Systems Journal*. [DOI](https://doi.org/10.1111/j.1365-2575.1993.tb00127.x).
- Eriksson, O., & Öhlund, A. (2024). Digital Institutionalization: The Case of E-Prescribing. *Journal of the Association for Information Systems*. [DOI](https://doi.org/10.17705/1jais.00845).
- Gebele, J., & Matthes, F. (2026). Semantic Non-Fungibility and Violations of the Law of One Price in Prediction Markets. arXiv:2601.01706v1, preprint. [Version](https://arxiv.org/html/2601.01706v1).
- Wang, G. (2026). Do prediction markets price events or adjudication? Evidence from the disputed Polymarket markets. *Economics Letters, 268*, 113176. [DOI](https://doi.org/10.1016/j.econlet.2026.113176). Review access was partial.
- Nechepurenko, M. (2026). Resolution Is Not Settlement, Part I: Oracle Adjudication and Semantic Governance on Polymarket. arXiv:2609.15368v1, preprint. [Version](https://arxiv.org/html/2609.15368v1).
- Capponi, A., Gliozzo, A., & Zhu, B. (2025). Semantic Trading: Agentic AI for Clustering and Relationship Discovery in Prediction Markets. arXiv:2512.02436v1, preprint. [Version](https://arxiv.org/html/2512.02436v1).

The linked citations in section 2 are the verified review source map. Recent preprints, partial article access and abstract-only leads retain their stated evidence levels. The former Bayesian source audit is preserved as history; the elementary expected-payout identity supplies no new updating theorem.
