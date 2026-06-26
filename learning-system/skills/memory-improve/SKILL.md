---
name: memory-improve
description: >-
  Use for memory audits, memory consolidation proposals, stale memory
  detection, retrieval quality checks, and explicit memory update workflows.
  Child skill of `auto-improve`; route here from the parent router when this
  lane is the narrowest owner.
---

# Memory Improve

This child skill owns memory audits, memory consolidation proposals, stale memory detection, retrieval quality checks, and explicit memory update workflows. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about memory audits, memory consolidation proposals, stale memory detection, retrieval quality checks, and explicit memory update workflows.
- The parent router [`../auto-improve/SKILL.md`](../auto-improve/SKILL.md) selects this child.
- The work needs this lane's references, scripts, examples, hooks, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `scripts/` contains executable helpers owned by this lane.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.
- `hooks/` contains hook entrypoints only when this lane owns hook behavior.

## Chain Rules

- Chain to `memory-management`, `second-brain`, `code-documentation`, `agentic-development/agent-harness-improvement`, `message-outreach/sender-voice-calibration` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
