# 方寸跃迁（Fangcun Leap）深度尽调报告（完整版）

> Date: `2026-08-30` ｜ p-research 公开尽调 ｜ 对象: 方寸跃迁（雄安）科技有限公司 · fangcunleap.com
> 定位: **研究驱动的 AI 安全公司**——Agent Runtime 安全 + 大模型安全评测
> 更新: 基于官网/文档/招聘/JD/开源（替代此前"影子版"尽调）

---

## 0. TL;DR

- **方寸跃迁 = 研究驱动的 AI 安全公司**（不是影子公司）——"以 AI 治 AI，建立人与 AI 之间的信任中间层"
- **背景**：依托**清华大学交叉信息研究院**（姚班系）AI 安全技术积累
- **团队**：核心毕业于**清华/UC Berkeley/UCL/悉尼/莱斯**，曾在百度/中国电信
- **产品**：Agent Runtime 安全（Agent IAM/Observer/Guard/SkillWard/Steward）+ 大模型安全评测（RedTeam/Multi-Agent 攻击）
- **开源**：**SkillWard**（Agent Skill 安全扫描器，Apache 2.0，三阶段：静态+LLM+Docker 沙箱）
- **在招**：AI 安全工程师（大模型方向，**含 RLHF/DPO**）+ 产品经理（C 端 AI 安全）+ 研究员/工程师
- **合作**：水木清华/SEE Fund/星联/奇智 + Dify 市场 + 新智元报道


---

## 1. 公司基本面

| 项 | 信息 |
|---|---|
| 公司 | 方寸跃迁（雄安）科技有限公司 |
| 品牌 | Fangcun Leap（fangcunleap.com）|
| 定位 | 研究驱动 AI 安全公司——"构建防御系统保护 AI 模型/LLM/自主智能体免受对抗性威胁" |
| 使命 | "守护人工智能的安全未来"· "以 AI 治 AI，建立人与 AI 之间的信任中间层" |
| 学术 | **依托清华大学交叉信息研究院** AI 安全团队 |
| 团队 | 核心毕业于清华/UC Berkeley/UCL/悉尼/莱斯，曾任百度/中国电信 |
| 地点 | 雄安新区 + 北京（清华系）|
| 备案 | 冀ICP备2026005892号 |

## 2. 产品矩阵（全链路 AI 安全）

### 2.1 Agent Runtime 安全
| 产品 | 功能 |
|---|---|
| **Agent IAM** | 身份认证与权限管理——Agent/任务/工具独立身份、最小权限策略 |
| **方寸 Observer** | 运行时监控 + 行为审计——命令/文件/网络/行为链全留痕 |
| **方寸 Guard** | 实时内容护栏——**F1 91.1 / p99 8ms / 10 类风险 / 中文专项 / 6 项 benchmark 对齐** |
| **SkillWard** | Skill/MCP 安全检测器——三阶段扫描（静态+LLM+Docker 沙箱）|
| **Steward Agent** | 中控监督——多 Agent 管理、任务协调、跨 Agent 审计 |

### 2.2 大模型安全评测
| 产品 | 功能 |
|---|---|
| **方寸 RedTeam** | 自动化红队测试平台——攻击用例生成、规模化对抗、结果复现、风险归因 |
| **Multi-Agent 自动化攻击** | 多智能体协同多阶段攻击——"攻-防-评"闭环 |

### 2.3 威胁覆盖
Prompt 注入 · 越狱攻击 · 对抗样本 · 模型投毒 · Agent 越权 · 供应链风险 · 数据泄露

## 3. 开源资产（可验证）

| 项目 | 说明 |
|---|---|
| **SkillWard**（Fangcun-AI/SkillWard）| Agent Skill 安全扫描器——静态分析+LLM 评估+沙箱验证（Apache 2.0 / Python 3.10+ / Docker）|
| 组织 | GitHub: Fangcun-AI |
| 生态 | Trendshift 收录 + Dify 市场 + 观猹产品页 |

## 4. 招聘（2026-08 官网）

### AI 安全工程师（大模型方向）
**职责关键点**：
- 大模型全链路攻防（Prompt 注入/越狱/对抗样本/投毒）
- **大模型训练全流程（PT/SFT/RLHF/DPO）——端到端**
- 训练数据质量（标注/去重/脱敏/语料构建）
- **AI 安全 Benchmark 构建 + 红队测试集**
- 护栏系统开发（内容安全/数据脱敏/行为约束/多模态）
- 跟踪法规与前沿（对齐/可解释性/鲁棒性）

**要求关键点**：
- 硕士+优先（应届/实习亦可）
- Python + PyTorch/DeepSpeed/Megatron
- **熟悉 RLHF/DPO + LoRA/QLoRA**
- 数据工程能力
- **了解 Agent 架构（ReAct/Tool Use/Multi-Agent）安全挑战**
- **熟练使用 Claude Code/Cursor**（AI 辅助开发文化）
- 系统工程（Linux/Docker/K8s/CI-CD）

**加分**：大模型预训练/大规模 RLHF 实战 · 安全对齐/红队 · 顶会论文（ACL/NeurIPS/ICLR/USENIX Security）· CTF/AI 安全竞赛 · 模型压缩 · 标注平台

### 产品经理（C 端 AI 安全产品负责人）
- 从 0 到 1 定义 C 端安全产品 + 增长
- 5 年+ 产品经验，2 年+ 带 10 人团队

### 其他
- "我们在招研究员与工程师，欢迎对 AI 安全有热情的你加入"

## 5. 工作环境（JD 披露）
- **扁平化**、结果导向、无层级内耗/无效加班
- 创新源于自主与无后顾之忧
- 使用 Claude Code/Cursor（AI-native 开发文化）

## 6. 前景判断

### 利好
- **AI 安全 = 2026 最热赛道之一**（agent 普及 → 安全刚需爆发）
- 清华交叉信息研究院背书（学术+人才）
- 产品已上线（Guard/Observer/RedTeam 可体验）+ 开源生态（SkillWard）
- 政策支持（网安标委智能体安全指引 2026-07）
- AI 安全赛道（FlagSafe/朱雀等同赛道）

### 风险
- 公司新（融资未公开披露）
- AI 安全竞争激烈（FlagSafe/朱雀/海外 labs）
- C 端产品未验证（招聘显示还在 0→1）

## 8. 信息来源
- 官网 fangcunleap.com（首页/关于/招聘/文档/新闻）
- GitHub Fangcun-AI/SkillWard（开源项目）
- 新智元（2026-05-07）: Agent 暗藏风险，清华团队组合拳
- 网安标委/AIIA（智能体安全指引 2026）
