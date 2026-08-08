---
name: growth
description: Route revenue operations while directly owning customer growth, retention, expansion, churn-risk review, lifecycle nudges, and growth experiments.
---

# Growth Router

## Children

- [`revenue-ops`](../revenue-ops/SKILL.md) - Revenue Ops work.

## Route

| Request | Use |
| --- | --- |
| revenue ops requests | [`revenue-ops`](../revenue-ops/SKILL.md) |
| Customer growth, retention, expansion, churn risk, lifecycle nudges, or customer-success GTM | Handle directly with this skill using `references/customer-growth-playbook.md` |

## Chain Rules

Chain to these skills when the task crosses this skill's boundary:

- `go-to-market`
- `sales-pipeline`
- `reporting`
- `product-marketing`
- `product-development`
- `outreach`
- `prospect`
- `research`

## Operating Rules

- Keep this parent compact; use children for lane-specific execution depth.
- Prefer the child skill's bundled resources when a child owns the request.
- Preserve local skill rules, repo facts, safety gates, product/channel constraints, and explicit local exceptions over external guidance when they conflict.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
