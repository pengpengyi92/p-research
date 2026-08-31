# 📏 Evaluation 深度研究：Eval 是自进化的反馈通道（DeepSeek / Kimi / OpenAI × 研究视角）

> **P-Research 深度报告** · 2026-08-28 · eval 深化（五大模块系列收官）
> 方法：P-Research corpus（363 篇 eval 论文，占语料 63%）+ 三家公开资料 + P-Research 的 Eval 实践
> 关联：2026-08-19 Eval 报告 · RAG/Harness/Memory/Tool/Planning 报告 · AI-native Trading 愿景

---

## 0. 一句话结论

> **Eval 不是五大模块之一——它是其他四个模块的公共基座，是自进化的反馈通道。**
> 前沿原话："**self-evolution without eval is Brownian motion**"（无 eval 的自进化是布朗运动）。
> 本文强调 Eval——现在有完整的理论支撑：**Eval 让适应有方向，而不是随机。**

---

## 一、前沿趋势（363 篇论文，占语料 63%）

### 1. Eval 是语料中最大的主题
- 63% 论文涉及 eval · 2026 半年 138 篇（加速中）
- **Eval 不是第五元素，是其他四元素的公共基座**

### 2. 基准饱和 vs 缺失（双重偏差）
- 饱和：MATH（29）/GSM8K（8）——数学常识基准主导
- 缺失：agent 基准几乎空白（AgentBench 仅 1 次）
- **四大模块各自缺基准**（RAG 缺 retrieve-or-abstain · Memory 缺模块基准 · Tool 缺金融审计 · Planning 缺金融规划）——结构性缺口

### 3. 环境即基准（形式革命）
- **SPADE**：合成可执行环境自博弈——环境自己生成任务，评估与训练合一
- HarnessEval-W / MCPVerse / StartupBench：真实世界 agent 基准
- → 基准从"静态测试集"变成"可执行动态环境"——**自进化需要无限任务供给**

### 4. Eval 作为诊断工具（不只是打分）
- "Precision, Not Capability"——测量精度细化
- **Open-MOPD**：诊断并修复多智能体能力失衡——**eval 驱动的系统修复**
- → Eval 从"期末考试"变成"健康检查"：诊断、定位、修复

### 5. 自进化需要 eval 环（核心论点）
```
act → eval → diagnose → update（递归环）
```
- 每个自进化系统（SPADE/EvoTS-Agent/AutoSR）都内嵌 eval
- **Eval 不是跑完的关卡，是让适应有方向的反馈通道**

---

## 二、三家厂商的 Eval（怎么做）

### 1. DeepSeek：评测闭环（P-Research 第一手实践）

| 机制 | 实现 |
|---|---|
| **Harness 评测** | dsh 用来自我评测（benchmark 自己的工具）|
| **快照审计** | 每次执行留证据，可回放 |
| **CI 门禁** | dsh-quant（开源项目）的 7 道 CI（含 coverage ≥85%）|

**哲学**：Eval = 开发流程的一部分（不是事后）——harness 里评测闭环，工具可自证。

### 2. Kimi：基准 + 记忆评估

| 机制 | 实现 |
|---|---|
| **K2 基准** | K2/K2.6 用大规模基准评测（长上下文/agent）|
| **记忆评估** | 外部记忆系统的评测 |
| **Skills 验证** | 技能包验证流程 |

**哲学**：Eval = 模型/技能上线的关卡（benchmark-driven）。

### 3. OpenAI：Eval 产品化（Evals）

| 机制 | 实现 |
|---|---|
| **OpenAI Evals** | 开源评测框架（evals 库）|
| **Red Teaming** | 安全评测（对抗测试）|
| **Agents SDK eval** | agent 行为评估 |

**哲学**：Eval = 产品化基础设施（开源 evals + 安全对抗）。

---

## 三、三家对比 + Eval 研究视角

| 维度 | DeepSeek | Kimi | OpenAI |
|---|---|---|---|
| **Eval 定位** | 开发闭环（harness）| 上线关卡（基准）| 产品基础设施（evals）|
| **核心机制** | 快照+CI | K2 基准 | Evals 库 + red team |
| **自进化** | 评测反馈 | 基准迭代 | 对抗改进 |
| **P-Research 已采用** | ✅ 在用（dsh CI）| 参考 | 可参考 evals 库 |

### Eval 研究视角（本文强调）

**dsh-quant 的 Eval 实践**（已经做了）：
1. **手算单测**（215 个）——每个数值函数有手算基准
2. **Coverage ≥85%**（93.9%）——知道测了什么
3. **7 道 CI 门禁**——build/test/typecheck/bench/coverage/consumer
4. **Benchmark smoke**——性能退化防线
5. **数据质量标注**（点级 label/severity）——输入侧 eval

**实盘 Eval（尽早实盘的关键）**：
```text
回测 eval（历史验证）→ 模拟盘 eval（实时验证）→ 小额实盘 eval（真实验证）
→ 每层都有 eval 门禁 → 过一关进一层
```
**这正是 Live Promotion Gate 的思路**——Eval 不是跑完的检查，是每一层的反馈通道。

### 自进化视角（无限自进化）
```
交易/研究动作 → eval（回测/模拟/实盘/诊断）
  → diagnose（哪里不对：因子失效/规划失误/工具错误）
  → update（修正策略/规划/工具）
  → 再行动（递归）
```
**关键**：全 AI-native Trading = **eval 驱动的自进化**——
每笔交易都被 eval，每个反馈都更新系统。

---

## 四、研究意义（五大模块收官）

| 角度 | 意义 |
|---|---|
| **公共基座** | Eval 连接 RAG/Memory/Tool/Planning——它们各自缺基准，可补齐 |
| **实盘门禁** | 回测→模拟→实盘三层 eval = 尽早实盘的安全路径 |
| **自进化** | eval 环 = 核心论点（act→eval→diagnose→update）|
| **量化 Eval** | 手算基准/IC/回测 = 量化特有的 eval 文化 |
| **缺口机会** | 四大模块缺基准 → 可建设（金融 RAG 审计基准等）|

**要点**：Eval 不只是研究主题——**dsh-quant 是 eval 驱动的工程**（215 测试/93.9% 覆盖/7 CI），
全 AI-native Trading 是 eval 驱动的自进化。Eval 一直是本文强调的主题，现在有了完整理论。

## 🐳 一句话

> **"Self-evolution without eval is Brownian motion."**
> Eval 是自进化的反馈通道——本文强调它，现在证明它对：
> **每笔交易都被 eval，每个反馈都更新系统，这就是无限自进化。**

---

## 📚 参考

- P-Research Eval 报告（2026-08-19，363 篇论文）
- SPADE / HarnessEval-W / MCPVerse / Open-MOPD（arXiv）
- DeepSeek Harness 评测 · Kimi K2 基准 · OpenAI Evals 库

欢迎翻阅、指正、PR 🐳
