# AutoMemory — p-research 视角

**Last reviewed:** 2026-11-14 (Asia/Shanghai). **Profile:** research.

[官方仓库](https://github.com/HKUDS/AutoMemory) · [固定提交 README](https://github.com/HKUDS/AutoMemory/blob/f06be29b69da33dade1a278109372a40c9023d49/README.md).
来源提交：`f06be29b69da33dade1a278109372a40c9023d49`；逐条时间与公开元数据见 [catalog.json](../catalog.json)。

## 用途

Agent 记忆管理与改进流程的研究实现。

## 为何在本仓库收录

研究 memory 的状态、来源、质量与改进 gate，保留真实 refine blocker 贡献线索。 这是目录编者的选题理由，不是已测量的优越性或官方背书。

## 源码入口

以下路径已在上述固定 Git tree 中核对；路径存在不等于本轮完成源码审计。

1. [源码入口 1](https://github.com/HKUDS/AutoMemory/blob/f06be29b69da33dade1a278109372a40c9023d49/scaffolds/check_refine_state.py)：`scaffolds/check_refine_state.py`。
2. [源码入口 2](https://github.com/HKUDS/AutoMemory/blob/f06be29b69da33dade1a278109372a40c9023d49/tests/test_check_refine_state.py)：`tests/test_check_refine_state.py`。

## 学习路线

先读官方 README 与许可，再按上述入口追踪一个输入、状态变化和输出；对照其测试，写下问题：**失效记忆是否被明确报错而非静默接受？**

## 练习（未执行）

设计畸形状态、缺字段、不可用记忆和回滚的合成对照；改进必须由固定任务集验证。 本轮新增练习的实测效果、性能和学习收益均为 **NOT RUN / UNMEASURED**，不沿用旧 PR 的局部测试冒充新实验。

## 贡献证据

本轮独立读回的公开 PR 元数据如下；MERGED、OPEN 与 CLOSED_UNMERGED 分开记录，不由关闭推断合并，也不由本地测试推断 CI 成功。

| PR | 当前状态 | 公开主题 |
| --- | --- | --- |
| [#8](https://github.com/HKUDS/AutoMemory/pull/8) | OPEN | fix(refine): report malformed state values as blockers |

这是有界样本：查询总匹配 1，本页最多保留 5 条详细记录，不是全历史审计。

## 许可与限制

GitHub 许可证信号：**未识别**。 本轮未取得可链接的根许可证；标为 **NEEDS_PERMISSION**，仅收录外部参考，不提供安装、复制、修改或分发授权。
本次没有安装/运行此库、调用收费服务、下载模型、签署新 CLA/DCO 或提交上游改动。公开 PR 仅作学习案例；不构成就业、团队合作或生产采用声明。

[分类路线](README.md) · [本目录总入口](../README.md) · [学习与证据模板](../HOW_TO_STUDY.md)
