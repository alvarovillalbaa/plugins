# Contributing

Thank you for contributing to the Agent Company plugins repository. This guide covers how to add or improve skills, commands, agents, and references.

## Repository Structure

```
company-root/
├── <department>/               # One folder per department plugin
│   ├── .claude-plugin/
│   ├── .codex-plugin/
│   ├── .cursor-plugin/
│   ├── agents/                 # Agent persona definitions
│   ├── commands/               # Slash-command definitions
│   ├── hooks/                  # Department-level hooks
│   ├── rules/                  # Routing and policy rules
│   ├── skills/
│   │   └── <skill-name>/
│   │       ├── .skillmeta.yml  # Required — install metadata
│   │       ├── SKILL.md        # Required — skill instructions
│   │       ├── references/     # Supporting reference docs
│   │       ├── examples/       # Worked examples
│   │       ├── templates/      # Output templates
│   │       ├── scripts/        # Utility scripts
│   │       └── hooks/          # Skill-level lifecycle hooks
│   ├── profile.yaml
│   └── mcp.json
```

## Adding a New Skill

1. Create a directory under the appropriate department's `skills/` folder.
2. Add a `SKILL.md` with valid frontmatter:
   ```yaml
   ---
   name: your-skill-name
   description: One-line description enabling semantic matching.
   ---
   ```
3. Add a `.skillmeta.yml` following the pattern in existing skills.
4. Add at least one `references/` document with domain guidance.
5. Run `python scripts/validate_skills.py .` to confirm no errors.

## Skill Naming Rules

- Use lowercase kebab-case: `my-skill-name`.
- The `name` field in `SKILL.md` frontmatter must match the directory name exactly.
- Names may not exceed 64 characters.
- No XML or HTML tags in `description`.

## Adding References

Reference files in `references/` should contain actionable guidance — not just links. Include:
- Frameworks and checklists the agent should follow.
- Decision trees for common scenarios.
- Anti-patterns to avoid.

## Adding Templates

Templates in `templates/` are output-format starters. Use markdown. Begin with a frontmatter block describing the template's purpose and audience.

## Adding Scripts

Scripts in `scripts/` should be executable standalone tools. Include a `#!/usr/bin/env python3` or `#!/usr/bin/env bash` shebang. Scripts should accept `--help` and fail loudly with informative error messages.

## Adding Hooks

Hooks in `hooks/` are shell scripts triggered at lifecycle events:
- `pre-tool.sh` — runs before a tool is called (receives tool name as `$1`).
- `post-bash.sh` — runs after a Bash command completes.
- `session-end.sh` — runs when the agent session ends.

Hooks must be fast (under 200 ms) and non-blocking.

## Pull Request Checklist

Before opening a PR:
- [ ] `python scripts/validate_skills.py .` passes with zero errors.
- [ ] No `Placeholder for X` README files left in new skill directories.
- [ ] All referenced local files (`references/foo.md`) exist.
- [ ] `.skillmeta.yml` is present for every new skill.
- [ ] Skill `name` matches its directory name.

## Commit Style

Use imperative mood: `add`, `fix`, `update`, `remove`. Keep the subject line under 72 characters. Reference the skill or plugin in the subject when the change is scoped: `add marketing/skills/seo-and-geo reference docs`.
