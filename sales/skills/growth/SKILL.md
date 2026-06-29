---
name: growth
description: Router for revenue operations, customer growth, retention, and growth experiments.
---

# Growth Router

## Children

- [`revenue-ops`](../revenue-ops/SKILL.md) - Revenue Ops work.
- [`customer-growth`](../customer-growth/SKILL.md) - Customer Growth work.

## Route

| Request | Use |
| --- | --- |
| revenue ops requests | [`revenue-ops`](../revenue-ops/SKILL.md) |
| customer growth requests | [`customer-growth`](../customer-growth/SKILL.md) |

## Chain Rules

Chain to these skills when the task crosses this skill's boundary:

- `go-to-market`
- `sales-pipeline`
- `reporting`

## Operating Rules

- Keep this parent compact; use children for lane-specific execution depth.
- Prefer the child skill's bundled resources when a child owns the request.
- Preserve local skill rules, repo facts, safety gates, product/channel constraints, and explicit local exceptions over external guidance when they conflict.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
