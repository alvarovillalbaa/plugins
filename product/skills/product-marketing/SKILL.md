---
name: product-marketing
description: Router for product marketing, CRO, content-led growth, lead magnets, and buyer psychology.
---

# Product Marketing Router

## Children

- [`cro`](../cro/SKILL.md) - Cro work.
- [`content-led`](../content-led/SKILL.md) - Content Led work.
- [`lead-magnets`](../lead-magnets/SKILL.md) - Lead Magnets work.
- [`buyer-psychology`](../buyer-psychology/SKILL.md) - Buyer Psychology work.

## Route

| Request | Use |
| --- | --- |
| cro requests | [`cro`](../cro/SKILL.md) |
| content led requests | [`content-led`](../content-led/SKILL.md) |
| lead magnets requests | [`lead-magnets`](../lead-magnets/SKILL.md) |
| buyer psychology requests | [`buyer-psychology`](../buyer-psychology/SKILL.md) |

## Chain Rules

Chain to these skills when the task crosses this skill's boundary:

- `content`
- `discoverability`
- `go-to-market`
- `frontend`
- `reporting`

## Operating Rules

- Keep this parent compact; use children for lane-specific execution depth.
- Prefer the child skill's bundled resources when a child owns the request.
- Preserve local skill rules, repo facts, safety gates, product/channel constraints, and explicit local exceptions over external guidance when they conflict.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `hallmark`: Audit, redesign, study, or build UI with anti-AI-slop design constraints. Install: `python scripts/install-external-skills.py --skill hallmark --agent codex`.
- `browserbase-competitor-analysis`: Use browser-backed competitor analysis workflows for market and SEO comparisons. Install: `python scripts/install-external-skills.py --skill browserbase-competitor-analysis --agent codex`.
- `office-hours`: Use startup office-hours guidance for GTM, early customer, and product-market questions. Install: `python scripts/install-external-skills.py --skill office-hours --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
