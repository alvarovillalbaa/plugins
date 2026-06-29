---
name: communication-style
description: >-
  Use for writing-style capture, approved-example analysis, sender or brand
  voice summaries, and reusable style constraints. Child skill of
  `personalize`; route here from the parent router when this lane is the
  narrowest owner.
---

# Writing Style Learning

This child skill owns writing-style capture, approved-example analysis, sender or brand voice summaries, and reusable style constraints. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about writing-style capture, approved-example analysis, sender or brand voice summaries, and reusable style constraints.
- The parent router [`../personalize/SKILL.md`](../personalize/SKILL.md) selects this child.
- The work needs this lane's references, scripts, examples, hooks, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `scripts/` contains executable helpers owned by this lane.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.
- `hooks/` contains hook entrypoints only when this lane owns hook behavior.

## Chain Rules

- Chain to `memory`, `brain`, `code-documentation`, `agentic-development/agent-harness`, `personalize/voice` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `unslop`: Remove generic AI-writing tells while preserving meaning and voice. Install: `python scripts/install-external-skills.py --skill unslop --agent codex`.
- `stop-slop`: Apply stricter prose cleanup for predictable AI writing patterns. Install: `python scripts/install-external-skills.py --skill stop-slop --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
