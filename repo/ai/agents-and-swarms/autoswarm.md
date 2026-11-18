# AutoSwarm — p-research 视角

**Last reviewed:** 2026-11-18T19:19:17.651011+08:00 (Asia/Shanghai). **Profile:** research.
**分类：AI → Multi-Agent / Agent Swarms**；标签：AI、Multi-Agent、Context Sharing。

[官方仓库](https://github.com/HKUDS/AutoSwarm) · [固定 README](https://github.com/HKUDS/AutoSwarm/blob/68463dd562640ada92a9dbbb1a1a5091b0811866/README.md)。
来源提交：`68463dd562640ada92a9dbbb1a1a5091b0811866`。包定义为 `2.0.0.dev0`：**开发快照，不是稳定发布声明**。
[机器条目](../../catalog.json)；其他条目的来源观测时间保持不变。

## 用途

面向已有 Agent 原生 CLI 的协作与任务交接项目。上游文档区分插件核心和 Desk
使用层，README 列出 Codex、DeepSeek Harness 等协作者。这是上游描述与源码
入口，不是本轮的本机兼容性、权限隔离或性能验证。

## 为何在本仓库收录

研究多 Agent 协作相对单 Agent 的有效收益，分离上下文共享、任务分工和协调成本，并用固定任务集检验。
这是原创选题理由，不是工具优越性、官方合作或生产采用声明。

## 源码入口

以下路径和 blob 已在同一固定 Git tree 核对；存在不等于源码审计或测试通过。

- [pyproject.toml](https://github.com/HKUDS/AutoSwarm/blob/68463dd562640ada92a9dbbb1a1a5091b0811866/pyproject.toml)
- [docs/architecture.md](https://github.com/HKUDS/AutoSwarm/blob/68463dd562640ada92a9dbbb1a1a5091b0811866/docs/architecture.md)
- [src/autoswarm/cli.py](https://github.com/HKUDS/AutoSwarm/blob/68463dd562640ada92a9dbbb1a1a5091b0811866/src/autoswarm/cli.py)
- [src/autoswarm/engine.py](https://github.com/HKUDS/AutoSwarm/blob/68463dd562640ada92a9dbbb1a1a5091b0811866/src/autoswarm/engine.py)
- [src/autoswarm/approvals.py](https://github.com/HKUDS/AutoSwarm/blob/68463dd562640ada92a9dbbb1a1a5091b0811866/src/autoswarm/approvals.py)
- [src/autoswarm/providers.py](https://github.com/HKUDS/AutoSwarm/blob/68463dd562640ada92a9dbbb1a1a5091b0811866/src/autoswarm/providers.py)
- [tests/test_runtime.py](https://github.com/HKUDS/AutoSwarm/blob/68463dd562640ada92a9dbbb1a1a5091b0811866/tests/test_runtime.py)
- [tests/test_approvals.py](https://github.com/HKUDS/AutoSwarm/blob/68463dd562640ada92a9dbbb1a1a5091b0811866/tests/test_approvals.py)

## 学习路线

1. 明确协作需求来自能力互补、上下文交接还是独立验证。
2. 先固定单 Agent baseline，再比较顺序交接和双 Agent，不先增加数量。
3. 固定任务集、模型版本、上下文与总预算，区分实现测试与任务收益。
4. 记录正确率、交接错误、耗时、资源代价和负面结果；独立评审需要真实评审者。

可证伪问题：**相同任务、模型与预算下，协作的正确率收益能否覆盖交接和资源成本？**

## 练习（未执行）

预注册单 Agent、顺序交接、双 Agent 三组；固定公开或合成任务、模型版本、总调用/时间预算和盲评标准，保留负面结果。

拟测有效完成率、盲评正确性、交接错误率、总耗时和每个有效输出的成本。
先写合成输入、预期结果、失败/拒绝对照和停止条件，得到明确授权后才执行。
真实双 Agent、模型调用、Desk 安装与收益均 **NOT RUN / UNMEASURED**。

## 贡献证据

公开查询总匹配1，本轮只核对这一项，不是全历史审计。

| PR | 当前状态 | 公开主题 |
| --- | --- | --- |
| [#45](https://github.com/HKUDS/AutoSwarm/pull/45) | OPEN | feat(mcp): scope servers and tools by runtime context |

这是未合并的历史 PR，不是当前主线 MCP 实现或本次新贡献的证据。
当前架构文档写明 MCP 不作为当前依赖；不能从旧 PR 标题推断已实现。
本次未提交上游改动，不将旧测试/配置验证外推到这一开发快照。

## 许可与限制

GitHub 许可信号 **MIT**；见[固定许可](https://github.com/HKUDS/AutoSwarm/blob/68463dd562640ada92a9dbbb1a1a5091b0811866/LICENSE)。
代码许可不替代第三方依赖、原生 Agent 服务、数据/模型权重、账户和费用条款。
README 安装/doctor probe 示例不是本次执行授权；probe 可能产生模型调用。
不要同步凭据、私人会话、受保护数据或未经批准的跨项目上下文。
本轮只有公开收录和目录回归，没有安装、原生 Agent 探测、付费调用或部署。

[历史卡](../../agents-and-memory/autoswarm.md) · [历史条目元数据](autoswarm-history.json)。

[AI 分类](../README.md) · [子分类](README.md) · [Repo 总目录](../../README.md) · [学习与证据模板](../../HOW_TO_STUDY.md)。
