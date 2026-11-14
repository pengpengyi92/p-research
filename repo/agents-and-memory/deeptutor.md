# DeepTutor — p-research 视角

**Last reviewed:** 2026-11-14 (Asia/Shanghai). **Profile:** research.

[官方仓库](https://github.com/HKUDS/DeepTutor) · [固定提交 README](https://github.com/HKUDS/DeepTutor/blob/60fb3bdfddb30b7740c7ce3bd9b28d908f2af6db/README.md).
来源提交：`60fb3bdfddb30b7740c7ce3bd9b28d908f2af6db`；逐条时间与公开元数据见 [catalog.json](../catalog.json)。

## 用途

面向学习/解题的 Agent 工作流。

## 为何在本仓库收录

研究教学 Agent 的规划、工具、结构化响应和评估，避免以演示替代学习效果证据。 这是目录编者的选题理由，不是已测量的优越性或官方背书。

## 源码入口

以下路径已在上述固定 Git tree 中核对；路径存在不等于本轮完成源码审计。

1. [源码入口 1](https://github.com/HKUDS/DeepTutor/blob/60fb3bdfddb30b7740c7ce3bd9b28d908f2af6db/deeptutor/agents/_shared/json_output.py)：`deeptutor/agents/_shared/json_output.py`。
2. [源码入口 2](https://github.com/HKUDS/DeepTutor/blob/60fb3bdfddb30b7740c7ce3bd9b28d908f2af6db/deeptutor/agents/loop/ask_user_drafts.py)：`deeptutor/agents/loop/ask_user_drafts.py`。

## 学习路线

先读官方 README 与许可，再按上述入口追踪一个输入、状态变化和输出；对照其测试，写下问题：**正确输出是否来自合法且完成的推理/格式边界？**

## 练习（未执行）

用固定问题集检查结构化输出边界、拒答和证据；模型答对率与真实学习增益分开评价。 本轮新增练习的实测效果、性能和学习收益均为 **NOT RUN / UNMEASURED**，不沿用旧 PR 的局部测试冒充新实验。

## 贡献证据

本轮独立读回的公开 PR 元数据如下；MERGED、OPEN 与 CLOSED_UNMERGED 分开记录，不由关闭推断合并，也不由本地测试推断 CI 成功。

| PR | 当前状态 | 公开主题 |
| --- | --- | --- |
| [#2677](https://github.com/HKUDS/DeepTutor/pull/2677) | OPEN | fix(agents): reject JSON drafts inside unfinished reasoning |
| [#1199](https://github.com/HKUDS/DeepTutor/pull/1199) | OPEN | fix(agentic): fall back for Gemini thinking tools |
| [#1198](https://github.com/HKUDS/DeepTutor/pull/1198) | CLOSED_UNMERGED | fix(cron): support migration locks on Windows |

这是有界样本：查询总匹配 4，本页最多保留 5 条详细记录，不是全历史审计。

## 许可与限制

GitHub 许可证信号：**Apache-2.0**。 阅读 [上游许可](https://github.com/HKUDS/DeepTutor/blob/60fb3bdfddb30b7740c7ce3bd9b28d908f2af6db/LICENSE)；API 分类不替代许可原文、第三方依赖、数据/模型权重和商用条件。
本次没有安装/运行此库、调用收费服务、下载模型、签署新 CLA/DCO 或提交上游改动。公开 PR 仅作学习案例；不构成就业、团队合作或生产采用声明。

[分类路线](README.md) · [本目录总入口](../README.md) · [学习与证据模板](../HOW_TO_STUDY.md)
