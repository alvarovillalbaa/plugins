# Technical SEO Audit — {{SITE}}

- **Domain:** {{example.com}}
- **Date:** {{YYYY-MM-DD}}
- **Crawl tool / source:** {{Screaming Frog, Ahrefs Site Audit, Lighthouse, manual}}
- **Pages crawled:** {{n}}

## Severity Legend
🔴 critical (blocks indexing/ranking) · 🟡 important · 🟢 minor / polish

## 1. Crawlability & Indexation
| Check | Status | Severity | Notes |
| --- | --- | --- | --- |
| robots.txt correct (no over-blocking) | ☐ | | |
| XML sitemap present, fresh, referenced | ☐ | | |
| No noindex on important pages | ☐ | | |
| Canonical tags correct (self/cross) | ☐ | | |
| No redirect chains / loops | ☐ | | |
| 4xx / 5xx errors | ☐ | | {{count}} |
| Orphan pages | ☐ | | {{count}} |
| Pagination / faceted URLs controlled | ☐ | | |

## 2. Site Architecture & Internal Linking
- Click depth of key pages: {{}}
- Internal link distribution issues: {{}}
- URL structure consistency: {{}}

## 3. Performance (Core Web Vitals)
| Metric | Mobile | Desktop | Target |
| --- | --- | --- | --- |
| LCP | {{}} | {{}} | < 2.5s |
| INP | {{}} | {{}} | < 200ms |
| CLS | {{}} | {{}} | < 0.1 |
- Top offenders + cause: {{render-blocking JS, unoptimized images, ...}}
- Hand off heavy fixes to `frontend/performance`.

## 4. Structured Data
- Types implemented: {{}}
- Validation errors (Rich Results / schema.org): {{}}
- Missing opportunities: {{Article, FAQ, Product, Breadcrumb}}

## 5. Metadata & Rendering
- Title/meta uniqueness issues: {{count}}
- Server vs. client rendering of content: {{SSR/CSR — does crawler see content?}}
- Hreflang / i18n (if applicable): {{}}

## 6. Security / Hygiene
- HTTPS enforced, HSTS: ☐
- Mixed content: ☐
- Mobile-friendly / viewport: ☐

## Prioritized Remediation
| # | Issue | Severity | Owner | Effort | Est. impact |
| --- | --- | --- | --- | --- | --- |
| 1 | {{}} | 🔴 | | | |
| 2 | {{}} | 🟡 | | | |
| 3 | {{}} | 🟢 | | | |

## Re-crawl plan
- Re-crawl after fixes ship; confirm 🔴 items resolved before measuring rank impact.
