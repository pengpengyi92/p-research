# Baseline -> Change -> Measure -> Result -> Trade-off -> Next Action

## Baseline

P-Research8412aa3 has a ten-repo guide,67 passing core tests and the pinned
Socratic Tutor snapshot, but no executable DuckDB/Python PIT comparison case.
The independent stdlib reference and hand-computed anchors are the correctness
baseline, not DuckDB agreeing with itself. Wrong SQL variants are negative controls.

## Change

Optional v0.1.0 example: frozen synthetic inputs, independent snapshot/label
implementations, explicit common accounting, mutation/causality tests and practice.
Root runtime dependency list, core CLI, corpus, survey and imported skill untouched.

## Measure

Fixed seed166; same fixture for both engines; compare16snapshot and24label rows,
identities/NULLs/times/values at1e-12 tolerance; detect5wrong query semantics;
mutate future data at6cutoffs and labels independently. Test data contracts,
calendar purge, costs, missing prices, deterministic output and no-overwrite.
Use exact command receipts/environment/hash manifests; CI is a separate status.

## Result

Final48example tests PASS;71core/reference tests PASS in a runtime without
DuckDB (baseline67). The13Tutor snapshot tests are part of the core suite,
not13additional independent learner tests. Receipts are in reports/verification.
Remote CI NOT RUN; it is not inferred from these local counts.
Top1 synthetic OOS is about -8.16% over only3decisions; negative evidence retained.
Sharpe, real-world alpha, learning effect and production value UNMEASURED.

## Trade-off

Tiny data make correctness review cheap, not economically representative.
Two independent data/label implementations share accounting: not independent
backtest engines. DuckDB128MB configuration is not a process RSS cap. No speed
claim is inferred from one run. Five mutations are not all possible leakage.

## Next Action

Freeze a second arrival-lag fixture before looking at its results; separately
begin a single learner diagnostic without assigning unobserved mastery scores.
