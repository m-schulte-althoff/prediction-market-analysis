# Construct Architecture

## Payable claims and the information needed to settle them

The study examines when similarly presented prediction-market questions expose traders to different settlements. Published rules specify the qualifying event, milestone, measurement convention, deadline, evidence authority, exceptions, fallback and settlement amount. These are observable dimensions through which rules differentiate claims. The archives establish the published specifications; they do not establish why designers chose them or how those choices were negotiated.

**Payoff divergence**, the payout-relevant use of semantic divergence in this study, exists when two contracts assign different normalized settlements to at least one explicitly specified relevant scenario. A separating scenario states the facts and required institutional inputs, applies the complete operative rules, and records both payouts. Different sources, procedures or wording are candidate explanations until such a payout difference is established. Use **equivalent/non-equivalent**, with the audited domain stated, rather than high/low divergence: this study estimates no divergence magnitude or probability-weighted prevalence.

**Written-rule determinacy** concerns whether a specified rule version fixes a payout given the scenario information held fixed. Every assessment must state that information and identify any remaining input or interpretation. A rule may require a later authority decision and still define a unique eventual settlement once that decision is included. An unresolved future fact, an unavailable reference price, an underdefined category and an incomplete adjudication procedure are distinct reasons an analyst may be unable to infer a payout; record the applicable reason rather than treating them as one form of institutional incompleteness.

The concepts address different comparisons. First place and top-two advancement can each be explicit while assigning different payouts when a candidate finishes second. Clothing and timing can be known while a rule still requires credible-reporting adjudication of whether the clothing counts as a suit. Conceptual distinctness does not imply statistical independence of any empirical measures.

## Concrete evidence and its practical consequence

- **Steve Hilton, realized settlement contrast:** the certified June 2026 California primary placed Hilton second. The archived first-place contract finalized NO; the advancement contract resolved YES. A comparison of these contracts requires their qualifying positions, and treating the positions as interchangeable would give an incorrect offset or forecast-evaluation target. The archived rule version, tie clauses and deadlines remain part of the audit; this ordinary second-place outcome establishes a separating state rather than global nesting of all allowable settlements.
- **Ali Khamenei, realized fractional-settlement contrast:** the archived Kalshi departure contract finalized at 45 cents under a rule containing a death-only, price-based allocation clause; the Polymarket departure contract resolved YES. Both complete windows and exceptions must remain visible. To evaluate the former claim, a trader needs the payout rule and its price/adjudication inputs as well as a forecast of departure. The contrast is not a controlled estimate of one clause's effect. Contract settlement amounts are distinct from account receipts, which may include reported reimbursements; individual cash flows were not audited.
- **Zelenskyy's suit, reported dispute and recorded adjudication:** the rules require qualifying authentic images/video within the event window and use credible-reporting consensus. The preserved Gamma record reports repeated proposal/dispute states and final NO after the event window. This demonstrates consequential adjudication of a category, without establishing an objectively incorrect result, manipulation, or the absence of a unique eventual payout. Holding clothing and timing fixed does not also hold the later adjudication fixed.

Exact clauses, IDs, archived fingerprints, source links and evidence categories belong in the [casebook](../output/REPRESENTATION_CASEBOOK.md). Hilton and Khamenei are traced to the restored research snapshots and separately preserved October records in the [lead evidence notes](../output/paper-revision/2026-10-12-01/LEAD_REVIEW.md). The suit verification is documented in the retained [theory review](../output/paper-revision/2026-10-12-01/THEORY_REVIEW.md); it is current follow-up evidence, not proof that those records belonged to the historically filtered sample. Other hypothetical witnesses test possible non-equivalence without estimating its incidence, economic magnitude or effect on trader beliefs.

## Compact payoff formalism

Let `Ω` be the stated domain of relevant histories under the audited rule versions. A history includes every payout-relevant input: event facts, dates, evidence, reference prices and applicable authority decisions. For a determinate normalized settlement mapping:

```text
r_c: Ω → [0,1]
q_c = E_mu[r_c]
q_A − q_B = E_mu[r_A − r_B]
```

Here `mu` is **any common probability distribution** over those histories. `q_c` is an expected normalized contract payout, not automatically an observed market price. Different payout mappings can have different expected payouts under common beliefs. They need not: separating states may have zero probability, or differences in opposite directions may cancel. A witness establishes non-equivalence; it does not measure the witness's probability or an actual price effect. The identities require no Bayesian updating theorem and constitute no extension of Meehan and Zhang. The [source audit](BAYES_SOURCE_AUDIT.md) preserves the earlier philosophical reading as history and explains its revised role.

If all settlements in the audited domain are binary, define `Y_c = {ω: r_c(ω) = 1}`. Then:

```text
q_c = mu(Y_c)
q_A − q_B = mu(Y_A \ Y_B) − mu(Y_B \ Y_A)
```

Fractional settlements require the general expected-payout expression. A specified tie payout of `1/n` can be fully determinate while nonbinary. A price-based death allocation likewise requires its amount and reference inputs; committee discretion may add a required authority decision. These clauses prevent importing binary-event identities globally even when a particular scenario has 0/1 payouts. As a synthetic illustration, a 20% chance of one dollar and a 30% chance of 50 cents contribute an expected payout of 35 cents. These are illustrative probabilities, not estimated trader beliefs.

## Conditional determinacy and adjudication

Let `I` denote the information specified in an audited scenario and `v` the operative rule version. Let `R_c(v,I)` contain the payouts compatible with that information and the rule's relevant completions. A singleton means the written rules and specified information fix the payout. Multiple values mean the payout is not fixed at that information level; the audit must identify what remains to be supplied.

For example, separate substantive facts `x` from a later adjudication `a`. Settlement may be `r_c(x,a)`, even though the clothing and timing described in `x` do not supply `a`. This is uncertainty about the remaining institutional input, not proof that a complete history lacks a payout mapping. A substantive claim of institutional incompleteness would require evidence that incompatible payouts remain permissible after the governing procedure's relevant inputs are fixed. The present suit evidence does not establish that stronger claim.

For pair comparisons, hold the underlying event history fixed and state each contract's applicable institutional inputs. Preserve deadlines, exceptions and settlement methods on both sides. A pair can diverge in payout while both rules are determinate; a rule can require adjudication even without a demonstrated cross-contract difference. Neither property is measured by raw text distance.

## Complete-rule relations and conditional coherence

Relations are oriented A to B. Validate them against the complete archived rules over a stated common domain, including dates, ties, cancellations, fallbacks, competing outcomes and nonbinary settlements. A single separating witness rejects equivalence but generally does not establish inclusion, exclusivity or a probability ordering.

| Validated relation of determinate binary events | Implication under a common distribution |
|---|---|
| `equivalent`: `Y_A = Y_B` | `q_A = q_B` |
| `subset`: `Y_A ⊆ Y_B` | `q_A ≤ q_B` |
| `superset`: `Y_A ⊇ Y_B` | `q_A ≥ q_B` |
| `disjoint`: `Y_A ∩ Y_B = ∅` | `q_A + q_B ≤ 1` |
| `complement`: `Y_A = Ω \ Y_B` | `q_A + q_B = 1` |
| `overlap_non_nested` | No additional marginal restriction without more information. |
| `non_equivalent_unclassified` | A separating witness establishes non-equivalence only. |
| `indeterminate` | No point restriction supplied at the audited information level. |
| `unclassified` | Insufficient relation validation. |

The existing election and minerals audits identify separating states in both directions and an intersection under their stated archived-rule readings. Fed is unclassified beyond its conditional witness. First-place and departure cases include nonbinary clauses; the suit concerns within-contract interpretation. These audits supply no eligible synchronized-price test. Manual confidence is an assessment of the audit, not a numerical posterior. Fingerprints bind semantic assertions to the audited IDs and full operative text; changed inputs require revalidation of dependent witness and payout claims.

`src/coherence.py` implements binary relation implications and conditional price diagnostics. For a validated subset, raw excess is `max(0, p_A − p_B)`, with a separate tolerance flag. Missing eligible evidence is `not_estimable`, not zero excess. Observed-price analogues require appropriate timing, freshness, YES orientation and comparable pricing conditions; liquidity, spreads, fees, risk preferences and limits to arbitrage can affect prices. Daily alignment and forward filling alone do not establish synchronized fresh observations. Neither a price excess nor a difference in claims establishes irrationality.

## Measures, evidence roles and literature boundary

Call the automated measure **rule-text specificity**. Its legacy column `determinacy_score` is an exploratory composite of textual components; it is not a validated measure of conditional written-rule determinacy or institutionally permissible payouts. Lexical, numeric, source, stage and deadline features support description and candidate retrieval. Human rule application and an explicit separating scenario establish the pair-level inference. Contract-level portfolio profiles and supplementary volume associations answer different questions and do not validate payoff divergence, trader understanding or adjudication mechanisms. The old composite composition-reversal claim is withdrawn after bounded parser corrections.

The study offers a focused empirical audit of comparability. Wolfers and Zitzewitz already discuss contract specification and adjudication. Wand and Weber address representational clarity; Eriksson and Öhlund analyze digital constitutive rules. Gebele and Matthes directly model prediction-market resolution semantics and cross-market relationships. Wang studies prices while oracle adjudication is pending; Nechepurenko distinguishes adjudication and settlement stages; Capponi, Gliozzo and Zhu develop automated relationship discovery. Their verified passages and access limits are recorded in the [theory review](../output/paper-revision/2026-10-12-01/THEORY_REVIEW.md). Against those foundations, this study's contribution is the documented diagnostic distinction among realized payout differences, separating-rule witnesses and interpretation dependent on later adjudication. It does not claim priority for payoff mappings, event equivalence or the general importance of contract design.
