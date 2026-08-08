---
name: revenue-intelligence
description: Use for revenue intelligence from calls, opportunities, CRM, and attribution; pipeline risk; forecast inputs; and buying committee insight. Child of `go-to-market`.
---

# Revenue Intelligence

This child skill owns revenue intelligence from calls, opportunities, CRM, and attribution, including pipeline risk, forecast inputs, and buying committee insight. Route public prospect-event discovery and Signals database persistence to `lead-signals`.

## Use When

- The request is primarily about revenue intelligence from calls, opportunities, CRM, or attribution, including pipeline risk, forecast inputs, and buying committee insight.
- The parent router [`../go-to-market/SKILL.md`](../go-to-market/SKILL.md) selects this child.
- The work needs this lane's references, examples, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.

## Chain Rules

- Chain to `lead-signals`, `product-marketing`, `product-development`, `outreach`, `sales-pipeline`, `prospect`, `research` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
