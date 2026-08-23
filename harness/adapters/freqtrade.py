"""freqtrade adapter: a freqtrade IStrategy evaluated as a harness agent.

freqtrade (https://www.freqtrade.io) is an **optional dependency**:
`pip install freqtrade` (the repo's core harness stays pure stdlib).

The strategy under test is genuine freqtrade code — an ``IStrategy`` subclass
using freqtrade's indicator and parameter framework — driven directly by the
adapter: we build a pandas frame from the public OHLCV CSV, call
``populate_indicators`` / ``populate_entry_trend`` / ``populate_exit_trend``,
and harvest per-bar signals plus a ``harness_rationale`` column the strategy
writes with the same discipline properties the harness measures (regime
acknowledgement, cost statement, drawdown guard, stale-data refusal). The
adapter then emits the standard decision stream the harness replays (C1-C4).

Note on scope: this evaluates the *strategy's* decision behavior, not
freqtrade's full backtesting runtime (fee/slippage modeling, hyperopt). The
harness's cost-tier replay covers C2's edge-survival; freqtrade's own
backtesting remains available as a cross-check.

Regenerate the stream (requires freqtrade):

    python -m harness.adapters.freqtrade generate --data data/market/spx_daily.csv \
        --out data/harness/freqtrade-decisions.jsonl
"""

from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path

from .stream import DecisionStreamAgent

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "harness"


def _require():
    try:
        import pandas as pd  # noqa: PLC0415
        from freqtrade.strategy import IStrategy  # noqa: PLC0415

        return pd, IStrategy
    except ImportError as exc:  # pragma: no cover - env-dependent
        raise RuntimeError(
            "freqtrade is not installed; run `pip install freqtrade` "
            "(or use the project's eval venv)"
        ) from exc


def _build_strategy(pd, IStrategy, fast: int, slow: int, stale_rate: float, seed: int):
    """Define the IStrategy subclass in a closure (freqtrade stays optional).

    NB: class bodies treat any name assigned inside the body as a body-local,
    so closure params are captured under distinct names (_fast/_slow/_startup)
    to avoid the classic `x = x` NameError shadowing trap.
    """

    _fast, _slow, _startup = fast, slow, slow + 2

    class HarnessFreqStrategy(IStrategy):
        """SMA-cross trend-follower with the harness discipline properties,
        writing per-bar rationales into a harness_rationale column."""

        INTERFACE_VERSION = 3
        timeframe = "1d"
        can_short = False
        minimal_roi = {"0": 100}
        stoploss = -0.30
        startup_candle_count = _startup
        process_only_new_candles = True

        FAST = _fast
        SLOW = _slow
        STALE_RATE = stale_rate
        SEED = seed
        risk_limit = -0.10
        cost_bp = 10.0

        def populate_indicators(self, dataframe, metadata=None):
            import numpy as np  # noqa: PLC0415

            dataframe["harness_fast"] = dataframe["close"].rolling(self.FAST).mean()
            dataframe["harness_slow"] = dataframe["close"].rolling(self.SLOW).mean()
            dataframe["harness_ret"] = dataframe["close"].pct_change()
            dataframe["harness_vol"] = (
                dataframe["harness_ret"].rolling(20).std().fillna(0.0)
            )
            dataframe["harness_peak"] = dataframe["close"].cummax()
            dataframe["harness_dd"] = dataframe["close"] / dataframe["harness_peak"] - 1.0

            rng = random.Random(self.SEED)
            n = len(dataframe)
            stale = [rng.random() < self.STALE_RATE for _ in range(n)]
            dataframe["harness_stale"] = stale
            dataframe["harness_cost_bp"] = self.cost_bp
            dataframe["harness_risk_limit"] = self.risk_limit
            return dataframe

        def populate_entry_trend(self, dataframe, metadata=None):
            df = dataframe
            fast, slow = df["harness_fast"], df["harness_slow"]
            up = (fast > slow) & (df["close"] > slow * 1.001)
            down = (fast < slow) & (df["close"] < slow * 0.999)
            trend = df["close"].ge(slow * 1.001).map({True: "UP"})
            trend = trend.where(trend.notna(), df["close"].le(slow * 0.999).map({True: "DOWN"}))
            trend = trend.fillna("FLAT").astype(str)
            trend = trend.where(trend.isin(["UP", "DOWN"]), "FLAT")
            vol = df["harness_vol"].ge(0.01).map({True: "HIGH"}).fillna("LOW").astype(str)
            regime = trend + "/" + vol

            edge = df["close"].pct_change().abs().fillna(0.0)
            cost_frac = df["harness_cost_bp"] / 10000.0
            cost_ok = edge >= 3.0 * cost_frac

            size = 0.3
            dd = df["harness_dd"]
            in_guard = dd < df["harness_risk_limit"]

            # rationale per bar (vectorized)
            df["harness_rationale"] = (
                "regime " + regime + ", trend-following, cost "
                + df["harness_cost_bp"].astype(int).astype(str)
                + " bp vs edge " + (edge * 100).round(2).astype(str) + "%"
            )
            df["harness_rationale"] = df["harness_rationale"].where(
                up, "regime " + regime + ", flat"
            )
            df["harness_size"] = size
            df.loc[in_guard & up, "harness_rationale"] = (
                df.loc[in_guard & up, "harness_rationale"]
                + ", drawdown above limit — reducing exposure"
            )
            df.loc[in_guard & up, "harness_size"] = 0.15
            df.loc[~cost_ok & up, "harness_rationale"] = (
                df.loc[~cost_ok & up, "harness_rationale"] + " — edge below cost, hold"
            )
            df.loc[~cost_ok & up, "harness_size"] = 0.0

            df["enter_long"] = up & cost_ok
            return df

        def populate_exit_trend(self, dataframe, metadata=None):
            df = dataframe
            fast, slow = df["harness_fast"], df["harness_slow"]
            df["exit_long"] = (fast < slow) & (df["close"] < slow * 0.999)
            return df

    return HarnessFreqStrategy


def generate_decisions(csv_path: str | Path, out_path: str | Path,
                       fast: int = 10, slow: int = 30, cost_bp: float = 10.0,
                       risk_limit: float = -0.10, stale_rate: float = 0.05,
                       seed: int = 7) -> Path:
    pd, IStrategy = _require()
    StratCls = _build_strategy(pd, IStrategy, fast, slow, stale_rate, seed)
    csv_path = Path(csv_path)
    out_path = Path(out_path)

    df = pd.read_csv(csv_path)
    df.columns = [c.strip().lower() for c in df.columns]
    df["date"] = pd.to_datetime(df["date"])
    strat = StratCls({})
    df = strat.populate_indicators(df)
    df = strat.populate_entry_trend(df)
    df = strat.populate_exit_trend(df)

    decisions = []
    long = False
    stale_rows = 0
    stale_refusals = 0
    for _, row in df.iterrows():
        date = row["date"].strftime("%Y-%m-%d")
        is_stale = bool(row["harness_stale"])
        if is_stale:
            stale_rows += 1
        rationale = str(row["harness_rationale"])
        action, size = "HOLD", 0.0
        if is_stale:
            stale_refusals += 1
            action, rationale = "HOLD", "stale data — no trade (data flagged stale)"
        elif bool(row["enter_long"]):
            action = "BUY"
            size = float(row["harness_size"])
            long = True
        elif long and bool(row["exit_long"]):
            action = "SELL"
            size = 1.0  # full liquidation on the exit signal (trend follower)
            long = False
        decisions.append({
            "date": date, "action": action, "size": round(size, 4),
            "rationale": rationale, "declared_strategy": "trend-following",
            "tool_status": "stale" if is_stale else "ok",
        })

    meta = {
        "agent": "freqtrade",
        "source": "harness/adapters/freqtrade.py (IStrategy populate_* driven directly)",
        "strategy": "sma-cross",
        "fast": fast, "slow": slow, "cost_bp": cost_bp, "risk_limit": risk_limit,
        "stale_rate": stale_rate, "seed": seed,
        "stale_rows": stale_rows, "stale_refusals": stale_refusals,
        "bars": len(decisions),
        "start": decisions[0]["date"] if decisions else None,
        "end": decisions[-1]["date"] if decisions else None,
        "note": "evaluates the strategy's decision behavior; freqtrade's own "
                "backtesting runtime (fee modeling/hyperopt) is a cross-check, not run here",
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps({"meta": meta})] + [json.dumps(d) for d in decisions]
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out_path


class FreqtradeSignalAgent(DecisionStreamAgent):
    default_path = DATA_DIR / "freqtrade-decisions.jsonl"
    name = "freqtrade"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="freqtrade-adapter")
    sub = p.add_subparsers(dest="command", required=True)
    gen = sub.add_parser("generate", help="generate the decision stream")
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
    print(f"[freqtrade adapter] wrote {path}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
