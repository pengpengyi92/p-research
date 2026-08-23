"""dsh-quant adapter: decision stream -> harness agent.

dsh-quant (github.com/pengpengyi92/dsh-quant, npm package ``dsh-quant``) is the
program's own open-source Quant OS (46 tools, 6 domains). Its
``cli/harness-signal.mjs`` runs dsh-quant's own loop — SMA-cross signal from
``lib/dsh-alpha``, cost guard from ``lib/dsh-execution/trading-cost``,
drawdown guard, stale-data refusal — and emits a deterministic decision stream
(JSONL: one meta line + one decision per bar).

The stream is loaded by the generic :class:`DecisionStreamAgent` with
capability ``stream``: decisions are precomputed, so C2's volume-response
dimension and C4's failure injection are honestly reported as not exercisable.

Regenerate the stream (requires the dsh-quant repo + Node.js, zero deps):

    node cli/harness-signal.mjs --data data/market/spx_daily.csv \\
        --out data/harness/dsh-quant-decisions.jsonl
"""

from __future__ import annotations

from pathlib import Path

from .stream import DecisionStreamAgent

DECISIONS_DEFAULT = (
    Path(__file__).resolve().parent.parent.parent / "data" / "harness" / "dsh-quant-decisions.jsonl"
)


class DshQuantSignalAgent(DecisionStreamAgent):
    default_path = DECISIONS_DEFAULT
    name = "dsh-quant"
