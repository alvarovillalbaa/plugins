---
name: content-writing
description: >-
  Router for humanizing, repurposing/syndication, keywords, content audit,
  support-to-content, and copywriting.
---

# Content Writing Router

This parent is a router. Select the narrowest child and load that child before using lane-specific assets.

## Children

- [`humanizing`](../humanizing/SKILL.md) - rewriting AI-like or stiff prose into human, specific, voice-aligned writing while preserving meaning
- [`repurposing-syndication`](../repurposing-syndication/SKILL.md) - turning one source asset into channel-specific posts, newsletters, articles, and distribution packs
- [`keywords`](../keywords/SKILL.md) - keyword discovery, search intent mapping, opportunity scoring, topic clusters, and content calendar inputs
- [`content-audit`](../content-audit/SKILL.md) - content audits, quality checks, decay diagnosis, content refresh plans, and publishing quality gates
- [`support-to-content`](../support-to-content/SKILL.md) - turning support tickets, customer questions, sales objections, and internal FAQs into content briefs and help articles
- [`copywriting`](../copywriting/SKILL.md) - editorial and general-purpose copywriting that is not in-product UX copy or conversion-owned product marketing copy

## Route

| User asks for | Use |
| --- | --- |
| rewriting AI-like or stiff prose into human, specific, voice-aligned writing while preserving meaning | [`humanizing`](../humanizing/SKILL.md) |
| turning one source asset into channel-specific posts, newsletters, articles, and distribution packs | [`repurposing-syndication`](../repurposing-syndication/SKILL.md) |
| keyword discovery, search intent mapping, opportunity scoring, topic clusters, and content calendar inputs | [`keywords`](../keywords/SKILL.md) |
| content audits, quality checks, decay diagnosis, content refresh plans, and publishing quality gates | [`content-audit`](../content-audit/SKILL.md) |
| turning support tickets, customer questions, sales objections, and internal FAQs into content briefs and help articles | [`support-to-content`](../support-to-content/SKILL.md) |
| editorial and general-purpose copywriting that is not in-product UX copy or conversion-owned product marketing copy | [`copywriting`](../copywriting/SKILL.md) |

## Chain Rules

- `seo-and-geo/geo-ai-discoverability`
- `seo-and-geo/on-page-seo-optimization`
- `social-media-management`
- `product-marketing`

## Operating Rules

- Keep this `SKILL.md` small and routing-focused.
- Do not recreate the old broad parent behavior here; put execution depth in child assets.
- If no child matches, handle only shared methodology/default workflow or document the missing lane.
- Every child and parent skill must keep `examples/`, `hooks/`, `references/`, `scripts/`, and `templates/`.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `unslop`: Remove AI tells from prose while preserving meaning and voice. Install: `python scripts/install-external-skills.py --skill unslop --agent codex`.
- `stop-slop`: Apply stricter prose cleanup for predictable AI writing patterns. Install: `python scripts/install-external-skills.py --skill stop-slop --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
