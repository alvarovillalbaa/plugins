---
name: diligence-vendor-research
description: Use for vendor diligence, product comparisons, buyer risk, filings, practitioner research, and decision-ready diligence memos. Child of `research`.
---

# Diligence Vendor Research

This child skill owns vendor diligence, product comparisons, buyer risk, filings, practitioner research, and decision-ready diligence memos. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about vendor diligence, product comparisons, buyer risk, filings, practitioner research, and decision-ready diligence memos.
- The parent router [`../research/SKILL.md`](../research/SKILL.md) selects this child.
- The work needs this lane's references, examples, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.

## Chain Rules

- Chain to `reporting`, `go-to-market`, `product-development`, `outreach`, `prospect` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `last30days`: Use recent-30-days research guidance when freshness is part of the task. Install: `python3 scripts/install-external-skills.py --skill last30days --agent codex`.
- `browserbase-company-research`: Use browser-backed company research workflows for account and market context. Install: `python3 scripts/install-external-skills.py --skill browserbase-company-research --agent codex`.
- `browserbase-search`: Use Browserbase search guidance for web discovery tasks. Install: `python3 scripts/install-external-skills.py --skill browserbase-search --agent codex`.
- `browserbase-fetch`: Use Browserbase fetch guidance for web retrieval tasks. Install: `python3 scripts/install-external-skills.py --skill browserbase-fetch --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
