# LightRAG — p-research 视角

**Last reviewed:** 2026-11-14 (Asia/Shanghai). **Profile:** research.

[官方仓库](https://github.com/HKUDS/LightRAG) · [固定提交 README](https://github.com/HKUDS/LightRAG/blob/3605ac2160929ac5d3ea16cb1e4b18658c89dead/README.md).
来源提交：`3605ac2160929ac5d3ea16cb1e4b18658c89dead`；逐条时间与公开元数据见 [catalog.json](../catalog.json)。

## 用途

检索增强生成及图/文本检索相关实现。

## 为何在本仓库收录

研究检索、知识组织、证据与回答质量的关系，结合实际 parser 贡献案例。 这是目录编者的选题理由，不是已测量的优越性或官方背书。

## 源码入口

以下路径已在上述固定 Git tree 中核对；路径存在不等于本轮完成源码审计。

1. [源码入口 1](https://github.com/HKUDS/LightRAG/blob/3605ac2160929ac5d3ea16cb1e4b18658c89dead/lightrag/lightrag.py)：`lightrag/lightrag.py`。
2. [源码入口 2](https://github.com/HKUDS/LightRAG/blob/3605ac2160929ac5d3ea16cb1e4b18658c89dead/lightrag/operate.py)：`lightrag/operate.py`。

## 学习路线

先读官方 README 与许可，再按上述入口追踪一个输入、状态变化和输出；对照其测试，写下问题：**回答能否追溯到正确检索证据？**

## 练习（未执行）

先用小型授权文本设计检索命中、证据引用和缺证据拒答对照；不调用收费模型。 本轮新增练习的实测效果、性能和学习收益均为 **NOT RUN / UNMEASURED**，不沿用旧 PR 的局部测试冒充新实验。

## 贡献证据

本轮独立读回的公开 PR 元数据如下；MERGED、OPEN 与 CLOSED_UNMERGED 分开记录，不由关闭推断合并，也不由本地测试推断 CI 成功。

| PR | 当前状态 | 公开主题 |
| --- | --- | --- |
| [#4364](https://github.com/HKUDS/LightRAG/pull/4364) | MERGED | fix(parser): recognize entity-only blank HTML table headers |
| [#3717](https://github.com/HKUDS/LightRAG/pull/3717) | MERGED | fix(embeddings): keep provider API keys request-local |
| [#3632](https://github.com/HKUDS/LightRAG/pull/3632) | MERGED | fix(api): preserve source files when deleting duplicate markers |

这是有界样本：查询总匹配 8，本页最多保留 5 条详细记录，不是全历史审计。

## 许可与限制

GitHub 许可证信号：**MIT**。 阅读 [上游许可](https://github.com/HKUDS/LightRAG/blob/3605ac2160929ac5d3ea16cb1e4b18658c89dead/LICENSE)；API 分类不替代许可原文、第三方依赖、数据/模型权重和商用条件。
本次没有安装/运行此库、调用收费服务、下载模型、签署新 CLA/DCO 或提交上游改动。公开 PR 仅作学习案例；不构成就业、团队合作或生产采用声明。

[分类路线](README.md) · [本目录总入口](../README.md) · [学习与证据模板](../HOW_TO_STUDY.md)
