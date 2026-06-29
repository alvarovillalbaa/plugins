# AEO Audit Report — {{PAGE_OR_SITE}}

- **Audited URL:** {{URL}}
- **Date:** {{YYYY-MM-DD}}
- **Target queries:** {{primary question(s) this page should answer}}
- **Auditor:** {{name / agent}}

## Score Summary

| Dimension | Status | Notes |
| --- | --- | --- |
| Structured data (FAQPage/HowTo/Article) | ☐ pass / ☐ fail | |
| Direct-answer block in first 100 words | ☐ pass / ☐ fail | |
| Question-shaped H2/H3 headings | ☐ pass / ☐ fail | |
| Entity clarity (defined terms, no ambiguous pronouns) | ☐ pass / ☐ fail | |
| Concise answer length (40–60 words per Q) | ☐ pass / ☐ fail | |
| Source/authority signals (author, date, citations) | ☐ pass / ☐ fail | |

## Findings

### 1. Structured data
- Detected JSON-LD types: {{list from check_schema_markup.py}}
- Gaps: {{missing FAQPage / HowTo / Article}}
- Fix: {{add schema using templates/faq-schema-template.json}}

### 2. Answer blocks
- {{Which questions currently lack a concise, self-contained answer}}
- Fix: {{rewrite to lead with the answer, one detail sentence, no preamble}}

### 3. Question coverage
- Questions a user actually asks but the page does not answer: {{list}}
- Source for the gap list: {{People Also Ask / support tickets / context-to-content}}

### 4. Entity & wording
- {{Ambiguous terms, undefined acronyms, vague pronouns to fix}}

## Prioritized Actions

| # | Action | Effort | Expected impact |
| --- | --- | --- | --- |
| 1 | {{}} | S/M/L | High/Med/Low |
| 2 | {{}} | | |
| 3 | {{}} | | |

## Re-test plan
- Re-run `scripts/check_schema_markup.py {{URL}}` after changes.
- Re-check featured-snippet / AI-answer capture in {{2–4 weeks}}.
