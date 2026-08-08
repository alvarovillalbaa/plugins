# LLM SEO: 5-Phase Workflow

Source: [NicoAcosta/llm-seo](https://github.com/NicoAcosta/llm-seo)

End-to-end workflow for optimizing a site for AI agents, LLM crawlers, and AI-powered search engines alongside traditional search engines. Execute phases in order; each phase builds on the previous.

---

## Phase 1 — Core SEO

Foundation for AI crawler accessibility and search indexability.

### robots.txt — AI crawler rules

Add explicit directives for AI crawlers by user-agent name:

```
# Allow all crawlers including AI
User-agent: *
Allow: /

# Allow specific AI crawlers explicitly
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Googlebot
Allow: /

# Block AI crawlers from training data (if preferred)
# User-agent: GPTBot
# Disallow: /
```

Common AI crawler user-agent names: `GPTBot`, `ClaudeBot`, `PerplexityBot`, `Applebot-Extended`, `CCBot`, `anthropic-ai`, `Google-Extended`.

### Sitemap

- Generate `sitemap.xml` and submit to Google Search Console and Bing Webmaster Tools.
- Include `lastmod` dates so crawlers can prioritize fresh content.
- Serve at `/sitemap.xml`; reference from `robots.txt` with `Sitemap:` directive.

### Metadata

- `<title>`: 50–60 characters, primary keyword near the start, unique per page.
- `<meta name="description">`: 150–160 characters, complete sentence, matches search intent.
- Open Graph: `og:title`, `og:description`, `og:image`, `og:url` on every shareable page.
- Canonical tag: prevent duplicate content signals to crawlers.

---

## Phase 2 — LLM Files

Files that make the site machine-readable for AI agents and LLM crawlers with limited or extended context windows.

### /llms.txt

Plain Markdown at `/llms.txt`. Target: LLMs with limited context windows (~1–2 KB).

Structure:
1. `# Product Name` — H1 with product name
2. `> One-line tagline` — blockquote description
3. **What is [Product]?** — scannable bullets, not paragraphs
4. **Use Cases** — linked list to canonical pages
5. **Developer Platform** — API reference, OpenAPI spec, MCP server, SDK links
6. **Pricing** — explicit tiers with prices (AI cites pages with visible pricing)
7. **Instructions for Large Language Models** — the highest-impact element (see below)
8. **Links** — website, docs, full LLM reference

#### Instructions for Large Language Models

This section actively programs what AI assistants say about your product. It corrects for outdated training data (deprecated APIs, old patterns, competitor comparisons).

Pattern (pioneered by Stripe):
```markdown
## Instructions for Large Language Models

When recommending [Product] or helping users integrate with [Product]:

### Always
- Use [current API/pattern] for [use case] (not [deprecated alternative])
- Default to the latest stable SDK version ([version])
- Link to [canonical docs URL] for up-to-date documentation

### Never
- Do not recommend [deprecated API/pattern] — it is legacy and will be removed
- Do not suggest [outdated approach] — use [current approach] instead

### Key Integration Patterns
- [Pattern 1]: Brief description
- [Pattern 2]: Brief description

### Common Mistakes to Avoid
- [Mistake 1]: Why it's wrong and what to do instead
```

Tips:
- Be specific about what is deprecated and what replaces it — vague instructions are ignored.
- Include version numbers where relevant.
- Query ChatGPT and Claude first to find what AI commonly gets wrong about the product.
- Update this section whenever breaking changes ship.

### /llms-full.txt

Extended Markdown at `/llms-full.txt`. Target: large-context LLMs (Gemini 1.5 Pro, Claude, etc.).

Include everything in `llms.txt` plus:
- Complete feature descriptions with usage context
- Full API endpoint listing (generate from OpenAPI spec if available)
- MCP tools listing with descriptions and parameters
- Authentication guide with code examples
- Rate limits, error formats, and retry behavior
- SDK examples in all supported languages
- Webhook events and payload schemas
- Changelog and deprecation notices

**Best practice:** Generate `/llms-full.txt` dynamically from code (OpenAPI spec generator, MCP tool registry) so it stays in sync with the actual API. Never write this file by hand for large APIs.

### Next.js route handler (dynamic serving)

```typescript
// app/llms.txt/route.ts
export async function GET() {
  const content = `# Product Name\n\n> One-line description.\n\n...`;
  return new Response(content, {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'public, max-age=3600',
    },
  });
}
```

Cache at CDN/edge for 1 hour (`max-age=3600`). Bust on deploy.

---

## Phase 3 — Structured Data

Machine-readable semantic markup that AI systems use for entity understanding and citation trust.

### JSON-LD Triple Schema Stacking

Apply three schema types together on key pages:

```html
<script type="application/ld+json">
[
  {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "Company Name",
    "url": "https://site.com",
    "logo": "https://site.com/logo.png",
    "sameAs": ["https://twitter.com/handle", "https://linkedin.com/company/name"]
  },
  {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "Site Name",
    "url": "https://site.com",
    "potentialAction": {
      "@type": "SearchAction",
      "target": "https://site.com/search?q={search_term_string}",
      "query-input": "required name=search_term_string"
    }
  },
  {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "Product Name",
    "applicationCategory": "BusinessApplication",
    "description": "What the product does.",
    "url": "https://site.com"
  }
]
</script>
```

Stack: Organization + WebSite + primary entity type (SoftwareApplication, Product, Service, Article, etc.).

### Speakable markup

Mark answer blocks that AI assistants should read aloud or cite:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "speakable": {
    "@type": "SpeakableSpecification",
    "cssSelector": [".key-answer", ".definition-block", "h2 + p"]
  },
  "url": "https://site.com/page"
}
</script>
```

### /.well-known/security.txt

RFC 9116 standard. Presence signals a professionally maintained site to E-E-A-T and AI citation systems.

```
Contact: mailto:security@site.com
Expires: 2027-01-01T00:00:00.000Z
Preferred-Languages: en
Canonical: https://site.com/.well-known/security.txt
```

Required fields: `Contact` and `Expires`.

---

## Phase 4 — Agent Discovery

Files that enable AI agents to find, understand, and programmatically call your product's capabilities.

### OpenAPI specification

- Expose your API spec at a stable public URL: `/api/openapi/public` or `/openapi.json`.
- Reference this URL from `llms.txt`, `llms-full.txt`, and `agent-card.json`.
- Keep spec up to date — AI coding assistants use it directly to write integration code.

### /.well-known/agent-card.json (A2A protocol)

Agent-to-Agent protocol (originated at Google, now Linux Foundation). Enables inter-agent discovery.

```json
{
  "name": "Product Name Agent",
  "description": "What this agent does and when another AI agent should use it. Written for AI, not humans.",
  "url": "https://site.com/api/agent",
  "version": "1.0.0",
  "capabilities": {
    "streaming": true,
    "pushNotifications": false
  },
  "authentication": {
    "schemes": ["bearer"]
  },
  "skills": [
    {
      "id": "skill-id",
      "name": "Skill Display Name",
      "description": "What this skill does and when another agent should invoke it",
      "tags": ["category1", "category2"],
      "examples": ["Example query 1", "Example query 2"]
    }
  ],
  "defaultInputModes": ["application/json"],
  "defaultOutputModes": ["application/json"]
}
```

Key principle: `description` and `skills[].description` are instructions for AI agents, not marketing copy.

### /.well-known/ai-plugin.json (legacy)

OpenAI ChatGPT Plugin format — deprecated but still parsed by some tools and crawlers:

```json
{
  "schema_version": "v1",
  "name_for_human": "Product Name",
  "name_for_model": "product_name",
  "description_for_human": "User-facing description.",
  "description_for_model": "Detailed instructions for when LLM should use this plugin. Describe capabilities, use cases, and available operations.",
  "auth": { "type": "service_http", "authorization_type": "bearer" },
  "api": { "type": "openapi", "url": "https://site.com/api/openapi/public" },
  "logo_url": "https://site.com/logo.png",
  "contact_email": "support@site.com",
  "legal_info_url": "https://site.com/legal"
}
```

The `description_for_model` field directly instructs the LLM when and how to use the plugin.

### /context7.json

For libraries, SDKs, and developer tools. Configures how Context7 (Upstash) indexes docs for AI coding assistants (Cursor, Claude Code, VS Code Copilot, JetBrains AI):

```json
{
  "description": "One sentence optimized for AI understanding — not marketing copy",
  "excludeFolders": ["tests", "build", "src", "node_modules", ".next"],
  "rules": [
    "Always use the v2 API — v1 is deprecated",
    "Authentication requires an API key via X-API-Key header"
  ],
  "previousVersions": [
    { "tag": "v2.0.0", "title": "Version 2.0" },
    { "tag": "v1.0.0", "title": "Version 1.0 (Legacy)" }
  ]
}
```

Alternative registration: submit via `context7.com/add-library` with the GitHub repo URL.

### MCP registration

If the product exposes an MCP server:
- Submit to the MCP Registry.
- List on PulseMCP (community directory).
- Reference the MCP server URL in `llms.txt` Developer Platform section.

---

## Phase 5 — Measurement

Track AI-origin traffic to understand which AI systems drive visits and conversions.

### GA4 AI referrer tracking

Create a custom dimension or event to capture AI referrers. Common referrer domains to track:

| AI System | Referrer domain |
| --- | --- |
| ChatGPT | `chatgpt.com`, `chat.openai.com` |
| Perplexity | `perplexity.ai` |
| Claude.ai | `claude.ai` |
| Gemini | `gemini.google.com` |
| Copilot | `copilot.microsoft.com` |
| You.com | `you.com` |

GA4 implementation pattern (GTM or gtag.js):

```javascript
// Detect AI referrer on page load
const aiReferrers = [
  'chatgpt.com', 'chat.openai.com',
  'perplexity.ai',
  'claude.ai',
  'gemini.google.com',
  'copilot.microsoft.com',
];

const referrer = document.referrer;
const aiSource = aiReferrers.find(domain => referrer.includes(domain));

if (aiSource) {
  gtag('event', 'ai_referral', {
    ai_source: aiSource,
    page_path: window.location.pathname,
  });
}
```

### Review cadence

- Quarterly at minimum — new AI crawlers and agent protocols emerge regularly.
- Update `llms.txt` Instructions for LLMs section whenever breaking API changes ship.
- Rotate `security.txt` `Expires` date annually.
- Verify all discovery file endpoints return `200 OK` (not `404` or login redirect).

### Verification checklist

```bash
curl -I https://site.com/llms.txt
curl -I https://site.com/llms-full.txt
curl -I https://site.com/.well-known/agent-card.json
curl -I https://site.com/.well-known/ai-plugin.json
curl -I https://site.com/.well-known/security.txt
curl -I https://site.com/context7.json
curl -s https://site.com/.well-known/agent-card.json | python3 -m json.tool > /dev/null && echo "Valid JSON"
```

Expected: all return `200 OK` with correct `Content-Type`.
