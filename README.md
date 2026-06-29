# Agent Company

This repository is a company package with department-level plugins for Claude, Codex, Cursor, OpenClaw, and portable skill installation.

## Active Plugins

- `system`: skills management, memory, knowledge base, lessons, brain ingestion, personalization, and loops
- `marketing`: content, discoverability, social media, video, images, slides, and visualization
- `sales`: go-to-market, sales pipeline, outreach, launches, virality, and growth
- `engineering`: agentic development, AI engineering, backend, frontend, cloud, pentest, PRs, QA, and code documentation
- `product`: product development, product marketing, and design
- `finances`: expenses, reconciliation, planning, taxes, fundraising, fiscal close, and analysis
- `productivity`: reporting, research, review, and documentation drift

## Install

Install a department plugin from the root marketplace, or install individual skill folders with your runtime's skill installer.

```bash
npx -y skills add -a codex ./engineering
npx -y skills add -a codex ./marketing
npx -y skills add -a codex ./system
```

Install individual skills:

```bash
cp -R marketing/skills/discoverability ~/.codex/skills/
cp -R sales/skills/outreach ~/.codex/skills/
cp -R productivity/skills/research ~/.codex/skills/
```

## Portable Skills And Hooks

Skills are portable across supported harnesses. Runtime hooks are explicit skill-owned adapters, not department-plugin root files. Agentic development hook wrappers live under `engineering/skills/agent-harness/hooks/runtimes/`.

## Source And Runtime Model

This repository is the canonical source for distributed skills. Installed agent
folders are runtime copies or symlinks. Use `scripts/skillctl.py` to trace
provenance, render local overlays, classify diffs, and generate upstream patch
bundles without leaking private personalization data.

```bash
python3 scripts/skillctl.py structure check --root .
python3 scripts/skillctl.py meta check --root .
python3 scripts/skillctl.py personalize init --skill system/skills/auto-improve --dry-run
python3 scripts/skillctl.py trace-origin system/skills/auto-improve
python3 scripts/skillctl.py diff-classify --base HEAD --head HEAD --fail-on-private
```

## External Skill Chains

Some internal skills chain to external owner skills instead of duplicating full methodology. The registry is `references/external-skills.yaml`; the skill graph is `skills-chaining-map.md`.

Check local availability:

```bash
python3 scripts/check-external-skills.py --offline --all --agent codex
```
