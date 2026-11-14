# How to Study — p-research

**Updated:** 2026-11-14 (Asia/Shanghai). AI 为主；Agent、RAG、多模态、记忆、模型和研究评价；Quant × AI 保留为应用分支。

## 一个小问题，而非一次安装所有库

先固定问题、baseline 和 holdout；再看 LightRAG / RAG-Anything / VideoRAG 的证据链；接着比较 smolagents / AutoSwarm / HELIX / DeepCode 的工具与交接；最后评价 memory / tutoring 的实际收益，而不是只看演示。

1. 核对官方来源、固定 commit、许可、依赖和数据/权重权利；NEEDS_PERMISSION 项目先停在参考层。
2. README → 一个核心入口 → 对应测试；先辨别训练/推理、真实/合成、外部服务/本地函数。
3. 设可证伪问题与独立 baseline；固定样本、种子、配置、版本、资源预算和评价标准。
4. 将训练、开发、一次性审计 holdout 分开；分组/时序泄漏、缺字段、异常和越权要有负面对照。
5. 记录正确性、误差/质量、耗时与成本；未运行写 NOT RUN，未测量写 UNMEASURED，不捏造分数。
6. 新 GPU/模型下载、付费服务、私有数据、上游发帖和 CLA/DCO 都需要单独授权；目录不是运行许可。
7. 记录失败与 trade-off，再决定下一步；真实实验另立项目，不能把 catalog tests 当成模型效果证据。

## 最小实验记录

```text
Question / official source / commit / license:
Baseline / proposed change:
Dataset rights / split / fixed fixture / seed:
Metric / units / tolerance / budget:
Environment / exact command:
Observed result: PASS / FAIL / NOT RUN
Cost / limitations / negative findings:
Next Action:
```

## 三个仓库各自负责什么

- [P-ML](https://github.com/pengpengyi92/P-ML/tree/main/ml-repo)：学习模型与方法，训练/数据/评价基础。
- [P-Research](https://github.com/pengpengyi92/p-research/tree/main/repo)：AI 研究问题、Agent/RAG/Memory、假设与可复现评价。
- [P-CSDSAI](https://github.com/pengpengyi92/p-csdsai/tree/main/repo)：系统、编程、serving、编译、分布式和数据工程。

相同库共享事实来源，但阅读问题不同，不重复宣称三次实验或三次贡献。只发布公开/合成材料，不导出私人策略、论文、对话或工作区日志。

[总目录](README.md)
