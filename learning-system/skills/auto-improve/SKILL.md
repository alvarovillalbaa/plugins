---
name: auto-improve
description: >-
  Router for explicit skill eval loops, memory improvement, knowledge-base
  improvement, writing-style learning, and agent-doc drift review.
---

# Auto Improve Router

This parent is a router. Select the narrowest child and load that child before using lane-specific assets.

## Children

- [`skill-eval-loop`](../skill-eval-loop/SKILL.md) - skill evaluation loops, regression checks for skill behavior, prompt/skill mutation proposals, and explicit improvement gates
- [`memory-improve`](../memory-improve/SKILL.md) - memory audits, memory consolidation proposals, stale memory detection, retrieval quality checks, and explicit memory update workflows
- [`knowledge-base-improve`](../knowledge-base-improve/SKILL.md) - knowledge-base improvement, dedupe proposals, canonical page health, missing source promotion, and knowledge drift repair
- [`writing-style-learning`](../writing-style-learning/SKILL.md) - writing-style capture, approved-example analysis, sender or brand voice summaries, and reusable style constraints
- [`agent-doc-drift-review`](../agent-doc-drift-review/SKILL.md) - agent documentation drift review, instruction-file audits, stale doc detection, and owner-doc update recommendations

## Route

| User asks for | Use |
| --- | --- |
| skill evaluation loops, regression checks for skill behavior, prompt/skill mutation proposals, and explicit improvement gates | [`skill-eval-loop`](../skill-eval-loop/SKILL.md) |
| memory audits, memory consolidation proposals, stale memory detection, retrieval quality checks, and explicit memory update workflows | [`memory-improve`](../memory-improve/SKILL.md) |
| knowledge-base improvement, dedupe proposals, canonical page health, missing source promotion, and knowledge drift repair | [`knowledge-base-improve`](../knowledge-base-improve/SKILL.md) |
| writing-style capture, approved-example analysis, sender or brand voice summaries, and reusable style constraints | [`writing-style-learning`](../writing-style-learning/SKILL.md) |
| agent documentation drift review, instruction-file audits, stale doc detection, and owner-doc update recommendations | [`agent-doc-drift-review`](../agent-doc-drift-review/SKILL.md) |

## Chain Rules

- `memory-management`
- `second-brain`
- `code-documentation`
- `agentic-development/agent-harness-improvement`
- `message-outreach/sender-voice-calibration`

## Operating Rules

- Keep this `SKILL.md` small and routing-focused.
- Do not recreate the old broad parent behavior here; put execution depth in child assets.
- If no child matches, handle only shared methodology/default workflow or document the missing lane.
- Every child and parent skill must keep `examples/`, `hooks/`, `references/`, `scripts/`, and `templates/`.

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
