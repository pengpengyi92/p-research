"""dsh-quant adapter: decision stream -> harness agent.

dsh-quant (github.com/pengpengyi92/dsh-quant, npm package ``dsh-quant``) is the
program's own open-source Quant OS (46 tools, 6 domains). Its
``cli/harness-signal.mjs`` runs dsh-quant's own loop — SMA-cross signal from
``lib/dsh-alpha``, cost guard from ``lib/dsh-execution/trading-cost``,
drawdown guard, stale-data refusal — and emits a deterministic decision stream
(JSONL: one meta line + one decision per bar).

This adapter loads that stream and exposes it to the harness as a black-box
agent with capability ``stream``: decisions are precomputed, so C2's
volume-response dimension and C4's failure injection are honestly reported as
not exercisable (the harness already handles both paths).

Regenerate the stream (requires the dsh-quant repo, Node.js, zero deps):

    node cli/harness-signal.mjs --data data/market/spx_daily.csv \\
        --out data/harness/dsh-quant-decisions.jsonl
"""

from __future__ import annotations

import json
from pathlib import Path

from ..agent import ACTION_HOLD, Decision

DECISIONS_DEFAULT = (
    Path(__file__).resolve().parent.parent.parent / "data" / "harness" / "dsh-quant-decisions.jsonl"
)


class DshQuantSignalAgent:
    """Black-box agent wrapping a dsh-quant decision stream (stateless: looks
    up decisions by bar date, so the same instance can be replayed across
    cost tiers)."""

    capabilities = {"stream"}

    @classmethod
    def decisions_path(cls) -> Path:
        return DECISIONS_DEFAULT

    def __init__(self, decisions_path: str | Path | None = None):
        path = Path(decisions_path) if decisions_path else DECISIONS_DEFAULT
        lines = path.read_text(encoding="utf-8").strip().splitlines()
        self.meta = json.loads(lines[0])["meta"]
        self.decisions = [json.loads(line) for line in lines[1:]]
        self._by_date = {d["date"]: d for d in self.decisions}
        first = self.decisions[0] if self.decisions else {}
        self.declared_strategy = first.get("declared_strategy", "unspecified")
        self.risk_limit = float(self.meta.get("risk_limit", -0.10))
        self.name = self.meta.get("agent", "dsh-quant")

    def observe(self, state) -> Decision:
        d = self._by_date.get(state.date)
        if d is None:
            return Decision(ACTION_HOLD, 0.0, "no decision for bar", self.declared_strategy)
        return Decision(
            action=d["action"],
            size=float(d["size"]),
            rationale=d["rationale"],
            declared_strategy=d.get("declared_strategy", self.declared_strategy),
        )

    @property
    def stale_refusals(self) -> dict:
        return {
            "stale_rows": self.meta.get("stale_rows", 0),
            "stale_refusals": self.meta.get("stale_refusals", 0),
        }
