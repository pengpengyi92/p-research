# Python / SQL quant research learning protocol

Status: proposed exercises; NOT RUN except the separately recorded PyPika tests.
Use synthetic fixtures first. Choose an authorized fixed tutor/model separately;
no claim that a tutor skill or company label improves learning.

## Fixed tasks and falsifiable checks

| Task | Python baseline | SQL / repository path | Pass condition |
| --- | --- | --- | --- |
| Grouped PnL with NULL and duplicate trades | Explicit reference loop | SQLite/DuckDB GROUP BY/FILTER | Exact row multiset and NULL semantics; duplicates rejected by agreed key |
| Lagged daily feature | Per-symbol sorted records | LAG/window partition | Changing future rows must not change earlier features |
| As-of signal join | Filter available_at <= decision then choose latest | DuckDB ASOF plus explicit availability filter | Late revisions cannot enter earlier decisions; cardinality preserved |
| Cross-sectional rank | Fixed as-of membership fixture | Window rank and deterministic ties | Delisted/late entrants do not silently alter history |
| Query reuse | Rebuild each query from scratch | PyPika replace_table with FILTER | Original unchanged; generated query executes and matches reference |
| Train/OOS split | Explicit calendar and embargo lists | SQL materialized split | No overlapping label horizon crosses the boundary |
| Order lifecycle | Fixed synthetic feed | Backtrader or bt, separately installed | Earliest fill after availability; modeled costs cannot raise net PnL |

## Protocol

1. Freeze 20-50 synthetic rows, timestamps, expected outputs, seed and hash.
2. Explain behavior before running; implement Python reference first.
3. Use the same fixture and cost convention in SQL and Python. Compare values,
   cardinality, NULLs, ordering assumptions and dtypes, not only runtime.
4. Add one deliberate leak, duplicate and wrong join. The validator must reject
   each mutation. A test that only executes without error is insufficient.
5. Measure correctness on held-out variants. Only then measure time, memory,
   dependencies and implementation complexity. Report UNMEASURED before execution.
6. For any upstream contribution, search existing issues/PRs, read the current
   contributor/AI policy, reproduce the bug on base, then show candidate results.

## Suggested reading paths

- Data track: DuckDB Python integration -> SQL windows/ASOF -> Ibis expression
  compilation -> Polars plans and I/O pushdown.
- Language/tooling track: PyPika Term/Function/criterion traversal -> SQLGlot
  parsing/scope/optimizer rule ordering. Query construction is not query execution.
- Quant track: Backtrader data/strategy/broker boundary -> bt allocation/rebalance
  -> Qlib dataset/model/evaluation workflow. Backtest outputs are not live alpha.

## Benchmark

Baseline: reference loops + explicit SQL with no helper AST transformation.
Change: introduce one library at a time. Measure exact semantic equality,
mutation detection, setup cost, latency and memory on the same held-out fixture.
Result: only PyPika FILTER replacement is currently measured; learning gain,
database speed and economic value remain UNMEASURED. Next: implement the small
availability-time join exercise before choosing a larger quant framework.
