---
name: fiscal-close
description: Use for month-end close calendars, owners, blockers, dependencies, close dashboards, T+ cadences, and accelerated close work. Child of `finances`.
---

# Month End Close

This child skill owns month-end close calendars, owners, blockers, dependencies, close dashboards, T+ cadences, and accelerated close work. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about month-end close calendars, owners, blockers, dependencies, close dashboards, T+ cadences, and accelerated close work.
- The parent router [`../finances/SKILL.md`](../finances/SKILL.md) selects this child.
- The work needs this lane's references, examples, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.

## Chain Rules

- Chain to `reporting`, `research`, `product-marketing` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
