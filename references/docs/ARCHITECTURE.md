# Architecture

The repository is now a company package with department-level plugins instead of one monolithic plugin root.

```text
Company Root
├── .claude-plugin/marketplace.json
├── COMPANY.md
├── assets/
├── scripts/
├── references/
└── Department Plugins
    ├── system/
    ├── marketing/
    ├── sales/
    ├── engineering/
    ├── product/
    ├── finances/
    └── productivity/
```

## Department plugin contract

Each department is its own portable plugin surface for Claude, Codex, and Cursor.

```text
department/
├── .claude-plugin/plugin.json
├── .codex-plugin/plugin.json
├── .cursor-plugin/plugin.json
├── TEAM.md
├── profile.yaml
├── mcp.json
├── skills/
├── agents/
├── commands/
└── rules/
```

## Responsibilities

- **Company root**: company narrative, marketplace catalog, shared references, shared scripts, install guidance
- **Department plugin**: runtime-specific install surface plus the department's own skills, agents, commands, rules, MCP declaration, and metadata
- **Skills**: smallest portable capability unit; skill-owned `scripts/`, `references/`, `templates/`, and `examples/` live inside each skill folder
- **Commands**: stable end-to-end workflows
- **Agents**: generalized orchestrators for multi-step or cross-artifact work; every plugin skill has at least one same-plugin agent route, with overlap and handoff rules defined in [`agents.md`](agents.md)
- **Root scripts**: shared repo tooling such as validation, installs, provenance, and external-skill checks
- **Hooks**: registered lifecycle configuration. Claude plugin hooks use
  `<department>/hooks/hooks.json`; skill-scoped hook registrations use
  `SKILL.md` frontmatter. Their executable handlers live in `scripts/`.

See [`hooks-and-scripts.md`](hooks-and-scripts.md) for the required boundary and
cross-runtime fallback rule.

## Platform implications

- **Portable project runtime (preferred)**: materialize complete plugins or
  selected components into `.agents/{skills,commands,rules,agents}` with the
  first-party interactive installer.
- **Claude**: the root marketplace remains available when Claude's namespaced
  plugin/cache model is preferable.
- **Codex and Cursor**: source department directories remain valid development
  plugin surfaces; durable cross-runtime project installs use `.agents`.
- **Agent company**: clone the whole repository to preserve source teams,
  departments, cross-functional coordination, and safe update provenance.

## Installed runtime contract

Plugin boundaries organize source ownership but do not partition installed
components. The project runtime is flat:

```text
.agents/
├── skills/<name>/
├── commands/<name>.md
├── rules/<name>.md
├── agents/<name>.md
├── .plugin-lock.json
├── registry.json
├── component-graph.json
└── runtime-contract.json
```

See [`INSTALLATION.md`](INSTALLATION.md) for collision and update semantics and
[`runtime-context.md`](runtime-context.md) for inherited personalization,
invocation variables, and cycle-safe recursive chaining.

## Validation

```bash
python3 scripts/skillctl.py structure check --root .
python3 scripts/skillctl.py meta check --root . --require-all
python3 scripts/skillctl.py conflicts check --root .
python3 scripts/validate_skills.py .
python3 scripts/audit_hooks_scripts.py .
python3 scripts/audit_commands.py .
python3 scripts/audit_agents.py .
```
