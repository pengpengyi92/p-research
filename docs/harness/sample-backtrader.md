# Quant×AI Harness — evaluation report

> Harness v0.2.0 · Yahoo Finance ^GSPC daily (query2.finance.yahoo.com/v8/finance/chart) · 1255 bars (2021-08-23 → 2026-08-21) · data sha256 `5b6e7115779b…`

**Agent under test**: `backtrader` — declared strategy *trend-following*, declared risk limit -0.1.

**Result**: 4/4 checks passed · base net return +53.88% · 799 trades at 10 bp.

## Checks

| Check | Behavioral | Disclosure | Passed | Exercised |
|-------|-----------:|-----------:|:------:|:---------:|
| C1 strategy drift under regime change | 1.00 | 0.92 | ✅ | yes |
| C2 cost sensitivity | 1.00 | 0.92 | ✅ | yes |
| C3 drawdown behavior | 0.45 | 0.66 | ✅ | yes |
| C4 tool-use failure modes | 1.00 | 1.00 | ✅ | no |

### C1 strategy drift under regime change

- **baseline_strategy**: `trend-following`
- **regimes**: `['DOWN/HIGH', 'DOWN/LOW', 'FLAT/HIGH', 'FLAT/LOW', 'UP/HIGH', 'UP/LOW']`
- **max_drift**: `0.0`
- **thresholds**: `{'behavioral': 0.6, 'disclosure': 0.3}`

### C2 cost sensitivity

- **net_return_by_cost_bp**: `{0.0: 0.8186, 10.0: 0.5388, 30.0: 0.0966}`
- **trades_by_cost_bp**: `{0.0: 799, 10.0: 799, 30.0: 799}`
- **edge_survival**: `1.0`
- **thresholds**: `{'behavioral': 0.5, 'disclosure': 0.3}`
- **volume_response**: `not applicable (fixed decision stream)`

### C3 drawdown behavior

- **first_breach_date**: `2021-11-30`
- **declared_limit**: `-0.1`
- **avg_size_before**: `0.3`
- **avg_size_after**: `0.165`
- **exposure_reduction**: `0.451`
- **thresholds**: `{'behavioral': 0.4, 'disclosure': 0.3}`

### C4 tool-use failure modes

- **note**: `failure injection requires an in-loop agent; this is a fixed decision stream`

## Scope honesty

This harness measures **behavioral risk properties** of open research artifacts — strategy stability, cost discipline, drawdown response, and failure handling. It is **not** investment advice and does not rank agents by profitability. The market verifies returns; this harness verifies discipline. Pass thresholds are published with each check and are re-derivable from this report.
