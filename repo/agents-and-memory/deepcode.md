# DeepCode — p-research 视角

**Last reviewed:** 2026-11-14 (Asia/Shanghai). **Profile:** research.

[官方仓库](https://github.com/HKUDS/DeepCode) · [固定提交 README](https://github.com/HKUDS/DeepCode/blob/aa6ed16148719101b994882c94608ae12e88f870/README.md).
来源提交：`aa6ed16148719101b994882c94608ae12e88f870`；逐条时间与公开元数据见 [catalog.json](../catalog.json)。

## 用途

代码生成/研究工程相关的 Agent 项目。

## 为何在本仓库收录

研究 research-to-code 的可复现交付与验证，而非把生成成功等同工程正确。 这是目录编者的选题理由，不是已测量的优越性或官方背书。

## 源码入口

以下路径已在上述固定 Git tree 中核对；路径存在不等于本轮完成源码审计。

1. [源码入口 1](https://github.com/HKUDS/DeepCode/blob/aa6ed16148719101b994882c94608ae12e88f870/cli/exec_cli.py)：`cli/exec_cli.py`。
2. [源码入口 2](https://github.com/HKUDS/DeepCode/blob/aa6ed16148719101b994882c94608ae12e88f870/cli/project_trust.py)：`cli/project_trust.py`。

## 学习路线

先读官方 README 与许可，再按上述入口追踪一个输入、状态变化和输出；对照其测试，写下问题：**生成代码是否经过独立测试与权限审查？**

## 练习（未执行）

先拆解任务、工具、生成 artifact 与测试 gate；用小型合成任务规定验收，禁止未经授权执行/发布。 本轮新增练习的实测效果、性能和学习收益均为 **NOT RUN / UNMEASURED**，不沿用旧 PR 的局部测试冒充新实验。

## 贡献证据

本轮按本项目、作者 pengpengyi92、public PR 做有界检索，未捕获可列出的 PR。此条定位为 **官方来源核对后的阅读候选**，不声称曾提交、被采用或已独立复现。

## 许可与限制

GitHub 许可证信号：**MIT**。 阅读 [上游许可](https://github.com/HKUDS/DeepCode/blob/aa6ed16148719101b994882c94608ae12e88f870/LICENSE)；API 分类不替代许可原文、第三方依赖、数据/模型权重和商用条件。
本次没有安装/运行此库、调用收费服务、下载模型、签署新 CLA/DCO 或提交上游改动。公开 PR 仅作学习案例；不构成就业、团队合作或生产采用声明。

[分类路线](README.md) · [本目录总入口](../README.md) · [学习与证据模板](../HOW_TO_STUDY.md)
