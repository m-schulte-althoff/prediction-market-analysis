# Same Future, Different Claim

This repository studies how prediction-market platforms turn ostensibly shared future phenomena into different digitally tradable and institutionally resolvable claims. It separates **semantic determinacy** within a contract from **semantic divergence** between contracts and combines systematic Kalshi/Polymarket metadata with an audited counterfactual casebook.

The clearest result is representational: finishing first versus advancing, an election call versus inauguration, rounding a 12.5-basis-point move, announcing versus signing a minerals agreement, and individual departure versus being the first leader to leave can imply different settlements. Each case preserves archived official rules and an explicit hypothetical scenario. The separate “suit” case explains an unspecified clothing category whose interpretation is delegated to credible reporting.

A focused representation-aware Bayesian layer sharpens this mechanism: the same posterior over world histories can assign different probabilities to different platform-defined payoff events. For a determinate binary mapping, `q_c(e) = E[r_c | e] = P(Y_c | e)`. An incomplete settlement category does not yet supply a unique event; specified fractional payouts require expected-payout rather than binary-event reasoning. This is our IS extension inspired by [Meehan and Zhang (2025)](https://doi.org/10.1215/00318108-11873775), with the transfer checked against the supplied PDF in the [source audit](docs/BAYES_SOURCE_AUDIT.md).

The corrected metadata sample contains 12,251 Kalshi and 7,249 Polymarket non-sports binary contracts. Its most interesting descriptive contrast is a **composition reversal**: Kalshi has the higher overall determinacy proxy (.624 versus .610), while Polymarket scores higher within both threshold-flag groups (.575 versus .548 without the flag; .724 versus .640 with it). The flag appears in 82.1% of sampled Kalshi contracts and 23.7% of Polymarket contracts. Raw component profiles show more temporal and edge-clause detail on Polymarket and higher outcome-definition and discretion scores on Kalshi. These describe the sampled rule texts, not overall platform quality.

The preferred exposure/cohort-adjusted association with standardized log volume is −0.129 (HC3 SE 0.009). Within-family estimates are −0.077 (p=.342) on Kalshi and +0.030 (p=.265) on Polymarket, using a different residual-score scale. The volume result remains secondary: it does not establish that ambiguity causes trading. Current numbers include the correction recognizing clock-context “ET” deadlines.

Start with the generated [ICIS paper outline](output/PAPER_OUTLINE.md), [research summary](output/RESEARCH_SUMMARY.md), and [critic feedback and implemented revisions](docs/CRITIC_REVIEW.md).

The [claim-confidence overview](output/CLAIM_CONFIDENCE.md) assesses each current claim's magnitude, significance, robustness, alternative explanations, and strongest example. It is a dated interpretation of the existing evidence, separate from the generated analysis.

## Reproduce the results

Install [uv](https://docs.astral.sh/uv/), then run:

```bash
uv sync --dev
uv run python3 main.py all
uv run pytest -q
uv run ruff check .
uv run mypy .
```

On Windows, use uv’s managed `python` executable if `python3` resolves to the Microsoft Store shim:

```powershell
uv run python main.py all
```

Stages can also run separately:

```bash
uv run python3 main.py download
uv run python3 main.py preprocess
uv run python3 main.py match
uv run python3 main.py anecdotes
uv run python3 main.py panel
uv run python3 main.py analyze
```

To reproduce the included September 10, 2026 snapshots when cached locally:

```bash
uv run python3 main.py all --retrieval-date 2026-09-10 \
  --kalshi-series-limit 120 --polymarket-limit 8000 --matched-panel-limit 12
```

Raw API responses are date-stamped and immutable. Raw and processed data are Git-ignored; a fresh future run can differ as platform archives and rules evolve.

For the critic-driven revision using locally cached snapshots, regenerate the affected stages without downloading new histories:

```bash
uv run python3 main.py preprocess --retrieval-date 2026-09-10
uv run python3 main.py match
uv run python3 main.py anecdotes --retrieval-date 2026-09-10
uv run python3 main.py analyze
```

Use `uv run python` for these commands on Windows when `python3` selects the Store interpreter outside the project environment. In restricted sessions, `uv --cache-dir .uv-cache run ...` keeps the uv cache inside the workspace. No new dependencies or branches are required. `analyze` regenerates the profiles, figures, case-based research summary, and paper outline, screening cached price histories against current match eligibility.

For the Bayesian extension, only `anecdotes --retrieval-date 2026-09-10` and `analyze` are needed with the existing processed contracts/matches/panel. No fresh download or new project dependency is required. `analyze` revalidates the case audit against archived ID/rule fingerprints and writes explicit coherence diagnostics. The manuscript in `input/` is a local theoretical source, not pipeline input.

Optional future price observations go in `data/processed/coherence-price-observations.csv`, with columns `case_id,price_a,price_b,observed_at_a,observed_at_b,comparable_prices,comparison_basis`. A/B follow the case matrix. Use normalized YES prices, identical timezone-aware original observation timestamps and an explicit `True` flag; the basis must document freshness, common horizons and comparable conditions. A separately audited determinate binary relation must first support a marginal restriction. Do not populate this file with forward-filled daily panel rows: matching timestamps after resampling cannot certify freshness. Missing evidence produces `not_estimable`, not a zero excess. `excess` retains the raw inequality distance; the flag uses a numerical tolerance of `1e-9`, not an allowance for trading costs.

## Design

The construct architecture is documented in [docs/CONSTRUCTS.md](docs/CONSTRUCTS.md), with consequential choices in [docs/DECISIONS.md](docs/DECISIONS.md). In brief:

- determinacy asks whether one contract maps a relevant world history uniquely to a settlement;
- divergence asks whether two contracts about one phenomenon can settle differently;
- automated text and metadata distances retrieve candidates but do not prove semantic equivalence;
- a coded divergence requires a plausible witness state and implied settlement on both sides.

The determinacy proxy averages source specificity, temporal specificity, operational definition, edge-case completeness, and discretion clarity. Calendar years are distinguished from substantive quantitative thresholds. Volume models include the original baseline, observed-exposure/opening-cohort adjustment, resolved-only estimates, qualitative/quantitative splits, leave-one-component-out checks, family clustering and aggregation, and estimates based only on within-family variation.

**Semantic differentiation** names the process that creates the claims. The profile table reports raw component means and overall/threshold-stratified composite means, rather than comparing within-platform standardized scores. Threshold flags also enter the proxy, so stratification describes portfolio composition rather than independently validating the scale. Family statistics use Kalshi series and Polymarket events and retain that granularity distinction.

Matching now has two stages: retrieval uses shared-phenomenon language without quantities, while claim-equivalence screening separately considers full wording, numeric overlap, predicates, and deadlines. This prevents divergent thresholds or dates from automatically removing an otherwise useful phenomenon candidate.

## Data sources

Only unauthenticated official APIs are used:

- Kalshi series, live/historical markets, historical cutoff, event records, and candlesticks.
- Polymarket Gamma market/event metadata and CLOB token price histories.

Polymarket sports rows are removed before its high-volume cap using official sports fields plus the conservative taxonomy in `src/taxonomy.py`. Exact endpoints, fields, selection rules, and limitations are in [DATA_SOURCES.md](DATA_SOURCES.md).

## Main outputs

- [Research summary](output/RESEARCH_SUMMARY.md): current contribution, cases, estimates, interpretation, and paper storyline.
- [Representation casebook](output/REPRESENTATION_CASEBOOK.md): plain-language explanations with exact archived rules.
- [Conference paper outline](output/PAPER_OUTLINE.md): Introduction, Literature, Method, Results, and Discussion/Conclusion, linked to the current findings.
- [Platform rule profile figure](output/figures/views-platform-rule-profiles.svg) and `output/tables/analysis-platform-profiles.csv`: component differences, contract mix, and conditional comparisons.
- [Research status](output/RESEARCH_STATUS.md): concise handoff of current evidence and locked decisions.
- `output/tables/representation-case-matrix.csv`: structured signatures, witness states, payouts, URLs, scope, and confidence.
- `output/tables/coherence-case-diagnostics.csv`: relation-specific restrictions, observation eligibility and conditional price excess; currently all six cases are `not_estimable`.
- `output/tables/coherence-panel-readiness.csv`: the two eligible legacy pairs have nine daily rows each, with insufficient semantic/synchronization validation.
- `output/tables/analysis-market-models.csv`: all main and robustness estimates.
- `output/tables/matching-representative-pairs.csv`: auditable automated candidates; divergence columns remain diagnostics.
- `output/figures/views-conceptual-schematic.svg`: claim constitution and Bayesian world-belief updating meet at claim valuation, followed by aggregation and price.
- `output/figures/views-determinacy-volume.svg`: descriptive score–volume pattern.

## File structure

```text
main.py                  # controller / command dispatch
views.py                 # vector figures
src/
  anecdotes.py           # official-rule archive and witness-state case matrix
  coherence.py           # audited binary-relation implications and guarded price diagnostics
  taxonomy.py            # shared sports exclusion rules
  preprocessing.py       # normalized contract database and observed exposure
  semantics.py           # determinacy and diagnostic divergence features
  matching.py            # phenomenon retrieval and claim screening
  panel.py               # diagnostic price-history alignment
  analysis.py            # platform profiles, empirical models, existing diagnostics
  reporting.py           # generated research documents and ICIS paper outline
docs/                    # constructs and persistent research decisions
tests/                   # unit tests; no network or LLM calls
data/raw/                # immutable local API snapshots (ignored)
data/processed/          # reproducible derived data (ignored)
output/tables/           # generated analysis tables
output/figures/          # generated vector figures
logs/                    # timestamped pipeline logs (ignored)
```

## Limitations

The samples are purposive and cumulative volume is not a direct measure of information aggregation. Sports exclusion uses a transparent but imperfect taxonomy. The determinacy measure is an auditable proxy rather than a validated scale. Relatively few repeated families vary internally in determinacy. The two currently aligned matched histories are too sparse and homogeneous for a divergence–price-wedge test. The strongest next steps are independent signature coding, fixed-window volume, common-horizon prices, and broader cross-platform history coverage.

The relation audit does not force an inequality: election/minerals cases overlap without nesting; Fed remains unclassified beyond conditional non-equivalence; primary ties and leader death clauses allow fractional payouts; suit is adjudicatively incomplete. None currently yields a useful binary marginal restriction. Daily alignment uses up to seven-day forward fill and lacks original price-time provenance. No current coherence test, trader-irrationality conclusion, platform Bayesian ranking or causal divergence-price effect is claimed.
