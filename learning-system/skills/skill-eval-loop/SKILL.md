---
name: skill-eval-loop
description: >-
  Use for skill evaluation loops, regression checks for skill behavior,
  prompt/skill mutation proposals, and explicit improvement gates. Child
  skill of `auto-improve`; route here from the parent router when this lane
  is the narrowest owner.
---

# Skill Eval Loop

This child skill owns skill evaluation loops, regression checks for skill behavior, prompt/skill mutation proposals, and explicit improvement gates. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about skill evaluation loops, regression checks for skill behavior, prompt/skill mutation proposals, and explicit improvement gates.
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

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `writing-great-skills`: Use external skill-authoring quality rules when creating or revising skills. Install: `python scripts/install-external-skills.py --skill writing-great-skills --agent codex`.
- `teach`: Create mission-grounded learning material, resources, records, and lessons. Install: `python scripts/install-external-skills.py --skill teach --agent codex`.
- `grilling`: Interview one decision at a time until a plan or design is sharp. Install: `python scripts/install-external-skills.py --skill grilling --agent codex`.
- `grill-me`: Shortcut into a grilling session for plan or design stress testing. Install: `python scripts/install-external-skills.py --skill grill-me --agent codex`.
- `grill-with-docs`: Stress-test a plan or design while maintaining docs, ADRs, and glossary context. Install: `python scripts/install-external-skills.py --skill grill-with-docs --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
