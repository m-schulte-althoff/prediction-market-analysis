# Semantic Determinacy in Prediction Markets

This repository implements a first end-to-end empirical study of how prediction-market platforms define the future events they subsequently price. It introduces transparent measures of **semantic determinacy** within contracts and **semantic divergence** across same-event contracts, using official public data from Kalshi and Polymarket.

The initial sample contains 12,251 non-sports Kalshi contracts and 3,663 non-sports binary Polymarket contracts spanning 2020–2026. The main exploratory result is unexpected but robust enough to motivate follow-up work: lower determinacy is associated with higher within-platform trading volume. The association survives controls for rule length, duration, category, platform, series-clustered uncertainty, and aggregation to 1,366 series/events. Determinacy does not predict Kalshi last-trade absolute forecast error. This pattern is consistent with semantic indeterminacy stimulating trade through heterogeneous interpretations without demonstrably improving accuracy; it is associative, not causal.

The matcher also isolates 11 manually inspected, high-confidence cross-platform pairs. Leader-departure contracts supply the clearest examples: announcement, actual removal, death, and caretaker rules can map the same real-world trajectory to different formal outcomes. Only three accepted pairs currently expose aligned histories through both official history endpoints, so the matched-price analysis remains diagnostic rather than confirmatory.

## Reproduce the results

Install [uv](https://docs.astral.sh/uv/), then run:

```bash
uv sync --dev
uv run python3 main.py all
uv run pytest -q
uv run ruff check .
uv run mypy .
```

On Windows, where the `python3` executable name may resolve to the Microsoft Store shim, use uv's managed `python` executable:

```powershell
uv run python main.py all
```

Pipeline stages can be run separately:

```bash
uv run python3 main.py download
uv run python3 main.py preprocess
uv run python3 main.py match
uv run python3 main.py panel
uv run python3 main.py analyze
```

The downloader caches date-stamped raw API responses and never overwrites them. To reproduce the included September 10, 2026 package exactly when those local snapshots are present:

```bash
uv run python3 main.py all --retrieval-date 2026-09-10 \
  --kalshi-series-limit 120 --polymarket-limit 8000 --matched-panel-limit 12
```

Raw and processed data are intentionally Git-ignored. A fresh future run will use the then-current API archive and may differ as platforms revise metadata or API coverage.

## Data sources

Only unauthenticated official platform APIs are used:

- Kalshi series, live/historical markets, historical cutoff, and daily candlesticks.
- Polymarket Gamma market metadata via keyset pagination and CLOB token price histories.

Exact endpoints, fields, retrieval dates, coverage, and limitations are documented in [DATA_SOURCES.md](DATA_SOURCES.md).

## Measurement and analysis

The 0–1 determinacy composite averages five auditable components:

1. named resolution-source specificity;
2. explicit date/time/timezone specificity;
3. operational outcome definition;
4. edge-case and fallback completeness;
5. absence of discretionary resolution language.

Rule length and conditional-clause counts remain separate from determinacy. The cross-platform divergence measure separately compares wording, numeric/date conditions, named sources, required event stages, and deadlines. No LLM annotations or expensive model calls are needed.

Market models use standardized log volume within platform. Main uncertainty is HC3; a robustness model clusters by Kalshi series or Polymarket event, and another collapses repeated contracts to those units. Kalshi last-trade error is tested separately with series-clustered uncertainty. Price histories are oriented to YES and aligned daily using only contemporaneous or earlier observations.

## Main outputs

- [Research summary](output/RESEARCH_SUMMARY.md): question, mechanism, estimates, examples, storyline, abstract, and next steps.
- [Research log](output/research-log.md): all substantive iterations, including the terminal-error null and limited matched-price specification.
- `output/tables/analysis-market-models.csv`: main and robustness models.
- `output/tables/matching-representative-pairs.csv`: full rules for auditable matched examples.
- `output/figures/views-determinacy-volume.svg`: the central descriptive pattern.
- `output/figures/views-matched-trajectories.svg`: the three currently aligned matched pairs.

## File structure

```text
main.py                  # controller / command dispatch
views.py                 # tables and vector figures
src/
  config.py              # paths and sample design
  http_client.py         # bounded retries for public APIs
  kalshi.py              # Kalshi acquisition
  polymarket.py          # Polymarket acquisition
  preprocessing.py       # common contract database
  semantics.py           # determinacy/divergence measures
  matching.py            # conservative event matching
  panel.py               # price-history alignment
  analysis.py            # empirical models
  reporting.py           # research log and summary
tests/                   # unit tests; no network or LLM calls
data/raw/                # immutable local API snapshots (ignored)
data/processed/          # reproducible derived data (ignored)
output/tables/           # analysis tables
output/figures/          # vector figures
logs/                    # timestamped pipeline logs (ignored)
```

## Current limitations

The samples are purposive rather than population-representative: Kalshi uses the 120 highest-volume series in pre-specified non-sports categories, and Polymarket uses the 8,000 highest-volume closed markets before binary/sports filtering. Cumulative volume is participation, not aggregation quality. Terminal prices are not measured at a common forecast horizon. Archive category labels are sparse on Polymarket, requiring a fixed keyword taxonomy. Match precision has been manually checked only for the 11 accepted pairs, and official cross-platform history overlap is currently sparse. These limitations bound every claim in the generated research summary.

