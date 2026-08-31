# ClawTeam 深度研究 — Agent Swarm Intelligence（2026-08-31）

> p-research 公开研究 ｜ 对象: HKUDS/ClawTeam（GitHub ⭐5.5k）
> 定位: "让 AI Agent 组成团队，思考、协作、交付"——Solo → Swarm
> 关联: Multi-Agent 研究方向全景 · HKUDS Multi-Agent 研究

---

## 0. TL;DR

**ClawTeam** 是 HKUDS 开源的 **Agent Swarm Intelligence** 框架——让多个 AI agent 自组织成团队协作完成复杂任务。核心设计：**leader agent 用 `clawteam spawn` 生成 worker，每个 worker 有独立 git worktree/tmux/身份；agent 间通过 inbox 通信；所有状态存 JSON 文件（无数据库/服务器/云）**。它把 Multi-Agent 从"研究概念"做成了"一条命令可用的产品"，且 roadmap 直指生产级（Redis 传输→共享状态→Agent 市场→自适应调度→auth/审计）。

---

## 1. 项目速览

| 项 | 信息 |
|---|---|
| Repo | HKUDS/ClawTeam |
| Stars | ~5.5k（MIT 开源）|
| 定位 | Agent Swarm Intelligence——Agent 自组织团队 |
| 理念 | Solo 🤖 → Swarm 🦞🤖🤖🤖 |
| 发布 | 2026-03-18 公开 · v0.2.0（2026-03-23）· v0.3 roadmap 基线 |
| 兼容 | Claude Code / Codex / OpenClaw / nanobot / Cursor / 任何 CLI agent |
| 语言 | Python 3.10+ · Typer CLI |
| 传输 | File（默认）/ P2P（ZeroMQ + fallback）|

## 2. 核心设计

### 2.1 架构（Leader → Workers）
```
Human 给目标 → Leader agent → clawteam spawn → Worker(s)
每个 Worker: git worktree（隔离代码）+ tmux（隔离进程）+ 独立身份
Worker 用: task list（领任务）/ task update（报进度）/ inbox（通信）
状态: ~/.clawteam/ 下 JSON 文件（teams/tasks/inboxes/workspaces）
```

**关键设计选择**：
- **无服务器架构**：纯 JSON 文件 + 原子写（tmp+rename 崩溃安全）——零运维
- **物理隔离**：每个 worker 独立 worktree/tmux——互不干扰
- **CLI 注入**：通信命令自动注入 agent prompt——agent 学会"用团队"
- **多 agent 兼容**：leader 用 Claude Code，worker 可以是 Codex/任何 CLI

### 2.2 命令流（agent 视角）
```bash
# Leader:
clawteam spawn --team my-team --agent-name worker1 --task "实现 auth 模块"
clawteam task create / inbox send / board show / task wait

# Worker:
clawteam task list my-team --owner me
clawteam inbox send my-team leader "Auth done. All tests passing."
```

### 2.3 传输层
| 传输 | 机制 | 适用 |
|---|---|---|
| **file**（默认）| JSON 文件在 inbox 目录 | 单机共享 FS |
| **p2p** | ZeroMQ PUSH/PULL + file fallback | 低延迟、自动降级 |

## 3. 用例（Swarm Intelligence in Action）

### 🔬 AI 研究自动化（旗舰演示）
- **leader agent 编排 8 个专用子 agent 跨 8×H100 GPU**
- 自主设计实验、动态重分配资源（按实时性能）
- **系统跨团队综合突破、独立进化策略——全自动研究，无需人类干预**
- 技术来源：@karpathy/autoresearch（8-agent swarm demo 用的框架）

### 💰 AI Hedge Fund（模板）
- 多策略组合优化 + 实时风控 + 算法交易执行监控
- 灵感来源：virattt/ai-hedge-fund（multi-analyst 模板）

### 🏗️ Agentic Engineering
- 全栈自主开发、自进化软件、协作开源开发

### 🎪 自定义 Swarm
- 科研团队 / 投资委员会 / 业务运营 / 内容制作

## 4. Roadmap（方向信号）

| Phase | 版本 | 内容 | 状态 |
|---|---|---|---|
| 当前 | v0.3 | File+P2P 传输、Web UI、多用户、团队模板 | ✅ Shipped |
| 1 | v0.4 | **Redis 传输**（跨机器消息）| 🔜 |
| 2 | v0.5 | **共享状态层**（跨机器团队配置/任务）| 🔜 |
| 3 | v0.6 | **Agent 市场**（社区复用模板）| 💡 |
| 4 | v0.7 | **自适应调度**（按性能动态重分配）| 💡 |
| 5 | v1.0 | **生产级**（auth/权限/审计日志）| 💡 |

**趋势**：从单机 → 跨机器 → 市场 → 自适应 → 生产级——**swarm 正在变成基础设施**

## 5. 技术洞察

1. **"无服务器"是聪明选择**：JSON 文件起步（零部署），Redis 跨机（v0.4）——渐进式
2. **物理隔离 = 工程正确**：worktree/tmux 让 agent 真正并行不冲突
3. **CLI 注入 = 低门槛**：现有 agent（Claude/Codex）无需改就能加入团队
4. **模板化 = 可复用**：科研/对冲基金/工程——领域模板开箱即用
5. **自适应调度是终局**（v0.7）：按性能重分配 = 团队自组织的高级形态

## 6. 与 Multi-Agent 研究方向的对应

| ClawTeam 实现 | Multi-Agent 研究方向 |
|---|---|
| leader→worker 编排 | 单监督编排模式 |
| inbox 通信 | 通信协议 |
| spawn 自组织 | 涌现（Solo→Swarm）|
| 模板（对冲基金等）| 协作价值决策（按领域选）|
| v1.0 auth/审计 | 多体安全/治理 |

## 7. 生态位置

- **HKUDS 系**：ClawTeam（swarm）+ OpenSpace（技能）+ AgentSpace（人机）+ CLI-Anything（agent-native）
- **互补**：Karpathy autoresearch（研究框架）、virattt ai-hedge-fund（对冲模板）
- **意义**：HKUDS 把 Multi-Agent 研究做成产品矩阵——**学术→产品的完整弧线**

## 8. 信息来源
- GitHub HKUDS/ClawTeam README（2026-08-31 抓取，548 行完整）
- HKUDS Multi-Agent 研究解读（2026-08-31）
- Multi-Agent 研究方向全景（2026-08-31）
