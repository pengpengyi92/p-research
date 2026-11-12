# DuckDB + Python synthetic PIT research v0.1.0

Artifact P-RESEARCH-SYN-PIT-001. [Project](../examples/duckdb_pit_research/README.md)
/ [EADB card](../examples/duckdb_pit_research/EADB_CARD.json).
Source commit `0ea3421549e6cccd044af29c2d144e7459e7e76c`; root package version unchanged.

Original fixed seed166 input,31feature versions/5membership events/28opens/
6decisions. Independent SQL/reference comparisons:16snapshots/24labels;
five wrong-query controls caught, six-cutoff invariance and label isolation.
Shared explicit accounting; top1 synthetic OOS about-8.16% over three decisions,
negative result preserved. No alpha, real OOS or production claim.

Sealed-source tests48example PASS;71core/reference PASS without DuckDB;
13Tutor integrity tests are a subset. Two full runs yield byte-identical results,
with fixture/code/output fingerprints and source HEAD. Remote CI NOT RUN.
EADB three docs and original practice pack included; six upstream Tutor files
unchanged. Human diagnostic/mastery/delayed recall NOT RUN, no learner data stored.

Publication is separate from the observed test/run evidence; the final delivery
receipt records actual remote identity after a successful authorized push.
