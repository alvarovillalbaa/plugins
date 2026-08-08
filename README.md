# Agent Company

This repository is a company package with department-level plugins and a
runtime-neutral project installer for Claude, Codex, Cursor, OpenClaw, and other
agents that read the shared `.agents` standard.

## Active Plugins

- `system`: plugins management, skill evaluation, memory, knowledge base, lessons, brain ingestion, personalization, transparent explanations, and loops
- `marketing`: content, course creation, discoverability, social media, video, images, slides, and visualization
- `sales`: go-to-market, sales pipeline, outreach, launches, virality, and growth
- `engineering`: agentic development, councils, dynamic loops/graphs/goals, AI evals, backend, frontend, cloud, pentest, PRs, QA, and code documentation
- `product`: product development, product marketing, and design
- `finances`: expenses, reconciliation, planning, taxes, fundraising, fiscal close, and analysis
- `productivity`: reporting, research, review, personal improvement, performance, meetings, and documentation drift

## Install

The first-choice installer is this repository's own interactive command. Keep a
source clone, enter the project that should receive the components, and run:

```bash
git clone https://github.com/alvarovillalbaa/plugins.git ~/.local/share/clous-plugins
cd /path/to/your-project
~/.local/share/clous-plugins/scripts/plugins install
```

It installs complete plugins or individual skills, commands, rules, and agents
into one flat project-local tree:

```text
.agents/skills/<skill-name>/
.agents/commands/<command-name>.md
.agents/rules/<rule-name>.md
.agents/agents/<agent-name>.md
```

There are no `.agents/<plugin-name>/` runtime folders. The persistent lock keeps
source provenance, supports idempotent reinstall, and preserves personalization
and local edits through safe merges. If an update cannot merge safely, the
explicit `scripts/plugins reconcile --project <path>` command can export a
provider-neutral base/local/incoming review bundle. It never invokes AI, applies
patches, or changes managed project files. After a human reviews and manually
applies a component resolution, the separate confirmation-gated
`--accept-local <conflict-id>` mode can adopt only its metadata without editing
the target. Managed document blocks instead restore generated content inside
their markers and keep project customization outside. For explicit CI
selectors, update behavior, and secondary methods including `npx skills add`,
Claude/Codex marketplaces, runtime plugin directories, symlinks, and manual
copies, see the
[installation guide](references/docs/INSTALLATION.md).

## LLM And Agent Discovery

- [`llms.txt`](llms.txt): concise LLM-readable repository index
- [`llms-full.txt`](llms-full.txt): complete plugin and component catalog
- [`catalog.json`](catalog.json): machine-readable inventory with canonical source links
- [`context7.json`](context7.json): developer-agent indexing hints
- [`skills-chaining-map.md`](skills-chaining-map.md): human-readable relationship map
- [`component-graph.json`](component-graph.json): complete generated typed relationship graph
- [`references/component-graph.json`](references/component-graph.json): source overlay for explicit cross-element relationships and graph policy
- [`references/docs/REQUIREMENT-COVERAGE.md`](references/docs/REQUIREMENT-COVERAGE.md): requirement-by-requirement implementation and verification map

## Portable Skills And Hooks

Skills are portable across supported harnesses. Runtime hooks are explicit skill-owned adapters, not department-plugin root files. Agentic development hook wrappers live under `engineering/skills/agent-harness/hooks/runtimes/`.

## Source And Runtime Model

This repository is the canonical source for distributed components. Installed
`.agents` folders are managed runtime copies or symlinks. The source plugin is
provenance, not a runtime namespace. Use the first-party command to inspect
relationships and resolve dynamic context, and use `skillctl.py` for source
provenance and upstream-safe contribution flows.

```bash
python3 scripts/skillctl.py structure check --root .
python3 scripts/skillctl.py meta check --root .
./scripts/plugins graph resolve skill:system/auto-improve
./scripts/plugins graph resolve skill:marketing/seo --project /path/to/project --available-only
./scripts/plugins configure --project /path/to/project --set project.name="Atlas"
python3 scripts/skillctl.py trace-origin system/skills/auto-improve
python3 scripts/skillctl.py diff-classify --base HEAD --head HEAD --fail-on-private
```

Run the full structural and bundled behavioral validation before publishing:

```bash
python3 scripts/validate_skills.py .
python3 scripts/audit_agents.py .
python3 scripts/run_skill_tests.py .
python3 scripts/generate_discovery_catalog.py --check
```

## External Skill Chains

Some internal skills chain to external owner skills instead of duplicating full methodology. The registry is `references/external-skills.yaml`; the skill graph is `skills-chaining-map.md`.

Check local availability:

```bash
python3 scripts/check-external-skills.py --offline --all --agent project
```
