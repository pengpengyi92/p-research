# 🔧 Agentic Harness 深度研究：DeepSeek / Kimi / ChatGPT（OpenAI）怎么做 Agentic AI

> **P-Research 深度报告** · 2026-08-28 · harness 主题深化（我们超级关注 harness）
> 方法：三家公开资料 + 我们自己的 DeepSeek Harness 第一手经验（我们在用 dsh 开发！）
> 关联：P-Research planning/tool-use 报告 · dsh-quant（DeepSeek Harness 生态）

---

## 0. 一句话结论

> **2026 年三家主流 AI 厂商殊途同归：都把"agentic AI"押注在 Harness（运行时骨架）上**
> ——OpenAI 开放 Codex 同款 harness · DeepSeek 开源自进化 harness · Kimi 做常驻 swarm agent。
> **Harness 正在取代"马鞍工程"（prompt 拼装），成为 agent 的新地基。**

---

## 一、DeepSeek：自进化的 Harness（我们的第一手经验）

### 1.1 是什么
- **DeepSeek Harness（dsh）**：DeepSeek 官方开源的 agent 运行时/评测工具
- 定位："DeepSeek 用来自我评测的工具"开源化——**它 benchmark 自己的工具**

### 1.2 核心设计（我们的第一手认知）
- **Agent Scope Runtime**：一个 opaque key 选择一层——作用域路由
- **无损快照**：工具调用后先快照再规范化——**"AGI 自进化有了后悔药"**（雷峰网）
- **规范化输出契约**：候选结果先无损快照 → 注册表 → 失败转普通错误
- **评测闭环**：agent 行为被评测（benchmark）→ 反馈 → 自进化

### 1.3 行业解读
- "DeepSeek 对 Agent Runtime 的一次重新思考"（datalearner）
- 社区：**"新代理架构，替代马鞍工程（Harness Engineering）"**（DeepSeek-V3 issue #1210）
- 核心理念：**可回滚、可快照、可评测的 agent 执行 = 自进化的前提**

### 1.4 我们的关系
- **我们正在用 dsh 开发**（dsh-quant 是 DeepSeek Harness 插件，59 工具）
- 我们理解它的契约（canonical outputs / null alignment / no look-ahead）
- **第一手用户视角**：它解决"agent 怎么可靠地跑长流程"——正是 harness 的核心

---

## 二、Kimi（Moonshot AI）：常驻桌面 + Swarm 架构

### 2.1 Kimi Work（桌面 agent）
- **常驻桌面 agent**：always-on 桌面助手
- **Web 自动化** + **规划引擎**（scheduling engine）
- **Swarm 架构**：多个 agent 协同（swarm-based architecture）
- 定位：从"问答"到"替你干活"（数字员工）

### 2.2 Kimi K2.6 Agent 架构
- **多步推理 + 工具调用的工程落地**（CSDN 深度解析）
- 工具 schema 暴露、上下文/记忆机制（K2.5 分析）
- **外部记忆系统**（K2.6 external memory）：agent 的持久记忆

### 2.3 Kimi Code / CLI（工程 agent）
- **非交互 agentic 工作流**：JSONL 流式 + 测试 + 会话记忆（marktechpost）
- Skills 体系（Agent/Claw/Kimi Code Skills）
- 定位：把 agentic coding 变成可编程的流水线

### 2.4 特点总结
- **强项：常驻 + swarm + 记忆**——agent 不是"一次性问答"，是"持续工作的员工"
- 规划引擎 + 会话记忆 → 长期任务执行

---

## 三、OpenAI / ChatGPT：Codex Harness 全面开放

### 3.1 GPT-5.4：Codex 同款 Harness 全面开放
- **GPT-5.4 神装**：Codex 同款 harness 全面开放（36kr/c114）
- 含义：把**训练 Codex（编码 agent）的运行时**开放给所有人
- "ChatGPT 进化成超级助理，能替你用电脑干活"（Operator 方向）

### 3.2 Agents SDK（2026 更新）
- **安全 agent 构建**（building secure agents）——aibusiness
- tool use agentic：2026 大更新
- SDK 化：把 agent 构建从"prompt"变成"SDK 工程"

### 3.3 特点总结
- **强项：把最成功的编码 agent（Codex）的运行时产品化**
- Harness = 产品卖点（不是内部工具，是开放能力）
- 安全优先（secure agents）

---

## 四、三家对比（怎么做 agentic AI）

| 维度 | DeepSeek | Kimi | OpenAI |
|---|---|---|---|
| **核心产品** | DeepSeek Harness（开源）| Kimi Work + K2.6 | GPT-5.4 + Codex Harness |
| **Harness 定位** | 自进化评测工具（开源）| 常驻 agent 运行时 | 产品能力（Codex 同款）|
| **关键设计** | 无损快照/作用域路由/评测闭环 | swarm 架构/规划引擎/外部记忆 | harness 开放/SDK/安全 |
| **Agent 形态** | 工具 + 评测（可靠执行）| 常驻桌面（持续工作）| 超级助理（替你干活）|
| **自进化** | ✅ 核心（后悔药）| 记忆累积 | Codex 迭代 |
| **开源** | ✅ 全开源 | 部分（K2 模型开源）| ❌ 闭源（SDK 开放）|
| **我们能用** | ✅ 正在用（dsh-quant）| 部分（Kimi 模型）| API |

### 关键洞察（三家的共同点）

1. **Harness 是 2026 的主战场**：三家都把 agentic 押注在运行时，而非模型本身
2. **可回滚/可评测成为标配**：DeepSeek 快照 · OpenAI 安全 · Kimi 记忆——都要"可靠的执行"
3. **从 prompt 到工程**："马鞍工程"被 harness 取代——agent 是工程问题，不是文本问题
4. **记忆是分水岭**：Kimi 外部记忆 · DeepSeek 快照（执行记忆）· OpenAI 会话——记忆决定 agent 深度

---

## 五、对我们的意义（dsh-quant / P-Research）

| 角度 | 意义 |
|---|---|
| **我们在第一线** | dsh-quant 是 DeepSeek Harness 插件——我们用着最前沿的 harness 做量化 |
| **五大模块** | harness 连接 Planning（作用域路由）· Tool Use（工具契约）· Eval（评测闭环）|
| **RSI/自进化** | DeepSeek 的"后悔药"（快照回滚）= 自进化的安全网——我们的 north-star |
| **Quant×Agent** | 全 AI-native Trading（我们的愿景）= 用 harness 做量化 agent |

**站位**：我们不只是观察者——**dsh-quant 本身就是"harness 上的量化 OS"**，
三家怎么做的，我们正在用自己的方式实践（59 工具/契约/评测/自动发布）。

## 🐳 一句话

> **Harness 正在取代马鞍工程——agent 的地基从 prompt 变成运行时。
> DeepSeek 开源自进化 · OpenAI 开放 Codex 同款 · Kimi 做常驻 swarm——
> 而我们，正站在 DeepSeek Harness 上做量化。**

---

## 📚 参考

- DeepSeek Harness：github.com/deepseek-ai/deepseek-harness（我们在用）
- 雷峰网：《深度拆解 DeepSeek Harness 架构：AGI 的自进化终于有了后悔药》
- Kimi Work（swarm 架构）/ K2.6 Agent 架构
- OpenAI GPT-5.4 Codex Harness 开放 / Agents SDK 2026

欢迎翻阅、指正、PR 🐳
