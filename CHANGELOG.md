# Changelog

## [Unreleased] - 2026-11-13

### Added

- Optional synthetic DuckDB/Python PIT research example v0.1.0: versioned input,
  independent snapshots/labels, five wrong-query controls, future/label invariance,
  costs, missing-data handling and calendar purge/embargo. Negative results retained.
- EADB three-document delivery, manifests/test receipts and an original Socratic
  Tutor exercise pack; four root stdlib reference tests. Core dependencies,
  corpus/survey, imported skill bytes and root package version unchanged.

- Quant Python/SQL ten-repo public guide, dated metadata, primary sources,
  validation/failure ledger and falsifiable training protocol; PyPika PR3559.
- Five offline catalogue-integrity tests, separate from upstream software tests.

- Exact six-file Jane Street agent_skills snapshot, pinned to 7c6715c, under
  skills/jane-street-socratic-tutor/upstream; MIT copyright/license retained.
- Chinese origin, meaning, usage, safety and evaluation documentation; Git
  tree/blob and SHA-256 manifest, offline verifier and 13 integrity tests.
- No model or learning-effectiveness claim; no global skill installation,
  survey/corpus changes, or root package version bump.

## [0.2.0] - 2026-08-18

### Added

- Historical corpus backfill with non-overlapping date windows (`presearch backfill`) — corpus grew to 500+ papers across 2023-2026.
- Full-text verification (`presearch verify`): ar5iv-first with arXiv native HTML fallback, abs-page rejection, partial-response salvage, and `verified` metadata on database records.
- Survey outline v0.2: 7-section compute-allocation structure + inclusion criteria.
- Database record updates (atomic rewrite) for verification metadata.

## [0.1.0] - 2026-08-18

### Added

- Weekly frontier-AI pipeline: six-pillar arXiv sweep -> deterministic
  structuring -> append-only JSONL database -> cross-pillar clustering ->
  weekly digest + index + survey outline.
- `presearch` CLI: `weekly`, `fetch`, `db stats`, `survey`.
- Rate-limited arXiv client with retries and truncated-response salvage.
- GitHub Actions weekly cron with auto-commit.
- Offline unit tests (25 in the internal suite; ported subset here).
