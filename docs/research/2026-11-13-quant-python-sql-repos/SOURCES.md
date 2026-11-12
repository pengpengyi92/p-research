# Primary source ledger

Observed 2026-11-13 Asia/Shanghai. Web documentation is mutable; repository
metadata has individual UTC observation timestamps in REPOSITORY_SOURCES.json.
Only the PyPika base/candidate below is a pinned code-level reproduction.

| ID | Primary source | Use / limitation |
| --- | --- | --- |
| S01 | [Backtrader features](https://backtrader.com/home/features/) / [feed contract](https://www.backtrader.com/docu/datafeed/) / [operating](https://www.backtrader.com/docu/operating/) | Event-driven roles; not an independent installation test |
| S02 | [backtesting.py](https://github.com/kernc/backtesting.py) | Project's own positioning, not reproduced performance |
| S03 | [bt documentation](https://pmorissette.github.io/bt/) | Portfolio/rebalance components; documentation example not our result |
| S04 | [Qlib](https://github.com/microsoft/qlib) | qrun research workflow; displayed returns not independently reproduced |
| S05 | [DuckDB Python/Ibis](https://duckdb.org/docs/current/guides/python/ibis) / [FROM and ASOF](https://duckdb.org/docs/lts/sql/query_syntax/from) | SQL/Python and join semantics, no local speed measurement |
| S06 | [Ibis SQL tutorial](https://ibis-project.org/tutorials/coming-from/sql) / [DuckDB backend](https://ibis-project.org/backends/duckdb) | Relational Python API; package is ibis-framework, not unrelated ibis |
| S07 | [SQLGlot API](https://sqlglot.com/sqlglot.html) / [contributing](https://github.com/tobymao/sqlglot/blob/main/CONTRIBUTING.md) | Parser/optimizer and contribution policy; no execution engine claim |
| S08 | [PyPika baseline terms.py](https://github.com/kayak/pypika/blob/93facd17d443c2b0b2d9ca4b6da55857667289a9/pypika/terms.py) / [candidate](https://github.com/kayak/pypika/commit/37452621f549ba121e6fbe1063d92a8301c2d9ad) / [PR3559](https://github.com/kayak/pypika/pull/3559) | Actual code-level reproduction; not maintainer acceptance |
| S09 | [Polars SQLContext](https://docs.pola.rs/user-guide/sql/intro/) | Lazy SQL/DataFrame interfaces, not performance benchmark |
| S10 | [Point72/polars-io-tools](https://github.com/Point72/polars-io-tools) | I/O and pushdown architecture; not internal deployment evidence |
| S11 | [SQLGlot PR9040](https://github.com/tobymao/sqlglot/pull/9040) | Existing ASOF/join rewrite work; avoided duplicate contribution |
| S12 | [PyPika issue3551](https://github.com/kayak/pypika/issues/3551) | Separate IN/NOT IN container issue with reporter's proposed solution; not our patch |

GitHub API URLs, license metadata and pushed_at values for all ten candidates
are stored in REPOSITORY_SOURCES.json. API fields are dated observations, not
release dates, maintenance guarantees, legal opinions or quality ratings.
