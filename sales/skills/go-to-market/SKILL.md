---
name: go-to-market
description: Router for GTM strategy, first customers, technical sales, lead signals, and revenue intelligence.
---

# Go To Market Router

## Children

- [`first-customers`](../first-customers/SKILL.md) - First Customers work.
- [`technical-sales`](../technical-sales/SKILL.md) - Technical Sales work.
- [`lead-signals`](../lead-signals/SKILL.md) - Prospect signal discovery, capture, relations, and record views.
- [`revenue-intelligence`](../revenue-intelligence/SKILL.md) - Revenue Intelligence work.

## Route

| Request | Use |
| --- | --- |
| first customers requests | [`first-customers`](../first-customers/SKILL.md) |
| technical sales requests | [`technical-sales`](../technical-sales/SKILL.md) |
| lead or prospect signal discovery and database capture | [`lead-signals`](../lead-signals/SKILL.md) |
| revenue intelligence requests | [`revenue-intelligence`](../revenue-intelligence/SKILL.md) |

## Chain Rules

Chain to these skills when the task crosses this skill's boundary:

- `product-marketing`
- `product-development`
- `outreach`
- `sales-pipeline`
- `research`

## Operating Rules

- Keep this parent compact; use children for lane-specific execution depth.
- Prefer the child skill's bundled resources when a child owns the request.
- Preserve local skill rules, repo facts, safety gates, product/channel constraints, and explicit local exceptions over external guidance when they conflict.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `last30days`: Use recent-30-days research guidance when freshness is part of the task. Install: `python3 scripts/install-external-skills.py --skill last30days --agent codex`.
- `office-hours`: Use startup office-hours guidance for GTM, early customer, and product-market questions. Install: `python3 scripts/install-external-skills.py --skill office-hours --agent codex`.
- `browserbase-company-research`: Use browser-backed company research workflows for account and market context. Install: `python3 scripts/install-external-skills.py --skill browserbase-company-research --agent codex`.
- `browserbase-competitor-analysis`: Use browser-backed competitor analysis workflows for market and SEO comparisons. Install: `python3 scripts/install-external-skills.py --skill browserbase-competitor-analysis --agent codex`.
- `browserbase-event-prospecting`: Use browser-backed event prospecting workflows for GTM research. Install: `python3 scripts/install-external-skills.py --skill browserbase-event-prospecting --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
