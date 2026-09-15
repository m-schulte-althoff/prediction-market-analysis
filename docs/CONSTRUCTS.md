# Construct Architecture

The study begins with a **public-world phenomenon**: the socially recognizable issue traders think they are forecasting. A platform’s **resolution architecture** turns that phenomenon into a digitally tradable and institutionally resolvable claim by selecting a predicate, event stage, metric, threshold, temporal boundary, evidence authority, exceptions, fallback, and settlement method.

**Semantic differentiation** names that design process: specifying what counts, when it counts, and whose evidence counts. **Divergence** is a possible difference between the resulting claims; **determinacy** is a property of each claim. For example, a first-place contract and a top-two advancement contract can both be precise while paying differently when a candidate finishes second.

Let a contract be a possibly set-valued mapping, `R_c(ω)`, from a relevant world history `ω` to institutionally permissible normalized settlements.

- **Semantic determinacy, (D_c), is intra-contract.** It concerns how uniquely a world history maps to a settlement under contract (c). Undefined category boundaries or discretionary evidence can make the mapping set-valued.
- **Semantic divergence, (\Delta_{ab}), is inter-contract.** It exists when two contracts about the same public-world phenomenon map at least one plausible world history to different payouts or settlement procedures.

These constructs are orthogonal:

| | Low divergence | High divergence |
|---|---|---|
| **High determinacy** | precise paraphrases of the same claim | two precise but different claims, such as election call versus inauguration |
| **Low determinacy** | shared vague language | a vague claim paired with a precise claim whose outcomes can separate |

“Orthogonal” here means conceptually distinct; it does not claim statistical independence of their empirical measures.

## Representation before claim valuation

Meehan and Zhang's [*Bayes Is Back* (2025)](https://doi.org/10.1215/00318108-11873775) concerns rational updating within a specified prior space `(S, π)` and a represented strongest evidence proposition. Non-contrastiveness holds the posterior fixed across learning situations given that same prior space and evidence at the same state; global evidential constancy additionally fixes it across states with that evidence. This condition alone does not select Bayesian conditionalization. Their accuracy argument distinguishes expected accuracy within a learning situation from total expected accuracy across situations. We use the representational prerequisite, not Hi-TEA as an empirical test. The [source audit](BAYES_SOURCE_AUDIT.md) identifies manuscript sections/pages and the limits of this transfer.

Our IS extension asks what payoff-relevant proposition the system defines. Let `Ω` be relevant modeled world histories, including institutionally relevant evidence, deadlines and authority decisions; let `e` be represented evidence with positive prior probability. A Bayesian posterior is `μ_e = P(· | e)`. For a determinate binary contract:

```text
r_c: Ω → {0,1}
Y_c = {ω ∈ Ω: r_c(ω) = 1}
q_c(e) = E_{μ_e}[r_c(ω)] = P(Y_c | e)
```

`q_c` is claim-specific credence/expected normalized payout, not automatically an observed price. Platform design selects `r_c`/`Y_c`; evidence updates the distribution over histories; applying that distribution to the mapping values the particular claim. This is an analytical separation, not a chronological assertion that no learning occurs before rules are written. Unlike updating within a fixed representation, constituting the claim is the mechanism investigated here. We do not attribute this market argument to Meehan and Zhang.

For two binary claims under exactly the same posterior:

```text
q_A(e) − q_B(e) = μ_e(Y_A \ Y_B) − μ_e(Y_B \ Y_A)
```

Hence `Y_A ≠ Y_B` **can**, but need not, produce different credences. Separating states may have zero posterior mass, or the masses in both differences may cancel. A witness establishes non-equivalence without measuring its probability or economic magnitude. In a synthetic model with ordinary, tie-free first/second/other outcomes assigned masses .2/.3/.5, first place and advancement have expected payouts .2/.5. This illustration estimates no actual trader belief and does not assert global nesting of the archived primary contracts.

## Incomplete versus nonbinary settlement mappings

For an institutionally incomplete binary representation, use a **nonempty** `R_c(ω) ⊆ {0,1}`. When `R_c(ω) = {0,1}`, the rule alone does not choose a unique payout at that state. There may therefore be multiple permissible binary events, depending on institutional completion. If unresolved states have positive posterior mass, different permissible completions can have different expected payouts; incompleteness on zero-mass states need not change expected payout.

This distinguishes uncertainty about **which world obtains** from incompleteness in **how that world is mapped to settlement**. The suit witness holds images and timing fixed while the garment category lacks an operational boundary. Credible-reporting adjudication supplies institutional completion. A posterior over a richer model of adjudication could yield a price, but that adds assumptions beyond the written garment definition; the case does not show an undefined eventual institutional settlement. Nor does an automated determinacy score tell us the set of permissible completions. No numerical partial-identification bounds are estimated here.

Fractional payouts are a different issue: a specified tie payout of `1/n` is determinate but nonbinary. For `r_c: Ω → [0,1]`, `q_c = E_{μ_e}[r_c]` still applies, while `q_c = P(Y_c | e)` generally does not. The primary contract's tie rule and leader contract's death-price/fair-allocation clause preclude imposing a binary restriction globally. A committee-based clause may additionally need adjudication. These qualifications do not undo the existing 0/1 witness states.

## Representation-aware coherence

Relations are oriented A to B and must be validated against complete archived rules over the stated modeled histories, including deadlines, exceptions, fallbacks, ties and competing outcomes.

| Validated relation of determinate binary events | Exact implication under a common distribution |
|---|---|
| `equivalent`: `Y_A = Y_B` | `q_A = q_B` |
| `subset`: `Y_A ⊆ Y_B` | `q_A ≤ q_B` |
| `superset`: `Y_A ⊇ Y_B` | `q_A ≥ q_B` |
| `disjoint`: `Y_A ∩ Y_B = ∅` | `q_A + q_B ≤ 1` |
| `complement`: `Y_A = Ω \ Y_B` | `q_A + q_B = 1` |
| `overlap_non_nested` | No extra useful pairwise marginal restriction without more set/probability information. |
| `non_equivalent_unclassified` | A witness establishes non-equivalence, not inclusion or probability ordering. |
| `indeterminate` | No unique point restriction supplied by the written representation alone. |
| `unclassified` | Insufficient relation validation. |

The election and minerals audits supply witness states in both set differences and their intersection under the stated archived-rule reading. Neither needs or supports a nesting inequality. Fed remains unclassified beyond conditional non-equivalence. The primary and leader cases are outside globally binary mappings; suit is within-contract incompleteness. Manual audit confidence is not a numerical posterior. Fingerprints bind these judgments to archived contract IDs and complete rule text; revised versions fail closed pending review.

`src/coherence.py` implements these implications and conditional price diagnostics. For a validated subset, raw excess is `max(0, p_A − p_B)`, with a separate numerical-tolerance flag. Missing evidence is `not_estimable`, not zero excess. Price analogues require a probability-price approximation: liquidity, fees, spreads, risk preferences, stale trading, timing, market composition and limits to arbitrage can matter. The legacy daily panel uses up to seven-day forward fill, so alignment alone is not synchronized fresh evidence. Neither price excess nor differing claims demonstrates Bayesian irrationality or violation of global evidential constancy.

An automated lexical, numeric, source, stage, or deadline distance is a **candidate diagnostic**, not proof of semantic divergence. The operational standard for a coded divergence is a counterfactual witness state plus the implied settlement on both sides. The generated representation case matrix records that evidence.

Distinguish procedural divergence from demonstrated payout divergence: different evidence authorities or fallback procedures do not alone establish that the payouts differ. The casebook states what each particular witness establishes. Its scenarios are hypothetical; the archived rule text is the observed evidence. The suit example demonstrates an unspecified garment category whose institutional interpretation is delegated to credible reporting, not a documented realized dispute.

The automated determinacy score is a **textual specification proxy**, not a validated measurement of every institutionally permissible outcome. Its threshold flag also contributes to its outcome-definition component. Comparing scores within threshold-flag groups reveals portfolio composition; it is not an independent validation or causal adjustment.

The expected downstream consequences also differ. Indeterminacy can create interpretive latitude within one claim. Divergence creates different state exposure across claims and can therefore produce rational price wedges that only look like forecast disagreement.
