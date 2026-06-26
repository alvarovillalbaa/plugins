---
name: review
description: >-
  Router for code/diff review, design/UX review, and grill-style adversarial
  critique.
---

# Review Router

This parent is a router. Select the narrowest child and load that child before using lane-specific assets.

## Children

- [`code-diff-review`](../code-diff-review/SKILL.md) - code review, diff risk assessment, PR findings, regression risk, test gaps, and maintainability critique
- [`design-ux-review`](../design-ux-review/SKILL.md) - design review, UX critique, visual hierarchy, interaction risk, accessibility observations, and polish recommendations
- [`grill`](../grill/SKILL.md) - adversarial critique, plan stress-testing, simplification pressure, execution risk, and weak-assumption exposure

## Route

| User asks for | Use |
| --- | --- |
| code review, diff risk assessment, PR findings, regression risk, test gaps, and maintainability critique | [`code-diff-review`](../code-diff-review/SKILL.md) |
| design review, UX critique, visual hierarchy, interaction risk, accessibility observations, and polish recommendations | [`design-ux-review`](../design-ux-review/SKILL.md) |
| adversarial critique, plan stress-testing, simplification pressure, execution risk, and weak-assumption exposure | [`grill`](../grill/SKILL.md) |

## Chain Rules

- `quality-assurance`
- `frontend`
- `product-development`
- `pr-management`

## Operating Rules

- Keep this `SKILL.md` small and routing-focused.
- Do not recreate the old broad parent behavior here; put execution depth in child assets.
- If no child matches, handle only shared methodology/default workflow or document the missing lane.
- Every child and parent skill must keep `examples/`, `hooks/`, `references/`, `scripts/`, and `templates/`.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
