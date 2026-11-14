# GPU 还有空闲，为什么 Agent 还是这么慢？

**Public article** · `2026-11-15T00:35:10+08:00`（Asia/Shanghai）

**Source:** P University · CSDSAI / Department of AI · Working Article ARTICLE-CSDSAI-014（2026-11-13）的选编公开版，按配套工作论文的七层框架重新编排。**无新实测，不是同行评审文章。**

> **Selected shared from P University**, an independent private proprietary research workspace. This public adaptation draws on the original work by Pengyi Peng（彭一）, with AI-assisted editing. The selected observation and experiment-design ideas from **PINF** and **P Compute (P-Compute)** come from private proprietary (prop) repositories. The originals and implementation remain private; no private repo access is needed.

想象一个多轮 Agent 服务：GPU 利用率看起来不高，短请求却排得越来越久；后台还在收长轨迹，有些生成完才发现策略版本已经过期。先不用下结论说「GPU 不够」。从请求的生命周期追一遍：

1. **L1 主机：先看谁在等。** Python/C++ 线程是不是堵住了？队列有没有上限？同一个请求超时重试，是不是回调了两次？
2. **L2 GPU：再看设备在忙什么。** 是算术、HBM 搬运、同步，还是 kernel 一直在等 CPU 发出指令？看时间线和数值正确性，不只看显存占用截图。
3. **L3 推理：区分首 token 和后续速度。** 看 prefill、decode、batch 和 KV cache。重复前缀能省计算，但用缓存让长会话驻留，也可能挤掉短请求。
4. **L4 分布式：加一张卡不一定更快。** 模型切分后，最慢 rank、通信和专家负载可能决定全局时钟。
5. **L5 训练：快了也要能恢复。** 混合精度或更大的有效 batch 值不值，要看固定数据上的 loss、显存与 checkpoint 恢复。
6. **L6 Rollout：生成不等于被用上。** 把 rollout ID 和策略版本跟到 trainer。过期、重复、超时、丢失，都会让看起来漂亮的 tokens/s 变成零有效输入的一部分。
7. **L7 研究：让别人能推翻你。** 固定负载、基线和判定线，公布好坏两档结果。L7 不是最后补一张图，它从你定义指标时就开始了。

## 第一个周末可以做什么？

不用先租 GPU。做一个小队列模拟：混入短请求、重复前缀和长尾负载，固定 arrival trace，对比 FIFO 和一种缓存友好的策略。第一关不是跑快，而是**每个逻辑 ID 只出现一个终态**；第二关才是看短请求 p95 和有效完成数是否一起改善。两个候选策略也可以各自只在某一种负载下占优——那就把边界写清楚。

**PINF（私有 prop repo）**选编的是「从主机到设备的观测边界」；**P Compute / P-Compute（私有 prop repo）**选编的是「同一负载做对照、按被验证的产出算成本」。我们分享这两点的原因很简单：指标能回答问题，比工具栈更长更重要。

阅读下一站：[七层 working paper](working-paper.md) · [每层四个公开仓库](../../repo/ai-infra/README.md)。欢迎带一个小复现、一个失败用例，或一个更公平的控制组来讨论。
