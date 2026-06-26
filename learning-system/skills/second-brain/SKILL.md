---
name: second-brain
description: >-
  Second-brain architecture skill with a raw-ingestion child for source
  ingestion and canonical promotion.
---

# Second Brain Router

This parent keeps shared methodology/default workflow ownership and routes specialized lanes to children.

## Children

- [`raw-ingestion`](../raw-ingestion/SKILL.md) - raw source ingestion, transcript or artifact parsing, canonical page promotion, unreadable-source preservation, and BRAIN.md-bound cleanup

## Route

| User asks for | Use |
| --- | --- |
| raw source ingestion, transcript or artifact parsing, canonical page promotion, unreadable-source preservation, and BRAIN.md-bound cleanup | [`raw-ingestion`](../raw-ingestion/SKILL.md) |

## Chain Rules

- `auto-improve/knowledge-base-improve`
- `code-documentation`
- `research`
- `reporting`

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
