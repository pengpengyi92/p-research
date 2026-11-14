# AI Infra 七层能力体系：从 Linux/C++ 到可复现系统研究

**English title:** A Seven-Layer Research Framework for GPU-Native AI Infrastructure

**Public edition:** v0.1 · `2026-11-15T00:35:10+08:00`（Asia/Shanghai）

**Source:** P University · CSDSAI / Department of AI · Working Paper PAPER-CSDSAI-0006（2026-11-13）的选编公开版。

**Status:** Working paper · NOT PEER REVIEWED · EXPERIMENTS NOT RUN

> **Selected shared from P University**, an independent private proprietary research workspace. This public adaptation draws on the original work by Pengyi Peng（彭一）, with AI-assisted editing. The selected observation and experiment-design ideas from **PINF** and **P Compute (P-Compute)** come from private proprietary (prop) repositories. The originals and implementation remain private; no private repo access is needed.

## 摘要

一项 AI 系统优化如何穿过 CPU、GPU、推理服务、分布式通信和训练，最后变成更多可验证的产出？原工作论文提出 L1–L7，把能力、失效模式和验证证据放在同一张地图上。它是研究和学习框架，不是行业标准、职位等级或严格调用栈。存储、权限、可观测性、可靠性与成本横跨多层；L7 贯穿前六层。

## 七层能力与证据

| 层 | 主要对象和常见失效模式 | 可证伪的第一步 |
| --- | --- | --- |
| L1 · Linux/C++ Host Systems | 线程、所有权、内存、I/O、网络和回压；无限排队、重复完成、主机饥饿 | 同一到达/取消序列对照有界与无界队列；按逻辑 ID 验证唯一终态，量等待 p95 和峰值 RSS。 |
| L2 · GPU Programming and Memory | CUDA/Triton、warp、寄存器、shared memory、HBM；布局错误、隐式同步或内核发射开销 | 固定 dtype 与 shape，用 PyTorch 参考验证归约误差；有授权设备再记录 kernel 时间、带宽和内存。 |
| L3 · LLM Inference Serving | Prefill、decode、批处理、KV cache、admission；驱逐、长尾等待和短任务饥饿 | 对照 FCFS 和 cache-aware 策略；按负载类型比较 TTFT、TPOT、KV 驱逐和**满足 SLO 的有效请求/秒**。 |
| L4 · Distributed Execution | ranks、DP/TP/PP/EP、collectives 与拓扑；通信、慢 rank 和专家负载不均 | 固定总工作量，对比单卡与双卡的时间及每 rank 等待；没有真实拓扑就不宣称扩展性。 |
| L5 · Training Systems | Forward/backward、精度、分片、优化器、checkpoint；溢出、恢复偏差和数据顺序漂移 | 固定数据和有效 batch，比较 FP32 与混合精度；检查 loss、显存、恢复一致性及达到同一阈值的成本。 |
| L6 · RL/Rollout Infrastructure | actors、策略版本、轨迹完整性、learner；重复、过期、取消和交接丢失 | 同一轨迹对照 FCFS 与 freshness-aware，记录版本滞后和被 trainer 接受的有效新鲜轨迹/秒；不把它当成学习质量。 |
| L7 · Systems Research | 假设、对照、消融、复制；缓存、预热、随机性或选择性报告造成假收益 | 冻结版本、负载、种子、失败规则和主要指标，做重复与负对照；报告效应、不确定度和退化条件。 |

## 两个私有项目贡献的公开选段

- **PINF（prop repo）· 观测合同（selected shared）**：区分主机 RSS、固定页内存和设备显存；不要把 VRAM 的总占用解释为 KV cache。分开核对权重、激活、分配器保留、通信缓冲和 KV。按同一个 request/rollout ID 连起 CPU 排队、网络、GPU 时间线和训练交接，并记录采样开销。这里分享方法，不分享机器拓扑、遥测或部署。
- **P Compute / P-Compute（prop repo）· 对照与成本（selected shared）**：先用可分发的合成 trace 做 CPU 对照。统一按 `可归属总成本 / 被接收且通过验证的输出数` 计成本；没有有效输出时报告未定义和失败，而不是零成本。记录重试、存储、网络与操作开销；模型、设备和支出未经授权不启动。这里分享协议，不公开预算、内部实现或测量记录。

## 一个跨层实验：越快生成，越慢学习？

假设在长短混合流量中，缓存感知 admission 可以复用前缀。它也可能让长会话长期占用缓存、拖慢短请求；如果训练端频繁更新权重，更快生成也可能带来更多失效轨迹。原始 tokens/s 与有效学习输入可以方向相反。

1. **负载与基线**：预先冻结 4 类合成到达序列：短请求、长输入短输出、重复前缀、重尾多轮。固定 trace、服务时钟、缓存额度、输出预算、更新节奏；以 FCFS 为基线。
2. **干预与对照**：同一资源预算下分别打开缓存感知、版本新鲜度限制，再做两者组合。加入无前缀复用的负对照。生成策略版本和接收版本都要记录；跨版本轨迹记录分段版本。取消、失败、重复尝试及超时不要悄悄从逻辑 ID 账本消失。
3. **测量与判定**：预先设定短请求 p95、可接受策略滞后和正确性门槛；主指标为单位时间内被接受且满足完整性、新鲜度条件的轨迹数。另报生成吞吐、TTFT（请求发出到首 token）、TPOT（剩余输出的平均每 token 时间，单 token 无此值）、缓存压力、各组失败率和不确定度。实际学习质量必须另做训练后评估。
4. **可复现与外推**：记录 commit、workload 哈希、种子、预热、采样方式、版本、硬件和必要权限。把 CPU/模拟、单 GPU、集群和生产结果分别标记。模拟结果不能冒充 GPU 的毫秒数或租赁账单。

## 公开参考和研究边界

机制参考：[NVIDIA CUDA programming model](https://docs.nvidia.com/cuda/cuda-programming-guide/01-introduction/programming-model.html) · [vLLM latency definitions](https://docs.vllm.ai/en/latest/benchmarking/cli/) · [verl async trainer](https://verl.readthedocs.io/en/latest/advance/v1_async_trainer.html) · [MLCommons Inference rules](https://github.com/mlcommons/inference_policies/blob/master/inference_rules.adoc)。

完整内部原稿未发布；没有执行 GPU、训练或 RL 实验，不报告速度提升、质量改善或生产结论。下一步从固定 trace 和终态检查开始。另见[配套文章](article.md)和[七层公开仓库索引](../../repo/ai-infra/README.md)。
