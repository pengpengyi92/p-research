"""Adapters: connect external agents to the harness.

The harness is agent-agnostic by design; adapters bridge external black-box
agents (any language, any stack) into the `observe(state) -> Decision`
protocol. A black box that emits a deterministic decision stream — one
decision per bar, with rationale and declared strategy — can be evaluated
without running it in-process.
"""

from .dsh_quant import DshQuantSignalAgent

__all__ = ["DshQuantSignalAgent"]
