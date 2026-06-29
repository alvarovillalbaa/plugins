# Agent Company

This repository is now organized as an agent company with department-level plugins for Claude, Codex, and Cursor.

## Company Shape

- `system`: skills management, memory, knowledge base, brain ingestion, personalization, and loops
- `marketing`: content, discoverability, social, slides, video, images, and visualization
- `sales`: prospecting, outreach, GTM, pipeline support
- `engineering`: architecture, implementation, QA, security, docs, cloud
- `product`: product development, product marketing, and design
- `finances`: expenses, reconciliation, planning, taxes, fundraising, fiscal close, and analysis
- `productivity`: reporting, research, review, documentation drift, and operational cadence

## Active Agents

- `sales/sales-prospecting`
- `productivity/executive`
- `productivity/deep-research`
- `finances/financial-analyst`
- `marketing/growth-lead`
- `engineering/principal-engineer`
- `productivity/vp-of-operations`

## Teams

- CEO + Executive Assistant
- CTO + Cloud Architect + Software Engineer x3 + Product Manager + Designer + AI Engineer
- CSO + GTM Engineers x2 + SDR x3 + Account Executive x2
- CFO + Financial Analyst + Accountant

## Installation Model

- Claude uses the root marketplace at [`.claude-plugin/marketplace.json`](/Users/alvipe/Desktop/plugins/.claude-plugin/marketplace.json).
- Codex installs one department directory at a time, because each department is a standalone plugin with its own [`.codex-plugin/plugin.json`](/Users/alvipe/Desktop/plugins/engineering/.codex-plugin/plugin.json).
- Cursor installs one department directory at a time, because each department ships its own [`.cursor-plugin/plugin.json`](/Users/alvipe/Desktop/plugins/engineering/.cursor-plugin/plugin.json).
- Individual skills are copied from `<department>/skills/<skill-name>/`.
- The full repository acts as the company package and coordination layer.

## Directory Contract

```text
company-root/
├── .claude-plugin/marketplace.json
├── COMPANY.md
├── assets/
├── scripts/
├── references/
└── <department>/
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
