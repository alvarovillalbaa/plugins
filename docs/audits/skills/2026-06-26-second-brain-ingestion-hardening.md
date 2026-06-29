# Second-Brain Ingestion Hardening Audit - 2026-06-26

## Summary

Status: Done on 2026-06-26.

- Strengthened the `brain`/`ingestion` router split instead of reviving the older monolithic second-brain skill.
- Added an explicit `BRAIN.md` boundary and adaptation contract for strict AFS, partial AFS, and native company standards.
- Made `compile-raw` cover repo-local Memory inputs in addition to `raw/`.
- Added fail-closed handling for unreadable, metadata-only, login-walled, deleted, encrypted, or unsupported raw sources.
- Added a read-only inventory helper for brain boundaries, raw queue status/source breakdown, Memory counts, and extraction tool availability.

## Contract Decisions

- Canonical knowledge defaults to `knowledge/<domain>/<subject>/<topic>/<case>/`; alternate paths must come from `BRAIN.md`.
- A target repo, workspace, codebase, or database has one active brain. Multiple `BRAIN.md` files under the target root require explicit selection before writes.
- Raw entries use `unprocessed`, `processed`, or `blocked` status. Blocked entries require `blocked_reason`.
- Processed cleanup is narrow: mark processed by default, or remove only exact processed queue pointers when `BRAIN.md` says to remove pointers.
- Memory folders are evidence inputs, not canonical truth. Durable learnings are promoted by rewriting existing owner pages and preserving provenance.

## Files Updated

- `system/skills/brain/SKILL.md`
- `system/skills/brain/README.md`
- `system/skills/brain/agents/openai.yaml`
- `system/skills/brain/references/brain_contract.md`
- `system/skills/brain/references/operational_modes.md`
- `system/skills/ingestion/SKILL.md`
- `system/skills/ingestion/references/ingest_sources.md`
- `system/skills/ingestion/references/wiki_compiler.md`
- `system/skills/ingestion/scripts/brain_inventory.py`
- `system/commands/ingest.md`
- `system/commands/compile-raw.md`

## Validation

- Pass: `python scripts/validate_skills.py` validated 140 skill files.
- Pass: `python -m py_compile system/skills/ingestion/scripts/brain_inventory.py`.
- Pass: helper fixture checks for missing, single, and multiple `BRAIN.md` cases.
- Pass: `python system/skills/ingestion/scripts/brain_inventory.py . --include-memory --json`.
- Pass: `git diff --check -- system/skills/brain system/skills/ingestion system/commands docs/audits/skills docs/changelog/skills`.
- Note: `system/` is currently untracked in this checkout, so ordinary `git diff` output does not show these new files.

## Completion Recheck

- Pass: `python3 scripts/validate_skills.py` validated 141 skill files and 7 department plugin structures.
- Pass: `python3 scripts/skillctl.py meta check --root .`.
- Pass: `git diff --check`.
- Done: this audit's hardening files remain present in `system/skills/brain`, `system/skills/ingestion`, and `system/commands`.
