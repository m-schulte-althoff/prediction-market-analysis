# Same Future, Different Claim

This project audits when apparently similar prediction-market questions expose traders to different settlements and when written rules leave a scenario to later adjudication. The case-led working paper uses verified Hilton first-place versus advancement settlements, Khamenei's recorded 45-cent versus YES settlements, and the Zelenskyy clothing/adjudication episode. Minerals contracts provide an observed chronology with two YES outcomes; other archived-rule scenarios remain explicitly hypothetical.

**Payoff divergence** requires different payouts in an explicitly specified scenario. **Written-rule determinacy** asks whether a specified rule version determines the payout given the information held fixed. Ordinary expected-payout reasoning includes fractional amounts and expectations about adjudication. This is a diagnostic empirical contribution, with no priority claim for payoff mappings or new Bayesian updating result.

The historical metadata sample remains fixed at 19,500 rows (12,251 Kalshi; 7,249 Polymarket). Its Polymarket selection used a flawed sports filter. The filter is repaired for future acquisition; excluded historical records and the exact rejected/overflow split cannot be recovered. The old composition-reversal and platform-ranking claims are withdrawn. Literal text features provide portfolio context; the composite is an exploratory specificity index. Activity and terminal-error analyses are supplementary, with platform-qualified family-clustered uncertainty for the exact preferred volume formula.

Start with [PAPER_OUTLINE.md](output/PAPER_OUTLINE.md), [RESEARCH_SUMMARY.md](output/RESEARCH_SUMMARY.md), the [casebook](output/REPRESENTATION_CASEBOOK.md), and [supplementary analysis](output/SUPPLEMENTARY_ANALYSIS.md). Approval, pre-revision preservation and validation are recorded in `output/paper-revision/2026-10-12-01/`.

## Reproduce the approved revision from restored archives

Use the existing `pyproject.toml` and lockfile with [uv](https://docs.astral.sh/uv/). Raw data are local and Git-ignored. No network calls are required for these commands:

```bash
uv sync --dev
uv run python3 main.py preprocess --retrieval-date 2026-09-10
uv run python3 main.py match
uv run python3 main.py anecdotes --retrieval-date 2026-09-10 \
  --case-evidence output/paper-revision/2026-10-12-01/case-evidence/case-source-bundle.json
uv run python3 main.py panel --retrieval-date 2026-09-10 \
  --history-snapshot data/raw/matched-price-histories-2026-09-10-bad72f8883-interval-max.json
uv run python3 main.py analyze
uv run pytest -q tests/test_acquisition.py tests/test_preprocessing.py tests/test_taxonomy.py
uv run pytest -q tests/test_semantics.py tests/test_analysis.py
uv run pytest -q tests/test_anecdotes.py tests/test_coherence.py tests/test_matching.py tests/test_panel.py
uv run ruff check .
uv run mypy .
```

The explicitly selected history version reproduces the dormant retained pair inventory after clipping. The currently selected ID hash has no corresponding archive; using its default path fails rather than collecting fresh historical responses. The alternate `627b27c83f-interval-max` history has a third still-eligible pair and remains preserved. The anecdote bundle is derived from versioned official records and independent event sources preserved during the approved review, rather than a replacement metadata sample.

The manuscript consists of Markdown and SVG artifacts; there is no PDF/TeX build. `analyze` regenerates the paper, summary, status, confidence overview, supplementary note, tables and figures. It never rewrites the persistent [research log](output/research-log.md). Meaningful decisions and failed attempts are appended by the research agent. Old paper materials and related implementation sources are saved in `output/paper-revision/2026-10-12-01/pre-revision/` with SHA-256 hashes.

On Windows, use `uv run python` if `python3` resolves to the Store shim. Static checking targets the installed Python 3.12 interpreter and numerical-library stubs; Python 3.11 compatibility is not separately validated in this session. Tooling excludes the preserved archive and `work/` scratch files from mypy.

## Acquisition and provenance

Only unauthenticated official Kalshi and Polymarket APIs feed the metadata pipeline. Named case records additionally cite independent event reporting and certified election results. Endpoint, selection, timestamp and outcome details are in [DATA_SOURCES.md](DATA_SOURCES.md).

`download` or `all` can acquire a new current-date sample when explicitly desired. An absent historical or future-date cache fails before network access. Cache reuse validates recorded selection parameters, including the Kalshi per-tier cap. New responses record `acquired_at_utc`; legacy `retrieved_at_date` labels remain readable without invented acquisition timestamps. The three source updates on September 11 under a September 10 wrapper remain an unresolved inconsistency.

The outcome schema separates recorded Kalshi binary results and scalar payouts from Polymarket endpoint-price inference and final-status evidence. Original intraday history timestamps and fill ages survive daily aggregation. Neither closure fields nor daily bucket labels prove synchronized-price freshness. No optional `coherence-price-observations.csv` has been supplied or collected.

## File structure

```text
main.py                  # controller and explicit cached-stage dispatch
views.py                 # deterministic vector figures
src/
  config.py              # paths, immutable-cache and acquisition-date guards
  kalshi.py              # official Kalshi metadata acquisition/cache validation
  polymarket.py          # official Polymarket metadata acquisition/cache validation
  taxonomy.py            # reason-coded substantive sports classification
  preprocessing.py       # normalized rows, outcome/exposure/attrition ledgers
  semantics.py           # literal text cues and exploratory specificity index
  matching.py            # phenomenon retrieval and claim candidate screening
  panel.py               # clipped source histories, daily buckets and fill ages
  anecdotes.py           # versioned cases and complete-input assertion audits
  coherence.py           # guarded binary-relation/price diagnostics
  analysis.py            # selected-portfolio supplementary models and profiles
  reporting.py           # generated case-led manuscript and companion outputs
docs/                    # constructs, decisions and historical source audit
tests/                   # focused deterministic tests; no network or LLM calls
data/raw/                # immutable restored official API snapshots (ignored)
data/processed/          # reproducible derived tables (ignored)
output/tables/           # generated evidence, analysis and audit tables
output/figures/          # deterministic SVG figures
output/paper-revision/   # approval, reviews, case evidence and preservation archive
work/                    # intermediate implementation diagnostics (ignored)
logs/                    # timestamped pipeline logs (ignored)
```

## Main outputs and interpretation

- `preprocessing-normalization-ledger.csv`, `preprocessing-outcome-ledger.csv` and `preprocessing-exposure-ledger.csv`: reconcile retained rows and evidence categories.
- `representation-case-matrix.csv`: complete operative inputs, source roles, hypothetical/observed labels, payouts and audit eligibility. Changed inputs block stale assertions.
- `analysis-platform-profiles.csv`: literal components and threshold-stratified exploratory composite descriptions.
- `analysis-market-models.csv`: existing specifications, exact preferred family-clustered row and same-formula HC3 comparison, confidence intervals and sample sizes.
- `coherence-case-diagnostics.csv` and `coherence-panel-readiness.csv`: explicit missing-evidence gates. Missing excess means not estimable.

The portfolios are purposive and selected by volume; categories and family units differ by platform. The index lacks independent human construct validation. Case evidence establishes existence and distinctions, without population prevalence, trader understanding, causal effects, manipulation findings or account-level redemption audits. Account reimbursements and contract settlement amounts are separate. Interface recommendations are untested proposals. Deferred work O1–O4 requires separate approval.
