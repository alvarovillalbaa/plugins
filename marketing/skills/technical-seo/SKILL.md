---
name: technical-seo
description: Use for technical SEO audits, crawlability, robots, sitemaps, metadata implementation, structured data, and web performance constraints. Child of `seo`.
---

# Technical SEO Audits

This child skill owns technical SEO audits, crawlability, robots, sitemaps, metadata implementation, structured data, and web performance constraints. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about technical SEO audits, crawlability, robots, sitemaps, metadata implementation, structured data, and web performance constraints.
- The parent router [`../seo/SKILL.md`](../seo/SKILL.md) selects this child.
- The work needs this lane's references, scripts, examples, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `scripts/` contains executable helpers owned by this lane.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.

## Chain Rules

- Chain to `content`, `product-marketing/cro`, `frontend/performance`, `reporting` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `browserbase-search`: Use Browserbase search guidance for web discovery tasks. Install: `python3 scripts/install-external-skills.py --skill browserbase-search --agent codex`.
- `browserbase-fetch`: Use Browserbase fetch guidance for web retrieval tasks. Install: `python3 scripts/install-external-skills.py --skill browserbase-fetch --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
