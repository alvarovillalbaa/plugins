# Second-Brain Ingestion Hardening - 2026-06-26

## Changed

- Added an explicit brain contract for `BRAIN.md` boundaries, AFS/native adaptation modes, canonical knowledge paths, raw status semantics, and Memory-to-knowledge compilation.
- Updated `/ingest` and `/compile-raw` instructions to fail closed on missing or ambiguous brain boundaries.
- Expanded ingestion guidance for X via `xurl`, LinkedIn, web URLs, YouTube, PDFs, images, structured files, archives, office files, and unknown binaries.
- Added blocked-source handling so unreadable inputs stay in `raw/` with exact reasons instead of being over-promoted.
- Added `brain_inventory.py` as a read-only helper for brain and raw queue readiness checks.

## Validation

- Pass: `python scripts/validate_skills.py`
- Pass: `python -m py_compile system/skills/ingestion/scripts/brain_inventory.py`
- Pass: helper fixture checks for missing, single, and multiple `BRAIN.md` cases
- Pass: `python system/skills/ingestion/scripts/brain_inventory.py . --include-memory --json`
- Pass: `git diff --check -- system/skills/brain system/skills/ingestion system/commands docs/audits/skills docs/changelog/skills`
