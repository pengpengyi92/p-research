# Testing and debugging: observed versus proposed

Environment: Windows11 build26200, CPython3.12.14, DuckDB2.0.0 (MIT).
Only a14.7MiB binary wheel installed in a fresh ignored .venv; no extras, model,
GPU, market data or paid service. Setup used local uv with a project-local cache.
Python/DuckDB versions are pinned/tested, not assumed valid on every OS/version.

## Commands and receipts

From the repository root:

```powershell
python -X utf8 -m unittest discover -s tests
python -X utf8 -m unittest discover -s examples/duckdb_pit_research/tests -v
python -X utf8 skills/jane-street-socratic-tutor/verify_snapshot.py
python -m examples.duckdb_pit_research.run --output .cache/a-fresh-run
```

scripts/record_tests.py runs those test suites with immutable labels, timestamp,
OS/Python/DuckDB, exact normalized command, exit/counts and sanitized output hash.
It removes host paths; raw private machine logs are not exported.
Observed initial receipts: core-baseline67/67 PASS, example-first37/37 PASS,
exit0,0skip. Final reruns and counts are in reports/verification; CI NOT RUN
unless a separate observed receipt explicitly changes that status.

Final observed runs (2026-11-12UTC /2026-11-13Asia/Shanghai):
example-complete48/48 PASS at17:25:50-17:25:59UTC; core-final-stdlib71/71 PASS
at17:26:02UTC, DuckDB NOT_INSTALLED in that interpreter;0fail/0error/0skip.
The13Tutor integrity tests are included in71, not a learner-efficacy measurement.
Staged/final source run and identical deterministic output receipts are recorded
separately after the source commit is actually created.

## Coverage

Hand-calculated 0.05/0.01 anchors; frozen generation; snapshot16andlabel24row
comparison; NULLs; inclusive/microsecond boundary; late bar and known revision;
dynamic membership; six-cutoff future mutations; label perturbation isolation;
five deliberately wrong SQL semantics; duplicates/schema/price/NaN/time ordering;
fill/label timing; purge60min embargo; cost monotonicity; zero-cash turnover;
missing labels; negative outcome; shuffled rows; offset normalization; unknown
mutation rejection; disabled external access; deterministic output; no-overwrite;
CLI missing input. These are software checks, not economic or learning tests.
Additional boundaries cover nonpositive NAV rejection (no bankruptcy model),
integer seed, timezone-normalized membership revisions, zero-signal cash,
deterministic tie-break, source/output hashes and tampered result/report rejection.

## Actual failure ledger

1. First uv venv attempt used an inaccessible sandbox temp cache. Installation
   then failed because no environment existed. Recreated with local cache and
   authorized host execution; pinned wheel installed. No global config changed.
2. First direct TIMESTAMPTZ fetch failed: DuckDB requested missing pytz. Kept
   timezone-aware types/SQL semantics, cast to VARCHAR only at output boundary
   and normalize strings. No undeclared dependency or naive timestamp workaround.
3. Full test/mutation failures, if any, retain separate labeled receipts; never
   rewrite a failed run as PASS. A detected wrong query is an expected negative
   control, not a failed candidate suite.

## Debugging rules

If equivalence fails, inspect version IDs, availability and NULLs before PnL.
If only provenance passes, still compare session choice: latest-arrival bug is
causal but uses the wrong lookback. A final-revision-before-asof bug may merely
drop valid history; absence of leaked rows alone is not sufficient validation.
Changing labels must not change feature output; an available_at guard alone
cannot prove all future feature implementations are safe.

No network required after installing the wheel. Do not interpret a future-data
mutation suite as proof against every possible leakage. Real datasets, corporate
actions, cross-platform CI, coverage percentage and model/tutor learning gains
remain NOT RUN / UNMEASURED as applicable.
