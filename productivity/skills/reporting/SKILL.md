---
name: reporting
description: Router for reporting and content audit workflows.
---

# Reporting Router

## Children

- [`content-audit`](../content-audit/SKILL.md) - Content Audit work.

## Route

| Request | Use |
| --- | --- |
| content audit requests | [`content-audit`](../content-audit/SKILL.md) |

## Chain Rules

Chain to these skills when the task crosses this skill's boundary:

- `research`
- `finances`
- `product-development`

## Operating Rules

- Keep this parent compact; use children for lane-specific execution depth.
- Prefer the child skill's bundled resources when a child owns the request.
- Preserve local skill rules, repo facts, safety gates, product/channel constraints, and explicit local exceptions over external guidance when they conflict.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
