# AI alpha literature and selected methods release

Owner: Pengyi Peng (PNGY), with Codex assistance.
Requested 2026-11-14; prepared 2026-11-15 (Asia/Shanghai).

## Scope

Base public HEAD: `bec70c5be2603c11966c7623de08d10662b65940`.
Additive reading set, bibliography, provenance and a selected original methods
essay. This is not an alpha model implementation, journal submission, author
outreach, new platform audit or full private working-paper release.

- [Paper index](../paper/ai-alpha-research/README.md)
- [Original report](../report/2026-11-15-alpha-gpt-pengyi166/README.md)
- [Selected-release provenance and exclusions](../paper/ai-alpha-research/PROVENANCE.md)
- [Structured literature records](../paper/ai-alpha-research/sources.json)

The actual prior working paper is attributed to proprietary **P University /
P Lab**, PAPER-PWOL-001, internal v0.1 dated2026-11-06. The public selection
rewrites methodological lessons only. The private source repositories are not
modified; existing PWOL user work is preserved. No protected records or private
source URLs/paths/commit receipts are included in this public package.

## Validation protocol and observed baseline

Environment: Windows, Python3.12.14, standard library only; no dependency
installation. Baseline worktree clean at the public HEAD above.

| Command | Observed baseline |
| --- | --- |
| `python -m unittest discover -s tests -v` | Exit1:81 run,80 pass,1 error. Existing `GroupsTest.test_group_classification_and_report` reads UTF-8 as GBK on Windows. |
| `python -X utf8 -m unittest discover -s tests -v` | Exit0:81 passed,0 failures/errors/skips. No production/test code changed to hide the first error. |

The Windows UTF-8 invocation is the documented reproduction command for this
release. Linux CI is a separate observation, not inferred from local success.
Known harness fixture output labeled FAIL describes expected negative controls,
not necessarily failed unittests.

## Final changed-tree checks

Receipt prepared2026-11-15T00:06:09+08:00; source HEAD remains the baseline
above with the described additive changes. Windows11 build26200; Python3.12.14.

| Command | Actual result |
| --- | --- |
| `python -X utf8 -m unittest discover -s tests -p test_alpha_gpt_release.py -v` (initial) | Exit1:11 run,10 pass,1 fail. One assertion expected the absent phrase "not the private" rather than the actual exclusion "not the full working paper". The assertion was corrected to check the intended boundary. |
| Same targeted command (corrected) | Exit0:11 passed,0 failures/errors/skips. |
| `python -X utf8 -m unittest discover -s tests -v` (changed tree) | Exit0:92 passed,0 failures/errors/skips; includes the11 new tests, not92+11. |
| `git diff --check` | Exit0; checked again before commit. |
| Remote CI | NOT RUN at commit preparation. The new read-only [Selected paper notes workflow](https://github.com/pengpengyi92/p-research/actions/workflows/paper-notes.yml) runs the full suite on relevant pushes/PRs; inspect the exact revision's run. |

Input/selection fingerprints (SHA-256, UTF-8 file bytes):

- `sources.json`: `8b056b00cd66b6639fa5cab459438fdbd0ab76025e71244244151d0c73168407`.
- `references.bib`: `52b4af6ea39b82ae43fd1c1435aa075d6816a8d621da9d19c03c7451e3714127`.
- `PROVENANCE.md`: `54215c7ca43a4f3f3241e74a34c027f0166aaf033105d38e459c41c6050e36c6`.
- Original report: `d832dfb474526765e039473e7294fc014eb977b53f438d892cde9ab67337dffc`.

Tests cover metadata/version/author order, bibliography, local links, explicit
limits, release file types and privacy-pattern mutations. They cannot establish
complete IP clearance, author agreement or economic alpha. Primary metadata
was reviewed manually; offline tests enforce captured records rather than
independently querying publishers. No new runtime dependency was installed.

## Boundaries and next action

Original source trees, existing HKUDS guides, repository catalogs, Socratic
Tutor import, corpus/survey and research runtime remain unchanged. No new
network weekly sweep, model/GPU job, BRAIN simulation, trade or paid service.
No manual site deployment or configuration change; normal repository workflows
may run on push.

Next: freeze three synthetic tasks, independent expected answers, prompt/model
versions, budget and final audit before considering a bounded model experiment.
All proposed AI/learning/economic improvements remain **UNMEASURED**.
