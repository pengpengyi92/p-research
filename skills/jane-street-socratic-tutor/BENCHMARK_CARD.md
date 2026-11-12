# Jane Street Socratic Tutor Import Benchmark

## Baseline

P-Research at 95beded has no tracked Jane Street skill snapshot. Its 49 existing
tests pass with explicit UTF-8 in the authorized Windows host environment.
The initial sandbox run had 15 Temp permission errors; the next default-GBK
host run had one decoding error. No pipeline code was changed to recover.

## Change

Vendor all six Git files from upstream 7c6715c without modifying their bytes.
Add Chinese provenance/usage/meaning/limits, a manifest, offline verifier and
negative integrity controls. No global skill installation or new model call.

## Measure

Same upstream commit and canonical raw Git objects for every file. Verify Git
blob and root tree IDs plus SHA-256/length/inventory. Mutation tests reject
modified skill, missing license, extra file, unsafe path and metadata changes.
Run old and added project tests under the same explicit UTF-8 setting.

## Result

Six-file snapshot and root tree match. Thirteen added integrity tests pass.
The full changed-tree suite passes 62 tests; the baseline passes 49 tests.
Observed commands, initial failures and limits are recorded in TEST_REPORT.md.
These results measure import integrity, not tutor behavior or learner benefit.

## Trade-off

Retains upstream copyright and exact bytes, but is a frozen directory snapshot,
not a GitHub fork parent relationship or automatic upstream synchronization.
Model correctness, pedagogy, delayed recall and task routing remain unverified.
Root package version and presearch/harness source behavior are unchanged.

## Next Action

Select and pin one authorized model/backend and a valid ordinary-tutor baseline
before using the fixed six-case dialogue protocol. Score protocol compliance,
answer correctness, delayed recall, human time and token cost separately.
Behavioral advantage and cost are UNMEASURED; no arbitrary combined quality score.
