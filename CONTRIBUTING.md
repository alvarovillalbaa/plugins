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
│   │       └── scripts/        # On-demand tools and registered hook handlers
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

Use a script for deterministic work selected by a user, skill, command, test,
maintainer, or registered hook. User-facing scripts should be executable
standalone tools, include a portable shebang, accept `--help`, and fail loudly
with informative error messages. Support modules and tests may live beside a
runnable script but are not standalone commands.

Every script must have one canonical owner and accept company-, user-, tenant-,
and environment-specific values as inputs. Do not hard-code private paths,
identities, endpoints, credentials, or IDs.

## Adding Hooks

Hooks are registrations for automatic lifecycle behavior. Claude plugin hooks
belong in a plugin-root `hooks/hooks.json`; supported skill-scoped hooks belong
in `SKILL.md` frontmatter. Executable handlers live in `scripts/`, receive the
runtime's JSON event on stdin, and must be referenced by a registration.

Do not put advisory reminders, Markdown checklists, or unregistered executables
in `hooks/`. Hooks must be narrowly matched, non-interactive, bounded, and fast.
Blocking is appropriate only for a documented safety or correctness boundary.

See [`references/docs/hooks-and-scripts.md`](references/docs/hooks-and-scripts.md)
for the decision tree, runtime contract, ownership rules, and addition checklist.

## Adding Commands

Commands are reserved for stable orchestration, lifecycle control,
deterministic helpers, or a narrower outcome that is not already exposed by a
same-name local skill. Skills are directly invokable, so do not add a command
only as an alias for a skill.

Every command must:

- be listed in its department `profile.yaml`;
- have one entry in `references/command-capabilities.json` with a unique
  capability, canonical `<plugin>/<skill>` owner, and explicit boundary;
- avoid a public name that matches a local skill, because the skill shadows the
  command;
- stay at or below 100 lines and route depth into its canonical skill;
- take organization-, project-, environment-, and person-specific values as
  inputs rather than embedding them.

Run `python3 scripts/audit_commands.py .` after any command change.

## Adding Agents

Agents orchestrate multi-step work across skills; they are not alternate copies
of individual skills or headcount placeholders. Every agent must:

- be listed in its department `profile.yaml`;
- declare its workflow scope, primary skills, and routing boundaries;
- cover a distinct workflow lane and name the adjacent agent used for handoff;
- take organization-, user-, account-, workspace-, and path-specific context at runtime;
- keep every same-plugin skill reachable through at least one department agent.

Use one reusable role agent with parallel spawn counts instead of numbered or
headcount-based copies. Run `python3 scripts/audit_agents.py .` after any agent
or plugin-skill inventory change. See
[`references/docs/agents.md`](references/docs/agents.md) for the full contract.

## Pull Request Checklist

Before opening a PR:
- [ ] `python3 scripts/validate_skills.py .` passes with zero errors.
- [ ] `python3 scripts/audit_rules.py .` reports full routing coverage for every plugin.
- [ ] `python3 scripts/audit_commands.py .` reports complete, unique command ownership.
- [ ] `python3 scripts/audit_agents.py .` reports full agent coverage with no unresolved overlap or portability findings.
- [ ] No `Placeholder for X` README files left in new skill directories.
- [ ] `python3 scripts/audit_hooks_scripts.py .` passes.
- [ ] All referenced local files (`references/foo.md`) exist.
- [ ] `.skillmeta.yml` is present for every new skill.
- [ ] Skill `name` matches its directory name.

## Commit Style

Use imperative mood: `add`, `fix`, `update`, `remove`. Keep the subject line under 72 characters. Reference the skill or plugin in the subject when the change is scoped: `add marketing/skills/seo reference docs`.
