# Synthetic PIT research results

SYNTHETIC ONLY / NOT INVESTMENT PERFORMANCE / NO TRADE

Fixture canonical SHA-256: `5d7ea8c851dec37c9977da0bf4b677b92f6198355daafa22e793b1eb21b6aa11`.

SQL/Python: 16 snapshots and 24 labels match (tolerance1e-12).
Portfolio outputs match using shared accounting, not two independent broker engines.

Mutation detection: 5/5; future-data invariance: 6 decision cutoffs in both implementations.
Label perturbation does not alter either implementation's signals.

## Calendar partition

```json
{
  "train": [
    "D0",
    "D1"
  ],
  "purged": [
    "D2"
  ],
  "oos": [
    "D3",
    "D4",
    "D5"
  ],
  "embargo_minutes": 60,
  "fitted_parameters": false
}
```

## Three-decision synthetic OOS partition

| Policy | Net return | Observations |
| --- | ---: | ---: |
| positive_top1 | -8.163357% | 3 |
| equal_weight_ready | -2.573942% | 3 |
| cash | 0.000000% | 3 |

Negative values are preserved. These hand-constructed data do not establish alpha,
statistical significance, real OOS or generalization. Annualized Sharpe is NOT IDENTIFIABLE.

## Cost sensitivity (return fraction, not percentage points)

```json
{
  "0.0": {
    "positive_top1": -0.0776591372957145,
    "equal_weight_ready": -0.021605877028374465,
    "cash": 0.0
  },
  "7.0": {
    "positive_top1": -0.08163357018193795,
    "equal_weight_ready": -0.025739421017424213,
    "cash": 0.0
  },
  "20.0": {
    "positive_top1": -0.08898434158455615,
    "equal_weight_ready": -0.03338508449924826,
    "cash": 0.0
  }
}
```

Base cost7bps/side is a synthetic assumption (5commission +2slippage), not a venue fee.
Each invested day opens and closes a unit gross book: turnover2; consecutive books are not netted.

## Mutation diagnostics

- event_time_only: DETECTED; row 0 field current_id differs: 'SYN_A-2026-01-09-r0' != 'SYN_A-2026-01-09-r1'
- published_only: DETECTED; row 0 field current_id differs: 'SYN_A-2026-01-09-r0' != 'SYN_A-2026-01-09-r1'
- global_latest_before_asof: DETECTED; row 0 field current_id differs: 'SYN_A-2026-01-09-r0' != 'SYN_A-2026-01-08-r0'
- future_membership: DETECTED; row count differs
- latest_arrival: DETECTED; row 9 field previous_id differs: 'SYN_A-2026-01-13-r0' != 'SYN_A-2026-01-09-r1'

## Next bounded experiment

Add a second predeclared synthetic fixture with different arrival lags and universe events.
Do not tune on this result or treat passing software tests as a trading permission.
