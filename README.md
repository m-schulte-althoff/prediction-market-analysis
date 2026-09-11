# Same Future, Different Claim

This repository studies how prediction-market platforms turn ostensibly shared future phenomena into different digitally tradable and institutionally resolvable claims. It separates **semantic determinacy** within a contract from **semantic divergence** between contracts and combines systematic Kalshi/Polymarket metadata with an audited counterfactual casebook.

The clearest result is representational: an election call and an inauguration, a 12.5-basis-point move under different quantization conventions, an announced versus signed minerals agreement, undefined “suit” attire, and announcement versus actual departure can map the same world history to different settlements. Each claim is backed by archived official rule text and a witness state in which the payouts separate.

The corrected metadata sample contains 12,251 Kalshi and 7,249 Polymarket non-sports binary contracts. The preferred exposure/cohort-adjusted association between determinacy and standardized log volume is −0.115 (HC3 SE 0.009), but it is primarily a between-family pattern: within-family estimates are −0.035 (p=.597) on Kalshi and +0.031 (p=.262) on Polymarket. The association is detectable for quantitative-threshold contracts, not qualitative contracts, and changes sharply by platform and period. These diagnostics make the volume result an interesting secondary finding rather than evidence that ambiguity causes trading.

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

## Design

The construct architecture is documented in [docs/CONSTRUCTS.md](docs/CONSTRUCTS.md), with consequential choices in [docs/DECISIONS.md](docs/DECISIONS.md). In brief:

- determinacy asks whether one contract maps a relevant world history uniquely to a settlement;
- divergence asks whether two contracts about one phenomenon can settle differently;
- automated text and metadata distances retrieve candidates but do not prove semantic equivalence;
- a coded divergence requires a plausible witness state and implied settlement on both sides.

The determinacy proxy averages source specificity, temporal specificity, operational definition, edge-case completeness, and discretion clarity. Calendar years are distinguished from substantive quantitative thresholds. Volume models include the original baseline, observed-exposure/opening-cohort adjustment, resolved-only estimates, qualitative/quantitative splits, leave-one-component-out checks, family clustering and aggregation, and estimates based only on within-family variation.

Matching now has two stages: retrieval uses shared-phenomenon language without quantities, while claim-equivalence screening separately considers full wording, numeric overlap, predicates, and deadlines. This prevents divergent thresholds or dates from automatically removing an otherwise useful phenomenon candidate.

## Data sources

Only unauthenticated official APIs are used:

- Kalshi series, live/historical markets, historical cutoff, event records, and candlesticks.
- Polymarket Gamma market/event metadata and CLOB token price histories.

Polymarket sports rows are removed before its high-volume cap using official sports fields plus the conservative taxonomy in `src/taxonomy.py`. Exact endpoints, fields, selection rules, and limitations are in [DATA_SOURCES.md](DATA_SOURCES.md).

## Main outputs

- [Research summary](output/RESEARCH_SUMMARY.md): current contribution, cases, estimates, interpretation, and paper storyline.
- [Representation casebook](output/REPRESENTATION_CASEBOOK.md): plain-language explanations with exact archived rules.
- [Research status](output/RESEARCH_STATUS.md): concise handoff of current evidence and locked decisions.
- `output/tables/representation-case-matrix.csv`: structured signatures, witness states, payouts, URLs, scope, and confidence.
- `output/tables/analysis-market-models.csv`: all main and robustness estimates.
- `output/tables/matching-representative-pairs.csv`: auditable automated candidates; divergence columns remain diagnostics.
- `output/figures/views-conceptual-schematic.svg`: one phenomenon branching into platform-specific claims.
- `output/figures/views-determinacy-volume.svg`: descriptive score–volume pattern.

## File structure

```text
main.py                  # controller / command dispatch
views.py                 # vector figures
src/
  anecdotes.py           # official-rule archive and witness-state case matrix
  taxonomy.py            # shared sports exclusion rules
  preprocessing.py       # normalized contract database and observed exposure
  semantics.py           # determinacy and diagnostic divergence features
  matching.py            # phenomenon retrieval and claim screening
  panel.py               # diagnostic price-history alignment
  analysis.py            # empirical models and robustness checks
  reporting.py           # generated research documents
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
