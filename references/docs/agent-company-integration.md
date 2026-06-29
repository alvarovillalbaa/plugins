# Agent Company Integration

This document is intentionally repo-specific. Use it for integration details
that should not live inside portable `SKILL.md` files or agent instructions.

## Department Commands

Commands live inside department plugin directories, for example:

- `marketing/commands/blog-draft.md`
- `sales/commands/outreach.md`
- `engineering/commands/review-pr.md`
- `system/commands/ar-run.md`

Treat runtime slash-command names as adapter details. The portable contract is
the department command file plus the skills it routes to.

## Project Context Files

If you want repository-local defaults, keep them in ignored project context or
overlay files instead of embedding them in generic skills.

Examples:

- Brand voice and publishing defaults
- Product context and ICP scorecards
- Finance defaults such as currency or chart of accounts
- User workflow preferences

Preferred local files include `.claude/plugins.local.md`,
`.claude/agent-company.local.md`, and `.overlays/**/*.local.yml`.

## Local Skill Registry Examples

Some assistant runtimes support a local skill registry. The exact path depends
on the runtime.

Examples include:

- `~/.codex/skills/`
- `~/.claude/skills/`
- `~/.cursor/skills/`
- `~/.openclaw/skills/`

Do not treat those paths as upstream. Trace them back to this repository with
`.skillmeta.yml` or a lockfile before proposing generic improvements.

## Validation

```bash
python3 scripts/skillctl.py structure check --root .
python3 scripts/skillctl.py meta check --root . --require-all
python3 scripts/validate_skills.py .
```
