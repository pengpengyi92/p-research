# 📏 Quant×AI Evaluation Harness

**The missing risk layer for open trading agents, delivered as a measurement
rig** — the implementation of Paper 3, §6
([paper3-quant-ai.md](../papers/paper3-quant-ai.md)).

The open-source frontier has productized the agent loop (market data, tool
registries, memory, autonomous research→decide→execute) — but almost none of
the risk layer that institutional quant treats as non-negotiable: backtest
hygiene, cost modeling, hard risk limits, attribution. This harness measures
**behavioral risk properties** of any trading agent, the way a risk desk files
exceptions — not the way a leaderboard ranks returns.

## Design (Paper 3, §6.1)

1. **Public data only** — one public OHLCV CSV
   ([`data/market/spx_daily.csv`](https://raw.githubusercontent.com/pengpengyi92/p-research/main/data/market/spx_daily.csv),
   provenance [here](https://github.com/pengpengyi92/p-research/blob/main/data/market/PROVENANCE.md));
   every result re-derives from it.
2. **Agent-agnostic interface** — any agent implementing
   `observe(state) -> Decision` can be evaluated; internals are a black box,
   behavior is the test subject.
3. **Checks, not leaderboards** — pass/fail on risk-relevant properties, with
   published thresholds.
4. **Failure modes are first-class outputs** — a clean diagnosis beats an
   impressive return.
5. **Zero dependencies, deterministic, no LLM in the chain** — pure Python
   standard library, same corpus-pipeline philosophy as the rest of P-Research.

## The four checks

| Check | What it measures | Pass signal |
|---|---|---|
| **C1 — Strategy drift under regime change** | whether the agent's *stated* strategy (from its own rationales) drifts with the regime | stated strategy is regime-stable even when returns are not |
| **C2 — Cost sensitivity** | edge survival at the stated cost model + whether decision volume falls as costs rise | edge survives 10 bp; volume falls 0→30 bp (cost-awareness, not cost-blindness) |
| **C3 — Drawdown behavior** | whether stated risk limits are behavior, not decoration | exposure falls after the declared drawdown limit is breached, and the trace says so |
| **C4 — Tool-use failure modes** | stale-data / broker-error handling at controlled injection rates | no trades on flagged-stale data; explicit retry/degrade; trace acknowledges failures |

Every check reports a **(behavioral, disclosure)** score pair: behavior
without disclosure is a silent failure; disclosure without behavior is
decoration.

## Evaluation cohort

Five agents are evaluated on the same public SPX series (2021-08 → 2026-08,
1255 bars) — same inputs, differentiated verdicts:

| Agent | Type | Capability | Result |
|---|---|---|---|
| **`disciplined`** — trend-following with a risk overlay | reference (in-loop) | reacts to cost/drawdown/failures per bar | **4/4** ([md](sample-disciplined.md) · [json](sample-disciplined.json)) |
| **`reckless`** — momentum chaser (strategy flips with regime, trades through costs, never reduces, trades on stale data) | reference (in-loop) | same | **0/4** ([md](sample-reckless.md) · [json](sample-reckless.json)) |
| **`dsh-quant`** — own Quant OS (SMA-cross + its `tradingCost`/drawdown/stale refusal) | black-box decision stream | `stream` | **4/4** ([md](sample-dsh-quant.md) · [json](sample-dsh-quant.json)) |
| **`backtrader`** — in-process backtest engine (bt.ind.SMA strategy + engine-level cost sweep) | framework decision stream | `stream` | **4/4** ([md](sample-backtrader.md) · [json](sample-backtrader.json)) |
| **`freqtrade`** — strategy framework (IStrategy, vectorized populate_*) | framework decision stream | `stream` | **3/4** ([md](sample-freqtrade.md) · [json](sample-freqtrade.json)) |

Cohort findings so far:

- **The three framework/library agents score like the disciplined reference**
  (4/4) when their strategies carry the same risk layer — cross-framework
  consistency is itself a validation of the checks.
- **freqtrade fails C3** (drawdown behavior, behavioral 0.00 / disclosure 0.10):
  its strategy reduces entry size in a guard but never responds at position
  level, and its trace rarely acknowledges drawdown state. This is a genuine
  framework-level finding — freqtrade's vectorized strategy API makes dynamic
  per-bar sizing hard — exactly what the harness is for. The ecosystem map
  predicted freqtrade would be the most informative on C3; it is.
- All stream agents honestly report C2's volume-response as not applicable and
  C4 as not exercised; their own stale refusals (52-79/79 rows) are in the
  report metadata.

Streams are generated once by each framework's own code and committed
(`data/harness/`), so the demo stays pure stdlib; regeneration commands are in
each adapter module docstring (`harness/adapters/backtrader.py`,
`harness/adapters/freqtrade.py` — both need the eval venv: `pip install
backtrader` / `pip install freqtrade`).

## Capabilities

The harness measures what an agent can express. `capabilities` on the agent
declares its mode:

- `{"in-loop"}` — the agent reacts per-`observe` to cost, drawdown, and
  injected tool failures → all four checks are fully exercisable.
- `{"stream"}` — precomputed decision stream → C2 scores edge survival (volume
  response reported as not applicable), C4 is reported not exercised, C1/C3
  evaluate the stream's stated strategy and drawdown response directly.

This keeps "passing" honest: a stream agent can never claim a C4 pass it did
not earn by refusing stale data in-loop — it is reported as not exercised.

## Metric note (C1)

Strategy drift is computed over *stated* strategies only: rationales that name
no strategy family ("flat", "warming up", stale refusals) are honest silence,
not a flip, and are excluded. An agent that never states a strategy is
reported as not exercised. (This was fixed in v0.2: the initial metric
penalized honest flat periods as drift.)

## Quickstart

```bash
# no dependencies beyond the Python standard library
python3 -m harness demo                        # all five agents -> docs/harness/
python3 -m harness run --agent freqtrade       # any stream agent by name
python3 -m harness run --agent disciplined --format json --out report.json
python3 -m unittest tests.test_harness         # 24 tests
```

Evaluate your own agent: implement the `observe(state) -> Decision` protocol
(see `harness/agent.py`), or emit a decision stream (one JSON per bar, with
`date`/`action`/`size`/`rationale`/`declared_strategy`) and load it through an
adapter like
[`harness/adapters/dsh_quant.py`](https://github.com/pengpengyi92/p-research/blob/main/harness/adapters/dsh_quant.py).
Run with `--data your.csv`.

## Scope honesty

This harness measures **behavioral risk properties of open research
artifacts** — strategy stability, cost discipline, drawdown response, failure
handling. It is **not** investment advice and does not rank agents by
profitability. The market verifies returns; this harness verifies discipline.
