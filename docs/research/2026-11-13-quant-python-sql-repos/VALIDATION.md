# Actual validation and limitations

Date: 2026-11-13 Asia/Shanghai. Local Windows 11 build 26200; CPython 3.12.14.
SQLite3.53.1. No production database, financial data, model, cloud job or trading system used.

## PyPika reproducibility

| Scope | Observed result |
| --- | --- |
| Clean baseline, fixed dev dependencies | 1,208 PASS |
| Eight corrected new regressions against unchanged baseline | 6 ERROR (stale alias), 2 PASS |
| Candidate full suite | 1,216 PASS; exit 0 |
| Added regression scope | 8 tests, 7 execute synthetic in-memory SQLite queries |
| Upstream pre-commit on both changed files | PASS; file-type checks without matching files SKIPPED |
| Remote CI / maintainer review | No checks/review reported at observation; NOT VERIFIED |

Base `93facd17d443c2b0b2d9ca4b6da55857667289a9`; candidate
`37452621f549ba121e6fbe1063d92a8301c2d9ad`.
Changed production behavior is limited to traversing aggregate FILTER predicates
while preserving the parent's existing argument/copy behavior. Tests cover SUM,
COUNT(*), compound filters, nested COALESCE, unrelated tables, chained replacement
and original-object preservation. Literal synthetic pnl values are unitless test
integers, not investment results.

Reproduce at the candidate checkout in a separate development environment:

```powershell
python -m pip install parameterized==0.9.0 black==25.9.0 pre-commit==4.2.0
python -X utf8 -m unittest discover -s pypika/tests
pre-commit run --files pypika/terms.py pypika/tests/test_criterions.py
```

The negative control loaded the candidate test class against the clean baseline
package and confirmed the imported baseline module location. It is not a claim
that the preexisting baseline suite itself had six product failures.

## Failure ledger

- Initial baseline without parameterized: 1,139 discovered with six import errors.
  Installing the fixed dev dependency resolved the environment blocker.
- First draft of one test used a Joiner instead of completing cross_join with
  `.cross()`; corrected before the final base/head comparison. That helper error
  is not counted as evidence of an upstream defect.
- An initial sandboxed formatter attempt stalled and was interrupted; subsequent
  per-file formatter checks and upstream pre-commit passed.
- A fork CLI option combination was unsupported; corrected CLI invocation created
  the verified fork. No upstream history was rewritten.
- The first P-Research suite in the sandbox ran 67 tests with 15 temporary-folder
  permission errors. The same tree in host context passed all 67; an unclosed
  SSL socket ResourceWarning was observed. No assertion was weakened to pass.

## Not tested

Backtrader installation/compatibility, DuckDB speed, Ibis backend equivalence,
SQLGlot full suite, Polars memory, Qlib training/returns, live database services,
production capacity, real PIT data and financial performance are **NOT RUN**.
This is neither a cross-platform tox matrix nor a full security/license audit.

The root P-Research test result and public payload check are recorded in
REPOSITORY_TEST_RECEIPT.json after actual execution. Catalogue integrity tests
validate documentation metadata, not the external repositories' correctness.
