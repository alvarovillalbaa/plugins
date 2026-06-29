---
name: launches
description: Router for launch motions and virality systems.
---

# Launches Router

## Children

- [`virality`](../virality/SKILL.md) - Virality work.

## Route

| Request | Use |
| --- | --- |
| virality requests | [`virality`](../virality/SKILL.md) |

## Chain Rules

Chain to these skills when the task crosses this skill's boundary:

- `content`
- `social-media`
- `video`
- `images`
- `go-to-market`

## Operating Rules

- Keep this parent compact; use children for lane-specific execution depth.
- Prefer the child skill's bundled resources when a child owns the request.
- Preserve local skill rules, repo facts, safety gates, product/channel constraints, and explicit local exceptions over external guidance when they conflict.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
