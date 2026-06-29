# Skills Management — Routing Guide

Router for skill lifecycle management. Routes to improvement or evaluation skills.

## Skill Lifecycle Stages

```
Install → Use → Evaluate → Improve → Promote/Archive
```

| Stage | Skill |
|-------|-------|
| Install | `skillctl.py install` command |
| Evaluate | `skill-eval-loop` |
| Improve | `skill-eval-loop` + `auto-improve` |
| Personalize | `personalize` |
| Promote upstream | `auto-improve` (propose-upstream) |

## When to Use This Skill Directly

- Auditing all installed skills for quality issues.
- Deciding which skills to add, update, or remove.
- Planning a skills roadmap for a new department or use case.
- Resolving conflicts between overlapping skills.

## Skills Audit Checklist

Run quarterly:
- [ ] All skills have a valid `.skillmeta.yml`.
- [ ] All `SKILL.md` frontmatter is valid (run `validate_skills.py`).
- [ ] No skill is referenced in a profile but not installed.
- [ ] No duplicate skill names across the same plugin.
- [ ] All referenced local files (`references/foo.md`) exist.
- [ ] Skills with no recent use are reviewed for archival.

## Skill Quality Signals

**High quality**: Clear trigger conditions, specific output contract, works without disambiguation, references contain actionable content.

**Low quality**: Vague description, overlaps significantly with another skill, requires constant clarification, references are empty stubs.

## Conflict Resolution

When two skills claim ownership of the same task:
1. Check the `skills-chaining-map.md` for the canonical owner.
2. Prefer the more specific skill over the more general one.
3. If genuinely ambiguous, document the boundary in both skills' `SKILL.md`.
