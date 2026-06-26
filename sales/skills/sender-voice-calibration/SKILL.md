---
name: sender-voice-calibration
description: >-
  Use for sender voice learning, approved-message analysis, style guides,
  forbidden phrases, and personalized writing constraints. Child skill of
  `message-outreach`; route here from the parent router when this lane is
  the narrowest owner.
---

# Sender Voice Calibration

This child skill owns sender voice learning, approved-message analysis, style guides, forbidden phrases, and personalized writing constraints. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about sender voice learning, approved-message analysis, style guides, forbidden phrases, and personalized writing constraints.
- The parent router [`../message-outreach/SKILL.md`](../message-outreach/SKILL.md) selects this child.
- The work needs this lane's references, scripts, examples, hooks, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `scripts/` contains executable helpers owned by this lane.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.
- `hooks/` contains hook entrypoints only when this lane owns hook behavior.

## Chain Rules

- Chain to `prospect-research`, `go-to-market/first-customer-gtm`, `sales-pipeline`, `auto-improve/writing-style-learning` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `unslop`: Remove AI tells from prose while preserving meaning and voice. Install: `python scripts/install-external-skills.py --skill unslop --agent codex`.
- `stop-slop`: Apply stricter prose cleanup for predictable AI writing patterns. Install: `python scripts/install-external-skills.py --skill stop-slop --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
