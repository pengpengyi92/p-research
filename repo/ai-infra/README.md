# AI Infra L1–L7 · 研究问题、可证伪假设与对照实验

**P-Research · 公共目录 v0.1** · 核对时间：`2026-11-15T00:35:10+08:00`（Asia/Shanghai）。

[Working paper](../../paper/ai-infra/working-paper.md) · [配套文章](../../paper/ai-infra/article.md) · [机器可读目录](catalog.json)

**Selected shared from P University.** 七层框架来自 P University（独立私有研究项目）；跨层观测和实验/成本准则分别选编自 PINF 与 P Compute（两者均为 private prop repo）。本目录的代码入口来自下列公开上游。L7 横跨前六层；每个仓库只分到一个**主要阅读入口**，不是完整用途或性能排名。

**范围：** 28 个公开仓库，每层 4 个。每个项目给出已核对的固定提交、README、真实入口与许可文件。研究提议均 **NOT RUN**，性能和收益 **UNMEASURED**；无上游代码、数据和模型镜像，无新的上游 PR。代码许可不能授权模型权重、数据、外部服务或第三方组件。

## L1 — Linux/C++ Host Systems · 主机、并发与网络

| 公开仓库 / 固定版本 | 研究问题或实验对照 | 源码与许可 |
| --- | --- | --- |
| [libuv/libuv](https://github.com/libuv/libuv/blob/fc7475a4dd8144e3eda0bf103892d774d1b675e1/README.md) | 用固定的 I/O 到达和取消序列，比较同步轮询与事件循环的排队时延；检查停止后是否有晚到回调。 | [主要入口](https://github.com/libuv/libuv/blob/fc7475a4dd8144e3eda0bf103892d774d1b675e1/src/unix/core.c) · [入口 2](https://github.com/libuv/libuv/blob/fc7475a4dd8144e3eda0bf103892d774d1b675e1/docs/src/design.rst) · [许可](https://github.com/libuv/libuv/blob/fc7475a4dd8144e3eda0bf103892d774d1b675e1/LICENSE)：MIT |
| [abseil/abseil-cpp](https://github.com/abseil/abseil-cpp/blob/be93ce230ef75c5e57366c500e71cac4f4f4241a/README.md) | 把互斥方案作为单变量，比较读写混合下的尾部等待；先验证输出一致、无丢任务。 | [主要入口](https://github.com/abseil/abseil-cpp/blob/be93ce230ef75c5e57366c500e71cac4f4f4241a/absl/synchronization/mutex.h) · [许可](https://github.com/abseil/abseil-cpp/blob/be93ce230ef75c5e57366c500e71cac4f4f4241a/LICENSE)：Apache-2.0 |
| [scylladb/seastar](https://github.com/scylladb/seastar/blob/04b1c04dcd056d9d9b276ea5c42c9687bc834493/README.md) | 对相同到达序列比较每核隔离与共享队列的负载偏斜，记录慢核和过载行为。 | [主要入口](https://github.com/scylladb/seastar/blob/04b1c04dcd056d9d9b276ea5c42c9687bc834493/include/seastar/core/reactor.hh) · [许可](https://github.com/scylladb/seastar/blob/04b1c04dcd056d9d9b276ea5c42c9687bc834493/LICENSE)：Apache-2.0 |
| [meta/folly](https://github.com/meta/folly/blob/9450293598dfa14aa1716cc1fb494d54076ffa87/README.md) | 控制 worker 数量与队列上限，记录小任务是否被长任务拖住及拒绝率。 | [主要入口](https://github.com/meta/folly/blob/9450293598dfa14aa1716cc1fb494d54076ffa87/folly/executors/CPUThreadPoolExecutor.h) · [许可](https://github.com/meta/folly/blob/9450293598dfa14aa1716cc1fb494d54076ffa87/LICENSE)：Apache-2.0 |

## L2 — GPU Programming and Memory · GPU 内核与显存

| 公开仓库 / 固定版本 | 研究问题或实验对照 | 源码与许可 |
| --- | --- | --- |
| [triton-lang/triton](https://github.com/triton-lang/triton/blob/1c53e566ef8f719ff9b69132a72ad943e5409492/README.md) | 用同一 dtype 扫非整倍数形状，对照 PyTorch eager 的误差、预热后延迟与显存搬运。 | [主要入口](https://github.com/triton-lang/triton/blob/1c53e566ef8f719ff9b69132a72ad943e5409492/python/tutorials/02-fused-softmax.py) · [许可](https://github.com/triton-lang/triton/blob/1c53e566ef8f719ff9b69132a72ad943e5409492/LICENSE)：MIT |
| [NVIDIA/cutlass](https://github.com/NVIDIA/cutlass/blob/b2f249acd20392beeb16f5e5a31f4f1a4e38b3bd/README.md) | 固定 GEMM 的数学操作，把 tile/layout 当单变量；比较吞吐前先固定输入、累加精度和容差。 | [主要入口](https://github.com/NVIDIA/cutlass/blob/b2f249acd20392beeb16f5e5a31f4f1a4e38b3bd/include/cutlass/gemm/gemm.h) · [入口 2](https://github.com/NVIDIA/cutlass/blob/b2f249acd20392beeb16f5e5a31f4f1a4e38b3bd/examples/00_basic_gemm/basic_gemm.cu) · [许可](https://github.com/NVIDIA/cutlass/blob/b2f249acd20392beeb16f5e5a31f4f1a4e38b3bd/LICENSE.txt)：BSD-3-Clause（根许可含 SPDX 声明） |
| [Dao-AILab/flash-attention](https://github.com/Dao-AILab/flash-attention/blob/f63c472c4dc19237c0635d6a629df065ff64796e/README.md) | 对照普通 attention，在固定 mask、序列长度和 dtype 下分别量 forward 与 backward，中短长度也要测。 | [主要入口](https://github.com/Dao-AILab/flash-attention/blob/f63c472c4dc19237c0635d6a629df065ff64796e/tests/test_flash_attn.py) · [入口 2](https://github.com/Dao-AILab/flash-attention/blob/f63c472c4dc19237c0635d6a629df065ff64796e/flash_attn/flash_attn_interface.py) · [许可](https://github.com/Dao-AILab/flash-attention/blob/f63c472c4dc19237c0635d6a629df065ff64796e/LICENSE)：BSD-3-Clause |
| [flashinfer-ai/flashinfer](https://github.com/flashinfer-ai/flashinfer/blob/9c50996794564e1e3b2a4b0683e9aa2bcc528df8/README.md) | 拆开 prefill 和 decode，用短/长上下文和相同预算找哪一段贡献 p95 改变。 | [主要入口](https://github.com/flashinfer-ai/flashinfer/blob/9c50996794564e1e3b2a4b0683e9aa2bcc528df8/flashinfer/decode.py) · [入口 2](https://github.com/flashinfer-ai/flashinfer/blob/9c50996794564e1e3b2a4b0683e9aa2bcc528df8/flashinfer/prefill.py) · [许可](https://github.com/flashinfer-ai/flashinfer/blob/9c50996794564e1e3b2a4b0683e9aa2bcc528df8/LICENSE)：Apache-2.0 |

## L3 — LLM Inference Serving · 推理调度与 KV Cache

| 公开仓库 / 固定版本 | 研究问题或实验对照 | 源码与许可 |
| --- | --- | --- |
| [vllm-project/vllm](https://github.com/vllm-project/vllm/blob/d2f92859b4c62434a2c111036ebe62cb0e9de243/README.md) | 冻结请求到达、模型和采样；比较两种 admission 设置的 SLO goodput、短请求 p95 与 KV 驱逐。 | [主要入口](https://github.com/vllm-project/vllm/blob/d2f92859b4c62434a2c111036ebe62cb0e9de243/vllm/v1/core/sched/scheduler.py) · [入口 2](https://github.com/vllm-project/vllm/blob/d2f92859b4c62434a2c111036ebe62cb0e9de243/vllm/benchmarks/serve.py) · [许可](https://github.com/vllm-project/vllm/blob/d2f92859b4c62434a2c111036ebe62cb0e9de243/LICENSE)：Apache-2.0 |
| [sgl-project/sglang](https://github.com/sgl-project/sglang/blob/6de483b326c7dd4145fde06afcac9866bf491024/README.md) | 用高复用 trace 和低复用负对照检验 cache-aware 的收益是否只在某类工作负载成立。 | [主要入口](https://github.com/sgl-project/sglang/blob/6de483b326c7dd4145fde06afcac9866bf491024/python/sglang/srt/mem_cache/radix_cache.py) · [许可](https://github.com/sgl-project/sglang/blob/6de483b326c7dd4145fde06afcac9866bf491024/LICENSE)：Apache-2.0 |
| [NVIDIA/TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM/blob/178ec0b5ba77813c0fa13e358d484e2136150dd0/README.md) | 对相同模型和设备，区分 batch/engine 配置的影响；无法匹配权重或精度就不做速度排名。 | [主要入口](https://github.com/NVIDIA/TensorRT-LLM/blob/178ec0b5ba77813c0fa13e358d484e2136150dd0/tensorrt_llm/_torch/pyexecutor/py_executor.py) · [许可](https://github.com/NVIDIA/TensorRT-LLM/blob/178ec0b5ba77813c0fa13e358d484e2136150dd0/LICENSE)：Apache-2.0 主体；含不同条款组件 |
| [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp/blob/3549c274dc22001d9118713fa56a10085b85de3b/README.md) | 作为低资源本地对照，固定量化文件和功能；把不同精度的质量差异与延迟分开。 | [主要入口](https://github.com/ggml-org/llama.cpp/blob/3549c274dc22001d9118713fa56a10085b85de3b/tools/server/README.md) · [入口 2](https://github.com/ggml-org/llama.cpp/blob/3549c274dc22001d9118713fa56a10085b85de3b/tools/server/server-context.cpp) · [许可](https://github.com/ggml-org/llama.cpp/blob/3549c274dc22001d9118713fa56a10085b85de3b/LICENSE)：MIT |

## L4 — Distributed Execution · 分布式执行与通信

| 公开仓库 / 固定版本 | 研究问题或实验对照 | 源码与许可 |
| --- | --- | --- |
| [NVIDIA/nccl](https://github.com/NVIDIA/nccl/blob/ad2d192c1f279aefcaf340f67e07880b65a1116b/README.md) | 固定总工作量和拓扑，扫 collective 消息大小；区分计算速度和最慢 rank 的通信等待。 | [主要入口](https://github.com/NVIDIA/nccl/blob/ad2d192c1f279aefcaf340f67e07880b65a1116b/src/collectives.cc) · [许可](https://github.com/NVIDIA/nccl/blob/ad2d192c1f279aefcaf340f67e07880b65a1116b/LICENSE.txt)：Apache-2.0 为主；部分 BSD/独立许可 |
| [ray-project/ray](https://github.com/ray-project/ray/blob/8957070d042006b416d89c02e9c607fa850c1dd9/README.md) | 比较相同资源配额下不同任务粒度，统计任务失败、重启和有效处理量。 | [主要入口](https://github.com/ray-project/ray/blob/8957070d042006b416d89c02e9c607fa850c1dd9/python/ray/train/torch/torch_trainer.py) · [入口 2](https://github.com/ray-project/ray/blob/8957070d042006b416d89c02e9c607fa850c1dd9/python/ray/_private/worker.py) · [许可](https://github.com/ray-project/ray/blob/8957070d042006b416d89c02e9c607fa850c1dd9/LICENSE)：Apache-2.0 |
| [deepseek-ai/DeepEP](https://github.com/deepseek-ai/DeepEP/blob/f6aa38fe06cd4a0489e7730365d4e0114970a2f3/README.md) | 控制 token-to-expert 分配，加入偏斜负对照；拆开 dispatch/combine 的通信与计算。 | [主要入口](https://github.com/deepseek-ai/DeepEP/blob/f6aa38fe06cd4a0489e7730365d4e0114970a2f3/deep_ep/__init__.py) · [入口 2](https://github.com/deepseek-ai/DeepEP/blob/f6aa38fe06cd4a0489e7730365d4e0114970a2f3/csrc/CMakeLists.txt) · [许可](https://github.com/deepseek-ai/DeepEP/blob/f6aa38fe06cd4a0489e7730365d4e0114970a2f3/LICENSE)：MIT |
| [open-mpi/ompi](https://github.com/open-mpi/ompi/blob/f7e4bd34f113f09930ab3272e97cc49c5021d8be/README.md) | 先用 CPU rank 验证相同消息量下延迟曲线；不把 MPI 数字当 NCCL 或 GPU 结果。 | [主要入口](https://github.com/open-mpi/ompi/blob/f7e4bd34f113f09930ab3272e97cc49c5021d8be/ompi/mca/coll/base/coll_base_allreduce.c) · [许可](https://github.com/open-mpi/ompi/blob/f7e4bd34f113f09930ab3272e97cc49c5021d8be/LICENSE)：NOASSERTION；按固定 LICENSE / 文件核对 |

## L5 — Training Systems · 训练、精度与恢复

| 公开仓库 / 固定版本 | 研究问题或实验对照 | 源码与许可 |
| --- | --- | --- |
| [pytorch/pytorch](https://github.com/pytorch/pytorch/blob/e63b330cbcbcc136d3aab1895a183579dbb80dde/README.md) | 用固定小模型比较 FP32 与 AMP；算到同一质量阈值的时间/显存并验证恢复后的数据顺序。 | [主要入口](https://github.com/pytorch/pytorch/blob/e63b330cbcbcc136d3aab1895a183579dbb80dde/torch/distributed/fsdp/fully_sharded_data_parallel.py) · [入口 2](https://github.com/pytorch/pytorch/blob/e63b330cbcbcc136d3aab1895a183579dbb80dde/torch/amp/autocast_mode.py) · [许可](https://github.com/pytorch/pytorch/blob/e63b330cbcbcc136d3aab1895a183579dbb80dde/LICENSE)：NOASSERTION；根 LICENSE 含多方条款 |
| [NVIDIA/Megatron-LM](https://github.com/NVIDIA/Megatron-LM/blob/154e7bd2f5117c745ad0a24937a576a7fae5e904/README.md) | 固定数据、有效 batch 和模型，研究不同并行切分对 step latency 和收敛的影响。 | [主要入口](https://github.com/NVIDIA/Megatron-LM/blob/154e7bd2f5117c745ad0a24937a576a7fae5e904/megatron/core/optimizer/optimizer.py) · [入口 2](https://github.com/NVIDIA/Megatron-LM/blob/154e7bd2f5117c745ad0a24937a576a7fae5e904/megatron/training/training.py) · [许可](https://github.com/NVIDIA/Megatron-LM/blob/154e7bd2f5117c745ad0a24937a576a7fae5e904/LICENSE)：NOASSERTION；按固定 LICENSE / 文件核对 |
| [deepspeedai/DeepSpeed](https://github.com/deepspeedai/DeepSpeed/blob/7d30f9207aba6bfc14821bc735b316b173fbdef8/README.md) | 对照相同优化器和质量门槛，拆解 ZeRO 分片或 offload 的内存与通信开销。 | [主要入口](https://github.com/deepspeedai/DeepSpeed/blob/7d30f9207aba6bfc14821bc735b316b173fbdef8/deepspeed/runtime/engine.py) · [入口 2](https://github.com/deepspeedai/DeepSpeed/blob/7d30f9207aba6bfc14821bc735b316b173fbdef8/deepspeed/runtime/zero/stage3.py) · [许可](https://github.com/deepspeedai/DeepSpeed/blob/7d30f9207aba6bfc14821bc735b316b173fbdef8/LICENSE)：Apache-2.0 |
| [pytorch/torchtitan](https://github.com/pytorch/torchtitan/blob/631d544b1f6794ecfeca734a7bba861e03ddd5e3/README.md) | 用小规模训练实验验证配置保持不变时，重新启动是否再现相同检查点和训练进度。 | [主要入口](https://github.com/pytorch/torchtitan/blob/631d544b1f6794ecfeca734a7bba861e03ddd5e3/torchtitan/train.py) · [许可](https://github.com/pytorch/torchtitan/blob/631d544b1f6794ecfeca734a7bba861e03ddd5e3/LICENSE)：BSD-3-Clause |

## L6 — RL/Rollout Infrastructure · 策略、轨迹与编排

| 公开仓库 / 固定版本 | 研究问题或实验对照 | 源码与许可 |
| --- | --- | --- |
| [verl-project/verl](https://github.com/verl-project/verl/blob/4191e7f910d85d69acb8c45f4840f10faa535165/README.md) | 固定策略更新时间和长短 rollout 混合负载，比较异步对有效新鲜轨迹率与学习质量的不同影响。 | [主要入口](https://github.com/verl-project/verl/blob/4191e7f910d85d69acb8c45f4840f10faa535165/docs/advance/fully_async.md) · [入口 2](https://github.com/verl-project/verl/blob/4191e7f910d85d69acb8c45f4840f10faa535165/verl/trainer/ppo/ray_trainer.py) · [许可](https://github.com/verl-project/verl/blob/4191e7f910d85d69acb8c45f4840f10faa535165/LICENSE)：Apache-2.0 |
| [OpenRLHF/OpenRLHF](https://github.com/OpenRLHF/OpenRLHF/blob/26494490bc237f6c3af62dab6117e6bbb0a78dba/README.md) | 在相同 reward、模型和硬件约束下，对照并行生成的容量与有效样本率，不拿 raw tok/s 代替。 | [主要入口](https://github.com/OpenRLHF/OpenRLHF/blob/26494490bc237f6c3af62dab6117e6bbb0a78dba/openrlhf/trainer/ray/ppo_actor.py) · [入口 2](https://github.com/OpenRLHF/OpenRLHF/blob/26494490bc237f6c3af62dab6117e6bbb0a78dba/openrlhf/cli/train_ppo_ray.py) · [许可](https://github.com/OpenRLHF/OpenRLHF/blob/26494490bc237f6c3af62dab6117e6bbb0a78dba/LICENSE)：Apache-2.0 |
| [huggingface/trl](https://github.com/huggingface/trl/blob/8ad18ec1b6493b85cf9fffbd87d376767ceb8611/README.md) | 用同批 prompts 和固定评分比较 GRPO 配置，记录被过滤样本与有效分母。 | [主要入口](https://github.com/huggingface/trl/blob/8ad18ec1b6493b85cf9fffbd87d376767ceb8611/trl/trainer/grpo_trainer.py) · [入口 2](https://github.com/huggingface/trl/blob/8ad18ec1b6493b85cf9fffbd87d376767ceb8611/docs/source/grpo_trainer.md) · [许可](https://github.com/huggingface/trl/blob/8ad18ec1b6493b85cf9fffbd87d376767ceb8611/LICENSE)：Apache-2.0 |
| [areal-project/AReaL](https://github.com/areal-project/AReaL/blob/11b6fb0ca9ea47a55e2fc3929c24b8d43693fd80/README.md) | 预注册可接受 policy lag，比较不同长尾占比下的新鲜度、样本利用率和学习指标。 | [主要入口](https://github.com/areal-project/AReaL/blob/11b6fb0ca9ea47a55e2fc3929c24b8d43693fd80/areal/trainer/rl_trainer.py) · [许可](https://github.com/areal-project/AReaL/blob/11b6fb0ca9ea47a55e2fc3929c24b8d43693fd80/LICENSE)：Apache-2.0 |

## L7 — Systems Research · 评测、测量与复现

| 公开仓库 / 固定版本 | 研究问题或实验对照 | 源码与许可 |
| --- | --- | --- |
| [mlcommons/inference](https://github.com/mlcommons/inference/blob/3fbc329939999c13d0a7b5e67fb2092287e06047/README.md) | 借 LoadGen 约束工作负载和测量窗口；把自定义测量与正式 MLPerf 结果分开标注。 | [主要入口](https://github.com/mlcommons/inference/blob/3fbc329939999c13d0a7b5e67fb2092287e06047/loadgen/README.md) · [入口 2](https://github.com/mlcommons/inference/blob/3fbc329939999c13d0a7b5e67fb2092287e06047/loadgen/loadgen.cc) · [许可](https://github.com/mlcommons/inference/blob/3fbc329939999c13d0a7b5e67fb2092287e06047/LICENSE.md)：Apache-2.0 |
| [EleutherAI/lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness/blob/d6de81643928d653435c431bae19945d41d32520/README.md) | 冻结任务样本和生成设置；先跑模型/评估器版本不变的重复对照以发现评分漂移。 | [主要入口](https://github.com/EleutherAI/lm-evaluation-harness/blob/d6de81643928d653435c431bae19945d41d32520/lm_eval/evaluator.py) · [许可](https://github.com/EleutherAI/lm-evaluation-harness/blob/d6de81643928d653435c431bae19945d41d32520/LICENSE.md)：MIT |
| [google/benchmark](https://github.com/google/benchmark/blob/cf4d7fedd59473f99042806fcba407ea767c5327/README.md) | 给 CPU 微基准设计负对照与多次独立运行，检验预热和编译器是否解释所谓提速。 | [主要入口](https://github.com/google/benchmark/blob/cf4d7fedd59473f99042806fcba407ea767c5327/docs/user_guide.md) · [入口 2](https://github.com/google/benchmark/blob/cf4d7fedd59473f99042806fcba407ea767c5327/src/benchmark_runner.cc) · [许可](https://github.com/google/benchmark/blob/cf4d7fedd59473f99042806fcba407ea767c5327/LICENSE)：Apache-2.0 |
| [open-telemetry/opentelemetry-collector](https://github.com/open-telemetry/opentelemetry-collector/blob/572057cde7e9bbe3aed6e5e3e8f16290d487f7d0/README.md) | 以开/关采样作对照，量化 tracing 对尾延迟和丢事件的影响。 | [主要入口](https://github.com/open-telemetry/opentelemetry-collector/blob/572057cde7e9bbe3aed6e5e3e8f16290d487f7d0/receiver/README.md) · [入口 2](https://github.com/open-telemetry/opentelemetry-collector/blob/572057cde7e9bbe3aed6e5e3e8f16290d487f7d0/processor/README.md) · [入口 3](https://github.com/open-telemetry/opentelemetry-collector/blob/572057cde7e9bbe3aed6e5e3e8f16290d487f7d0/service/service.go) · [许可](https://github.com/open-telemetry/opentelemetry-collector/blob/572057cde7e9bbe3aed6e5e3e8f16290d487f7d0/LICENSE)：Apache-2.0 |

## 怎么贡献

欢迎提交失败复现、负对照和可预注册假设。请附 commit、固定 workload、baseline、指标与失败判据。 讨论先找已有话题：[Paper Discussions](https://github.com/pengpengyi92/p-research/discussions/categories/paper) · [Repo Discussions](https://github.com/pengpengyi92/p-research/discussions/categories/repo)。附标题和时间戳；不要运行未授权的云/GPU 作业。
