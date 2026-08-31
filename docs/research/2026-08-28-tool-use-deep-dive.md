# 🔧 Tool Use 深度研究：工具即自进化的环境（DeepSeek / Kimi / OpenAI × 实盘视角）

> **P-Research 深度报告** · 2026-08-28 · tool use 深化（承接三家对比框架 + 自进化主题）
> 方法：P-Research corpus（清华工具学习线）+ 三家公开资料 + 本文的实盘视角
> 关联：2026-08-19 Tool Use 报告 · Harness 报告 · Memory 报告 · AI-native Trading 愿景

---

## 0. 一句话结论

> **工具不再是"冻在模型外的插件"——工具是 agent 自进化的环境。**
> 研究意义：**"尽早实盘 + 无限自进化" = 让交易工具成为量化 agent 的进化环境**——
> 每笔交易、每个因子、每个回测都是工具调用的记录，agent 在工具上自我迭代。

---

## 一、前沿趋势（清华工具学习线 → 2026）

### 谱系（清华大学主线）
```
2023 ToolLLM      16,000+ 真实 API——工具学习的规模化里程碑
2023 AgentBench   让 agent/工具使用成为可评测对象（ICLR 2024）
2023 ToolBench    大规模工具使用评测与训练集
2026 → 第三个问题：工具使用如何变得 安全、可审计、自进化
```

### 2026 四大前沿主题
1. **工具 × 自进化——训练环境即工具**
   - SPADE（自博弈合成可执行环境）· RTPO（逆向回合策略优化）
   - Write-Execute-Refine（从技能跟随者到技能优化者）
   - **工具 = agent 自进化的环境**（与递归自我改进主题相关）

2. **工具 × 最小权限——安全作为设计项**
   - Task-Conditioned Least-Privilege · SkillEffect（受限工具降级）
   - MCP/Skills 攻击面（When Agents Act on Web3）
   - → 呼应 AI 安全方向

3. **工具 × 可审计——痕迹即证据**
   - LEDGER（claim-to-evidence 追踪图）
   - → 呼应 harness 的证据链

4. **工具 × 契约（MCP/schema）**
   - Model Context Protocol 成为标准
   - 工具描述/schema 工程——"让模型会用工具"的下半场

---

## 二、三家厂商的 Tool Use（怎么做）

### 1. DeepSeek：契约驱动的工具（P-Research 第一手实践）

| 机制 | 实现 |
|---|---|
| **Canonical Output** | 工具返回结构化 JSON（output.schema 声明）|
| **Null Alignment** | 输出与输入等长、头部 null——无 padding |
| **No Look-ahead** | 工具契约保证无未来函数 |
| **作用域路由** | 工具调用状态隔离 |

**哲学**：工具 = 契约——模型/agent 依赖"确定的输入输出形状"，而不是模糊描述。
**实证表明**：dsh-quant 59 工具全是契约驱动（MCP/tools.json 运行时生成）。

### 2. Kimi：技能体系（Skills）

| 机制 | 实现 |
|---|---|
| **Skills 库** | Kimi Skills（Agent/Claw/Code Skills）|
| **Claw** | 桌面/浏览器操作工具 |
| **Kimi Code** | 编码 agent 工具链（CLI + 测试）|

**哲学**：工具 = 技能包——把"会用工具"变成"装技能"，agent 按需加载。

### 3. OpenAI：工具生态 + Agent SDK

| 机制 | 实现 |
|---|---|
| **Function Calling** | 最早的工具调用标准 |
| **Codex Harness** | 编码工具链（终端/文件/沙箱）|
| **Agents SDK** | 工具注册/编排 SDK 化 |
| **MCP 支持** | 拥抱开放工具协议 |

**哲学**：工具 = 生态——标准（function calling/MCP）+ SDK + 沙箱安全。

---

## 三、三家对比 + 实盘视角

| 维度 | DeepSeek | Kimi | OpenAI |
|---|---|---|---|
| **工具哲学** | 契约（确定性）| 技能（可加载）| 生态（标准化）|
| **核心机制** | canonical output + 作用域 | Skills 库 + Claw | Function calling + SDK |
| **安全** | 契约约束 | 技能权限 | 沙箱/least privilege |
| **自进化** | 评测闭环 | 技能迭代 | Codex 优化 |
| **实盘适配** | ⭐ 契约确定性最稳 | 技能灵活 | 生态成熟 |

### 实盘视角（"尽早实盘"）

**交易工具的特殊要求**（Tool Use 的实盘版）：
1. **确定性优先**：实盘不能有模糊工具——契约驱动（DeepSeek 式）最稳
2. **可审计**：每笔交易=工具调用记录（LEDGER 式）——合规+复盘
3. **最小权限**：交易工具权限最小化（least privilege）——风控红线
4. **可回滚**：错误交易能追溯（快照）——harness 的后悔药

**自进化视角（"无限自进化"）**：
```
实盘工具调用（交易/回测/因子）
  → 记录（trace/ledger）
  → 评测（哪些工具/策略有效）
  → 反馈（agent 迭代工具用法/策略）
  → 新的工具调用（进化循环）
```
**关键**：工具 = 自进化的环境——每笔实盘交易都是训练数据，agent 在工具上自我优化。

---

## 四、研究意义（dsh-quant → 实盘）

| 角度 | 意义 |
|---|---|
| **工具契约** | dsh-quant 59 工具契约驱动 = 实盘级确定性（DeepSeek 式）✅ |
| **实盘链路** | PDAT→PAAT→PCPT→PRT→PET 全是工具化（数据/因子/组合/风控/执行）|
| **自进化闭环** | 工具调用记录 → 评测 → 迭代（P-Research eval 线 + harness）|
| **最小权限** | 交易工具权限边界（ai-security 线）|
| **AI-native Trading** | 全 AI-native = 工具是 agent 的全部操作界面（研究视角）|

**要点**：工具不只是研究对象——**dsh-quant 的每个工具都在为实盘自进化铺路**：
契约驱动（确定性）+ 记录（可审计）+ 评测（进化）。

## 🐳 一句话

> **工具不再是插在模型外的插件——工具是 agent 自进化的环境。**
> 研究启示：**尽早实盘 = 让交易工具成为进化环境；无限自进化 = 每笔交易都是训练数据。**

---

## 📚 参考

- P-Research Tool Use 报告（2026-08-19，清华工具学习线）
- SPADE / RTPO / LEDGER（arXiv）
- DeepSeek Harness 契约 · Kimi Skills · OpenAI Function calling/Agents SDK

欢迎翻阅、指正、PR 🐳
