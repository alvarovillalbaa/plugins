---
name: follow-up
description: Use for follow-up messages, waiting-state nudges, reply drafting, conversation continuation, and next-step recovery. Child of `outreach`.
---

# Follow Up Messaging

This child skill owns follow-up messages, waiting-state nudges, reply drafting, conversation continuation, and next-step recovery. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about follow-up messages, waiting-state nudges, reply drafting, conversation continuation, and next-step recovery.
- The parent router [`../outreach/SKILL.md`](../outreach/SKILL.md) selects this child.
- The work needs this lane's references, examples, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.

## Chain Rules

- Chain to `prospect`, `go-to-market/first-customers`, `sales-pipeline`, `personalize/communication-style` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
