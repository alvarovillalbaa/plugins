---
name: product-development
description: >-
  Router for product strategy, discovery/prioritization, PRDs, product
  experimentation, user stories, and in-product UX copy.
---

# Product Development Router

This parent is a router. Select the narrowest child and load that child before using lane-specific assets.

## Children

- [`product-strategy`](../product-strategy/SKILL.md) - product strategy, quarterly direction, roadmap themes, vision, OKRs, portfolio tradeoffs, and decision memos
- [`discovery-prioritization`](../discovery-prioritization/SKILL.md) - customer discovery, JTBD, opportunity mapping, RICE/ICE/WSJF prioritization, and assumption testing
- [`prds`](../prds/SKILL.md) - PRDs, feature briefs, requirements, scope boundaries, release criteria, and cross-functional product specs
- [`product-experimentation`](../product-experimentation/SKILL.md) - product experiments, A/B tests, success metrics, sample sizing, decision rules, and experiment backlogs
- [`user-stories`](../user-stories/SKILL.md) - user stories, acceptance criteria, epic breakdown, story point estimation, sprint planning, and Definition of Done
- [`ux-copy-product`](../ux-copy-product/SKILL.md) - in-product UX copy for CTAs, errors, empty states, confirmations, loading states, onboarding, and recovery paths

## Route

| User asks for | Use |
| --- | --- |
| product strategy, quarterly direction, roadmap themes, vision, OKRs, portfolio tradeoffs, and decision memos | [`product-strategy`](../product-strategy/SKILL.md) |
| customer discovery, JTBD, opportunity mapping, RICE/ICE/WSJF prioritization, and assumption testing | [`discovery-prioritization`](../discovery-prioritization/SKILL.md) |
| PRDs, feature briefs, requirements, scope boundaries, release criteria, and cross-functional product specs | [`prds`](../prds/SKILL.md) |
| product experiments, A/B tests, success metrics, sample sizing, decision rules, and experiment backlogs | [`product-experimentation`](../product-experimentation/SKILL.md) |
| user stories, acceptance criteria, epic breakdown, story point estimation, sprint planning, and Definition of Done | [`user-stories`](../user-stories/SKILL.md) |
| in-product UX copy for CTAs, errors, empty states, confirmations, loading states, onboarding, and recovery paths | [`ux-copy-product`](../ux-copy-product/SKILL.md) |

## Chain Rules

- `product-marketing`
- `frontend/onboarding-flows`
- `quality-assurance/test-strategy-coverage`
- `reporting`

## Operating Rules

- Keep this `SKILL.md` small and routing-focused.
- Do not recreate the old broad parent behavior here; put execution depth in child assets.
- If no child matches, handle only shared methodology/default workflow or document the missing lane.
- Every child and parent skill must keep `examples/`, `hooks/`, `references/`, `scripts/`, and `templates/`.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
