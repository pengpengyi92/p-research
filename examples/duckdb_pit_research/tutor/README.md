# Socratic practice: PIT, Python and SQL

This is an original exercise pack using the preserved
[Jane Street Socratic Tutor protocol](../../../skills/jane-street-socratic-tutor/upstream/socratic-tutor/SKILL.md).
Upstream7c6715c, MIT copyright Jane Street Group, LLC; six original files remain
unchanged. This is not a Jane Street course, interview bank or endorsement.

## How to start

Ask the current assistant to use that protocol with this case. Begin with the
five diagnostic questions in QUESTIONS.json, **one at a time**, waiting for an
answer. Do not expose FACILITATOR_KEY.md before an attempt. There is no need to
install a global skill, call a paid API, or send data to another service.

Subskills: information-set timestamps; version/session selection; dynamic
membership and missing data; Python/SQL semantic equivalence; labels, purge and
costs; causal mutation tests. Initially all levels are UNKNOWN, not0 or4.
Only observed responses can establish a skill map. Two independent checks,
including unprompted recall, are needed before promoting a level. Separate
delayed recall and mixed assessment from a just-explained answer.

Use the runner's actual snapshot/version IDs and query output in practical
exercises. If an answer is wrong, narrow the question before explaining; after
2-3 failed attempts explain briefly and use a different transfer case. Respect
`just tell me`, `harder`, `easier`, `save state`, `resume from:`.

## Evaluation protocol (NOT RUN)

Baseline: same chosen model, ordinary explanation/tutor prompt, same data and
time/token budget. Candidate: pinned Socratic protocol +same fixed exercises.
Measure held-out reasoning correctness, code/query correctness, false-mastery
rate, delayed recall, elapsed time and token/cost budget; randomize order and
do not grade a copied answer as recall. Model/backend NOT_SELECTED; no A/B trial
or learner interaction has been claimed. Practice-pack tests check structure,
not tutoring compliance, knowledge improvement or interview performance.

SESSION_STATE.json is a blank template, not a learning record. Keep real user
answers private; do not commit them to this public repository by default.
