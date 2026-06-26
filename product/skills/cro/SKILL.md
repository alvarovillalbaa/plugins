---
name: cro
description: >-
  Use for conversion-rate optimization for pages and funnels, page
  diagnostics, CTA promises, proof placement, and test ideas. Child skill of
  `product-marketing`; route here from the parent router when this lane is
  the narrowest owner.
---

# Cro

This child skill owns conversion-rate optimization for pages and funnels, page diagnostics, CTA promises, proof placement, and test ideas. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about conversion-rate optimization for pages and funnels, page diagnostics, CTA promises, proof placement, and test ideas.
- The parent router [`../product-marketing/SKILL.md`](../product-marketing/SKILL.md) selects this child.
- The work needs this lane's references, scripts, examples, hooks, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `scripts/` contains executable helpers owned by this lane.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.
- `hooks/` contains hook entrypoints only when this lane owns hook behavior.

## Chain Rules

- Chain to `content-writing`, `seo-and-geo`, `go-to-market`, `frontend`, `reporting` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
