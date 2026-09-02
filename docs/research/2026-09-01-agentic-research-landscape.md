# Agentic AI 研究方向全景（2026-09-01）

> p-research 公开研究 ｜ 主题: Agentic AI 研究地图
> 语境: 本 repo 主线 = Evaluation（Benchmark）+ Agentic 优先（charter 2026-08-31）
> 语料: P-Research corpus 737 篇 + 2026 前沿综述

---

## 0. TL;DR

Agentic AI 研究 2026 年已从"框架选型"进入**系统化/工程化**阶段。研究全景分四层：

1. **架构层**：单体 → 多智能体（swarm）→ 自主系统（Perceive-Plan-Act-SelfCorrect）
2. **能力层**：记忆 / 工具 / 规划 / 上下文工程（五大能力模块）
3. **协议层**：MCP / 通信 / Agent 间标准（Internet of Agentic AI）
4. **评测层**：Agent 评估基准（General Agent Evaluation）——**本 repo 主线**

---

## 1. 架构层（Agent 形态演进）

| 形态 | 特征 | 2026 状态 |
|---|---|---|
| **单体 Agent**（ReAct 类）| 单 agent 思考-行动 | 成熟基线 |
| **多智能体**（Multi-Agent）| 角色分工/协作 | 产品化（ClawTeam 等）|
| **Swarm** | 自组织团队 | 新兴（Solo→Swarm）|
| **自主系统** | Perceive-Plan-Act-Self-Correct 闭环 | 前沿框架 |

**架构趋势**：从"一个 agent 干所有"→"多个 agent 协作"→"系统自组织 + 自纠正"——**架构研究转向自主性（autonomy）与闭环**

## 2. 能力层（五大模块——PAT 核心）

### 2.1 Memory（记忆）——2026 热点
- **Tool-based memory**（记忆即工具）——2026 benchmark 倾向（usewire）
- 记忆分层：短期上下文 / 长期记忆 / 参数化记忆
- 记忆治理：MGP / Awesome-AI-Memory 知识库（IAAR-Shanghai）
- **趋势**：记忆从"附件"变"一等公民"

### 2.2 Tool Use（工具）
- MCP（Model Context Protocol）——工具标准化
- Skill 生命周期（retrieve/evaluate/share/evolve）——OpenSpace 模式
- 工具安全（Skill 扫描）——呼应 AI 安全

### 2.3 Planning（规划）
- 任务分解 / 依赖管理 / 动态重规划
- Context Engineering（2026 北大 MCE 论文）——**静态 skill 文件是当前实际标准**

### 2.4 Context Engineering（上下文工程，2026 新兴）
- 人类手写 skill 文件 = 当前实用标准（MCE 2026）
- 上下文作为一等设计对象（非模型参数）

### 2.5 Evaluation（评测）——主线
- **General Agent Evaluation**（2026）——通用 agent 评估框架
- 从"跑分"到"行为风险属性"（策略漂移/成本敏感/失败处理）
- benchmark 优先：每个能力模块需要独立基准

## 3. 协议层（Agent 互联）

| 方向 | 内容 | 状态 |
|---|---|---|
| **MCP** | 工具/资源标准化 | 事实标准（Anthropic）|
| Agent 通信 | inbox/消息传递（ClawTeam）| 工程实践 |
| **IoA**（Internet of Agentic AI）| 大规模 agent 互联/发现/路由 | 学术前沿 |
| Agent 市场 | 模板复用 | ClawTeam roadmap v0.6 |

**趋势**：从"单体工具协议"→"Agent 间协议"→"Agent 互联网"——**标准化是规模化前提**

## 4. 评测层（本 repo 主线）

### 4.1 为什么评测是核心
> 没有 eval 的适应是随机游走——**评测 = 自进化的反馈通道**

### 4.2 评测研究方向
| 子方向 | 内容 |
|---|---|
| **General Agent Evaluation** | 跨任务通用评估框架（2026）|
| 行为风险属性 | 策略漂移/成本敏感/回撤响应/失败处理（我们 harness）|
| 记忆评测 | 记忆系统基准（2026 benchmark 倾向 tool-based memory）|
| 多 agent 评测 | swarm 的集体表现如何衡量 |
| 评测基准构建 | 可复现、可审计、可对比 |

## 5. 生态与工具（2026）

### 框架
AutoGen / CrewAI / LangGraph / MetaGPT / ClawTeam / OpenSpace / AgentSpace

### 知识库
- State of AI Agents（2026-03 报告）
- Awesome-AI-Memory（IAAR-Shanghai）
- awesome-ai-agent-frameworks（决策树）
- Oreilly: The Open Source Agent Toolkit in 2026

## 6. 研究趋势总结（2026 关键信号）

1. **记忆 = 2026 最热**（tool-based memory 被 benchmark 青睐）
2. **上下文工程 = 新学科**（MCE：skill 文件是当前标准）
3. **协议标准化**（MCP 已定，Agent 间协议进行中）
4. **评测 = 自进化关键**（从跑分到行为属性）
5. **自主系统**（Self-Correct 闭环）是架构前沿
6. **开源生态成熟**（框架从 starter kit → 基础设施）

## 7. 对 P-Research 的意义（主线落点）

- **评测层 = 本 repo 主线**：General Agent Evaluation + 行为风险属性
- **能力层**：五模块（RAG/Memory/Tool/Planning/Eval）持续深挖
- **Agentic 优先**：多 agent / swarm / 自主系统重点跟踪
- 与 PAT 联动：五模块 = PAT 开源镜像

## 8. 信息来源
- A Holistic Review of Agentic AI Frameworks（Springer 2026）
- Lifecycle-oriented survey of LLM-based agents（Neurocomputing 2026）
- State of AI Agents（2026-03）
- Oreilly: Open Source Agent Toolkit 2026
- General Agent Evaluation（2026）
- usewire: Tool-based agent memory 2026
- MCE paper（北大 2026）
- Awesome-AI-Memory / awesome-ai-agent-frameworks
- P-Research corpus（737 篇）
