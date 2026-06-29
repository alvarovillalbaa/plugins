# Skill Preference Sweep Changelog - 2026-06-26

## Changed

- Added default `quality-assurance` and `code-documentation` chaining for engineering and product-spec work.
- Updated API, architecture, frontend, and product-spec guidance to prefer hard cuts over compatibility residue.
- Reframed PRD templates around product-focused implementation notes instead of broad technical specifications.
- Added Fluid Functionalism guidance for UI motion and hover behavior.

## Added

- Added a dated audit under `docs/audits/skills/`.
- Added this dated changelog under `docs/changelog/skills/`.

## Deprecated

- Deprecated default guidance for backfills, backward compatibility shims, facade layers, route bridges, and frontend payload-shape normalization.

## Validation

- `python scripts/validate_skills.py` passed with `Validated 140 skill file(s).`
- `git diff --check` passed.
- Targeted `rg` checks found no stale exact phrases for compatibility-first guidance, broad technical specifications, facade migration steps, or view-level data-transform guidance in the edited files.
