---
name: personalize
description: Router for user, company, voice, positioning, and ICP personalization.
---

# Personalize Router

## Children

- [`communication-style`](../communication-style/SKILL.md) - Communication Style work.
- [`voice`](../voice/SKILL.md) - Voice work.
- [`calibration`](../calibration/SKILL.md) - Calibration work.
- [`positioning`](../positioning/SKILL.md) - Positioning work.
- [`icp`](../icp/SKILL.md) - Icp work.

## Route

| Request | Use |
| --- | --- |
| communication style requests | [`communication-style`](../communication-style/SKILL.md) |
| voice requests | [`voice`](../voice/SKILL.md) |
| calibration requests | [`calibration`](../calibration/SKILL.md) |
| positioning requests | [`positioning`](../positioning/SKILL.md) |
| icp requests | [`icp`](../icp/SKILL.md) |

## Chain Rules

Chain to these skills when the task crosses this skill's boundary:

- `outreach`
- `content`
- `product-marketing`
- `research`

## Operating Rules

- Keep this parent compact; use children for lane-specific execution depth.
- Prefer the child skill's bundled resources when a child owns the request.
- Preserve local skill rules, repo facts, safety gates, product/channel constraints, and explicit local exceptions over external guidance when they conflict.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
