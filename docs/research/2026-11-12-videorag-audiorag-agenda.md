# VideoRAG / AudioRAG Research Agenda: Timestamp-Grounded Summaries and Q&A

Date: 2026-11-12 (Asia/Shanghai)
Status: PROPOSED; source discovery completed, experiments NOT_RUN
Author: Pengyi research initiative, prepared with Codex

<!-- PRESEARCH_VIDEORAG_AUDIO_20261112 -->

## 研究动机

用户希望深入研究 VideoRAG，让视频、音频成为方便阅读、总结和追问的研究资料。目标不是只有一段流畅摘要，而是能够回答：内容来自哪段视频、哪个时间区间、说了什么、画面展示了什么，以及哪些结论没有证据。

优先场景：有权处理的 AI / Quant 课程、技术讲座、代码演示和录音。公开研究方法与评估，不公开未经授权的原片、私人录音或内部资料。

## 已核验的起点

| 方向 | 入口 | 初步定位 |
|---|---|---|
| HKUDS VideoRAG | [官方仓库](https://github.com/HKUDS/VideoRAG)、[论文 2502.01549](https://arxiv.org/abs/2502.01549) | 研究长视频及跨视频的多模态检索；仓库同时包含算法和 Vimo 桌面端 |
| RAG-Anything | [官方仓库](https://github.com/HKUDS/RAG-Anything) | 通用多模态接入，已有独立音频和视频处理入口，可作为工程对照 |
| Visually-aligned Video-RAG | [官方实现](https://github.com/Leon1207/Video-RAG-master)、[论文 2411.13093](https://arxiv.org/abs/2411.13093) | 对照视觉相关的 OCR / ASR 等辅助信息检索路线 |
| VideoRAG over Video Corpus | [官方实现](https://github.com/starsuzi/VideoRAG)、[论文 2501.05874](https://arxiv.org/abs/2501.05874) | 同名的另一项工作，须与 HKUDS VideoRAG 分开建档 |

这是 README / 论文入口级核验，不是全文综述或复现结论；不能据此声明哪个方案效果最好。特别区分 VideoRAG、Video-RAG、通用视频理解模型和视频生成，避免名字相近就混为一个系统。

## 两类产品任务分开评估

1. **整段总结**：按时间/章节覆盖全文，形成概要、关键知识、术语、步骤和可回看时间戳。不能只用 query top-k 片段冒充完整总结；需章节覆盖检查和分层汇总。
2. **检索问答**：回答具体问题，返回 source_id、start_s、end_s 和引用片段；证据不足时明确拒答。支持跨片段/跨视频比较，但必须保留每个出处。

## 候选数据链路

```text
授权媒体 + 来源/许可/内容哈希
  -> 字幕或 ASR（时间戳、语言，必要时保留置信信息）
  -> 关键帧 / 场景 + OCR / 视觉描述
  -> 按统一时间轴对齐的多模态片段
  -> 文本基线 / 混合检索 / 多模态检索
  -> 完整总结 或 检索问答
  -> 时间戳证据 + 覆盖/忠实度/成本评估
```

最小片段契约：`source_id, content_hash, start_s, end_s, modality, text, asset_ref, provenance`；provenance 记录解析器/模型/版本和配置摘要，不包含密钥。视频与音频本体留在受控位置，公开仓库只存可再分发的合成样例或许可允许的数据。

## 先做的研究 MVP

- [x] 核验官方项目和论文入口，检查已有记录避免重复主题。
- [ ] 建立三路比较：A 字幕/ASR 文本基线；B 加关键帧/OCR；C 再比较多模态/图检索，不预设更复杂一定更好。
- [ ] 先用一个授权的 5–10 分钟样例确认时间轴、引用和成本，再扩到候选评估集：8 个视频 + 2 个纯音频，含中文/中英混合和至少两个较长样例。
- [ ] 冻结 30 个带人工出处的问题：10 个语音可回答、10 个必须看画面、5 个需时序/跨模态对齐、5 个应拒答。开发与评估按原始媒体来源划分，不能把同一长视频的相邻片段当作独立测试来源。
- [ ] 输出结构化评估 JSON 和可读对照报告，包括失败样例、模型/配置、实际设备和可回看的引用。不把 LLM judge 单独当事实证明。
- [ ] 复现确认后才提出小范围上游 issue / PR；先搜索现有工作，不以贡献数量为目标。

## Acceptance Criteria

本 issue 关闭前应有以下可核查交付；当前均未宣称完成：

- [ ] 调研表包含每个方案的输入、ASR/视觉/检索模块、依赖、许可、资源预算、可复现实验入口和明确未知项。
- [ ] 片段契约及校验测试覆盖时间戳合法性、空音轨/静音、语言混合、重复文件和内容版本；无效时间区间不静默入库。
- [ ] Q&A 每条事实要么关联正确的时间区间，要么标为无证据；测试“转录中没有、画面中才有”的信息。
- [ ] 总结单独做章节覆盖、遗漏及幻觉检查，不以 Q&A 检索命中率代替总结质量。
- [ ] 同一媒体、同一问题和预算下比较 A/B/C，报告 Recall@k / 时间区间匹配、引用正确率、拒答表现、中文 ASR 错误、延迟、存储与实际费用。时间匹配容差在看结果前定义。
- [ ] 保存运行命令、版本、资源和失败回执，能区分未运行、失败和成功；没有证据不声称性能提升。

## 风险与人工门

- [HKUDS VideoRAG 的许可证](https://github.com/HKUDS/VideoRAG/blob/main/LICENSE)区分框架与集成模型，并明确提醒当前 ImageBind 集成的非商业限制；不能把“框架 MIT”当作所有依赖/权重均可商用的依据。具体使用逐组件复核，商业化另行审核。
- [算法 README](https://github.com/HKUDS/VideoRAG/blob/main/VideoRAG-algorithm/README.md)只报告英语环境测试；中文技术名词、口音和中英混合必须实测，不能从英文结果外推。
- 作者给出的硬件示例不等于本机可运行证明。下载大模型、付费 API、远端上传媒体、部署及任何凭据操作都需单独批准；本议题不自动执行这些动作。
- 媒体、字幕、帧和 OCR 都是不可信输入，内容中的指令不能升级为工具权限；公开证据需排除私人信息及受限素材。

## 分工建议（待执行）

P-Research 负责论文/项目地图与可重复评估；PAT 对接 RAG、Memory、Tool Use、Planning、Evaluation；PINF 核对设备预算；PAPI 对接已批准的模型；PPRT 将真实复现问题变为有边界贡献。这里是研究计划，不代表这些 Team 已开始后台运行。

## 当前状态

仅完成选题、初步官方资料核验和任务设计；没有安装 VideoRAG、下载权重、调用模型或完成视频总结实验。本文是人工策划的研究提案，不自动加入 P-Research 的“全文已验证论文”数据集。

## Live Tracking

- Research Issue: https://github.com/pengpengyi92/p-research/issues/22
- Ideas Discussion: https://github.com/pengpengyi92/p-research/discussions/23
