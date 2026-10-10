# Skill Preference Sweep Audit - 2026-06-26

## Summary

Status: Done on 2026-06-26.

- Updated the live canonical skill taxonomy after the in-progress hard-rename from older slugs such as `architecture-system-design`, `api-service-design`, and frontend visual lanes.
- Preserved the current router/child architecture and did not restore deleted old skill paths.
- Encoded default `quality-assurance` and `code-documentation` chaining for engineering and product-spec work.
- Replaced compatibility-first guidance with hard-cut owner-boundary guidance: no backfills, compatibility shims, backward-compat aliases, facade layers, or route bridges unless explicitly approved.
- Added product-spec guidance: PRDs and specs stay product-focused and include only small technical hints.
- Added Fluid Functionalism as UI reference guidance for meaningful motion, hover previews, and shadcn/Radix/Tailwind-compatible inspiration.

## Scope

| Area | Canonical owner updated |
|---|---|
| Shared routing and chain policy | `skills-chaining-map.md` |
| Engineering execution | `agentic-development`, `architecture`, `tech-debt` |
| Backend contracts | `backend`, `apis`, `databases` |
| Frontend implementation | `frontend` and frontend implementation source reference |
| Product specs | `product-development`, `prds`, `user-stories`, PRD templates |
| UI/design guidance | `design`, `design-systems`, `polish`, `direction`, `taste`, `critique` |

## Notes

- Database normalization remains valid as relational schema terminology; payload-shape normalization is explicitly discouraged.
- Existing router skills are intentionally preserved. "No routing files" was applied to implementation-level compatibility route bridges, not to the skill taxonomy.
- The Fluid Functionalism source was treated as design guidance, not as a dependency mandate.

## Validation

- `python scripts/validate_skills.py` passed with `Validated 140 skill file(s).`
- `git diff --check` passed.
- Targeted `rg` checks found no stale exact phrases for compatibility-first guidance, broad technical specifications, facade migration steps, or view-level data-transform guidance in the edited files.

## Completion Recheck

- Pass: `python3 scripts/validate_skills.py` validated 141 skill files and 7 department plugin structures.
- Pass: `python3 scripts/skillctl.py meta check --root .`.
- Pass: `git diff --check`.
- Done: the canonical router/child architecture remains intact and no deleted old skill paths were restored.
