# Construct Architecture

## Payable claims and the information needed to settle them

The study examines when similarly presented prediction-market questions expose traders to different settlements. Its organizing questions are what qualifies, how much pays, and which institutional inputs remain to be supplied. Qualifying achievements, milestones, measurement conventions, deadlines, evidence authorities and exceptions can overlap within one contract. These are observable rule dimensions, not an exhaustive taxonomy or independently identified causal mechanisms. The archives preserve the supplied API descriptions and explicitly linked evidence; they do not establish exhaustive historical governing-rule coverage or designers' motives.

**Payoff divergence** exists when two contracts assign different normalized settlements to at least one explicitly specified relevant scenario. A separating scenario states the facts and required institutional inputs, applies the audited rule version and records both payouts. A global claim requires complete applicable rules; an API-only hypothetical interpretation remains conditional where that coverage is missing. Different sources, procedures or wording are candidate explanations until a payout difference is established. Use **equivalent/non-equivalent**, with the audited domain stated, rather than high/low divergence: this study estimates no divergence magnitude or probability-weighted prevalence.

**Written-rule determinacy** concerns whether a specified rule version fixes a payout given the scenario information held fixed. Every assessment must state that information and identify any remaining input or interpretation. A rule may require a later authority decision and still define a unique eventual settlement once that decision is included. An unresolved future fact, an unavailable reference price, an underdefined category and an incomplete adjudication procedure are distinct reasons an analyst may be unable to infer a payout; record the applicable reason rather than treating them as one form of institutional incompleteness.

The concepts address different comparisons. First place and top-two advancement can each be explicit while assigning different payouts when a candidate finishes second. Clothing and timing can be known while a rule still requires credible-reporting adjudication of whether the clothing counts as a suit. Conceptual distinctness does not imply statistical independence of any empirical measures.

## Concrete evidence and its practical consequence

- **Steve Hilton, realized settlement contrast:** the certified June 2026 California primary placed Hilton second. The archived first-place contract finalized NO; the advancement contract resolved YES. A comparison of these contracts requires their qualifying positions, and treating the positions as interchangeable would give an incorrect offset or forecast-evaluation target. The archived rule version, tie clauses and deadlines remain part of the audit; this ordinary second-place outcome establishes a separating state rather than global nesting of all allowable settlements.
- **Ali Khamenei, realized fractional-settlement contrast:** the archived Kalshi departure contract finalized at 45 cents under a rule containing a death-only, price-based allocation clause; the Polymarket departure contract resolved YES. Both complete windows and exceptions must remain visible. To evaluate the former claim, a trader needs the payout rule and its price/adjudication inputs as well as a forecast of departure. The contrast is not a controlled estimate of one clause's effect. Contract settlement amounts are distinct from account receipts, which may include reported reimbursements; individual cash flows were not audited.
- **Zelenskyy's suit, documented criterion and institutional outcome:** one contract asks whether qualifying authentic images/video show a suit and uses credible-reporting consensus. The creator's stored May 29, 2025 update acknowledges a dispute; the July 1 update says that the required reporting consensus has not confirmed a suit. A pinned Polygon read corroborates NO and verifies the question/condition linkage. May 29 precedes the June 24 appearance, so that photograph cannot explain the whole dispute history. Historical event logs were inaccessible; individual dispute reasons and the original finality transaction remain unverified. Holding clothing and timing fixed does not also supply the reporting decision. No pairwise relation or institutional incompleteness is established.
- **Minerals, same-outcome milestone comparison:** the March and April contracts record YES/YES despite different agreement/signature conditions and deadlines. Their lifecycle and signing chronology provides a useful comparison without an observed payout split. The separate YES/NO witness is conditional on the archived question-rule binary model and hypothetical.

Exact clauses, IDs, archived fingerprints, source links and evidence categories belong in the [casebook](../output/REPRESENTATION_CASEBOOK.md). Hilton and Khamenei are traced to the restored research snapshots and separately preserved October records in the [lead evidence notes](../output/paper-revision/2026-10-12-01/LEAD_REVIEW.md). The new suit evidence and its bounded recovery are documented in [P2_OUTCOME.md](../output/paper-revision/2026-10-15-01/P2_OUTCOME.md). Current follow-up evidence does not establish membership in the historically filtered sample or pre-outcome rule availability. The presidential death/interruption witness is withheld because linked specifications contain additional exceptions with unverified historical applicability. Other hypothetical witnesses remain conditional on the supplied rule versions.

Pooling forecasts or scoring against one target requires a justified relation between claims and that target. Exact offsetting requires the corresponding relation between amounts across states. Useful hedging and comparisons of different achievements need not require identical claims. The audit identifies the relation needed for the proposed task; no actual trader misunderstanding is observed.

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

## Source-scoped relations and conditional coherence

Relations are oriented A to B. A global relation requires complete applicable rules over a stated common domain, including dates, ties, cancellations, fallbacks, competing outcomes and nonbinary settlements. Current labels are limited to their explicitly audited sources. A single separating witness rejects equivalence within that scope but generally does not establish inclusion, exclusivity or a probability ordering.

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
| `not_applicable` | A single-contract exhibit has no pairwise relation. |

The presidential election witness is withheld pending governing-version evidence. Minerals identifies separating states and an intersection within its `question_rule_binary_model`; that label does not certify all platform fallbacks. Fed is unclassified beyond its conditional witness. First-place and departure cases include nonbinary clauses; the suit is `not_applicable` for pairwise relations and `delegated_determination` for its evidence status. These audits supply no eligible synchronized-price test. Manual confidence is an assessment of the audit, not a numerical posterior. Fingerprints bind assertions to all supplied input fields, including linked protocol evidence. Changed inputs require revalidation; matching hashes do not certify exhaustive historical rule coverage.

`src/coherence.py` implements binary relation implications and conditional price diagnostics. For a validated subset, raw excess is `max(0, p_A − p_B)`, with a separate tolerance flag. Missing eligible evidence is `not_estimable`, not zero excess. Observed-price analogues require appropriate timing, freshness, YES orientation and comparable pricing conditions; liquidity, spreads, fees, risk preferences and limits to arbitrage can affect prices. Daily alignment and forward filling alone do not establish synchronized fresh observations. Neither a price excess nor a difference in claims establishes irrationality.

## Measures, evidence roles and literature boundary

Call the automated measure **rule-text specificity**. Its legacy column `determinacy_score` is an exploratory composite of textual components; it is not a validated measure of conditional written-rule determinacy or institutionally permissible payouts. Lexical, numeric, source, stage and deadline features support description and candidate retrieval. Human rule application and an explicit separating scenario establish the pair-level inference. Contract-level portfolio profiles and supplementary volume associations answer different questions and do not validate payoff divergence, trader understanding or adjudication mechanisms. The old composite composition-reversal claim is withdrawn after bounded parser corrections.

Component means are weighted lexical cue scores. In particular, `discretion_clarity = max(0, 1 − 0.25 × distinct configured phrases)`. A mean of 0.811 is not an 81.1% no-flag share. Scores, sample IDs and the preferred model formula are unchanged by this revision's label repair. Gamma `endDate` remains a metadata proxy; the named contracts' explicit ET deadlines are retained separately in [DATA_SOURCES.md](../DATA_SOURCES.md).

The study offers a focused empirical audit of comparability. Wolfers and Zitzewitz discuss contract specification and adjudication. Wand and Weber address representational clarity; Goh and colleagues retain interpretation context across systems; Wang and Strong connect data quality to a consumer's task. Recker and colleagues and Eriksson and Öhlund connect representation to digitally enacted institutional entities and rights. Close prediction-market work addresses semantic alignment and adjudication. The [literature usage record](../output/paper-revision/2026-10-15-01/LITERATURE_USAGE.md) identifies passages, exact versions and access limits. The contribution links these ideas to observed conditions, amounts and institutional records without claiming priority for payoff mappings, event equivalence or contract specification.
