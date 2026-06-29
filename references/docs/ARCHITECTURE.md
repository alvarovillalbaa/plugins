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
- **Skills**: smallest portable capability unit; skill-owned `hooks/`, `scripts/`, `references/`, `templates/`, and `examples/` live inside each skill folder
- **Commands**: stable end-to-end workflows
- **Agents**: orchestrators for multi-step or cross-artifact work
- **Root scripts**: shared repo tooling such as validation, installs, provenance, and external-skill checks

## Platform implications

- **Claude**: install department plugins through the root marketplace
- **Codex**: install a department by pointing Codex at that department directory
- **Cursor**: install a department by pointing Cursor at that department directory
- **Agent company**: clone the whole repository to preserve teams, departments, and cross-functional coordination

## Validation

```bash
python3 scripts/skillctl.py structure check --root .
python3 scripts/skillctl.py meta check --root . --require-all
python3 scripts/skillctl.py conflicts check --root .
python3 scripts/validate_skills.py .
```
