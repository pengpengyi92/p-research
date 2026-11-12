# Repository-selection benchmark

- **Baseline:** no unified, dated Python/SQL quant shortlist; PyPika base
  93facd17 has 1,208 passing existing tests but fails six new stale-alias cases.
- **Change:** fixed ten-repo comparison and a bounded aggregate FILTER traversal
  fix; no benchmark-driven claim that one framework is universally best.
- **Measure:** primary sources, license metadata, roles, fixed base/head tests,
  positive controls, SQLite execution and upstream pre-commit.
- **Result:** candidate 1,216 PASS; eight added tests; seven execute SQLite.
  PR3559 OPEN, remote CI/acceptance not verified. Documentation test receipt is
  separate from upstream software evidence.
- **Trade-off:** PyPika is not a SQL engine; backtest tools are not PIT data
  systems. Broad repo comparison is documentation-level, not ten full audits.
- **Next Action:** same-fixture Python/SQL as-of test, then choose a backtest
  layer only after timestamp, data-rights and cost contracts are explicit.

Learning benefit, production throughput, memory, strategy Sharpe and investment
performance: **UNMEASURED**.
