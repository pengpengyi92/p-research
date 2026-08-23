# The Open Quant/Trading-Agent Ecosystem — a cohort map for the Quant×AI harness

> 2026-08-23 · research note · generated for the P-Research Quant×AI evaluation program
> Method: web survey (GitHub READMEs, star-history.com snapshots, third-party coverage) + first-party repo inspection. Star counts are approximate snapshots from the cited sources, not verified at write time — treat as order-of-magnitude. Descriptive only; nothing here is investment advice.

The P-Research Quant×AI harness (Paper "Agent-Native Trading Systems" §6) evaluates trading agents on four risk-behavior checks — C1 strategy drift under regime change, C2 cost sensitivity, C3 drawdown behavior, C4 tool-use failure modes. This note maps the open-source quant/trading ecosystem so we can (a) pick an evaluation cohort the harness can actually run, and (b) position our own library (dsh-quant) honestly inside the map.

## The landscape at a glance

| Project | Stars (approx) | Language | What it is | Agent-native? | Risk layer present (backtest hygiene / cost modeling / risk limits / attribution) | Evaluation convention |
|---|---|---|---|---|---|---|
| [TradingAgents](https://github.com/TauricResearch/TradingAgents) | ~91K ([star-history](https://www.star-history.com/tauricresearch/tradingagents/)) | Python | Multi-agent LLM trading framework (analyst/researcher/trader/risk debate) | yes | backtest w/ look-ahead filtering · no public cost model · in-loop risk team + PM approval · decision-log reflection | Realized-return memory log (alpha vs SPY); explicitly non-reproducible returns |
| [Vibe-Trading](https://github.com/HKUDS/Vibe-Trading) | ~30K ([SkillsLLM](https://skillsllm.com/skill/vibe-trading)) | Python + React | Personal trading agent: NL → research, strategy, backtest, broker | yes | **all four**: PIT/look-ahead fixes, per-market cost stacks, mandate gate/kill switch/exposure caps, shadow-account + layered attribution | Backtest validation artifacts, run cards, alpha-zoo IC bench; no formal leaderboard |
| [AI-Trader](https://github.com/HKUDS/AI-Trader) | ~12–21K, unverified ([12K mid-2026](https://m.toutiao.com/article/7630339638036660770/)) | Python + React | Agent-native trading *platform*: agents join via SKILL.md, publish/copy signals | yes | paper trading ($100K sim) · live mark-to-market scoring · no public backtest/cost docs | Live paper-trading leaderboards + monthly challenges |
| [FinGPT](https://github.com/AI4Finance-Foundation/FinGPT) | ~21K ([star-history](https://www.star-history.com/ai4finance-foundation/fingpt/)) | Python | Open financial LLMs (sentiment, forecasting, RAG) | no | none (model layer) | Financial-NLP benchmarks (sentiment/forecasting); no trading eval |
| [FinRobot](https://github.com/AI4Finance-Foundation/FinRobot) | ~7.7K ([awesome-github](https://github.com/AnEntrypoint/awesome-github)) | Python | Multi-agent AI platform for financial analysis/research | partial | risk assessment *module* in research output · no backtest | Notebooks + desktop reports; no public benchmark |
| [FinRL](https://github.com/AI4Finance-Foundation/FinRL) | ~16K ([star-history](https://www.star-history.com/ai4finance-foundation/finrl/)) | Python | Deep RL library for trading (env → agent → backtest) | partial (RL agent, no LLM loop) | backtest of trained policies · cost via env reward design · no risk limits/attribution | RL episode returns on public envs |
| [Qlib](https://github.com/microsoft/qlib) | ~47K ([star-history](https://www.star-history.com/microsoft/qlib/)) | Python | AI-oriented quant platform (full ML pipeline, [point-in-time DB](https://github.com/microsoft/qlib)) | no (RD-Agent offshoot is agent-based) | point-in-time DB, cost/risk modeling, portfolio opt, rolling retrain | `qrun` workflow + public leaderboard (Alpha158/360, CSI300) |
| [vn.py](https://github.com/vnpy/vnpy) | ~44K ([star-history](https://www.star-history.com/vnpy/vnpy/)) | Python | Event-driven live trading framework (China-market first) | no | CTA backtest w/ commission+slippage params · live gateways · no formal attribution | Backtest → paper → live convention |
| [backtrader](https://github.com/mementum/backtrader) | ~22K ([star-history](https://www.star-history.com/mementum/backtrader/)) | Python | In-process backtesting engine (cerebro) | no | commission schemes + slippage fillers · analyzers (drawdown etc.) · no built-in walk-forward | Community backtests; no canonical benchmark |
| [freqtrade](https://github.com/freqtrade/freqtrade) | ~52K ([awesome-quant: 51,693](https://github.com/ernie55ernie/awesome-quant)) | Python | Crypto trading bot: backtest, hyperopt, dry-run, live | no | fee/slippage modeling in backtest, money mgmt, [lookahead-analysis & recursive-analysis](https://github.com/freqtrade/freqtrade) hygiene tools | Backtest → hyperopt → dry-run → live |
| [jesse](https://github.com/jesse-ai/jesse) | ~8K ([star-history](https://www.star-history.com/jesse-ai/jesse/)) | Python | Crypto trading framework (live + backtest) | no | fee/slippage modeling, paper trading | Backtest + paper + live |
| [Hummingbot](https://github.com/hummingbot/hummingbot) | ~19K ([star-history](https://www.star-history.com/hummingbot/hummingbot/)) | Python | Live market-making/arbitrage bots, script strategies | no | paper trading · execution-focused · limited backtest | Paper → live; strategy scripts |
| [OpenBB](https://github.com/OpenBB-finance/OpenBB) | ~64K ([coverage](https://m.163.com/dy/article/KPA7DEII05568W0A.html?spss=adap_pc&referFrom=)) | Python | Open data platform for analysts, quants and AI agents (CLI/SDK/REST) | partial (feeds agents; no loop) | none (data layer) | No canonical eval; consumed by others |
| [QuantConnect Lean](https://github.com/QuantConnect/Lean) | ~21K ([star-history](https://www.star-history.com/quantconnect/lean/)) | C# (+ Python) | Event-driven algorithmic engine (backtest + live) | no | brokerage models (fees/slippage/margin), optimization, algorithm-level risk | Backtest w/ brokerage simulation; QC cloud live |
| [zvt](https://github.com/zvtvz/zvt) | unverified | Python | Modular quant framework (data → factors → selectors → traders) | no | factor IC/IR eval · backtest + live gateways | Selection → backtest convention |
| gym-trading-env / [TradingGym](https://github.com/Yvictor/TradingGym) | unverified | Python | Gym-style RL trading environments | no | cost only via reward design | RL episode returns |
| dsh-quant (ours) | — | TypeScript | Indicator + backtest library, 46 tools / 6 pluggable domains | no | hand-computed backtest baselines, cost/risk math as reference | Deterministic unit-tested baselines (174 tests) |

Star counts not backed by a search result are marked **unverified** (zvt, gym-trading-env/TradingGym, AI-Trader's current count).

## Agent-native trading systems (the loop productized)

The agent-native tier is new relative to the quant tradition: the product is the **loop** (market data → tool registry → memory → research → decide → execute), not the backtest engine.

**Vibe-Trading (HKUDS, ~30K).** Loop is explicit in the README's [research workflow](https://github.com/HKUDS/Vibe-Trading): Plan (select skills/tools/data/swarm preset) → Ground (pull market context through 23 free data sources with per-market fallback chains) → Execute (generate testable strategy code, run tools, matching backtest engine) → Validate (metrics, benchmark comparison, Monte Carlo, Bootstrap, Walk-Forward, run cards) → Deliver (reports, TradingView/TDX/MT5 exports, MCP). Interfaces: CLI (`vibe-trading`), Web UI, REST API, MCP server (60+ tools), 16 IM-channel adapters (Telegram/Slack/Discord/WeChat/Feishu…), desktop Electron shell. Autonomy claims: natural-language prompts turn into runnable strategies, and real broker orders are possible via user-authorized connectors (Robinhood, Alpaca, eToro, Trading 212, IBKR…), while the README stresses it "holds no funds and never trades outside the limits you set, and you can halt it instantly." Risk layer is unusually visible: 9 market backtest engines, point-in-time data, look-ahead-bias fixes across optimizers, per-market cost stacks (fees/taxes/funding/liquidation), exposure caps, a mandate gate + kill switch, a hash-chained audit ledger, and attribution — a [Shadow Account](https://github.com/HKUDS/Vibe-Trading) that extracts a rule-based profile from your own broker journal, plus post-backtest layered attribution (trade-level winners/losers, beta regression, market-regime analysis, Monte Carlo permutation test). This is the closest thing in the agent tier to the "risk layer built" tradition.

**AI-Trader (HKUDS, ~12–21K, unverified current).** The loop is a *platform* rather than a local agent: any LLM agent joins by reading `SKILL.md` ([ai4trade.ai](https://ai4trade.ai)), registers, publishes signals, debates in "collective intelligence" channels, and can copy-trade or sync signals to brokers (Binance, Coinbase, IBKR…). Interfaces: platform REST API (OpenAPI specs in repo), prompt-based onboarding, live web platform. Autonomy claim: "100% Fully-Automated Agent-Native Trading." Risk layer is thin in public docs: $100K paper trading and live mark-to-market leaderboard scoring (used for monthly challenges); no public backtest, cost model, or attribution machinery — its scoring is reputational (points, followers), not behavioral.

**TradingAgents (TauricResearch, ~91K).** The loop is the famous multi-agent firm: [Analyst Team](https://github.com/TauricResearch/TradingAgents) (fundamental / sentiment / news / technical) → Researcher bull-bear debate → Trader composes the decision → Risk Management team reviews → Portfolio Manager approves/rejects → simulated exchange. Built on LangGraph; interfaces: interactive CLI (`tradingagents`), Python API (`TradingAgentsGraph().propagate(ticker, date)`), Docker. Memory is productized: every run appends to a decision log, the next run fetches realized return (raw and alpha vs SPY) and injects a reflection into the Portfolio Manager prompt. Reproducibility is *documented honestly*: a dedicated README section separates LLM sampling noise, live-data drift, and the deterministic parts (ticker identity, grounded price claims). Risk layer: in-loop risk team + PM approval, backtesting with "backtesting date fidelity" and Alpha Vantage look-ahead filtering (v0.3.1) — notable hygiene for an agent repo, though there is no public cost model or attribution.

**FinRobot (AI4Finance, ~7.7K).** Loop is research-oriented: a Lead Agent orchestrates Data → Analysis → Modeling → Synthesis → Report agents plus bull/bear/judge debate agents ([README](https://github.com/AI4Finance-Foundation/FinRobot)); desktop app on PydanticAI + FastAPI + React/Tauri. Interfaces: notebooks, desktop app, FinRobot Pro. It is an *analysis* loop, not a trading loop — risk appears only as a section of generated reports, with no backtest or execution surface.

## Traditional quant frameworks (the risk layer built)

These projects carry the risk layer the agent tier is still re-inventing:

- **Qlib** — the strongest hygiene story: a [point-in-time database](https://github.com/microsoft/qlib) (released 2022), nested decision/execution framework, online serving with automatic model rolling (a built-in answer to C1 drift), cost/risk modeling in the backtest workflow, and a workflow/leaderboard convention (`qrun`, Alpha158/Alpha360 on CSI300). Its RD-Agent offshoot is explicitly agent-based (factor mining + model optimization).
- **vn.py** — event-driven, live-first (China-market gateways); backtesting lives in the CTA strategy module with configurable commission/slippage; evaluation convention is backtest → paper → live.
- **backtrader** — the in-process reference engine: `cerebro` event loop, pluggable commission schemes and slippage fillers, analyzers for drawdown/returns; no built-in walk-forward, so regime robustness is DIY.
- **freqtrade** — the most tooled *convention*: `backtesting`, `hyperopt`, `edge`, dry-run, and explicit hygiene commands (`lookahead-analysis`, `recursive-analysis`) for detecting look-ahead/recursive bias in strategies; freqAI adds ML-driven strategy optimization.
- **jesse / Hummingbot** — crypto frameworks with fee modeling and paper trading; Hummingbot is execution-heavy (market-making/arbitrage), jesse is strategy-heavy.
- **OpenBB** — the data layer, not a risk layer: a provider-agnostic data platform (CLI/SDK/REST) explicitly aimed at "analysts, quants and AI agents"; backtest/risk is left to consumers.
- **QuantConnect Lean** — the institutional-convention engine: event-driven algorithms with realistic brokerage models (fees, slippage, margin), optimization support, and backtest→live through the same algorithm abstraction.
- **zvt / gym-trading-env / TradingGym / FinRL** — factor frameworks and RL environments; cost/risk enter only through reward design, so they are weakest on C2/C3 but trivially deterministic.

## Interface shapes (for harness integration)

For our harness — which needs a deterministic `observe(state) -> Decision` stream — the key question is how a third party can run the project:

- **(a) In-process Python API / backtest engine:** Qlib, backtrader, vn.py (partially), jesse, zvt, FinRL, gym-trading-env/TradingGym, dsh-quant (Node). Best fit: the harness can call them per-step with controlled inputs and record decisions exactly.
- **(b) CLI with data input/output:** freqtrade, QuantConnect Lean, Hummingbot, OpenBB. Deterministic given fixed data and config; run as subprocesses with pinned data.
- **(c) Interactive / agent-chat only:** Vibe-Trading, AI-Trader, TradingAgents, FinRobot. LLM-driven, so a raw run is non-deterministic; the harness must fix model/temperature/seed and evaluate either the emitted strategy artifacts or a wrapped `Decision` from a pinned prompt — this is exactly what C1/C4 are for, but it costs the most to integrate.
- **(d) Library of indicators/signals:** zvt factors, FinGPT models, dsh-quant. Deterministic by construction; used as signal sources or reference implementations, not as decision-makers.

## Where dsh-quant sits

dsh-quant (github.com/pengpengyi92/dsh-quant, npm `dsh-quant`, MIT, TypeScript) is an "everything-plugin Quant OS": 46 tools across 6 pluggable domains (data / alpha / ML / risk / execution), an indicator + backtest library, with "methods open, secrets internal" as its operating principle.

- **Category:** (a)/(d) — a deterministic, in-process library. It belongs to the *traditional* side of the map: its backtest and indicator tradition is backtrader/Qlib-like, and its tool-registry layout (data/alpha/ML/risk/execution domains) anticipates the agent-native tool surfaces of Vibe-Trading's MCP registry.
- **Shared with each tradition:** with the backtest tradition it shares determinism, hand-computed baselines (174 tests), and cost/risk math as first-class domains; with the agent tradition it shares the idea of a pluggable tool registry — but it has **no agent loop, no memory, no live trading**, and no LLM surface.
- **Honest gaps:** no decision-maker, no broker connectivity, no multi-agent orchestration — it cannot be evaluated for C1/C4 *as an agent*.
- **Role in the harness program:** (1) a **deterministic signal source** — indicator/alpha outputs can be fed as the controlled `state` stream into any agent under test; (2) a **risk-layer reference** — its cost/risk math and hand-computed baselines can serve as the ground-truth oracle against which agent decisions (and their PnL claims) are checked on C2/C3; (3) the **missing loop is the honest boundary**: pairing dsh-quant with an agent framework is a research direction, not a current capability.

> **Update (same day):** the "missing loop" boundary has since been crossed in
> one direction — the program shipped `cli/harness-signal.mjs`, which runs
> dsh-quant's own loop (SMA-cross + `tradingCost` + drawdown guard + stale
> refusal) and emits a decision stream the harness can evaluate: **dsh-quant
> scores 4/4** with `stream` capability (C4 honestly not exercised).
> See [../harness/sample-dsh-quant.md](../harness/sample-dsh-quant.md). The
> "cannot be evaluated as an agent" claim now reads: *as a decision stream it
> can; as an in-loop agent it cannot — yet.*

## Candidate evaluation cohort (recommendation)

Feasibility = deterministic to run + public data + reproducible artifacts. Ranked:

1. **Qlib** — Python API, point-in-time data, built-in cost model and rolling retrain. Most informative check: **C1 (strategy drift)** — its rolling/walk-forward machinery makes regime sensitivity directly measurable, and C2 via its backtest cost workflow.
2. **backtrader** — in-process, fully deterministic, analyzers out of the box. Most informative: **C2 (cost sensitivity)** — commission schemes and slippage fillers make cost behavior explicit, and C3 via drawdown analyzers.
3. **freqtrade** — CLI with pinned data, native fee/slippage modeling and hygiene tooling. Most informative: **C3 (drawdown behavior)** — backtest + hyperopt conventions expose drawdown stats cleanly; C2 as a cross-check on cost modeling.
4. **Vibe-Trading** — the most risk-complete agent-native repo. Most informative: **C4 (tool-use failure modes)** — its 60+ tool registry, sandbox, mandate gate and data-fallback chains are the richest tool-failure surface in the cohort; C1 via its backtest engines replaying generated strategies under regime splits.
5. **TradingAgents** — multi-agent with documented non-determinism. Most informative: **C1/C4** — whether debate structure resists regime change, and which agent-tool failures cascade into bad decisions; its honest reproducibility docs give the harness a fair baseline to work against.

Alternates: **jesse** and **QuantConnect Lean** are deterministic and eligible but add friction (framework conventions / C# runtime); **AI-Trader** is excluded from the top list only because its public surface is a hosted platform rather than a runnable local loop.

*Caveat for the whole agent tier:* LLM-driven repos cannot be evaluated for deterministic repeatability as-is; the harness should score the *artifacts* they emit under pinned models/prompts (strategy code, decisions, reports) and treat variance itself as a measured property (relevant to C1 and C4), not a failure to work around.
