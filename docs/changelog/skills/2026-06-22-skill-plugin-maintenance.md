# Skill & Plugin Maintenance Changelog - 2026-06-22

## Changed

- Preserved the current personal plugin router/child skill architecture instead of overwriting it with older source `.agents` monoliths.

## Added

- Added a dated personal plugin maintenance audit under `docs/audits/skills/`.
- Added this dated changelog under `docs/changelog/skills/`.

## Deprecated

- None.

## Docs

- Documented the missing declared target paths and inferred local equivalents.
- Documented the stale source `.agents` versus current target router split conflict.
- Referenced the four Clous skill updates made in `/Users/alvipe/Desktop/SOFTWARE/CLOUS/plugins`.

## Validation

- `git diff --check` passed.
- Historical note: `python scripts/validate_skills.py` previously failed on a
  visual-skill frontmatter/path mismatch; current recheck now passes.
- Historical note: `bash scripts/validate-plugin.sh` used to fail because the
  script expected the old single-plugin root manifest shape.
- Current recheck: `bash scripts/validate-plugin.sh` and `cd engineering && bash ../scripts/validate-plugin.sh` now pass with the department-plugin structure.

## Follow-ups

- Decide whether `/Users/alvipe/Desktop/plugins` is the permanent replacement for `/Users/alvipe/Desktop/alvarovillalbaa/plugins`.
- Decide whether source `.agents` skills should be backported from the current router-split plugin architecture.
