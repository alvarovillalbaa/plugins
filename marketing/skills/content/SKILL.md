---
name: content
description: Router for content creation, course design, adaptation, syndication, keyword work, and copy refinement.
---

# Content Router

## Children

- [`humanizing`](../humanizing/SKILL.md) - Humanizing work.
- [`repurposing`](../repurposing/SKILL.md) - Repurposing work.
- [`syndication`](../syndication/SKILL.md) - Syndication work.
- [`keywords`](../keywords/SKILL.md) - Keywords work.
- [`context-to-content`](../context-to-content/SKILL.md) - Context To Content work.
- [`coursify`](../coursify/SKILL.md) - Course design and multimodal production routing.
- [`copywrite`](../copywrite/SKILL.md) - Copywrite work.

## Route

| Request | Use |
| --- | --- |
| humanizing requests | [`humanizing`](../humanizing/SKILL.md) |
| repurposing requests | [`repurposing`](../repurposing/SKILL.md) |
| syndication requests | [`syndication`](../syndication/SKILL.md) |
| keywords requests | [`keywords`](../keywords/SKILL.md) |
| context to content requests | [`context-to-content`](../context-to-content/SKILL.md) |
| turn material into a course | [`coursify`](../coursify/SKILL.md) |
| copywrite requests | [`copywrite`](../copywrite/SKILL.md) |

## Chain Rules

Chain to these skills when the task crosses this skill's boundary:

- `discoverability`
- `social-media`
- `product-marketing`

## Operating Rules

- Keep this parent compact; use children for lane-specific execution depth.
- Prefer the child skill's bundled resources when a child owns the request.
- Preserve local skill rules, repo facts, safety gates, product/channel constraints, and explicit local exceptions over external guidance when they conflict.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `unslop`: Remove generic AI-writing tells while preserving meaning and voice. Install: `python3 scripts/install-external-skills.py --skill unslop --agent codex`.
- `stop-slop`: Apply stricter prose cleanup for predictable AI writing patterns. Install: `python3 scripts/install-external-skills.py --skill stop-slop --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
