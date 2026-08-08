---
name: sales-pipeline
description: Router for pipeline operations, commercial documents, collateral, and deal health work.
---

# Sales Pipeline Router

## Children

- [`commercial-docs`](../commercial-docs/SKILL.md) - Commercial Docs work.
- [`collateral`](../collateral/SKILL.md) - Collateral work.

## Route

| Request | Use |
| --- | --- |
| commercial docs requests | [`commercial-docs`](../commercial-docs/SKILL.md) |
| collateral requests | [`collateral`](../collateral/SKILL.md) |

## Chain Rules

Chain to these skills when the task crosses this skill's boundary:

- `go-to-market`
- `outreach`
- `growth`

## Operating Rules

- Keep this parent compact; use children for lane-specific execution depth.
- Prefer the child skill's bundled resources when a child owns the request.
- Preserve local skill rules, repo facts, safety gates, product/channel constraints, and explicit local exceptions over external guidance when they conflict.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `clous-object-management`: Use Clous-owned object management guidance for platform object workflows. Install: `python3 scripts/install-external-skills.py --skill clous-object-management --agent codex`.
- `clous-platform-operation`: Use Clous-owned platform operation guidance for runtime and workspace operations. Install: `python3 scripts/install-external-skills.py --skill clous-platform-operation --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
