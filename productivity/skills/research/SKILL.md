---
name: research
description: Router for market, vendor, customer, SEO-gap, and prospect research.
---

# Research Router

## Children

- [`market-competitor-research`](../market-competitor-research/SKILL.md) - Market Competitor Research work.
- [`diligence-vendor-research`](../diligence-vendor-research/SKILL.md) - Diligence Vendor Research work.
- [`seo-competitor-gap`](../seo-competitor-gap/SKILL.md) - Seo Competitor Gap work.
- [`prospect`](../prospect/SKILL.md) - Prospect work.

## Route

| Request | Use |
| --- | --- |
| market competitor research requests | [`market-competitor-research`](../market-competitor-research/SKILL.md) |
| diligence vendor research requests | [`diligence-vendor-research`](../diligence-vendor-research/SKILL.md) |
| Customer qualitative research, interviews, ICP learning, pain synthesis, account enrichment, or lead qualification | [`discovery`](../../../product/skills/discovery/SKILL.md) |
| seo competitor gap requests | [`seo-competitor-gap`](../seo-competitor-gap/SKILL.md) |
| prospect requests | [`prospect`](../prospect/SKILL.md) |

## Chain Rules

Chain to these skills when the task crosses this skill's boundary:

- `reporting`
- `go-to-market`
- `product-development`
- `outreach`

## Operating Rules

- Keep this parent compact; use children for lane-specific execution depth.
- Prefer the child skill's bundled resources when a child owns the request.
- Preserve local skill rules, repo facts, safety gates, product/channel constraints, and explicit local exceptions over external guidance when they conflict.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `last30days`: Use recent-30-days research guidance when freshness is part of the task. Install: `python3 scripts/install-external-skills.py --skill last30days --agent codex`.
- `browserbase-search`: Use Browserbase search guidance for web discovery tasks. Install: `python3 scripts/install-external-skills.py --skill browserbase-search --agent codex`.
- `browserbase-fetch`: Use Browserbase fetch guidance for web retrieval tasks. Install: `python3 scripts/install-external-skills.py --skill browserbase-fetch --agent codex`.
- `browserbase-company-research`: Use browser-backed company research workflows for account and market context. Install: `python3 scripts/install-external-skills.py --skill browserbase-company-research --agent codex`.
- `browserbase-competitor-analysis`: Use browser-backed competitor analysis workflows for market and SEO comparisons. Install: `python3 scripts/install-external-skills.py --skill browserbase-competitor-analysis --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
