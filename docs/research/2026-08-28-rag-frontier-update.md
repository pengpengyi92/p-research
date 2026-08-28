# 📚 RAG 前沿跟踪报告：检索正在成为"记忆 × 决策"的问题（2026-08 更新）

> **P-Research 前沿跟踪** · 基于 corpus（574 论文，含 64 篇 RAG）+ 2026-08 最新 arXiv 扫描
> 关联：P-Research docs/research/2026-08-19-rag.md（首份 RAG 报告）· 本文为前沿动态更新
> 发布：2026-08-28 · dsh-quant / P-Research 联合

---

## 0. 一句话结论

> **RAG 已不是"工程技巧"——前沿正在把它变成"记忆 × 决策"的核心问题：
> 什么时候检索、检索什么、怎么与 in-model 记忆融合、如何让自进化不脆弱。**

## 1. 趋势快照（数据）

| 指标 | 值 |
|---|---|
| corpus 中 RAG 论文 | **64 篇**（574 篇语料）|
| 年份分布 | 2023: 11 → 2024: 8 → 2025: 16 → **2026 半年: 29** |
| 顶级期刊雷达 | Unbiased Reasoning + Retrieval（0.657 分）居首 |

**观察 0**：2026 半年 RAG 论文 ≈ 2025 全年两倍——RAG 已是主战场。

## 2. 六大前沿信号（更新版）

### 1️⃣ RAG × Memory 正在融合（最强信号）
- Long Context（11 次共现）+ KV Cache（5 次）是 RAG 论文最常共现的方法族
- 最新：MoNe 模块化神经记忆 · Dynamic Compression · Bounded-State Restoration（KV Cache 恢复）
- **边界消融**：检索记忆（RAG 区）与模型内记忆（Memory 区）正在合并

### 2️⃣ 最新动态：RAG × Agent × 图（2026-08 新信号）🆕
- **MemGraphRAG**：记忆驱动的多智能体图 RAG（ACM 2026）
- **LivingRAG**：用经验增强图 RAG（experience-augmented）
- **Noēsis**：双向图 RAG + 自适应并行 + 跨知识库语义发现
- **ACE-GraphRAG**：Agentic 上下文工程（hierarchical GraphRAG）
- → **图 RAG + 多智能体 + 记忆 = 当前最活跃的融合方向**（印证 P-Research 报告判断）

### 3️⃣ 下一个前沿：知道什么时候*不*检索
- "Judge, Retrieve, or Abstain"——检索前先判断，不确定就放弃
- **检索不是"越多越好"，而是决策问题**

### 4️⃣ RAG × 自进化：脆弱性成为主题
- "On the Fragility of Self-Improving Agents"——自进化 agent 对任务顺序敏感
- 解药 = **评估（Eval）**——与我们的 north-star（递归）直接相关

### 5️⃣ RAG 走向多模态
- VLM 共现 9 次 · Memory Tree Guided Key Frame Querying（3D 问答）
- 索引结构正超越纯文本

### 6️⃣ RAG × 效率是安静的主线
- Quantization（7）+ Distillation（4）共现 · GraphRAG community 0（115 论文）
- **成本是 RAG 的命运**——效率与记忆同社区

## 3. RAG × Quant（我们的独特交叉）

- Quant/Trading 共现 **7 次**——金融 RAG（研究报告检索/知识访问/可审计证据链）是活跃方向
- **我们横跨 RAG 和 Quant 两线**，这在 corpus 中很少见
- 关联：dsh-quant 的 AGENTS.md/知识库 · P-Research 的语料管线 · 银行数据→alpha 研究的证据链需求

## 4. 对我们（P-Research / dsh-quant）的启示

| 能力 | 前沿信号 → 我们的动作 |
|---|---|
| RAG | 与 Memory 融合 → 研究"何时检索"决策（Judge/Abstain）|
| 记忆 | 模块化神经记忆（MoNe）→ 关注 |
| 工具 | 弱信号 → 延后专项扫描 |
| 规划 | 检索是规划问题 → 纳入 planning 课程 |
| 评估 | 自进化脆弱性的解药 → **强化 Eval 能力（我们的强项）** |

**两个站位**：
1. RAG/Memory 边界消融 → 两区合并研究（P-Research zones #3/#4）
2. "检索-评估"配对 → 前沿的 retrieve-or-abstain 方向——评估让自进化检索 agent 可靠

## 5. 开放问题

1. 形式化 RAG/Memory 边界——何时检索 vs 何时依赖参数记忆？
2. 检索决策（retrieve-or-abstain）的基准缺失——能不能建一个？
3. **金融 RAG 的可审计证据链**（呼应 harness 哲学 + ai-security 投毒防御）

## 🐳 一句话

> **前沿已停止把 RAG 当工程技巧：它在决定是否检索、把检索与模型内记忆融合、
> 并发现自进化脆弱性的解药是评估。图 RAG × 多智能体 × 记忆 = 2026 最热交叉。**

---

## 📚 相关

- P-Research：pengpengyi92/p-research（574 论文 corpus · 每周自动更新）
- 首份 RAG 报告：p-research/docs/research/2026-08-19-rag.md
- 前沿论文：MoNe / Judge-Retrieve-Abstain / MemGraphRAG / LivingRAG / Noēsis / ACE-GraphRAG

欢迎翻阅、指正、PR 🐳
