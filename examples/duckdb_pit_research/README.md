# Synthetic PIT Research Lab · DuckDB + Python

Version **0.1.0**. Original synthetic-only engineering example inside P-Research;
not a core runtime dependency, market-data product, live strategy or alpha claim.

## 研究问题

在每次 09:00 UTC 决策时，哪些成分股、哪一个历史数据版本真正已经可得？
用当时已知的最近两个 session 收盘价构造一阶动量，比较纯 Python 与 DuckDB SQL：

`source → validate → known membership → known revision/session → signal → allocation → isolated labels → costs → evaluation`

输入包含 **31 条价格版本、5 条成分事件、28 条 synthetic 开盘价、6 个决策**。
有迟到行情、历史修订、恰好在决策时可得的数据、未及时获知的成分股变更、显式 NULL。
所有价格都是原创合成的整数分，不是任何交易所报价。UTC 时点不模拟真实交易日历。

## Run

From the P-Research repository root, with a separate Python3.12 environment:

```powershell
python -m venv .venv
.venv/Scripts/python -m pip install -r examples/duckdb_pit_research/requirements.txt
.venv/Scripts/python -m examples.duckdb_pit_research.run --output .cache/pit-run-001
.venv/Scripts/python -m examples.duckdb_pit_research.verify_run --run .cache/pit-run-001
.venv/Scripts/python -m unittest discover -s examples/duckdb_pit_research/tests -v
```

POSIX: use `.venv/bin/python`. Core P-Research still runs without DuckDB; only
this optional example requires `duckdb==2.0.0`. No pandas, model, DB server,
credentials, extensions, market downloads, GPU or paid service.

Each run requires a **fresh output directory** and produces RESULTS.json,
RUN_MANIFEST.json and RESEARCH_REPORT.md. The frozen fixture is generated from
seed166; regeneration refuses to overwrite the existing source fixture.

## Information-set contract

- Per decision, choose membership effective **and available** by that instant.
- Per `(symbol, session)`, choose the highest revision **among already available
  versions**, then choose the latest two market sessions. Never globally dedup
  to the final revision before doing the as-of filter.
- `event_at <= published_at <= available_at <= decision_at < fill_at < exit_at`.
  Membership announcements can precede their future effective date; both
  effective and available constraints still apply.
- `available_at == decision_at` is included; one microsecond later is excluded.
- NULL closes remain missing signals. Missing labels remain NULL, never zero.
- Labels are ex-post synthetic next-open returns, isolated from signal creation.
- SQL/Python compare row keys, version IDs, NULLs, timestamps and values, not just
  aggregate PnL. Float comparison tolerance is1e-12; portfolio accounting is shared.

## Controls and interpretation

Five deliberately wrong SQL variants must be detected: event-time-only,
publication-only, global-final-revision-before-asof, future membership and
latest-arrival-instead-of-latest-session. Future-only data changes must not alter
past decisions in either implementation. Changing labels must not alter signals.

The fixed top1-positive policy is compared with equal-weight-ready and cash.
Cost is a synthetic **7bps/side** (5commission +2slippage), full daily round trips
with no netting between adjacent days. One training-candidate day is purged;
remaining label intervals plus60-minute embargo precede the synthetic OOS split.
No model is fitted and no parameter is selected using these outcomes.

The three-decision synthetic OOS top1 return is negative (approximately -8.16%).
Preserve that finding: passing code tests does not turn it into a useful alpha.
Annualized Sharpe is NOT IDENTIFIABLE; real PIT/OOS, capacity, execution, T+1,
lots, limits and market impact are NOT IMPLEMENTED/NOT RUN.

## EADB delivery and practice

- [Project guide and architecture](docs/PROJECT_GUIDE.md)
- [Testing / debugging and failure ledger](docs/TESTING_AND_DEBUGGING.md)
- [Versioned upgrade / initial delivery](docs/UPGRADE.md)
- [Hypothesis and predeclared protocol](docs/HYPOTHESIS_CARD.md)
- [Categorical EADB acceptance](docs/EADB_ACCEPTANCE.md)
- [Benchmark](BENCHMARK_CARD.md), [TODO](TODO.md), [source ledger](docs/SOURCES.md)
- [Socratic Tutor practice](tutor/README.md): one diagnostic question at a time;
  human mastery and tutor effectiveness remain **UNMEASURED**.

Observed test receipts are in [reports/verification](reports/verification/).
The [fixed run](reports/reference_run/RESEARCH_REPORT.md) is generated from the
committed source; [reproduction receipt](reports/REPRODUCTION.json) confirms two
byte-identical result files. Exact source commit, environment, input/code/output hashes
belong to its manifest; do not confuse artifact publication with validation.

[Machine EADB card](EADB_CARD.json): local engineering acceptance only;
scientific/economic validity NOT MET, production NO-GO and learning UNMEASURED.
