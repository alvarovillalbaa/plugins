---
name: expenses
description: Use for expense operations, bill monitoring, receipt intake, categorization, recurring bill calendars, and spend alerts. Child of `finances`.
---

# Expense Bill Ops

This child skill owns expense operations, bill monitoring, receipt intake, categorization, recurring bill calendars, and spend alerts. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about expense operations, bill monitoring, receipt intake, categorization, recurring bill calendars, and spend alerts.
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
