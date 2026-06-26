# Skill Extraction

Use this reference to decide whether a repo learning should become a skill, where it should live, and how it should be promoted. Use external skill `writing-great-skills` for the actual skill-writing method: description quality, file shape, splitting, context-load control, examples, and failure modes.

Install fallback:

```sh
python scripts/install-external-skills.py --skill writing-great-skills --agent codex
```

## Extraction boundary

Extract a skill only when the knowledge is:

- recurring enough to justify a reusable procedure
- verified by real work, not theory
- specific enough to change future behavior
- not already owned by official docs, an external skill, or a local parent skill
- safe to reuse without leaking secrets, private URLs, or company-only context

Do not create a skill for:

- one-off task logistics
- direct documentation lookups
- transient environment failures
- generic writing, TDD, design, or review methodology already owned by an external skill

## Search before creating

Search local and user-level skills first:

```sh
rg --files -g 'SKILL.md' .claude/skills ~/.claude/skills ~/.codex/skills 2>/dev/null
rg -i "keyword|error|technology" .claude/skills ~/.claude/skills ~/.codex/skills 2>/dev/null
```

If an existing skill owns the trigger, update that skill or add a pointer. If the external skill owns the method, keep only the local repo-specific contract and reference the external install command.

## Placement

| Scope | Location |
| --- | --- |
| repo-specific procedure | project skill directory or subsystem docs |
| reusable across projects | user-level skill directory |
| general methodology from listed external owners | external skill chain |
| raw memory or isolated discovery | `learning/` or second-brain artifact |

Keep local skills portable inside this plugin repo: no hardcoded user paths, credentials, or assumptions that only work in one checkout.

## Promotion flow

1. Capture the concrete incident in the learning system.
2. Check existing local skills, parent routers, and `skills-chaining-map.md`.
3. If the pattern is local context, add the smallest reference or skill change that prevents rediscovery.
4. If the pattern is general skill-writing quality, invoke `writing-great-skills` instead of duplicating its criteria.
5. Validate the changed skill with `python scripts/validate_skills.py`.

## Handoff note

When a skill extraction task needs teaching material, learning plans, or lesson construction, chain to `teach`. When it needs an interview loop to clarify the intended behavior, chain to `grill-me`, `grilling`, or `grill-with-docs` depending on whether the output is a quick answer, an interview, or maintained docs.
