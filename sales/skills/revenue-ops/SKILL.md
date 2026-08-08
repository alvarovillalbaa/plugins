---
name: revenue-ops
description: Use for revenue operations, CRM stages, lifecycle definitions, handoff rules, pipeline hygiene, and operating metrics. Child of `growth`.
---

# Revenue Ops

This child skill owns revenue operations, CRM stages, lifecycle definitions, handoff rules, pipeline hygiene, and operating metrics. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about revenue operations, CRM stages, lifecycle definitions, handoff rules, pipeline hygiene, and operating metrics.
- The parent router [`../growth/SKILL.md`](../growth/SKILL.md) selects this child.
- The work needs this lane's references, examples, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.

## Chain Rules

- Chain to `product-marketing`, `product-development`, `outreach`, `sales-pipeline`, `prospect`, `research` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
