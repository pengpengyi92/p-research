# VideoRAG / AudioRAG: Turn Video and Audio into Verifiable Research Material

Date: 2026-11-12 (Asia/Shanghai)
Category: Ideas
Status: Research proposal, not a released capability

<!-- PRESEARCH_VIDEORAG_AUDIO_20261112 -->

## 为什么关注这个方向

我们希望把视频、音频像论文和代码一样组织成可以学习、总结、追问和积累的知识资料。课程、技术分享和代码演示的信息不仅在说话内容里，也在画面、图表和操作的时间顺序里。

因此，我们关注的不是“生成一段看起来不错的文字”，而是：

> 总结能覆盖重要内容，答案能回到原始时间戳，缺失的证据能够诚实标记。

## 从哪些项目开始

- [HKUDS/VideoRAG](https://github.com/HKUDS/VideoRAG)：官方长视频 RAG 项目，包含算法和 Vimo 桌面端；[论文](https://arxiv.org/abs/2502.01549)。
- [HKUDS/RAG-Anything](https://github.com/HKUDS/RAG-Anything)：已有音视频处理入口，适合对照通用多模态接入。
- [Visually-aligned Video-RAG](https://github.com/Leon1207/Video-RAG-master)：比较 OCR / ASR 与视觉相关信息检索的路线。
- [starsuzi/VideoRAG](https://github.com/starsuzi/VideoRAG)：另一项同名工作，需要独立记录而非混淆成 HKUDS 实现。

以上只是初步研究入口，不是已复现的性能排名。HKUDS 实现的许可区分框架与第三方模型，集成 ImageBind 有非商业限制；中文效果、实际资源和成本也需要独立验证。参见[项目 LICENSE](https://github.com/HKUDS/VideoRAG/blob/main/LICENSE)及[算法说明](https://github.com/HKUDS/VideoRAG/blob/main/VideoRAG-algorithm/README.md)。

## 我们最关心的开放问题

1. **何时值得看画面？** 如果字幕就能回答，视觉模型是否增加了不必要的成本？哪些问题必须依靠图表、代码帧或演示动作？
2. **怎样做完整总结？** 检索 top-k 容易遗漏未命中的章节；分层总结如何保留覆盖率和可回看的原片段？
3. **怎样证明时间对齐正确？** ASR 分段、镜头切换、字幕偏移和视觉描述不同步，如何定位来源而不是给一个貌似精确的时间？
4. **怎样处理冲突和无答案？** 画面与口述不同、语音识别出错、原素材根本没有答案时，系统应如何提示而不是补全？
5. **怎样做有意义的评估？** 在相同媒体、问题与预算下，对比文本、文本加 OCR/帧、多模态检索；同时报告质量、覆盖、失败、延迟和实际费用。

## 一个克制的起步

先用一段有权处理的短视频，跑通“时间轴 → 文本基线 → 可回看引用”，再加入视觉信息做消融。纯音频必须能独立工作；整段总结与检索问答分别测。研究方法和合成样例可以公开，私人媒体和未经授权的内容不应上传。

欢迎有视频检索、音频理解、多模态评估经验的贡献者分享失败样例和可重复实验建议。讨论不预设必须使用某个模型，也不预设更复杂的系统就更好。

当前只立项与调研，没有启动付费调用、模型下载、视频上传或部署；执行清单另由配套研究 Issue 跟踪。

## Live Tracking

- Research Issue: https://github.com/pengpengyi92/p-research/issues/22
- Ideas Discussion: https://github.com/pengpengyi92/p-research/discussions/23
