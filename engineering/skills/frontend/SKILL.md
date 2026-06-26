---
name: frontend
description: >-
  Router for frontend implementation, design systems,
  accessibility/performance, onboarding flows, UI polish, visual taste
  calibration, design critique, and design direction.
---

# Frontend Router

This parent is a router. Select the narrowest child and load that child before using lane-specific assets.

## Children

- [`design-systems-components`](../design-systems-components/SKILL.md) - design systems, shared primitives, tokens, component APIs, reusable UI patterns, and design-system drift
- [`frontend-performance-accessibility`](../frontend-performance-accessibility/SKILL.md) - frontend performance, accessibility, responsiveness, rendering stability, bundle behavior, and Core Web Vitals
- [`onboarding-flows`](../onboarding-flows/SKILL.md) - signup, onboarding, activation, empty states, checklists, tours, verification flows, and activation instrumentation
- [`ui-polish-review`](../ui-polish-review/SKILL.md) - UI polish, visual defects, layout fit, spacing, states, motion, interaction finish, and screenshot-based cleanup
- [`frontend-implementation`](../frontend-implementation/SKILL.md) - ordinary React, Next, and browser implementation for components, routes, hooks, state, forms, styling, and framework integration
- [`visual-taste-calibration`](../visual-taste-calibration/SKILL.md) - visual taste calibration, style references, brand-sensitive quality bars, and qualitative direction for interface feel
- [`design-critique`](../design-critique/SKILL.md) - structured design critique, UX review, visual hierarchy assessment, and improvement recommendations before implementation
- [`design-direction`](../design-direction/SKILL.md) - visual direction, UI concept framing, design language choices, and option shaping before detailed component work

## Route

| User asks for | Use |
| --- | --- |
| design systems, shared primitives, tokens, component APIs, reusable UI patterns, and design-system drift | [`design-systems-components`](../design-systems-components/SKILL.md) |
| frontend performance, accessibility, responsiveness, rendering stability, bundle behavior, and Core Web Vitals | [`frontend-performance-accessibility`](../frontend-performance-accessibility/SKILL.md) |
| signup, onboarding, activation, empty states, checklists, tours, verification flows, and activation instrumentation | [`onboarding-flows`](../onboarding-flows/SKILL.md) |
| UI polish, visual defects, layout fit, spacing, states, motion, interaction finish, and screenshot-based cleanup | [`ui-polish-review`](../ui-polish-review/SKILL.md) |
| ordinary React, Next, and browser implementation for components, routes, hooks, state, forms, styling, and framework integration | [`frontend-implementation`](../frontend-implementation/SKILL.md) |
| visual taste calibration, style references, brand-sensitive quality bars, and qualitative direction for interface feel | [`visual-taste-calibration`](../visual-taste-calibration/SKILL.md) |
| structured design critique, UX review, visual hierarchy assessment, and improvement recommendations before implementation | [`design-critique`](../design-critique/SKILL.md) |
| visual direction, UI concept framing, design language choices, and option shaping before detailed component work | [`design-direction`](../design-direction/SKILL.md) |

## Chain Rules

- `product-development`
- `product-marketing`
- `quality-assurance/frontend-e2e-browser-qa`
- `code-as-images`
- `html-visual`

## Operating Rules

- Keep this `SKILL.md` small and routing-focused.
- Do not recreate the old broad parent behavior here; put execution depth in child assets.
- If no child matches, handle only shared methodology/default workflow or document the missing lane.
- Every child and parent skill must keep `examples/`, `hooks/`, `references/`, `scripts/`, and `templates/`.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `hallmark`: Audit, redesign, study, or build UI with anti-AI-slop design constraints. Install: `python scripts/install-external-skills.py --skill hallmark --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
