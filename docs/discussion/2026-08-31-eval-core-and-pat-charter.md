# P-Research 重大方向声明 — Evaluation（Benchmark）为核心 · 与 PAT 深度联动（2026-08-31）

> P-Research 讨论区公告 ｜ 重大方向声明 ｜ 中英双语
> 配套: README 理念更新（同步发布）

---

## 中文

### 一、P-Research 的新方向：以 Evaluation（Benchmark）为核心

**P-Research 从此以 benchmark / evaluation 作为主要深度研究方向。**

理由：评估（evaluation）是自进化的反馈通道——没有 eval 的适应是随机游走（"self-evolution without eval is Brownian motion"）。我们此前已完成 Evaluation 深度研究（2026-08-28），现在把它**从研究主题升级为组织主线**：

- **eval 驱动的研究**：每个方向的研究都要回答"怎么衡量它做得好不好"——benchmark 先行
- **量化方法论迁移**：把 quant 的"因子、归因、风险检查"纪律应用到 AI 研究评估
- **可复现的基准**：评估不只是跑分，是可复现、可审计、可对比的证据链

### 二、介绍内部 PAT（Pengyi Agent Team）

**PAT（Pengyi Agent Team）是 Pengyi 的内部 Agent 团队**，核心是五个能力模块的深度研究与运行：

```text
RAG + Memory + Tool Use + Planning + Evaluation
```

| 模块 | 职责 |
|---|---|
| **RAG** | 检索增强——知识接入 |
| **Memory** | 记忆——经验积累 |
| **Tool Use** | 工具使用——行动能力 |
| **Planning** | 规划——任务分解 |
| **Evaluation** | 评估——反馈闭环（与 P-Research 主线一致）|

五个 Foundation Agents 各自运行，Human 审批把关；理念：**框架开源、细节闭源**。

### 三、P-Research 与 PAT 的关系

**P-Research 之于 PAT，正如 dsh-quant 之于量化研究团队（PDAT-PAAT-PCPT-PRT-PET）：**

- **PAT 是内部团队**（Pengyi Agent Team）——五个模块的完整运行
- **P-Research 是开源前沿研究团队**——PAT 的开源部分在这里做
- **类比**：dsh-quant 是量化五团队（数据/alpha/组合/风控/执行）的开源化身；P-Research 是 PAT（RAG/Memory/Tool/Planning/Eval）的开源化身

### 四、P-Research 的理念（正式确立）

1. **框架开源，细节闭源**——研究框架/方法/benchmark 全公开；内部实现细节保留
2. **广泛 + 深度的开源研究**——来自内部（PAT 实践）和外部（arXiv 前沿）
3. **Agentic 优先**——P-Research 重点更新 agentic 相关研究（这是我们最感兴趣、也是 PAT 的主要工作方向）
4. **与 PAT 狠狠联动**——P-Research 的公开研究 = PAT 内部实践的镜像与反馈

### 五、接下来

- 重点更新：agentic 研究（multi-agent / swarm / eval benchmark）
- Evaluation 主线：agent 评估基准的构建与研究
- 联动：PAT 五模块的深度调研在 P-Research 同步开源

---

## English

### 1. New direction: Evaluation (Benchmark) as the core

**P-Research now takes benchmark / evaluation as its primary deep-research direction.** Evaluation is the feedback channel of self-evolution — without eval, adaptation is random. We upgrade it from a research topic to the organizational backbone: eval-driven research, quant-grade rigor (checks, not leaderboards), and reproducible benchmarks.

### 2. Introducing PAT (Pengyi Agent Team)

**PAT is Pengyi's internal Agent Team**, operating five capability modules:

```text
RAG + Memory + Tool Use + Planning + Evaluation
```

Operated by five Foundation Agents under human approval. Philosophy: **open frameworks, closed implementation details.**

### 3. The P-Research ↔ PAT relationship

**P-Research is to PAT what dsh-quant is to Pengyi's quant research teams (PDAT-PAAT-PCPT-PRT-PET):** PAT is the internal team; P-Research is the open-source frontier research team where PAT's open part lives.

### 4. P-Research's charter (formalized)

1. **Open frameworks, closed details** — methods and benchmarks public; internal specifics retained
2. **Broad + deep open research** — from internal (PAT practice) and external (arXiv frontier)
3. **Agentic-first** — P-Research will prioritize agentic research (our core interest and PAT's main work)
4. **Deep PAT collaboration** — public research mirrors and feeds internal practice

### 5. What's next

Agentic research updates · evaluation benchmark construction · PAT five-module deep dives open-sourced here.
