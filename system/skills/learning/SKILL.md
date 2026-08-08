---
name: learning
description: Router for lessons, teaching, and durable learning records.
---

# Learning Router

## Children

- [`lessons`](../lessons/SKILL.md) - Lessons work.

## Route

| Request | Use |
| --- | --- |
| lessons requests | [`lessons`](../lessons/SKILL.md) |

## Chain Rules

Chain to these skills when the task crosses this skill's boundary:

- `knowledge-base`
- `memory`
- `brain`
- `code-documentation`

## Operating Rules

- Keep this parent compact; use children for lane-specific execution depth.
- Prefer the child skill's bundled resources when a child owns the request.
- Preserve local skill rules, repo facts, safety gates, product/channel constraints, and explicit local exceptions over external guidance when they conflict.
- Use [`../../../references/docs/promotion-matrix.md`](../../../references/docs/promotion-matrix.md) to decide whether a durable learning belongs in `lessons/`, memory rules, `facts/`, `fixes/`, `knowledge/`, or a living owner doc.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `teach`: Create mission-grounded learning material, resources, records, and lessons. Install: `python3 scripts/install-external-skills.py --skill teach --agent codex`.
- `writing-great-skills`: Use external skill-authoring quality rules when creating or revising skills. Install: `python3 scripts/install-external-skills.py --skill writing-great-skills --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
