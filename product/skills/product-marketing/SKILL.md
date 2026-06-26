---
name: product-marketing
description: >-
  Router for positioning/messaging, CRO, conversion copywriting, content-led
  marketing, lead magnets, and buyer psychology.
---

# Product Marketing Router

This parent is a router. Select the narrowest child and load that child before using lane-specific assets.

## Children

- [`positioning-messaging`](../positioning-messaging/SKILL.md) - positioning, messaging, ICP/persona framing, differentiation, objection handling, and proof-point structure
- [`cro`](../cro/SKILL.md) - conversion-rate optimization for pages and funnels, page diagnostics, CTA promises, proof placement, and test ideas
- [`conversion-copywriting`](../conversion-copywriting/SKILL.md) - market-facing conversion copy tied to positioning, buyer psychology, landing pages, objections, and proof
- [`content-led-marketing`](../content-led-marketing/SKILL.md) - content strategy, editorial themes, distribution logic, thought leadership systems, and demand-generation content plans
- [`lead-magnets`](../lead-magnets/SKILL.md) - lead magnet strategy, survey/report assets, downloadable offers, gated assets, and nurture entry points
- [`buyer-psychology`](../buyer-psychology/SKILL.md) - buyer psychology, motivation mapping, emotional triggers, objection logic, decision criteria, and persuasion risk review

## Route

| User asks for | Use |
| --- | --- |
| positioning, messaging, ICP/persona framing, differentiation, objection handling, and proof-point structure | [`positioning-messaging`](../positioning-messaging/SKILL.md) |
| conversion-rate optimization for pages and funnels, page diagnostics, CTA promises, proof placement, and test ideas | [`cro`](../cro/SKILL.md) |
| market-facing conversion copy tied to positioning, buyer psychology, landing pages, objections, and proof | [`conversion-copywriting`](../conversion-copywriting/SKILL.md) |
| content strategy, editorial themes, distribution logic, thought leadership systems, and demand-generation content plans | [`content-led-marketing`](../content-led-marketing/SKILL.md) |
| lead magnet strategy, survey/report assets, downloadable offers, gated assets, and nurture entry points | [`lead-magnets`](../lead-magnets/SKILL.md) |
| buyer psychology, motivation mapping, emotional triggers, objection logic, decision criteria, and persuasion risk review | [`buyer-psychology`](../buyer-psychology/SKILL.md) |

## Chain Rules

- `content-writing`
- `seo-and-geo`
- `go-to-market`
- `frontend`
- `reporting`

## Operating Rules

- Keep this `SKILL.md` small and routing-focused.
- Do not recreate the old broad parent behavior here; put execution depth in child assets.
- If no child matches, handle only shared methodology/default workflow or document the missing lane.
- Every child and parent skill must keep `examples/`, `hooks/`, `references/`, `scripts/`, and `templates/`.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
