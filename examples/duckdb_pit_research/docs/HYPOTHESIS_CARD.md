# Hypothesis / preregistered scope

ID SYN-PIT-MOM-001; version0.1.0; original synthetic fixture seed166.
This file specifies a bounded demonstration, not a preregistered external trial.

Engineering hypothesis H1: filtering versioned records by true available_at before
session/revision selection yields the same information set as an explicit Python
reference and is invariant to changes strictly after each decision.
Reject H1 if any golden anchor, row/version/NULL/time/value comparison, future
invariance, label isolation or intended mutation detection fails.

Exploratory economic hypothesis H2: positive one-session close momentum can beat
equal-weight-ready/cash after declared costs on this fixture. Mechanism would be
short-term persistence; sign is ambiguous because reversal/costs can dominate.
H2 cannot establish real alpha on synthetic hand-constructed prices; even a
positive result would not close scientific validity. Preserve negative results.

Universe: four synthetic identifiers; membership known as of each decision.
Frequency: six daily decision instants, Jan12-19,2026 UTC; fictional calendar.
Feature: `(current_close - previous_close) / previous_close`, two latest known
sessions, using the latest revision actually available by09:00. Missing means
no signal, not an imputed zero. Signal sign and topK=1 fixed before first result.
Earliest hypothetical fill09:30; exit next fixture-session09:30; use ex-post
observed synthetic open prices only for labels/accounting.

Policies: positive-top1 (symbol lexical tie-break), equal-weight of READY
members, cash. Per-side commission5bps +slippage2bps; daily full round trip,
no netting across consecutive books, no compounding across missing-price gaps.
Cost sensitivity0/7/20bps per side is descriptive, not a parameter search.

Calendar split: D0-D2 training candidates; D3-D5 synthetic OOS; purge any training
label whose exit plus60min is not strictly before the first OOS decision. D2 is
purged. No fitting, hyperparameter search or data-driven promotion occurs.

Data rights: generated here, no external market data. Split/corporate-action
adjustments, halts, T+1, limits, round lots, borrow, financing, capacity, queue,
latency and impact: NOT IMPLEMENTED. Sharpe: NOT IDENTIFIABLE in this tiny sample.
One held-out-looking partition is not independent real-world external validation.
