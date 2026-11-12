# Observed verification report

Evidence date2026-11-13 Asia/Shanghai; timestamps below are2026-11-12UTC.
OS Windows11 build26200; Python3.12.14; optional example DuckDB2.0.0.

| Receipt | Command / scope | Exit | Observed |
| --- | --- | ---: | --- |
| core-baseline17:19:11 | `python -X utf8 -m unittest discover -s tests` | 0 | 67PASS/0fail/0error/0skip |
| example-first17:20:57 | `python -X utf8 -m unittest discover -s examples/duckdb_pit_research/tests -v` | 0 | 37PASS |
| example-final17:23:30 | same optional suite, plus practice metadata | 0 | 40PASS |
| example-sealed17:24:45 | same suite, added boundary cases | 0 | 45PASS |
| example-complete17:25:50 | same suite, added source/output tampering | 0 | 48PASS/0fail/0error/0skip |
| core-final-stdlib17:26:02 | core/reference suite, DuckDB NOT_INSTALLED | 0 | 71PASS/0fail/0error/0skip |

Each raw sanitized log and JSON receipt has exact environment, command, timestamp,
observed counts and log SHA-256 under verification/. The13Tutor integrity tests
are a subset of core71, not13additional experiments. Native Windows only;
cross-platform CI NOT RUN. Existing harness fixture "FAIL" outputs are expected
negative samples inside passing core tests, not candidate-suite failures.

Fixed fixture canonical SHA-256:
`5d7ea8c851dec37c9977da0bf4b677b92f6198355daafa22e793b1eb21b6aa11`.
31feature versions/5membership events/28opens/6decisions. Snapshot16andlabel24
rows match; five wrong SQL variants detected; six cutoff invariances checked
in both implementations; label changes leave features unchanged.

The data/label paths are independent, while portfolio accounting is shared.
No identical-PnL-only proof. Original hand anchors and temporal/adversarial
checks independently constrain the comparison.

Failures retained: first sandbox uv-cache permission error and consequent missing
venv install; initial TIMESTAMPTZ fetch required uninstalled pytz. The former was
resolved with authorized host/local-cache setup; the latter with explicit UTC
output serialization, preserving TIMESTAMPTZ semantics and a one-package example.
An editing patch with a nonexistent context line was rejected before changing
files; corrected patch applied. No test assertion was weakened to hide failure.

All current candidate suites pass. Single-run walltime is a manifest observation,
not a speed comparison. Source-only commit and reproducible fixed-run output
hashes are recorded in reference_run/RUN_MANIFEST.json after actual generation;
publication receipts pin their remote Git identities separately.

Scientific validity NOT MET; production NO-GO. Negative toy net return retained;
Sharpe NOT IDENTIFIABLE; Tutor learner evaluation and delayed recall NOT RUN.

## Sealed source reproduction

Actual source commit: `0ea3421549e6cccd044af29c2d144e7459e7e76c`.
Both48example and71core tests rerun on this clean tree (before and after tests);
the core interpreter has no DuckDB. Separate13Tutor integrity checks PASS and
remain a subset, not additional unique core tests. Exact final receipts:
verification/example-committed.json, core-committed-stdlib.json and
tutor-committed.json. Fixture/test source hashes are recorded in each receipt.

Two complete CLI executions began on that clean source and produced identical
RESULTS.json bytes. REPRODUCTION.json records the SHA and comparison; manifests
retain differing timestamps/walltime, as expected. The stdlib-only output verifier
passed eight source hashes, fixture hashes and two output hashes. No cross-platform
or external financial replication is implied. Final source/outputs remain public
synthetic scope; remote publication/readback is a separate delivery event.
