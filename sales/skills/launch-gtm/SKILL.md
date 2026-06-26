---
name: launch-gtm
description: >-
  Use for launch GTM planning, announcement motion, campaign sequencing,
  launch channels, and launch retrospectives. Child skill of `go-to-market`;
  route here from the parent router when this lane is the narrowest owner.
---

# Launch GTM

This child skill owns launch GTM planning, announcement motion, campaign sequencing, launch channels, and launch retrospectives. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about launch GTM planning, announcement motion, campaign sequencing, launch channels, and launch retrospectives.
- The parent router [`../go-to-market/SKILL.md`](../go-to-market/SKILL.md) selects this child.
- The work needs this lane's references, scripts, examples, hooks, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `scripts/` contains executable helpers owned by this lane.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.
- `hooks/` contains hook entrypoints only when this lane owns hook behavior.

## Chain Rules

- Chain to `product-marketing`, `product-development`, `message-outreach`, `sales-pipeline`, `prospect-research`, `research` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
