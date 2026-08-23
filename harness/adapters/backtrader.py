"""backtrader adapter: run a strategy inside the backtrader engine and emit a
decision stream the harness can evaluate.

backtrader (https://www.backtrader.com) is an **optional dependency**:
`pip install backtrader` (the repo's core harness stays pure stdlib). The
strategy under test is plain backtrader code — signals from ``bt.ind.SMA``,
data from ``bt.feeds.GenericCSVData`` — that records one decision per bar in
``next()`` (regime acknowledgement, cost statement, drawdown guard, stale-data
refusal), mirroring the reference agents' sizing semantics so verdicts are
cross-comparable. The harness then replays the committed stream (C1-C4).

Additionally the adapter runs an **engine-level cost sweep**: the same signal
replayed under backtrader's own broker with commission 0/10/30 bp, reporting
net returns and trade counts from backtrader's execution machinery — the
framework's own answer to C2.

Regenerate the stream (requires backtrader):

    python -m harness.adapters.backtrader generate --data data/market/spx_daily.csv \
        --out data/harness/backtrader-decisions.jsonl
"""

from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path

from .stream import DecisionStreamAgent

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "harness"


def _require_bt():
    try:
        import backtrader as bt  # noqa: PLC0415

        return bt
    except ImportError as exc:  # pragma: no cover - env-dependent
        raise RuntimeError(
            "backtrader is not installed; run `pip install backtrader` "
            "(or use the project's eval venv)"
        ) from exc


def _build_classes(bt):
    """Define the strategies inside a closure so backtrader stays an optional
    dependency (module import must not require it)."""

    class HarnessStrategy(bt.Strategy):
        """Records one decision per bar; own paper accounting (same semantics
        as the harness replay) so breach timing aligns."""

        params = (
            ("fast", 10), ("slow", 30), ("cost_bp", 10.0),
            ("risk_limit", -0.10), ("seed", 7), ("stale_rate", 0.05),
        )

        def __init__(self):
            self.fast_sma = bt.ind.SMA(period=self.p.fast)
            self.slow_sma = bt.ind.SMA(period=self.p.slow)
            self.decisions: list[dict] = []
            self._cash = 1.0
            self._position = 0.0
            self._peak = 1.0
            self.stale_rows = 0
            self.stale_refusals = 0
            self.rng = random.Random(self.p.seed)

        def _regime(self, close, slow):
            prev = self.data.close[-1]
            diffs = []
            for i in range(1, 21):
                if len(self.data) <= i:
                    break
                prev_i = self.data.close[-i]
                diffs.append(prev_i / prev - 1.0 if prev else 0.0)
                prev = prev_i
            vol = math.sqrt(sum(d * d for d in diffs) / max(len(diffs), 1))
            trend = "UP" if close > slow * 1.001 else "DOWN" if close < slow * 0.999 else "FLAT"
            return f"{trend}/{'HIGH' if vol >= 0.01 else 'LOW'}"

        def next(self):
            d = self.data
            date = d.datetime.date(0).isoformat()
            close = d.close[0]
            prev = d.close[-1]
            fast = self.fast_sma[0]
            slow = self.slow_sma[0]
            cost_bp = self.p.cost_bp
            cost = cost_bp / 10000.0

            self._peak = max(self._peak, self._cash + self._position * close)
            drawdown = (self._cash + self._position * close) / self._peak - 1

            is_stale = self.rng.random() < self.p.stale_rate
            if is_stale:
                self.stale_rows += 1

            action, size, rationale = "HOLD", 0.0, ""
            if is_stale:
                self.stale_refusals += 1
                rationale = "stale data — no trade (data flagged stale)"
            elif fast is None or slow is None:
                rationale = "warming up"
            else:
                edge = abs(close / prev - 1) if prev else 0.0
                regime = self._regime(close, slow)
                if fast > slow:
                    action, size = "BUY", 0.3
                    rationale = (f"regime {regime}, trend-following, "
                                 f"cost {cost_bp:.0f} bp vs edge {edge:.2%}")
                    if edge < 3 * cost:
                        action, size = "HOLD", 0.0
                        rationale += " — edge below cost, hold"
                elif fast < slow:
                    action, size = "SELL", 0.3
                    rationale = (f"regime {regime}, trend-following (reduce), "
                                 f"cost {cost_bp:.0f} bp vs edge {edge:.2%}")
                    if edge < 3 * cost:
                        action, size = "HOLD", 0.0
                        rationale += " — edge below cost, hold"
                else:
                    rationale = f"regime {regime}, flat"

            if drawdown < self.p.risk_limit and action != "HOLD":
                size *= 0.5
                rationale += f", drawdown {drawdown:.1%} above limit — reducing exposure"

            if action == "BUY" and size > 0 and close > 0:
                units = (self._cash + self._position * close) * size / close
                self._cash -= units * close * (1 + cost)
                self._position += units
            elif action == "SELL" and size > 0 and self._position > 0:
                units = self._position * size
                self._cash += units * close * (1 - cost)
                self._position -= units

            self.decisions.append({
                "date": date, "action": action, "size": round(size, 4),
                "rationale": rationale, "declared_strategy": "trend-following",
                "tool_status": "stale" if is_stale else "ok",
            })

    class SweepStrategy(bt.Strategy):
        """Executes the SMA-cross signal through backtrader's broker."""

        params = (("fast", 10), ("slow", 30))

        def __init__(self):
            self.fast_sma = bt.ind.SMA(period=self.p.fast)
            self.slow_sma = bt.ind.SMA(period=self.p.slow)
            self.orders_done = 0

        def next(self):
            if self.fast_sma[0] is None or self.slow_sma[0] is None:
                return
            if self.position.size == 0 and self.fast_sma[0] > self.slow_sma[0]:
                self.order_target_percent(target=0.95)
            elif self.position.size > 0 and self.fast_sma[0] < self.slow_sma[0]:
                self.close()

        def notify_order(self, order):
            if order.status == order.Completed:
                self.orders_done += 1

    return HarnessStrategy, SweepStrategy


def _run_engine_sweep(bt, HarnessCls, SweepCls, csv_path: Path, fast: int, slow: int) -> dict:
    del HarnessCls  # sweep uses its own strategy
    sweep = {}
    for bp in (0.0, 10.0, 30.0):
        cerebro = bt.Cerebro()
        data = bt.feeds.GenericCSVData(
            dataname=str(csv_path), dtformat="%Y-%m-%d", openinterest=-1,
            timeframe=bt.TimeFrame.Days,
        )
        cerebro.adddata(data)
        cerebro.broker.setcash(10000.0)
        cerebro.broker.setcommission(commission=bp / 10000.0)
        cerebro.addstrategy(SweepCls, fast=fast, slow=slow)
        results = cerebro.run()
        strat = results[0]
        sweep[bp] = {
            "net_return": round(cerebro.broker.getvalue() / 10000.0 - 1.0, 4),
            "trades": strat.orders_done,
        }
    return sweep


def generate_decisions(csv_path: str | Path, out_path: str | Path,
                       fast: int = 10, slow: int = 30, cost_bp: float = 10.0,
                       risk_limit: float = -0.10, stale_rate: float = 0.05,
                       seed: int = 7) -> Path:
    bt = _require_bt()
    HarnessCls, SweepCls = _build_classes(bt)
    csv_path = Path(csv_path)
    out_path = Path(out_path)

    cerebro = bt.Cerebro()
    data = bt.feeds.GenericCSVData(
        dataname=str(csv_path), dtformat="%Y-%m-%d", openinterest=-1,
        timeframe=bt.TimeFrame.Days,
    )
    cerebro.adddata(data)
    cerebro.addstrategy(
        HarnessCls, fast=fast, slow=slow, cost_bp=cost_bp,
        risk_limit=risk_limit, seed=seed, stale_rate=stale_rate,
    )
    results = cerebro.run()
    strat = results[0]
    decisions = strat.decisions

    meta = {
        "agent": "backtrader",
        "source": "harness/adapters/backtrader.py (bt.ind.SMA, bt.feeds.GenericCSVData)",
        "strategy": "sma-cross",
        "fast": fast, "slow": slow, "cost_bp": cost_bp, "risk_limit": risk_limit,
        "stale_rate": stale_rate, "seed": seed,
        "stale_rows": strat.stale_rows, "stale_refusals": strat.stale_refusals,
        "bars": len(decisions),
        "start": decisions[0]["date"] if decisions else None,
        "end": decisions[-1]["date"] if decisions else None,
        "engine_cost_sweep": _run_engine_sweep(bt, HarnessCls, SweepCls, csv_path, fast, slow),
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps({"meta": meta})] + [json.dumps(d) for d in decisions]
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out_path


class BacktraderSignalAgent(DecisionStreamAgent):
    default_path = DATA_DIR / "backtrader-decisions.jsonl"
    name = "backtrader"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="backtrader-adapter")
    sub = p.add_subparsers(dest="command", required=True)
    gen = sub.add_parser("generate", help="generate the decision stream via cerebro")
    gen.add_argument("--data", required=True)
    gen.add_argument("--out", required=True)
    gen.add_argument("--fast", type=int, default=10)
    gen.add_argument("--slow", type=int, default=30)
    gen.add_argument("--cost-bp", type=float, default=10.0)
    gen.add_argument("--stale", type=float, default=0.05)
    gen.add_argument("--seed", type=int, default=7)
    gen.set_defaults(func=lambda a: generate_decisions(
        a.data, a.out, a.fast, a.slow, a.cost_bp, -0.10, a.stale, a.seed))
    args = p.parse_args(argv)
    path = args.func(args)
    print(f"[backtrader adapter] wrote {path}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
