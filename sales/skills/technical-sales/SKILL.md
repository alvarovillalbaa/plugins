---
name: technical-sales
description: Use for technical sales motions, solution fit, discovery-to-demo translation, technical objections, and proof-of-concept framing. Child of `go-to-market`.
---

# Technical Sales

This child skill owns technical sales motions, solution fit, discovery-to-demo translation, technical objections, and proof-of-concept framing. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about technical sales motions, solution fit, discovery-to-demo translation, technical objections, and proof-of-concept framing.
- The parent router [`../go-to-market/SKILL.md`](../go-to-market/SKILL.md) selects this child.
- The work needs this lane's references, examples, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.

## Chain Rules

- Chain to `product-marketing`, `product-development`, `outreach`, `sales-pipeline`, `prospect`, `research` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `clous-api-use`: Use Clous-owned API usage guidance for consuming platform APIs. Install: `python3 scripts/install-external-skills.py --skill clous-api-use --agent codex`.
- `clous-platform-operation`: Use Clous-owned platform operation guidance for runtime and workspace operations. Install: `python3 scripts/install-external-skills.py --skill clous-platform-operation --agent codex`.
- `browserbase-company-research`: Use browser-backed company research workflows for account and market context. Install: `python3 scripts/install-external-skills.py --skill browserbase-company-research --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
