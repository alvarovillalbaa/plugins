---
name: seo-competitor-gap
description: >-
  Use for SEO competitor gap audits, SERP comparison, content gap analysis,
  authority benchmarking, and opportunity prioritization. Child skill of
  `research`; route here from the parent router when this lane is the
  narrowest owner.
---

# SEO Competitor Gap Audit

This child skill owns SEO competitor gap audits, SERP comparison, content gap analysis, authority benchmarking, and opportunity prioritization. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about SEO competitor gap audits, SERP comparison, content gap analysis, authority benchmarking, and opportunity prioritization.
- The parent router [`../research/SKILL.md`](../research/SKILL.md) selects this child.
- The work needs this lane's references, scripts, examples, hooks, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `scripts/` contains executable helpers owned by this lane.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.
- `hooks/` contains hook entrypoints only when this lane owns hook behavior.

## Chain Rules

- Chain to `content`, `product-marketing/cro`, `frontend/performance`, `reporting` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `browserbase-search`: Use Browserbase search guidance for web discovery tasks. Install: `python scripts/install-external-skills.py --skill browserbase-search --agent codex`.
- `browserbase-fetch`: Use Browserbase fetch guidance for web retrieval tasks. Install: `python scripts/install-external-skills.py --skill browserbase-fetch --agent codex`.
- `browserbase-competitor-analysis`: Use browser-backed competitor analysis workflows for market and SEO comparisons. Install: `python scripts/install-external-skills.py --skill browserbase-competitor-analysis --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
