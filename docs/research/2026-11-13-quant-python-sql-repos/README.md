# Quant-relevant Python + SQL repositories

Observed: 2026-11-13 (Asia/Shanghai). This is a fixed ten-repository research
shortlist, not an exhaustive census, performance ranking or production approval.
"btrader" is interpreted here as **Backtrader**; `bt` is a different project.

## 结论

**先用 DuckDB + Python 学数据研究，再接策略回测。** 这是基于接口与任务匹配的
建议，不是本轮跑分结论。DuckDB 是 SQL 分析引擎；Ibis 把 Python 关系表达式接到
SQL 后端；PyPika/SQLGlot 分别适合读 SQL 构造与解析/变换代码。
[DuckDB Python/Ibis guide](https://duckdb.org/docs/current/guides/python/ibis),
[Ibis SQL tutorial](https://ibis-project.org/tutorials/coming-from/sql),
[SQLGlot docs](https://sqlglot.com/sqlglot.html).

Backtrader 的重点是数据 feed、策略生命周期、订单与事件驱动回测，**不是 SQL 引擎**。
可以把 SQL 产出的、带可得时间的数据接到 feed，但不能因此认为 PIT、交易成本、
成交约束或数据授权已经解决。[Features](https://backtrader.com/home/features/),
[Data feeds](https://www.backtrader.com/docu/datafeed/).

## 十个仓库：不同层次，不是十个替代品

| Repository | 重点 / Python-SQL 接点 | 量化研究切入点 | 本轮边界 |
| --- | --- | --- | --- |
| [DuckDB](https://github.com/duckdb/duckdb) | C++ 引擎、Python API、原生 SQL | Parquet、窗口、分组、ASOF、PIT 数据集 | 文档/元数据；未跑本机 DuckDB 性能测试 |
| [Ibis](https://github.com/ibis-project/ibis) | Python 关系表达式和 SQL 后端 | 同一表达式的编译、执行和后端语义差异 | 文档/元数据；未跑跨后端等价测试 |
| [PyPika](https://github.com/kayak/pypika) | Python SQL query builder，不执行 SQL | 动态研究查询、表达式树、表替换与条件复用 | 实际代码审查、SQLite 回归、上游 PR |
| [SQLGlot](https://github.com/tobymao/sqlglot) | Python SQL parser/transpiler/optimizer | 方言、AST、作用域、优化前后结果等价 | 审查相关代码/Issue；已有重叠 PR，不重复提交 |
| [Polars](https://github.com/pola-rs/polars) | Rust 核心、Python API、SQLContext | lazy 数据变换、窗口与 SQL/表达式对照 | 文档/元数据；未测速度或内存 |
| [Point72/polars-io-tools](https://github.com/Point72/polars-io-tools) | Python lazy I/O、SQL predicate/projection pushdown | 数据源裁剪、时间窗口、join 与查询计划 | 文档/元数据；未运行数据库服务 |
| [Backtrader](https://github.com/mementum/backtrader) | Python 事件驱动回测 | feed → indicator → strategy → order → broker | 文档/元数据；未验证当前 Python 兼容矩阵 |
| [backtesting.py](https://github.com/kernc/backtesting.py) | Python 策略回测 API | 小型策略原型与执行假设审查 | 文档/元数据；未重跑回测 |
| [bt](https://github.com/pmorissette/bt) | Python 组合/调仓组件 | selection、weighting、rebalance、组合树 | 文档/元数据；未验证收益与成本模型 |
| [Qlib](https://github.com/microsoft/qlib) | Python ML quant research workflow | dataset → model → signal → backtest → analysis | 文档/元数据；未下载数据、训练或复现收益 |

用途来源见 [SOURCES.md](SOURCES.md)；原始 GitHub 元数据和观察时间见
[REPOSITORY_SOURCES.json](REPOSITORY_SOURCES.json)。星数、公司名和文档中的示例收益
不作为质量分数。没有证据说明任何具体团队在内部使用了这里建议的组合。

## Backtrader 到底怎么样？

- 适合读 Python 的事件循环、状态、订单生命周期和自定义数据 feed。
- 不适合把它当作 SQL 仓库、数仓、自动防未来函数工具或已验证的生产执行系统。
- 本次 API 观察到该仓库 `archived=false`、`pushed_at=2024-08-19`。
  这只表示该次公开仓库元数据，不能推出“已经停止维护”；当前依赖兼容性未实测。
- GPL-3.0（GitHub 元数据）需要在分发/集成前单独审查。backtesting.py 的元数据为
  AGPL-3.0；不能把它们的源文件直接复制进 MIT 项目而忽略许可义务。
- 如果目的是 Python/SQL 双练，先用 DuckDB 或 SQLite 生成可核对的数据表，再明确
  feature availability 和 earliest fill，最后才接回测层。

## 一项实际贡献，而不是只收集链接

[PyPika PR #3559](https://github.com/kayak/pypika/pull/3559)
修复 filtered aggregate 替换表时漏掉 `FILTER` 条件的错误：

```python
from pypika import Table, functions as fn
old = Table("trades", alias="old")
new = Table("archived_trades", alias="new")
expression = fn.Sum(old.pnl).filter(old.side == "BUY")
expression.replace_table(old, new)
# Before: SUM("new"."pnl") FILTER(WHERE "old"."side"='BUY')
# After:  SUM("new"."pnl") FILTER(WHERE "new"."side"='BUY')
```

Baseline: `93facd17d443c2b0b2d9ca4b6da55857667289a9`.
Candidate: `37452621f549ba121e6fbe1063d92a8301c2d9ad`.
Local full suite: **1,216 PASS**, including eight added regressions and seven
in-memory SQLite query checks. The unmodified baseline fails six of the eight
new tests; the two positive controls pass. See [VALIDATION.md](VALIDATION.md).

At observation the PR is **OPEN**, with no review decision or remote check runs
reported by GitHub. Submission is not upstream acceptance. The patch does not
fix every table-replacement case, IN/NOT IN containers or analytic window keys.

## 建议学习顺序

1. Python 数据契约 + SQL 分组/窗口/去重/NULL + 同一 fixture 结果核对。
2. PIT/ASOF、发布时间与首次可得时间；显式构造会泄漏的反例。
3. PyPika/SQLGlot 的 AST 与不可变复用；先证明语义错，再修正和跑回归。
4. 再接 Backtrader/bt 的策略、订单和组合层；ML 工作流另看 Qlib。

具体练习与可证伪验收见 [TRAINING_PLAN.md](TRAINING_PLAN.md)。这些练习除明确列明的
PyPika/SQLite 回归外 **NOT RUN**；学习收益、查询速度和交易收益均 **UNMEASURED**。

## 交付边界

本文件夹是原始研究说明与公开软件证据，不含私有研究档案、市场原始数据、
私信、凭据或内部职业计划。未运行交易、付费模型或云服务。仓库许可证不授予
行情数据的再分发权；对文档的阅读不等于完整代码或安全审计。
