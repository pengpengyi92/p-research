# Observed Import Verification

Date: 2026-11-13 Asia/Shanghai. Local Windows11 build26200, Python3.12.14.
P-Research base:95bededa26899022c4aaf9c92ade3c4ad0f1b400.
Branch:codex/jane-street-socratic-tutor-20261113. Commands are from repo root.
No survey, corpus, presearch package or harness source changes.

## Results

| Run | Command | Exit | Observed result |
| --- | --- | --- | --- |
| Unmodified baseline, sandbox | python -m unittest discover -s tests -v | 1 |49 tests;15 Temp permission errors |
| Unmodified baseline, authorized host | python -m unittest discover -s tests -v | 1 |49 tests; one pre-existing GBK decoding error |
| Unmodified baseline, explicit UTF-8 | python -X utf8 -m unittest discover -s tests -v | 0 |49 passed |
| New integrity suite | python -X utf8 -m unittest discover -s tests -p test_jane_street_socratic_tutor.py -v | 0 |13 passed |
| Changed-tree full suite, same UTF-8 host | python -X utf8 -m unittest discover -s tests -v | 0 |62 passed |
| Offline snapshot checker | python -X utf8 skills/jane-street-socratic-tutor/verify_snapshot.py | 0 |Six files, blob/SHA-256/root-tree all match |

The added13 tests are included in62, not additive to it. Snapshot negative
controls cover modified skill, missing license, extra files, path traversal,
duplicate manifest paths, unsupported mode and nested Git metadata. Empty Git
blob/tree goldens and canonical ordering check the local tree implementation.

The initial errors were not hidden by source edits: host execution handles
the sandbox Temp restriction, and explicit UTF-8 handles existing Windows
locale assumptions. Some existing tests emit a ResourceWarning; it was not
silenced or reclassified as an import regression. Harness output for reckless
and freqtrade fixtures intentionally contains FAIL findings; their assertions
pass and are not measurements of this tutor.

## Provenance

- Upstream commit:7c6715c29548a3b39d4a9545c698ee4fd17a7213.
- Root Git tree:6dd590cb153ac1e0073914cb2e89029d9fdef04e.
- Tutor subtree:13f2666c7b404ce5a0a4b93a3613b99e415a48bc.
- [Exact file/blob/SHA-256 manifest](SOURCE_MANIFEST.json).
- Canonical upstream bytes were extracted using git archive from the fixed
  source checkout. The surrounding .gitattributes disables normalization for
  upstream files. The staged and remote Git subtrees both equal the source
  root tree. Remote SKILL.md is5243 bytes with exact source blob93bb7bef.
- [Observed import/remote receipt](IMPORT_RECEIPT.json) identifies the verified
  content commit44d61e8 and OPEN [PR24](https://github.com/pengpengyi92/p-research/pull/24).
  It is a reviewed-branch delivery, not a merged main-branch release.

The manifest and this report contain public repository identities only, not
host paths, private PPRT notes, credentials or raw personal transcripts.

## Scope limits

GitHub CI: NOT RUN; no new CI workflow added. Tutor dialogue evaluation,
learning outcomes, human delayed recall and model/token cost: NOT RUN /
UNMEASURED. No global installation, training, fine-tuning or paid API call.
No claim of official Jane Street collaboration, employment or endorsement.
Root package version remains0.1.0; no release is claimed.
