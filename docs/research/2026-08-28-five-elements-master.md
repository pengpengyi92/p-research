# 🧠 AI 前沿五大模块总纲：RAG / Memory / Tool / Planning / Eval（PAT 能力栈 × 深度研究合集）

> **P-Research 总纲公告** · 2026-08-28 · 五大模块深度系列收官整合
> 关联：PAT（PENGYI AGENT TEAM）Agent Capability Stack · 六大深度报告 · AI-native Trading 愿景
> 系列：#10 RAG · #12 Harness · #13 Memory · #14 Tool Use · #15 Planning · #16 Eval

---

## 0. 总纲一句话

> **五大模块（RAG / Memory / Tool Use / Planning / Evaluation）= PAT 的 Agent 能力栈——
> 四个获取型能力被 Evaluation 支撑，Harness 是它们的运行时骨架。
> 深度研究结论：Eval 是自进化的反馈通道，Harness 是取代"马鞍工程"的新地基。**

---

## 一、五大模块总览（PAT 能力栈）

```text
RAG + Memory + Tool Use + Planning        ← 获取/执行型能力
                  |
             Evaluation                   ← 支撑层（反馈通道）
                  |
       Harness + 权限 + 运维               ← 运行时骨架（控制面）
```

| 模块 | 一句话 | 深度研究结论 | 报告 |
|---|---|---|---|
| **🧠 RAG** | 检索增强：什么时候检索、检索什么 | 检索记忆与模型内记忆边界消融；图 RAG×多智能体×记忆=2026 最热 | #10 |
| **🧬 Memory** | 记忆：显式可插拔架构组件 | 记忆是 agent 分水岭（谁有持久记忆谁跑长任务）| #13 |
| **🔧 Tool Use** | 工具：自进化的环境 | 工具不再是插件——是 agent 进化环境；实盘要确定性+可审计 | #14 |
| **🗺️ Planning** | 规划：递归的执行层 | 规划是被训练的策略（×RL）；EvoTS-Agent 证明金融自进化可行 | #15 |
| **📏 Evaluation** | 评估：公共基座 + 反馈通道 | "无 eval 的自进化是布朗运动"——Eval 让适应有方向 | #16 |
| **🛠️ Harness** | 运行时骨架（跨模块）| 取代马鞍工程——agent 的地基从 prompt 变运行时 | #12 |

---

## 二、五大模块的内在逻辑（为什么是这五个）

### 2.1 能力栈结构（PAT 定义）
- **获取型**：RAG（知识）· Memory（经验）· Tool Use（行动）· Planning（执行）——agent 怎么获取/使用
- **支撑型**：Evaluation——它们四个怎么被验证
- **骨架型**：Harness——它们四个跑在什么上面

### 2.2 深度研究揭示的交叉
1. **RAG × Memory 融合**（共现 51）——检索记忆与模型内记忆长成同一个东西
2. **Planning × RL**（最强信号）——规划从脚本变成被训练的策略
3. **Tool × 自进化**——SPADE：工具环境是训练场
4. **Eval 连接一切**——RAG 对不对 / Memory 记没记住 / Tool 用没用对 / Planning 规没规划好，全路由到 Eval
5. **Harness 提供骨架**——作用域路由/快照回滚/评测闭环

### 2.3 四缺一（研究机会）
四大模块各缺基准（RAG 缺 retrieve-or-abstain · Memory 缺模块基准 · Tool 缺金融审计 · Planning 缺金融规划）——**基准缺口 = 可建设方向**（呼应 Eval 报告的"结构性缺口"）。

---

## 三、呼应 PAT（PENGYI AGENT TEAM）

### 3.1 PAT 是什么
- **技术上是 Agent Harness Capability Platform**（不是领域团队）
- 位于模型层与领域层之间：`Model → PAT 能力平台 → Domain Agent 层`
- 五大模块 = PAT 能力栈的核心（可独立研究、版本化，共享一个运行时）

### 3.2 研究呼应（深度研究 → PAT 落地）

| PAT 能力栈 | 深度研究结论 → PAT 动作 |
|---|---|
| **Knowledge/RAG** | 边界消融 → RAG/Memory 合并研究 |
| **Memory** | 外部记忆是方向 → PAT 记忆基础设施 |
| **Tools/Skills** | 实盘确定性 → 工具契约（canonical output）|
| **Planning** | RL 规划 → 战术层升级 |
| **Evaluation** | **Eval 是自进化解药 → PAT 的适应-发布环（governed adaptation）** |
| **Harness 控制面** | 骨架 → PAT 的运行时 + 权限 + 安全控制面 |

### 3.3 关键：PAT 的适应-发布环（eval-driven）
```text
Domain Agent 层（PAAT/PDAT/PET...）产生真实任务证据
  → PAT 能力平台 eval（五大模块怎么被验证）
  → governed adaptation（有治理的适应）
  → 发布 → 循环（自进化）
```
**这正是一切深度研究的落点**：PAT 把五大模块 + eval 环变成可运营的平台。

---

## 四、研究意义（PAT → 实盘 → 自进化）

```text
五大模块（PAT 能力栈）
  → dsh-quant（AI-native 量化 OS：工具契约 + 评测闭环）
  → 三策略（多因子/趋势/做市）
  → 实盘（eval 三层门禁：回测→模拟→小额）
  → 自进化（每笔交易被 eval → 更新系统）
```

**一句话**：**PAT 是能力平台，dsh-quant 是量化 OS，三策略是引擎，Eval 是方向盘，Harness 是车身——全 AI-native Trading 是目的地。**

## 🐳 总纲一句话

> **五大模块 = 能力栈（RAG/Memory/Tool/Planning 被 Eval 支撑，Harness 是骨架）；
> PAT 把它们变成可运营平台；dsh-quant 在 Harness 上做量化；
> 每笔交易被 eval，每个反馈更新系统——这就是无限自进化。**

---

## 📚 关联资产

- PAT Agent Capability Stack：`PAT/docs/AGENT_CAPABILITY_STACK.md`
- 六大深度报告：p-research/docs/research/（RAG/Harness/Memory/Tool/Planning/Eval）
- 愿景：全 AI-native Trading（三策略支柱）

欢迎翻阅、指正、PR 🐳
