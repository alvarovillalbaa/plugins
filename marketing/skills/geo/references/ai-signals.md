# AI Signals: E-E-A-T, Trust, and GEO Credibility

External owner boundary:

- Use `unslop` and `stop-slop` for AI-writing tells, filler phrases, em dash rules, passive voice, rhythm, and prose cleanup.
- This file keeps GEO-specific trust and citation signals only.

## E-E-A-T

### Experience

Signals:

- original case studies, screenshots, or process notes
- specific numbers from real usage
- admitted limitations or failed attempts
- examples that could not be written without first-hand knowledge

Missing signals:

- generic claims
- stock-like visuals where original evidence is expected
- vague outcomes without scope, date, or mechanism

### Expertise

Signals:

- accurate domain terminology
- edge cases and common mistakes
- primary sources and official docs
- author credentials or body of work

### Authoritativeness

Signals:

- citations, backlinks, or mentions from recognized sources
- original research others cite
- expert interviews or community participation
- tools, datasets, or docs others use

### Trustworthiness

Signals:

- HTTPS
- accurate contact and about pages
- author attribution
- publication and update dates
- source citations for factual claims
- disclosure of sponsorship or affiliate relationships

Red flags:

- no author, date, or contact information
- unsupported claims
- inconsistent facts across pages
- stale content in current-year topics

## AI-specific citation signals

AI systems tend to cite:

- official documentation
- government and academic sources
- major publications
- peer-reviewed or institution-backed research
- established industry publications
- pages with named sources and dated claims

Lower citation probability:

- new or unknown domains
- content with no author/date/source trail
- thin content that appears generated
- claims without attribution

## Named source effect

Prefer named, dated, verifiable claims.

Weak:

> Studies show that marketers struggle with content consistency.

Stronger:

> According to HubSpot's 2024 State of Marketing Report, 68% of marketers cited content consistency as a primary challenge.

## Specificity signal

Prefer concrete mechanisms, numbers, examples, and timeframes.

Weak:

> SEO can improve traffic over time.

Stronger:

> After adding comparison pages for five high-intent queries, demo requests from organic search rose from 18 to 31 per month.

## Content trust audit

- [ ] author name visible
- [ ] author has relevant credentials or a clear first-hand role
- [ ] publication date visible
- [ ] last updated date visible when content changes
- [ ] key statistics cite named sources
- [ ] claims are accurate and verifiable
- [ ] screenshots or examples match the current product/tool state
- [ ] commercial relationships are disclosed
- [ ] prose has been cleaned with `unslop` or `stop-slop`
