---
name: frontend-performance-accessibility
description: >-
  Use for frontend performance, accessibility, responsiveness, rendering
  stability, bundle behavior, and Core Web Vitals. Child skill of
  `frontend`; route here from the parent router when this lane is the
  narrowest owner.
---

# Frontend Performance Accessibility

This child skill owns frontend performance, accessibility, responsiveness, rendering stability, bundle behavior, and Core Web Vitals. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about frontend performance, accessibility, responsiveness, rendering stability, bundle behavior, and Core Web Vitals.
- The parent router [`../frontend/SKILL.md`](../frontend/SKILL.md) selects this child.
- The work needs this lane's references, scripts, examples, hooks, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `scripts/` contains executable helpers owned by this lane.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.
- `hooks/` contains hook entrypoints only when this lane owns hook behavior.

## Chain Rules

- Chain to `product-development`, `product-marketing`, `quality-assurance/frontend-e2e-browser-qa`, `code-as-images`, `html-visual` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
