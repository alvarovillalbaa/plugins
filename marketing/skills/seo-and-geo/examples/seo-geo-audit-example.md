# Example: Full 5-phase LLM SEO workflow for a SaaS product

**Scenario:** "Tracebin", an error-tracking SaaS, wants both classic organic
traffic and AI-engine citations for its docs and product pages.

## Phase 0 — Baseline

```
$ python scripts/check_ai_discovery.py https://tracebin.example
[FAIL] llms.txt  (not found)
[FAIL] agent-card.json  (not found)
[ok ] robots.txt
Overall: NEEDS WORK -> llms.txt, agent-card.json
```

Organic baseline (from analytics): 18k monthly organic sessions, 0 measurable
AI-referrer sessions. Canonical domain: `tracebin.example` (apex, www redirects).

## Phase 1 — Core SEO

Route the narrow lanes to children:
- `on-page-seo`: fix title tags, H1/H2 structure, internal links on the top 20
  pages. Found 6 pages with duplicate titles and 3 orphan pages.
- `technical-seo`: sitemap.xml stale (missing 40 docs URLs), 12 pages with
  Core Web Vitals LCP > 4s. File issues and fix.

## Phase 2 — LLM files

Generate `llms.txt` from the docs README:

```
$ python scripts/generate_llms_txt.py docs/README.md \
    --base-url https://tracebin.example -o public/llms.txt
wrote public/llms.txt
```

Hand-curate it down to the 12 highest-signal URLs. Add a `llms-full.txt` that
inlines the core-concepts and quickstart content for engines that fetch it.

## Phase 3 — Structured data

- Add `Article` + `BreadcrumbList` JSON-LD to all blog/docs pages.
- Add `SoftwareApplication` JSON-LD to the product page (with `offers` pricing).
- Add `FAQPage` to the pricing and integrations pages.
- Verify with the `aeo` skill's `check_schema_markup.py`.

## Phase 4 — Agent discovery

Publish `/.well-known/agent-card.json` (from `templates/agent-card-template.json`)
describing Tracebin's public API capabilities. Also expose:
- `openapi.json` linked from the docs.
- An MCP server entry / Context7 registration so coding agents can pull docs.

```
$ python scripts/check_ai_discovery.py https://tracebin.example
[ok ] llms.txt
[ok ] llms-full.txt
[ok ] agent-card.json  (.well-known/agent-card.json)
[ok ] robots.txt
Overall: PASS
```

## Phase 5 — AI-referrer measurement

- Add referrer classification in analytics for `chatgpt.com`, `perplexity.ai`,
  `gemini.google.com`, etc.
- Set up a weekly query panel: track citation presence for 15 goal prompts.
- Define success: AI-referrer sessions and # of goal prompts where Tracebin is
  cited.

## Results (10 weeks)

| Metric | Before | After |
| --- | --- | --- |
| Organic sessions / mo | 18,000 | 24,500 |
| AI-referrer sessions / mo | ~0 | 1,300 |
| Goal prompts citing Tracebin | 1/15 | 9/15 |
| Pages with valid structured data | 12% | 95% |

## Takeaways

1. Do core SEO first — AI engines still lean on classic crawlability and links.
2. `llms.txt` + structured data + agent-card together compound; one alone is weak.
3. You can't claim GEO wins without phase-5 measurement wired up before phase 1.
