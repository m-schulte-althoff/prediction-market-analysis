# Research Status

Updated 2026-10-13 after approved P1–P7 implementation.

Steve Hilton finished second in California's June 2, 2026 gubernatorial primary and advanced under the top-two rule. The archived first-place Kalshi contract settled NO/$0; the Polymarket advancement contract recorded resolved YES. The result concerns one election, yet the contracts reward different achievements.

The case inventory contains 9 exhibits; 0 supply a validated binary marginal restriction. 0 observation-level price diagnostics are estimable.

The saved price histories are a dormant diagnostic panel. Original observations are clipped to the supported window before aggregation, and source timestamps and fill ages are retained. Daily labels and forward fills do not certify fresh synchronized quotes. No general divergence–price effect, trader misunderstanding, or forecast-accuracy advantage is established. Missing excess values mean insufficient evidence.

## Current sample and measurement

The fixed historical sample contains 19,500 contracts (Kalshi: 12,251; Polymarket: 7,249). Raw normalization reconciles 12,253 Kalshi rows minus two missing titles and 8,000 retained Polymarket rows minus 751 unsupported outcome-label rows. Raw snapshots remain unchanged.

Kalshi coverage selects 120 high-volume series and caps each acquisition tier. Polymarket coverage selects high-volume closed markets using a flawed historical sports filter. `gameStartTime` wrongly flagged named minerals and suit markets as sports. The classifier is repaired for future acquisition; omitted historical records are not restored by that repair. The 23,700 scanned minus 8,000 retained difference is 15,700, with no established sports/overflow split. These portfolios are purposive, use different category/family schemes, and support no population ranking.

September 10 is the legacy snapshot label, not a verified HTTP acquisition timestamp. Three Polymarket source updates fall on September 11; the discrepancy remains unresolved. Missing historical caches now fail before network access. Date-only retrieval boundaries and metadata elapsed time are exposure proxies. The audit separates scheduled future openings, positive-volume same-day openings and close-before-open records; neither clipping nor alternate date conventions establishes that rules preceded trading.

Outcome provenance separates Kalshi recorded binary results and scalar settlements from Polymarket final-status endpoint prices and unresolved price inference. Fifteen proposed-status and 38 missing-status endpoint records are qualified separately; two `settled` statuses count as recorded final status. Six Kalshi scalar settlements and ten Polymarket intermediate-price cases remain separate categories. See [data sources](../DATA_SOURCES.md) and the sample audit tables for the exact ledger.

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

## Supplementary association

| Specification | Coefficient | 95% interval | Uncertainty | n |
|---|---:|---:|---|---:|
| cohort_exposure_adjusted | -0.1243 | [-0.2048, -0.0438] | cluster; SE 0.0411 | 19,500 |
| cohort_exposure_adjusted_hc3 | -0.1243 | [-0.1426, -0.1060] | HC3; SE 0.0093 | 19,500 |
| within_family_kalshi | -0.0753 | [-0.2366, 0.0861] | cluster; SE 0.0823 | 6,345 |
| within_family_polymarket | -0.0445 | [-0.1218, 0.0327] | cluster; SE 0.0394 | 519 |

The preferred pooled coefficient uses one within-platform SD of the text index and standardized log cumulative volume. Its family clusters are qualified by platform. HC3 uses the same formula and rows as a covariance comparison. Within-family models use internally varying families and a different residual-score SD; their magnitudes are not directly comparable to the pooled coefficient.

Volume selection, retrospective rules, family concentration and incomplete exposure metadata limit interpretation to these selected portfolios. Subgroup significance differences do not test heterogeneity. The frozen review's top-five families contribute 69.48% of focal sandwich variance; its bounded largest-family deletion remains negative. Those checks concern the archived and frozen repaired specifications, rather than certifying the final field-invariant index. No new deletion grid was run.

## Locked scope

Use the case-led PAPER_OUTLINE.md and documented casebook. Keep payoff divergence distinct from written-rule determinacy. Treat text features as portfolio context and volume as supplementary. No replacement historical sample, new activity design, synchronized price collection, comprehension study or new critic round was authorized. Missing historical caches fail closed. Research-log entries survive regeneration; cycle approval, archives and validation are in paper-revision/2026-10-12-01/.
