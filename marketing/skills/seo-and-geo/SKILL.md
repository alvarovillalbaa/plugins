---
name: seo-and-geo
description: >-
  Router for technical SEO audits, on-page SEO optimization, AEO answer
  optimization, GEO/AI discoverability, and SEO competitor gap audits.
---

# SEO And GEO Router

This parent is a router. Select the narrowest child and load that child before using lane-specific assets.

## Children

- [`technical-seo-audits`](../technical-seo-audits/SKILL.md) - technical SEO audits, crawlability, robots, sitemaps, metadata implementation, structured data, and web performance constraints
- [`on-page-seo-optimization`](../on-page-seo-optimization/SKILL.md) - on-page SEO, headings, internal links, semantic coverage, snippet readiness, and page-level content optimization
- [`aeo-answer-optimization`](../aeo-answer-optimization/SKILL.md) - answer-engine optimization, FAQ coverage, concise answer blocks, entity clarity, and question-oriented content structure
- [`geo-ai-discoverability`](../geo-ai-discoverability/SKILL.md) - GEO and AI discoverability, quotable blocks, citation readiness, LLM visibility, and AI search content structure
- [`seo-competitor-gap-audit`](../seo-competitor-gap-audit/SKILL.md) - SEO competitor gap audits, SERP comparison, content gap analysis, authority benchmarking, and opportunity prioritization

## Route

| User asks for | Use |
| --- | --- |
| technical SEO audits, crawlability, robots, sitemaps, metadata implementation, structured data, and web performance constraints | [`technical-seo-audits`](../technical-seo-audits/SKILL.md) |
| on-page SEO, headings, internal links, semantic coverage, snippet readiness, and page-level content optimization | [`on-page-seo-optimization`](../on-page-seo-optimization/SKILL.md) |
| answer-engine optimization, FAQ coverage, concise answer blocks, entity clarity, and question-oriented content structure | [`aeo-answer-optimization`](../aeo-answer-optimization/SKILL.md) |
| GEO and AI discoverability, quotable blocks, citation readiness, LLM visibility, and AI search content structure | [`geo-ai-discoverability`](../geo-ai-discoverability/SKILL.md) |
| SEO competitor gap audits, SERP comparison, content gap analysis, authority benchmarking, and opportunity prioritization | [`seo-competitor-gap-audit`](../seo-competitor-gap-audit/SKILL.md) |

## Chain Rules

- `content-writing`
- `product-marketing/cro`
- `frontend/frontend-performance-accessibility`
- `reporting`

## Operating Rules

- Keep this `SKILL.md` small and routing-focused.
- Do not recreate the old broad parent behavior here; put execution depth in child assets.
- If no child matches, handle only shared methodology/default workflow or document the missing lane.
- Every child and parent skill must keep `examples/`, `hooks/`, `references/`, `scripts/`, and `templates/`.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
