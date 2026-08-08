---
name: seo
description: Router for combined SEO and GEO optimization — on-page SEO, LLM discovery files, structured data, and AI referrer measurement. Routes narrow technical work to `technical-seo`.
---

# SEO

This skill owns on-page SEO and combined SEO + GEO optimization: headings, internal links, semantic coverage, snippet readiness, the 5-phase LLM SEO workflow, AI-crawler accessibility, discovery files, structured data, agent protocols, and AI traffic measurement.

## Use When

- The request spans both traditional SEO (crawlability, metadata, structured data) and AI/LLM discoverability (llms.txt, agent-card.json, GEO signals) in the same task.
- The parent router [`../discoverability/SKILL.md`](../discoverability/SKILL.md) selects this child for combined or full-site LLM SEO work.
- A site needs end-to-end optimization for both search engines and AI agents.
- A page needs heading, internal-link, semantic-coverage, snippet-readiness, metadata, or content-intent optimization.
- The task involves any of: llms.txt authoring, agent-card.json, OpenAPI exposure for AI agents, GA4 AI referrer tracking, or JSON-LD Speakable.

## Children

- [`technical-seo`](../technical-seo/SKILL.md) - Technical Seo work.

## Route

| Request | Use |
| --- | --- |
| On-page SEO, headings, internal links, semantic coverage, snippets, and page-level content optimization | Handle directly with this skill |
| technical seo requests | [`technical-seo`](../technical-seo/SKILL.md) |

## 5-Phase LLM SEO Workflow

Execute these phases in order for end-to-end LLM SEO optimization. Each phase builds on the previous.

### Phase 1 — Core SEO

- Configure `robots.txt` with explicit AI-crawler rules (allow or block by crawler name).
- Generate and submit `sitemap.xml`.
- Audit `<title>`, `<meta description>`, and Open Graph tags for completeness and keyword fit.

### Phase 2 — LLM Files

- Author `/llms.txt`: concise product overview (~1–2 KB), scannable bullets, prominent developer links, visible pricing, and an "Instructions for Large Language Models" section that steers AI behavior away from deprecated patterns.
- Author `/llms-full.txt`: extended reference for large-context LLMs — full API endpoint listing, MCP tools, auth guide, SDK examples, webhook schemas, changelog.
- Generate `llms-full.txt` programmatically from OpenAPI spec or MCP tool registry where possible; never hand-write a complete API reference.

Reference: [`references/llm-seo-five-phase-workflow.md`](references/llm-seo-five-phase-workflow.md) and [`../geo/references/llm-discovery-files.md`](../geo/references/llm-discovery-files.md).

### Phase 3 — Structured Data

- Implement JSON-LD Triple Schema Stacking (Organization + WebSite + primary entity type on every page).
- Add `speakable` markup to key answer blocks.
- Add `/.well-known/security.txt` (RFC 9116): `Contact`, `Expires`, `Canonical` fields. Signals trust to E-E-A-T and AI citation systems.

### Phase 4 — Agent Discovery

- Expose OpenAPI spec at a stable URL (`/api/openapi/public` or equivalent).
- Author `/.well-known/agent-card.json` (A2A protocol) with `description`, `skills[]`, and `authentication` fields written for AI agents, not humans.
- Author `/.well-known/ai-plugin.json` for backward compatibility (legacy ChatGPT plugin format).
- Author `/context7.json` at repo root for developer-tool indexing (Cursor, Claude Code, VS Code Copilot).
- Register MCP server with MCP Registry and PulseMCP if applicable.
- Submit to Context7 via `context7.com/add-library` if a library or SDK.

### Phase 5 — Measurement

- Set up GA4 custom dimensions or events to track AI referrers: `ChatGPT`, `Perplexity`, `Claude.ai`, `Gemini`, `Copilot`, and similar.
- Build a segment or report to isolate AI-origin sessions and conversions.
- Review quarterly; new AI crawlers and agent protocols emerge regularly.

## Assets

- `references/llm-seo-five-phase-workflow.md` — Phase-by-phase implementation guide.
- `references/content-optimization.md`, `references/content-patterns.md`, and `references/seo-checklist.md` — On-page workflow and review criteria.
- `references/core-eeat-benchmark.md`, `references/entity-optimizer.md`, and `references/measurement.md` — Evidence, entity, and measurement guidance.
- `references/` — Lane-specific guidance for combined SEO+GEO work.
- `scripts/` — Executable helpers (llms.txt generators, agent-card scaffolders).
- `templates/` — llms.txt, agent-card.json, context7.json starter templates.
- `examples/` — Sample outputs for each phase.

## Chain Rules

Chain to these skills when the task crosses this skill's boundary:

- `geo`
- `content`
- `product-marketing/cro`
- `frontend/performance`
- `reporting`

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `browserbase-search`: Web discovery tasks. Install: `python3 scripts/install-external-skills.py --skill browserbase-search --agent codex`.
- `browserbase-fetch`: Web retrieval tasks. Install: `python3 scripts/install-external-skills.py --skill browserbase-fetch --agent codex`.
- `browserbase-competitor-analysis`: Competitor SEO and AI visibility analysis. Install: `python3 scripts/install-external-skills.py --skill browserbase-competitor-analysis --agent codex`.
- `unslop`: Remove generic AI-writing tells while preserving meaning and voice. Install: `python3 scripts/install-external-skills.py --skill unslop --agent codex`.
- `stop-slop`: Stricter prose cleanup for predictable AI writing patterns. Install: `python3 scripts/install-external-skills.py --skill stop-slop --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
