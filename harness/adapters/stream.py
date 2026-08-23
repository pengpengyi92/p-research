"""Generic decision-stream agent: loads a JSONL decision stream and exposes it
to the harness as a black-box agent with capability ``stream``.

Stream format (one meta line, then one decision per bar):

    {"meta": {"agent": ..., "declared_strategy"?: ..., "risk_limit"?: ..., ...}}
    {"date": "2026-08-21", "action": "BUY", "size": 0.3,
     "rationale": "...", "declared_strategy": "trend-following"}
    ...

Stateless by construction (date-keyed lookup), so the same instance can be
replayed across cost tiers without drift.
"""

from __future__ import annotations

import json
from pathlib import Path

from ..agent import ACTION_HOLD, Decision


class DecisionStreamAgent:
    """Black-box agent over a precomputed decision stream."""

    capabilities = {"stream"}
    default_path: Path | None = None  # set by subclasses
    name = "stream"

    def __init__(self, decisions_path: str | Path | None = None):
        path = Path(decisions_path) if decisions_path else self.default_path
        if path is None or not path.exists():
            raise FileNotFoundError(
                f"decision stream not found: {path} — generate it first "
                f"(see the adapter module docstring)"
            )
        lines = path.read_text(encoding="utf-8").strip().splitlines()
        self.meta = json.loads(lines[0])["meta"]
        self.decisions = [json.loads(line) for line in lines[1:]]
        self._by_date = {d["date"]: d for d in self.decisions}
        first = self.decisions[0] if self.decisions else {}
        self.declared_strategy = first.get("declared_strategy", "unspecified")
        self.risk_limit = float(self.meta.get("risk_limit", -0.10))
        self.name = self.meta.get("agent", self.name)

    @classmethod
    def decisions_path(cls) -> Path:
        if cls.default_path is None:
            raise NotImplementedError
        return cls.default_path

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
