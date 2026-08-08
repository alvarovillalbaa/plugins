# Instruction File Design

Use this reference for repo-local `AGENTS.md`, `CLAUDE.md`, rules, and harness maps. Use external skill `writing-great-skills` for skill authoring quality, skill splitting, descriptions, progressive disclosure, and context-load methodology.

## Local owner boundary

- This file owns where repo instructions live, how they route to local docs, and how harness validation checks them.
- `writing-great-skills` owns how to write or prune reusable `SKILL.md` files.
- Keep repo-specific paths, commands, invariants, and ownership rules local.
- Replace generic skill-writing doctrine with installable external-skill references.

Install fallback:

```sh
python3 scripts/install-external-skills.py --skill writing-great-skills --agent codex
```

## AGENTS.md as the repo map

Root `AGENTS.md` should be short enough to stay always-loaded and concrete enough to prevent wrong first moves.

Include:

- the repo objective in one paragraph
- instruction hierarchy and required local skills
- commands agents must know before touching code
- pointers to architecture, testing, CI, product context, and runbooks
- Always / Ask / Never boundaries that are truly repo-wide

Exclude:

- framework tutorials
- full architecture manuals
- complete command inventories
- skill-writing guidance
- long examples that belong in subsystem docs or references

For large repos, add subsystem `AGENTS.md` files next to high-risk code. Each subsystem guide should state the interface, invariants, anti-patterns, debug path, and specialized skills to load.

## CLAUDE.md and Cursor rules

Use these as environment-specific entrypoints, not duplicate handbooks.

- Point to the same canonical repo docs as `AGENTS.md`.
- Keep tool-specific command syntax local only when the tool actually differs.
- Put reusable operating rules in shared docs, then link from each entrypoint.
- Avoid copying `SKILL.md` content into rule files; reference the skill by path or name.

## Rules vs Procedures

Keep rule files declarative and procedure files operational.

| File type | Owns |
| --- | --- |
| rules | always/never constraints, security boundaries, style preferences |
| procedures | step-by-step workflows, runbooks, debug paths |
| skills | task-specific recipes and external installable methodology |

When a local rule grows into a reusable task recipe, evaluate whether it belongs in a local skill. If so, use `writing-great-skills` before creating or rewriting the skill.

## Validation

Add lightweight checks when possible:

- referenced files exist
- root and subsystem instruction files link to canonical docs
- stale links are reported before release
- high-risk directories have an instruction owner
- local skills named in instruction files still exist

Instruction files should help agents load the right local context quickly. External skill methodology should stay external unless it encodes a repo-specific rule.
