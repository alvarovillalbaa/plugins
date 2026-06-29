---
name: outreach
description: Router for outbound and follow-up messaging across email, LinkedIn, and X.
---

# Outreach Router

## Children

- [`initial`](../initial/SKILL.md) - Initial work.
- [`sequence`](../sequence/SKILL.md) - Sequence work.
- [`follow-up`](../follow-up/SKILL.md) - Follow Up work.
- [`linkedin-dms`](../linkedin-dms/SKILL.md) - Linkedin Dms work.
- [`x-dms`](../x-dms/SKILL.md) - X Dms work.

## Route

| Request | Use |
| --- | --- |
| initial requests | [`initial`](../initial/SKILL.md) |
| sequence requests | [`sequence`](../sequence/SKILL.md) |
| follow up requests | [`follow-up`](../follow-up/SKILL.md) |
| linkedin dms requests | [`linkedin-dms`](../linkedin-dms/SKILL.md) |
| x dms requests | [`x-dms`](../x-dms/SKILL.md) |

## Chain Rules

Chain to these skills when the task crosses this skill's boundary:

- `prospect`
- `go-to-market/first-customers`
- `sales-pipeline`
- `personalize`

## Operating Rules

- Keep this parent compact; use children for lane-specific execution depth.
- Prefer the child skill's bundled resources when a child owns the request.
- Preserve local skill rules, repo facts, safety gates, product/channel constraints, and explicit local exceptions over external guidance when they conflict.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `unslop`: Remove generic AI-writing tells while preserving meaning and voice. Install: `python scripts/install-external-skills.py --skill unslop --agent codex`.
- `stop-slop`: Apply stricter prose cleanup for predictable AI writing patterns. Install: `python scripts/install-external-skills.py --skill stop-slop --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
