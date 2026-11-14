# HELIX — p-research 视角

**Last reviewed:** 2026-11-14 (Asia/Shanghai). **Profile:** research.

[官方仓库](https://github.com/HKUDS/HELIX) · [固定提交 README](https://github.com/HKUDS/HELIX/blob/b5adffa6065931b4d8833f6576188ce93006217f/README.md).
来源提交：`b5adffa6065931b4d8833f6576188ce93006217f`；逐条时间与公开元数据见 [catalog.json](../catalog.json)。

## 用途

Agent harness 的组合、评估与训练轨迹数据循环。

## 为何在本仓库收录

研究 harness 组合、模型/环境协作与训练轨迹质量，关联已有公开文档契约修复。 这是目录编者的选题理由，不是已测量的优越性或官方背书。

## 源码入口

以下路径已在上述固定 Git tree 中核对；路径存在不等于本轮完成源码审计。

1. [源码入口 1](https://github.com/HKUDS/HELIX/blob/b5adffa6065931b4d8833f6576188ce93006217f/packages/contracts/src/index.ts)：`packages/contracts/src/index.ts`。
2. [源码入口 2](https://github.com/HKUDS/HELIX/blob/b5adffa6065931b4d8833f6576188ce93006217f/packages/lego-agent-loop/src/index.ts)：`packages/lego-agent-loop/src/index.ts`。

## 学习路线

先读官方 README 与许可，再按上述入口追踪一个输入、状态变化和输出；对照其测试，写下问题：**harness 改动能否通过独立评价并产生可追溯数据？**

## 练习（未执行）

先跟踪 harness 契约、Agent loop、verifier 和数据来源，再设计固定任务集的 ablation；不采信未经复现的性能宣传。 本轮新增练习的实测效果、性能和学习收益均为 **NOT RUN / UNMEASURED**，不沿用旧 PR 的局部测试冒充新实验。

## 贡献证据

本轮独立读回的公开 PR 元数据如下；MERGED、OPEN 与 CLOSED_UNMERGED 分开记录，不由关闭推断合并，也不由本地测试推断 CI 成功。

| PR | 当前状态 | 公开主题 |
| --- | --- | --- |
| [#3](https://github.com/HKUDS/HELIX/pull/3) | OPEN | fix(docs): honor clients that opt out of gzip |

这是有界样本：查询总匹配 1，本页最多保留 5 条详细记录，不是全历史审计。

## 许可与限制

GitHub 许可证信号：**MIT**。 阅读 [上游许可](https://github.com/HKUDS/HELIX/blob/b5adffa6065931b4d8833f6576188ce93006217f/LICENSE)；API 分类不替代许可原文、第三方依赖、数据/模型权重和商用条件。
本次没有安装/运行此库、调用收费服务、下载模型、签署新 CLA/DCO 或提交上游改动。公开 PR 仅作学习案例；不构成就业、团队合作或生产采用声明。

[分类路线](README.md) · [本目录总入口](../README.md) · [学习与证据模板](../HOW_TO_STUDY.md)
