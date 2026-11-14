# p-research — AI Repository Guide Delivery

**Date:** 2026-11-14 (Asia/Shanghai). **Owner:** Pengyi Peng. Prepared with Codex assistance.

## Scope and baseline

Base HEAD: `c8896abda1449e9bd721a83c36e904ec073c959c`. First batch: **12 project-specific cards**.
Across P-ML/P-Research/P-CSDSAI there are27 unique official repositories and32
cards; cross-listed repositories are not counted as extra research experiments
or upstream contributions. This is a selected starting inventory, not the whole
ML/AI ecosystem or all historical contributions.

AI 为主；Agent、RAG、多模态、记忆、模型和研究评价；Quant × AI 保留为应用分支。先固定问题、baseline 和 holdout；再看 LightRAG / RAG-Anything / VideoRAG 的证据链；接着比较 smolagents / AutoSwarm / HELIX / DeepCode 的工具与交接；最后评价 memory / tutoring 的实际收益，而不是只看演示。

[Catalog](../repo/README.md) · [Study guide](../repo/HOW_TO_STUDY.md) ·
[Source metadata](../repo/catalog.json).

## What changed

- Classified entries with original, per-project inclusion reasons, questions,
  fixed source HEADs, two verified code entry paths, and unrun study exercises.
- Re-read bounded public author PR metadata; MERGED / OPEN / CLOSED_UNMERGED
  remain separate. No PR found means a reading candidate, not a fake contribution.
- Added an independent stdlib-only catalog validator and read-only GitHub CI job.
- Updated README/agent navigation, TODO and benchmark records. No model training,
  inference serving, pricing logic, application runtime or deployment changes.

P-ML keeps ml-repo/ canonical with a repo/ bridge; P-Research is AI-first with
Quant × AI retained as an application branch; P-CSDSAI emphasizes systems.
Historical statements and project snapshots are not rewritten. Existing
LLMQuant guides, imported Socratic Tutor, synthetic quant cases and P-Trust code
are preserved where present. Different project perspectives are linked, not
passed off as separate validated model improvements.

## Actual validation

Environment: Windows, Python3.12.14; Node24.18.0 for the existing P-Trust checks.
Catalog SHA-256: `c48d755960f16348a31b66adc3b6007b790a0e67204546ad6a3bd8869c77dd59`.

| Check | Observed result | Boundary |
| --- | --- | --- |
| `python -m unittest discover -s tests -p test_repo_catalog.py -v` |10 passed, exit0 | Public source pins, card content/links, PR state semantics, permissions and no workstation/credential material |
| Existing scoped checks |目录10项；完整 unittest 81项通过（含原有71项与新增10项），不是91项 | No third-party model execution or learning-effect evidence |
| `git diff --check` |PASS | Authored changes only |

Full command: `python -m unittest discover -s tests -v`:81 passed,
exit0. The10 catalog cases are included in81, not additional to it. Existing
negative-control harness messages such as FAIL are expected fixture outcomes,
not unittest failures. The real network weekly sweep was not run.

LLMQuant file kept at Git blob `835e954aa17e97a3cfb542f4fb875a1ad0ef2e3f`.

未运行真实 arXiv sweep、第三方模型、GPU 或新 Agent workflow。

No new GPU job, model/dataset download, paid API call, investment or upstream
PR/comment/CLA/DCO action. Context7 returned a quota limit; official upstream
GitHub documents and metadata were used instead. Initial guessed paths in some
HKUDS repositories did not match their current layouts; corrected entries were
verified against the same pinned Git trees, not invented or tested by execution.

Remote CI is separate from local evidence and is not claimed green before it
is observed. The catalog cannot validate software safety, model claims,
benchmark scores, partnerships or employment. Learning benefit, real model
quality and performance gains remain **UNMEASURED**.

## License and publication boundary

Only public metadata, links and original commentary are published. No upstream
source/license mirrors or private research notes/logs/datasets/strategies are
exported. License classifiers are not legal permission: PyTorch/VideoRAG require
reading their texts; VideoRAG and dependencies/model weights have separate terms;
AutoMemory lacks a captured root license and stays NEEDS_PERMISSION/reference-only.
No particular code/data/weight reuse or commercial use is authorized by listing.

## Next action

Choose one small fixed fixture from a card. Record question, baseline, split,
metric/tolerance, cost and negative controls before execution. Keep model/method,
AI research protocol and systems-engineering results separate, linking an
existing artifact when the same work is relevant to more than one project.
