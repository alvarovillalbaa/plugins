---
name: finances
description: Router for finance operations, planning, taxes, fundraising, fiscal close, and analysis.
---

# Finances Router

## Children

- [`expenses`](../expenses/SKILL.md) - Expenses work.
- [`reconciliation`](../reconciliation/SKILL.md) - Reconciliation work.
- [`planning`](../planning/SKILL.md) - Planning work.
- [`taxes`](../taxes/SKILL.md) - Taxes work.
- [`fundraising`](../fundraising/SKILL.md) - Fundraising work.
- [`fiscal-close`](../fiscal-close/SKILL.md) - Fiscal Close work.
- [`quantitative`](../quantitative/SKILL.md) - Quantitative work.
- [`fundamentals`](../fundamentals/SKILL.md) - Fundamentals work.
- [`macro`](../macro/SKILL.md) - Macro work.

## Route

| Request | Use |
| --- | --- |
| expenses requests | [`expenses`](../expenses/SKILL.md) |
| reconciliation requests | [`reconciliation`](../reconciliation/SKILL.md) |
| planning requests | [`planning`](../planning/SKILL.md) |
| taxes requests | [`taxes`](../taxes/SKILL.md) |
| fundraising requests | [`fundraising`](../fundraising/SKILL.md) |
| fiscal close requests | [`fiscal-close`](../fiscal-close/SKILL.md) |
| quantitative requests | [`quantitative`](../quantitative/SKILL.md) |
| fundamentals requests | [`fundamentals`](../fundamentals/SKILL.md) |
| macro requests | [`macro`](../macro/SKILL.md) |

## Chain Rules

Chain to these skills when the task crosses this skill's boundary:

- `reporting`
- `research`
- `product-marketing`

## Operating Rules

- Keep this parent compact; use children for lane-specific execution depth.
- Prefer the child skill's bundled resources when a child owns the request.
- Preserve local skill rules, repo facts, safety gates, product/channel constraints, and explicit local exceptions over external guidance when they conflict.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
