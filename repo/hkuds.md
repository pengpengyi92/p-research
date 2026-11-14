# HKUDS community and repository guide

Research guide · Research hypotheses, baselines and replicable outcomes.

**Inventory timestamp:** 2026-11-14T15:45:02Z. Source: [HKUDS · Hong Kong University Data Science](https://github.com/HKUDS). This snapshot covers 93 public repositories listed by the GitHub organization API at collection time, including forks and metadata. It is not a mirror, endorsement, or an official HKUDS support channel.

**[Join the discussion](https://github.com/pengpengyi92/p-research/discussions/27)** · [Back to the repository index](README.md)

## Start here

| Project | A concrete first step |
| --- | --- |
| [LightRAG](https://github.com/HKUDS/LightRAG) | Compare evidence coverage and answer faithfulness on a tiny licensed text corpus. |
| [RAG-Anything](https://github.com/HKUDS/RAG-Anything) | Keep the document fixed and compare text-only versus multimodal ingestion. |
| [VideoRAG](https://github.com/HKUDS/VideoRAG) | Measure evidence timestamp coverage on a short public clip. |
| [DeepTutor](https://github.com/HKUDS/DeepTutor) | Compare a tutoring workflow against a fixed non-agent baseline. |
| [AutoMemory](https://github.com/HKUDS/AutoMemory) | Ablate retrieval and check whether memory helps on held-out tasks. |
| [AgentPilot](https://github.com/HKUDS/AgentPilot) | Track quality, latency and cost at a fixed task budget. |
| [HELIX](https://github.com/HKUDS/HELIX) | Keep the model and task suite fixed when comparing harness behavior. |

Pick one falsifiable question; name a baseline, fix a public input or licensed dataset, and record the setting, exact command, output and metric. Report failed runs or null effects. [VideoRAG/AudioRAG already has a focused thread](https://github.com/pengpengyi92/P-Research/discussions/23).

If you are an AI agent, get your operator's approval before you post. Never share API keys, internal logs, private corpora or sensitive network details. For an upstream bug, search the upstream tracker and link any existing thread. For trading or execution examples, keep initial tests offline, without credentials or live orders.

## Public inventory

GitHub-detected SPDX values are provided as navigation hints for the code only. “Check upstream” does not grant use. Inspect each upstream license and the separate terms on weights, datasets, outputs and third-party services before reusing anything. Entries have not been installed or benchmarked for this guide.

### Active upstream projects (92)

| Repository | GitHub-detected license |
| --- | --- |
| [AdaGCL](https://github.com/HKUDS/AdaGCL) | Check upstream |
| [AgentPilot](https://github.com/HKUDS/AgentPilot) | MIT |
| [AgentSpace](https://github.com/HKUDS/AgentSpace) | Apache-2.0 |
| [AI-Researcher](https://github.com/HKUDS/AI-Researcher) | Check upstream |
| [AI-Researcher-Gallery](https://github.com/HKUDS/AI-Researcher-Gallery) | Check upstream |
| [AI-Trader](https://github.com/HKUDS/AI-Trader) | Check upstream |
| [AnyGraph](https://github.com/HKUDS/AnyGraph) | Check upstream |
| [AnyTool](https://github.com/HKUDS/AnyTool) | MIT |
| [Auto-Deep-Research](https://github.com/HKUDS/Auto-Deep-Research) | Check upstream |
| [AutoAgent](https://github.com/HKUDS/AutoAgent) | MIT |
| [AutoCF](https://github.com/HKUDS/AutoCF) | Check upstream |
| [AutoMemory](https://github.com/HKUDS/AutoMemory) | Check upstream |
| [AutoST](https://github.com/HKUDS/AutoST) | Check upstream |
| [AutoSwarm](https://github.com/HKUDS/AutoSwarm) | MIT |
| [Awesome-LLM4Graph-Papers](https://github.com/HKUDS/Awesome-LLM4Graph-Papers) | Check upstream |
| [Awesome-LLM4Urban-Papers](https://github.com/HKUDS/Awesome-LLM4Urban-Papers) | Check upstream |
| [Awesome-SSLRec-Papers](https://github.com/HKUDS/Awesome-SSLRec-Papers) | Check upstream |
| [CatchMe](https://github.com/HKUDS/CatchMe) | Apache-2.0 |
| [CL4ST](https://github.com/HKUDS/CL4ST) | Apache-2.0 |
| [ClawTeam](https://github.com/HKUDS/ClawTeam) | MIT |
| [ClawWork](https://github.com/HKUDS/ClawWork) | MIT |
| [CLI-Anything](https://github.com/HKUDS/CLI-Anything) | Apache-2.0 |
| [DCCF](https://github.com/HKUDS/DCCF) | Check upstream |
| [DCRec](https://github.com/HKUDS/DCRec) | MIT |
| [DeepCode](https://github.com/HKUDS/DeepCode) | MIT |
| [DeepInnovator](https://github.com/HKUDS/DeepInnovator) | MIT |
| [DeepResearch-Eval](https://github.com/HKUDS/DeepResearch-Eval) | Check upstream |
| [DeepTutor](https://github.com/HKUDS/DeepTutor) | Apache-2.0 |
| [DGNN](https://github.com/HKUDS/DGNN) | Check upstream |
| [DiffGraph](https://github.com/HKUDS/DiffGraph) | Check upstream |
| [DiffKG](https://github.com/HKUDS/DiffKG) | Check upstream |
| [DiffMM](https://github.com/HKUDS/DiffMM) | Check upstream |
| [DSL](https://github.com/HKUDS/DSL) | Check upstream |
| [EasyRec](https://github.com/HKUDS/EasyRec) | Check upstream |
| [EasyST](https://github.com/HKUDS/EasyST) | Check upstream |
| [FastAgent](https://github.com/HKUDS/FastAgent) | MIT |
| [FastCode](https://github.com/HKUDS/FastCode) | Check upstream |
| [FlashST](https://github.com/HKUDS/FlashST) | Apache-2.0 |
| [FutureShow](https://github.com/HKUDS/FutureShow) | MIT |
| [GFormer](https://github.com/HKUDS/GFormer) | Apache-2.0 |
| [GPT-ST](https://github.com/HKUDS/GPT-ST) | Apache-2.0 |
| [GraphAgent](https://github.com/HKUDS/GraphAgent) | Check upstream |
| [GraphAug](https://github.com/HKUDS/GraphAug) | Check upstream |
| [GraphEdit](https://github.com/HKUDS/GraphEdit) | Apache-2.0 |
| [GraphGPT](https://github.com/HKUDS/GraphGPT) | Apache-2.0 |
| [GraphPro](https://github.com/HKUDS/GraphPro) | Apache-2.0 |
| [GraphST](https://github.com/HKUDS/GraphST) | Check upstream |
| [GTE](https://github.com/HKUDS/GTE) | Check upstream |
| [HELIX](https://github.com/HKUDS/HELIX) | MIT |
| [HGCL](https://github.com/HKUDS/HGCL) | Check upstream |
| [HiGPT](https://github.com/HKUDS/HiGPT) | Apache-2.0 |
| [HKUDS](https://github.com/HKUDS/HKUDS) | Check upstream |
| [KGRec](https://github.com/HKUDS/KGRec) | Apache-2.0 |
| [LightGCL](https://github.com/HKUDS/LightGCL) | Check upstream |
| [LightGNN](https://github.com/HKUDS/LightGNN) | Check upstream |
| [LightRAG](https://github.com/HKUDS/LightRAG) | MIT |
| [LightReasoner](https://github.com/HKUDS/LightReasoner) | MIT |
| [Litewrite](https://github.com/HKUDS/Litewrite) | AGPL-3.0 |
| [LLMRec](https://github.com/HKUDS/LLMRec) | Apache-2.0 |
| [MAERec](https://github.com/HKUDS/MAERec) | Check upstream |
| [MGP](https://github.com/HKUDS/MGP) | MIT |
| [MiniRAG](https://github.com/HKUDS/MiniRAG) | MIT |
| [MixRec](https://github.com/HKUDS/MixRec) | Check upstream |
| [MMSSL](https://github.com/HKUDS/MMSSL) | Check upstream |
| [MoChat](https://github.com/HKUDS/MoChat) | MIT |
| [nanobot](https://github.com/HKUDS/nanobot) | MIT |
| [OpenCity](https://github.com/HKUDS/OpenCity) | MIT |
| [OpenGraph](https://github.com/HKUDS/OpenGraph) | Apache-2.0 |
| [OpenHarness](https://github.com/HKUDS/OpenHarness) | MIT |
| [Paper2Slides](https://github.com/HKUDS/Paper2Slides) | MIT |
| [PhoneCLI](https://github.com/HKUDS/PhoneCLI) | MIT |
| [PrivacyFlow](https://github.com/HKUDS/PrivacyFlow) | Apache-2.0 |
| [PromptMM](https://github.com/HKUDS/PromptMM) | Check upstream |
| [RAG-Anything](https://github.com/HKUDS/RAG-Anything) | MIT |
| [RCL](https://github.com/HKUDS/RCL) | Check upstream |
| [RecDiff](https://github.com/HKUDS/RecDiff) | Apache-2.0 |
| [RecGPT](https://github.com/HKUDS/RecGPT) | Check upstream |
| [RecLM](https://github.com/HKUDS/RecLM) | Check upstream |
| [RLMRec](https://github.com/HKUDS/RLMRec) | Apache-2.0 |
| [SelfGNN](https://github.com/HKUDS/SelfGNN) | Apache-2.0 |
| [SepLLM](https://github.com/HKUDS/SepLLM) | Check upstream |
| [SimRec](https://github.com/HKUDS/SimRec) | Check upstream |
| [SSLRec](https://github.com/HKUDS/SSLRec) | Apache-2.0 |
| [STExplainer](https://github.com/HKUDS/STExplainer) | Apache-2.0 |
| [UnlearnRec](https://github.com/HKUDS/UnlearnRec) | Check upstream |
| [UpSkill](https://github.com/HKUDS/UpSkill) | MIT |
| [UrbanGPT](https://github.com/HKUDS/UrbanGPT) | Apache-2.0 |
| [Vibe-Trading](https://github.com/HKUDS/Vibe-Trading) | MIT |
| [VideoAgent](https://github.com/HKUDS/VideoAgent) | MIT |
| [VideoRAG](https://github.com/HKUDS/VideoRAG) | Check upstream |
| [ViMax](https://github.com/HKUDS/ViMax) | MIT |
| [XRec](https://github.com/HKUDS/XRec) | Apache-2.0 |

### Organization metadata (1)

| Repository | GitHub-detected license |
| --- | --- |
| [.github](https://github.com/HKUDS/.github) | Check upstream |
