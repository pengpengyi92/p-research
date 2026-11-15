# P-Research · Research Protocol and Public Provenance

**Imported:** `2026-11-15T12:17:22+08:00` (Asia/Shanghai).
**Status:** plans only, **NOT_RUN / UNMEASURED**.

## Evidence boundary

The public source is P-ML at commit
`f0492b80f9f97527926b7aa1cb1290c2ef73699b`,
path `ml-repo/cv-dl-rl/snapshot.json`.
Imported byte SHA256:
`2867982492edd317a0d0c6ce9bec1584e66acc11d946ac0e8d58deae2eaf9478`.
The source's per-query metadata/source times remain unchanged. The import timestamp is
not a fresh upstream search. Root licenses and API classifications have different roles;
89 pinned source links and rights exceptions remain in the byte-preserved snapshot.

No private research, upstream implementation, raw README/license text, model checkpoints,
data, credentials, live infrastructure or new external posts are included. Original
source snapshots/cards are not replaced. Three existing AI Infra projects are cross-linked,
not counted as new independent projects.

## Fixed-study requirements

Pre-register a falsifiable hypothesis, baseline, fixed train/selection/final-test split,
dataset/weight rights, seeds, trials and compute/interaction budget:
- CV: group subjects/videos/near-duplicates, hold out viewpoints and control prompt source;
  compare simple/frozen models, not cherry-picked frames.
- DL: fix tokens, effective batch, optimizer/selection budgets; separate pretrained weights,
  linear probes, fine-tuning, architecture and implementation changes.
- RL: random/scripted/behavior-cloning baseline as appropriate, equal real interactions
  or identical offline trajectories, independent evaluation seeds/opponents/scenes.
- Add ablations, weak controls, label/sequence contamination checks and uncertainty across
  seeds/groups. Preserve negative results and count failed trials.
- Show quality, calibration/robustness, failures and actual cost as a metric vector;
  no post-hoc universal score, unmeasured SOTA, economic benefit or real-world safety claim.

Each row in [view.json](view.json) has a target-specific question, baseline and proposed
measurement. These are study designs, not assertions about what upstream software guarantees.
No data collection, training, simulation, inference, GPU or paid service was performed.

Use **Baseline → Change → Measure → Result → Trade-off → Next Action**.
Record exact commands, source/data versions, seeds, actual output, time/hardware/cost and
limitations; all proposed gains remain **UNMEASURED** until independently tested.

## Maintenance and validation

The local generator is standard-library-only and offline. It rejects source hash changes,
wrong profiles, duplicate/mismatched identities, private/fork entries, result promotion,
future observations and escaping existing links. Generated pages preserve all source pins
and rights notes. `--check` rejects stale/missing pages without rewriting them.

Before changing the imported set, create a new dated provenance/measurement decision;
do not relabel cached source history as current. A passed directory test validates catalog
consistency, not model quality, integration, upstream runtime or production security.
