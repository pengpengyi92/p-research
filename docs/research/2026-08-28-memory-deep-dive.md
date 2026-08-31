# 🧬 Memory 深度研究：DeepSeek / Kimi / OpenAI 的记忆机制 × 前沿趋势

> **P-Research 深度报告** · 2026-08-28 · memory 主题深化（承接 harness 报告三家对比框架）
> 方法：P-Research corpus（95 篇 memory 论文）+ 三家公开资料 + P-Research 的第一手实践
> 关联：2026-08-19 In-Model Memory 报告 · RAG 报告 · Agentic Harness 报告

---

## 0. 一句话结论

> **2026 年记忆研究急剧加速（半年 36 篇论文，超任何全年）——记忆正从"参数的副产物"
> 变成"显式的可插拔架构组件"。三家厂商的路线：Kimi 做外部记忆系统 · OpenAI 做产品化
> 记忆（ChatGPT 记住你）· DeepSeek 做执行快照（harness 的后悔药）。**

---

## 一、前沿趋势（P-Research corpus 95 篇论文）

### 1. Memory × RAG 融合是主导（共现 51 次）
- 检索记忆与模型内记忆"长成同一个东西"——边界消融
- 印证 RAG 报告的判断（RAG 区与 Memory 区越来越难分）

### 2. 模块化神经记忆——新的架构类别 🆕
- **MoNe**（模块化神经记忆，高效长上下文推理）
- **ArborMem**（记忆森林，交互状态导航）
- **Dynamic Compression**（循环网络动态压缩）
- → 记忆从参数副产物 → **显式可插拔组件**

### 3. 恢复与持久化成为主题
- **Bounded-State Restoration**（解耦本地恢复与 KV-cache 状态）
- 保存/恢复/跨会话 = 一等公民 → 呼应 agent harness 的状态持久化

### 4. 记忆 × 推理深度
- "Beyond Memorization"（记忆让推理深度逃出死记硬背）
- 记忆 = 推理深度的燃料

### 5. 记忆 × 多模态（VLM 共现 19 次）
- Memory Tree / 关键帧查询 / 审计——记忆结构超越纯文本

### 6. 效率是命运
- Memory 与 KV Cache/MoE/量化同社区——记忆总带着成本约束

---

## 二、三家厂商的记忆机制（怎么做）

### 1. DeepSeek：执行快照 = 记忆的安全网

| 机制 | 实现 |
|---|---|
| **无损快照** | 工具调用后先快照再规范化——"执行记忆"可回滚 |
| **作用域路由** | opaque key 选择一层——状态隔离 |
| **跨会话持久化** | harness 状态保存/恢复（评测闭环的基础）|

**哲学**：记忆 = 可回滚的执行历史（"AGI 自进化的后悔药"）——记忆不是"记住更多"，
而是"错了能回到过去"。

### 2. Kimi：外部记忆系统（最激进）

| 机制 | 实现 |
|---|---|
| **K2.6 External Memory** | 显式外部记忆系统（独立于模型参数）|
| **会话记忆** | Kimi Code/CLI 持久会话（JSONL 流式）|
| **K2 长上下文工程** | 注意力头优化 + 长上下文效率（万亿基座）|

**哲学**：记忆 = 独立组件（模型是大脑，记忆是外接硬盘）——对应前沿的
"模块化神经记忆"方向，且已经产品化。

### 3. OpenAI / ChatGPT：产品化记忆

| 机制 | 实现 |
|---|---|
| **ChatGPT 记忆** | 跨会话记住用户偏好/事实（产品级）|
| **Codex harness** | 上下文管理 + 会话状态（编码 agent 的记忆）|
| **Agents SDK** | 会话/状态管理 SDK 化 |

**哲学**：记忆 = 产品体验（"ChatGPT 记住你"）——面向消费者的记忆，
与工程记忆（快照/恢复）并重。

---

## 三、三家对比

| 维度 | DeepSeek | Kimi | OpenAI |
|---|---|---|---|
| **记忆类型** | 执行快照（工程）| 外部记忆（架构）| 产品记忆（体验）|
| **核心机制** | 无损快照/作用域/恢复 | K2.6 external memory | 跨会话记住用户 |
| **面向** | 自进化（可靠执行）| 长任务（持续工作）| 消费者（好用）|
| **与前沿对应** | Bounded-State Restoration | 模块化神经记忆（MoNe 类）| 产品化 RAG/记忆 |
| **P-Research 已采用** | ✅ 在用（dsh）| 部分（K2 开源）| API |

### 关键洞察

1. **记忆 = agent 的分水岭**（harness 报告的延续）：谁有持久记忆，谁就能跑长任务
2. **三种记忆分工**：工程记忆（快照/回滚）· 架构记忆（外部组件）· 产品记忆（体验）
3. **前沿与厂商双向印证**：corpus 的模块化神经记忆 ↔ Kimi 外部记忆；恢复主题 ↔ DeepSeek 快照
4. **成本约束永远在**：记忆的敌人是 KV-cache 成本——效率是记忆的命运

---

## 四、研究意义（dsh-quant / P-Research）

| 角度 | 意义 |
|---|---|
| **五大模块** | Memory 是五大模块之一——本报告是其深化 |
| **RAG×Memory** | 边界消融 → RAG 与 Memory 两区合并研究 |
| **harness 记忆** | DeepSeek 快照 = P-Research 已采用（dsh-quant 的状态持久化）|
| **RSI/自进化** | 记忆是自进化的前提（忘了就不能进化）——核心论点关联 |
| **AI-native Trading** | 量化 agent 的跨会话记忆（策略迭代不丢上下文）|

**要点**：dsh-quant 采用 DeepSeek 的"执行快照记忆"，同时跟踪着
Kimi 的"外部记忆"和前沿的"模块化神经记忆"——三层记忆都在本文视野内。

## 🐳 一句话

> **记忆正在从参数的副产物变成显式的架构组件——Kimi 外接硬盘、DeepSeek 后悔药、
> OpenAI 记住你。记忆是 agent 的分水岭：谁有持久记忆，谁就能跑长任务。**

---

## 📚 参考

- P-Research In-Model Memory 报告（2026-08-19，95 篇论文）
- MoNe / ArborMem / Bounded-State Restoration（arXiv）
- Kimi K2.6 external memory · DeepSeek Harness 快照 · OpenAI ChatGPT 记忆

欢迎翻阅、指正、PR 🐳
