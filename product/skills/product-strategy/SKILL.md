---
name: product-strategy
description: >-
  Use for product strategy, quarterly direction, roadmap themes, vision, OKRs,
  portfolio tradeoffs, and decision memos. Child skill of `product-
  development`; route here from the parent router when this lane is the
  narrowest owner.
---

# Product Strategy

This child skill owns product strategy, quarterly direction, roadmap themes, vision, OKRs, portfolio tradeoffs, and decision memos. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about product strategy, quarterly direction, roadmap themes, vision, OKRs, portfolio tradeoffs, and decision memos.
- The parent router [`../product-development/SKILL.md`](../product-development/SKILL.md) selects this child.
- The work needs this lane's references, scripts, examples, hooks, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `scripts/` contains executable helpers owned by this lane.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.
- `hooks/` contains hook entrypoints only when this lane owns hook behavior.

## Chain Rules

- Chain to `product-marketing`, `frontend/onboarding-flows`, `quality-assurance/test-strategy-coverage`, `reporting` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
