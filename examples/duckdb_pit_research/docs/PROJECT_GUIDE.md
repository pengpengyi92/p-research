# Project guide: what, architecture and interfaces

Artifact P-RESEARCH-SYN-PIT-001 v0.1.0. Owner: P-Research / Pengyi Peng.
Goal: learn and verify Python/SQL quant data reasoning before choosing a larger
backtest framework. No reference to employer requirements or internal systems.

## Architecture

1. fixtures.py generates a fixed original JSON input; byte/canonical hashes differ
   in meaning and are both recorded. No data is downloaded.
2. model.validate enforces schema, keys, explicit missing values, positive integer
   price units, aware timestamps, availability order and revision chronology.
3. model.python_snapshots implements explicit known-membership/history loops.
4. duckdb_backend + snapshots.sql independently implement relational windows.
5. Python/labels.sql calculate forward returns separately from feature logic.
6. Common evaluate computes weights, round-trip turnover, exposures, cost and
   net/gross/equity diagnostics. It is not an independent exchange simulator.
7. run.experiment applies oracle, provenance, mutations, causality and isolation;
   write_run emits results + manifest + human report without overwriting.
8. verify_run checks frozen input, eight source files and both result/report
   byte hashes offline. It is an integrity check, not a signature or alpha test.

## Input contract

JSON schema_version1 / SYNTHETIC_ONLY; top-level keys: seed,symbols,evaluation_at,
decisions,features,memberships,opens. See frozen fixture for exact row fields.
Prices: integer cents, positive or explicit NULL close only; NULL open not valid.
Features unique `(symbol,session,revision)` plus feature_id; memberships unique
`(symbol,effective_at,revision)` plus membership_id; opens unique symbol/event_at;
decisions unique ID and instant. Input list order is irrelevant; availability per
logical event must not move backwards with revision. Times require explicit zone,
normalize to UTC; session refers to the UTC event date.

## Output / function interfaces

`python_snapshots(data)` / `duckdb_backend.snapshots(data)` return ordered dict rows
with decision/symbol, membership ID, current/previous feature IDs, prices,
availability, READY/MISSING_VALUE/INSUFFICIENT_HISTORY and signal or NULL.
`python_labels` / SQL labels return all24decision-symbol forward-return rows;
missing/not-yet-evaluated price produces NULL. Labels never select a portfolio.
`experiment` returns comparison, snapshots, labels, three policy books, split,
cost sensitivity, five negative-control receipts and six causal checks.

## Setup / operations

Python3.12.14 and pinned DuckDB2.0.0 actually tested on Windows11 build26200.
requirements.txt belongs only to this optional example; root package stays
stdlib-only. Run commands are in ../README.md. DuckDB is in-memory, one thread,
128MB buffer limit, external access disabled; no model, secret, DB daemon or API.
TIMESTAMPTZ is used internally; timestamps are explicitly cast to strings at the
result boundary to avoid an undeclared pytz fetch dependency, then normalized.

## Rights / boundaries / handoff

Original code follows this repository's MIT code licensing. Synthetic fixture
is owner-authored; no licensed prices, protected alpha expression or private
communications. Tutor upstream six files remain unchanged with MIT attribution;
exercise pack is original, not Jane Street interview material or endorsement.

No real PIT/OOS, production trading, exchange keys, paid models, deployment or
commercial data permission. Review observed results/limits, then predeclare a
new fixture or take the first learner diagnostic. EADB status is scoped local
engineering acceptance, not registration in another private repository.
