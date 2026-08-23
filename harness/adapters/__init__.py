"""Adapters: connect external agents to the harness.

The harness is agent-agnostic by design; adapters bridge external black-box
agents (any language, any stack) into the `observe(state) -> Decision`
protocol. A black box that emits a deterministic decision stream — one
decision per bar, with rationale and declared strategy — can be evaluated
without running it in-process.

Adapters currently shipped:

- dsh-quant (own Quant OS; Node generator, committed stream)
- backtrader (in-process backtest engine; optional dependency, committed stream)
- freqtrade (strategy framework; optional dependency, committed stream)
"""

from .backtrader import BacktraderSignalAgent
from .dsh_quant import DshQuantSignalAgent
from .freqtrade import FreqtradeSignalAgent
from .stream import DecisionStreamAgent

__all__ = [
    "BacktraderSignalAgent",
    "DshQuantSignalAgent",
    "FreqtradeSignalAgent",
    "DecisionStreamAgent",
]
