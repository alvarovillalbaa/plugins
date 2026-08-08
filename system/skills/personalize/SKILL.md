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
- Use `scripts/check_personalization.py` only as an on-demand completeness check after the child owner has supplied the relevant personalization context.
- In an installed project, read `.agents/runtime-contract.json` and
  `.agents/personalization.local.json` before the first relevant workflow.
- When initial personalization is reached through `auto-improve`, retain this
  skill as the value-capture owner and return the resolved local context to the
  original component workflow.
- Ask only for relevant missing values. Persist project-scoped values only with
  consent; never persist invocation-scoped inputs, credentials, customer
  secrets, or other sensitive values.
- Resolve dynamic values in this order: invocation input, current session,
  project personalization, declared default. Treat information already in the
  user's request as invocation input instead of asking again.
- Keep personalization outside managed component source so reinstall and update
  can merge upstream content without erasing user context.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
