# P-Research · CV / DL / RL Cross-list Report

**Title:** 从视觉、模型与策略建立可证伪的研究问题。
**Imported:** `2026-11-15T12:17:22+08:00` (Asia/Shanghai).
**Status:** public-source study design, NOT_RUN / UNMEASURED.

[Catalog](../repo/cv-dl-rl/README.md) covers43 primary projects (CV16 /DL11 /RL16),
linking the full116-project P-ML registry. This is not this repository's global unique
project count. DeepSpeed, torchtitan and Megatron-LM already exist in the local AI Infra
catalog and are linked back; no existing card or historical source observation is replaced.

## What this repository adds

每项新增的是可被数据推翻的问题、baseline和拟用指标，不是重复P-ML的学习介绍：
- CV研究提示/标注预算、独立主体/视频/相机holdout、时序记忆和跨域鲁棒性。
- DL研究预训练/线性探针/微调、数据和选择预算、组件消融以及质量-成本关系。
- RL研究相同真实交互/离线数据预算下的泛化、回报方差、对手/场景分布与动力学误差。
- 研究设计必须保留弱baseline、负对照、失败trial、uncertainty与未经优化的最终test。

[Three generated routes](../repo/cv-dl-rl/README.md) give43 individual questions,
baselines and measurement plans. They complement the other public repositories, rather
than claiming43 original algorithms or successful replications. All new experiments are unrun.

## Public provenance and rights

Source: P-ML commit`f0492b80f9f97527926b7aa1cb1290c2ef73699b`,
public path`ml-repo/cv-dl-rl/snapshot.json`.
Its copied bytes were compared to the published API before import; SHA256
`2867982492edd317a0d0c6ce9bec1584e66acc11d946ac0e8d58deae2eaf9478`.
Original metadata/source times, canonical redirects, roles, commit/file pins and89
README/license links remain unchanged. The import time is separate, not a fresh upstream audit.

Two archives, nanoGPT/D4RL/Brax maintenance/migration notes, nine unclassified license
signals, D2L's book/code distinction, SAM2's additional code/font notes, AGPL vs commercial
options and Minigrid's license-clarification gate remain explicit. Code, data, weights,
assets, dependencies and host/service terms require separate review.

No upstream source, textbook content, README/license text, weights/data, private P University,
PINF, P-Compute or PAT materials were migrated. No upstream posts or manual application
deployment/configuration changes. The owner's existing automatic Pages workflow is
observed separately after the authorized repository push.
The app/CLI, existing source cards, AI Infra snapshot, papers and data remain unchanged.

## Validation and next

[Checks](../repo/cv-dl-rl/CHECKS.json) record actual commands/hashes and remaining gaps.
The pre-change Python baseline passed94 tests. New offline contracts check
profile/identity/provenance, byte preservation, original timestamps, source links and
negative controls. Generator freshness is checked without network or third-party execution.

Next: choose one pre-registered representation, temporal-memory or fixed-budget RL study.
Use independent baselines and negative controls, actual measured costs and versioned decisions.
No model/gain/security/production result can be inferred from catalog checks.

Final local result:112 Python tests PASS (94 retained +18 new), with PYTHONUTF8=1.
Generator freshness and original CLI/source/AI Infra/papers/data preservation checks PASS.
The existing harness deliberately prints failed weak/reckless fixture evaluations in its
negative controls; these are not failed unit tests or new model-performance measurements.
