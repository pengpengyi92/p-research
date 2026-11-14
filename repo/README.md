# AI Research — Agent、RAG、Memory 与评价

**Last reviewed:** 2026-11-14 (Asia/Shanghai). 首批 **12** 个项目视角档案；选题范围：AI 为主；Agent、RAG、多模态、记忆、模型和研究评价；Quant × AI 保留为应用分支。

这不是整个生态的全量清单、星数排名或安装建议。历史公开 PR 已重新读回；无 PR 的项目标为阅读候选，不编造贡献或复现。每篇档案都有独立收录理由、固定源码入口、学习路线、未执行练习、许可与贡献状态。

## 分类路线

- [Agents, Harness & Memory / 智能体与研究工作流](agents-and-memory/README.md)
- [RAG & Multimodal / 检索、文档与视频](retrieval-and-multimodal/README.md)
- [Models, Data & Evaluation / 研究实验底座](models-and-evaluation/README.md)

## 收录索引

| 项目 | 本仓库为何收录 | 档案 |
| --- | --- | --- |
| Transformers | 把模型接口接到可复现研究假设、生成设置和评估协议，不把一次生成当成结论。 | [阅读](models-and-evaluation/transformers.md) |
| Datasets | 维护研究样本来源和可复现切分，区分数据集许可与加载器代码许可。 | [阅读](models-and-evaluation/datasets.md) |
| Evaluate | 建立 baseline/candidate、固定 holdout 和评价协议；评估工具本身不保证统计有效性。 | [阅读](models-and-evaluation/evaluate.md) |
| LightRAG | 研究检索、知识组织、证据与回答质量的关系，结合实际 parser 贡献案例。 | [阅读](retrieval-and-multimodal/lightrag.md) |
| RAG-Anything | 研究跨模态 ingestion 与测量边界，先分析已公开的解析回归再扩展模型实验。 | [阅读](retrieval-and-multimodal/rag-anything.md) |
| VideoRAG | 把时间覆盖和证据时点作为多模态研究问题，连接已有 fractional-duration 案例。 | [阅读](retrieval-and-multimodal/videorag.md) |
| DeepTutor | 研究教学 Agent 的规划、工具、结构化响应和评估，避免以演示替代学习效果证据。 | [阅读](agents-and-memory/deeptutor.md) |
| AutoMemory | 研究 memory 的状态、来源、质量与改进 gate，保留真实 refine blocker 贡献线索。 | [阅读](agents-and-memory/automemory.md) |
| AutoSwarm | 作为多 Agent 编排候选研究对象，比较单 Agent baseline、交接可靠性和成本；不宣称本机联调成功。 | [阅读](agents-and-memory/autoswarm.md) |
| smolagents | 研究 tool use、执行边界和 baseline 评估，结合已有模型接口转发 PR。 | [阅读](agents-and-memory/smolagents.md) |
| HELIX | 研究 harness 组合、模型/环境协作与训练轨迹质量，关联已有公开文档契约修复。 | [阅读](agents-and-memory/helix.md) |
| DeepCode | 研究 research-to-code 的可复现交付与验证，而非把生成成功等同工程正确。 | [阅读](agents-and-memory/deepcode.md) |

## 怎么开始

先固定问题、baseline 和 holdout；再看 LightRAG / RAG-Anything / VideoRAG 的证据链；接着比较 smolagents / AutoSwarm / HELIX / DeepCode 的工具与交接；最后评价 memory / tutoring 的实际收益，而不是只看演示。

[学习与证据模板](HOW_TO_STUDY.md) · [机器可读来源与状态](catalog.json)。所有新模型/Agent/GPU/性能实验 **NOT RUN**；目录校验不是第三方软件验收，学习收益与性能改进 **UNMEASURED**。

## 权限和来源

只发布原创说明、公开元数据与链接，不镜像上游源码、许可证或模型。代码、模型权重和数据许可分开看；NOASSERTION/未识别不是免费复用授权。AutoMemory 如出现在本目录，许可未明确，仅作参考；VideoRAG 需核对组件和第三方模型条款。条目不代表官方合作或雇佣关系。

## 相关目录

- [P-ML / 模型与方法](https://github.com/pengpengyi92/P-ML/tree/main/ml-repo)
- [P-Research / AI 研究](https://github.com/pengpengyi92/p-research/tree/main/repo)
- [P-CSDSAI / AI 系统与数据](https://github.com/pengpengyi92/p-csdsai/tree/main/repo)

## Existing community guide

- [LLMQuant community and repository guide](llmquant.md) — the complete public inventory with access notes, suggested starting points, and how to contribute. [Discuss LLMQuant (#26)](https://github.com/pengpengyi92/p-research/discussions/26).

Propose an entry in [Repo Discussions](https://github.com/pengpengyi92/p-research/discussions/categories/repo) or submit a focused PR. Include a title, timestamp with timezone, primary public source or synthetic fixture, rights, and one concrete reason it is useful. See [AGENTS.md](../AGENTS.md).
