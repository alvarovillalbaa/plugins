# Context-to-Content Reference

Reference for turning raw company context — support tickets, customer questions, sales objections, internal FAQs — into content briefs and help articles. The premise: your support queue and sales calls are a free, demand-validated content backlog. Pull voice and product facts from repo-local personalization docs.

## Why these sources are gold

Every repeated question is proof of search demand and a content gap. Unlike brainstormed topics, these come pre-validated:
- **Support tickets** → real friction, real language, real frequency.
- **Sales objections** → bottom-funnel, buying-intent topics.
- **Customer questions** (calls, community, chat) → the exact phrasing people search.
- **Internal FAQs / onboarding docs** → repeatable explanations worth publishing.

## Intake → triage

1. **Collect** a batch of raw inputs (last 30–90 days of tickets/questions).
2. **Cluster** by underlying question, not by ticket wording. Ten tickets about "can't log in after SSO change" = one topic.
3. **Count frequency** per cluster — frequency is your priority signal.
4. **Tag intent**: informational (how/what/why), navigational (where), transactional/commercial (which/vs/pricing), or troubleshooting.
5. **Map to funnel stage**: awareness (broad how/why), consideration (comparisons, objections), decision (setup, pricing, migration), retention (advanced usage, troubleshooting).

## Scoring which to write first

| Factor | High priority when… |
| --- | --- |
| Frequency | Asked often (recurring ticket driver) |
| Deflection value | A good article removes repeat support load |
| Search demand | The cluster maps to real query volume |
| Buying influence | Objection blocks deals; answering unblocks revenue |
| Effort | Answer is stable and self-contained |

Quick score: `(frequency + deflection + buying influence) / effort`. Write the cheap, high-frequency, deal-or-ticket-reducing ones first.

## From cluster to content brief

A brief is the contract handed to a writer (human or skill). Include:

- **Working title** — uses the searcher's words, not internal jargon.
- **Primary question** — the one job this piece does.
- **Search intent + funnel stage** — from triage.
- **Audience** — who asks this and what they already know.
- **Source evidence** — the actual tickets/quotes/objections (verbatim language to mirror).
- **Key points to cover** — the answer skeleton, derived from how support actually resolves it.
- **What success looks like** — deflects the ticket / overcomes the objection / ranks for the query.
- **Format** — help-center article, blog post, FAQ entry, or sales one-pager.
- **CTA / next step** — where the reader goes after.
- **Related/linkable content** — internal links, canonical owner.

## Writing the help article

Structure for scanning and self-service:
- **Lead with the direct answer** (inverted pyramid) — searchers want resolution, not buildup.
- **Mirror the user's language** in the title and first line so it matches their search and feels addressed.
- **Steps as numbered lists**; concepts as short paragraphs with descriptive H2/H3s.
- **Cover the edge cases** the tickets revealed — that's the difference between an article and a deflecting article.
- **One clear outcome per article.** Split multi-question tickets into multiple pieces.
- **Add prerequisites and "if this doesn't work" fallbacks** so it stands alone.

## Turning objections into content

Sales objections are decision-stage SEO and enablement gold:
- "It's too expensive" → ROI/TCO article or calculator.
- "We already use [competitor]" → honest comparison / migration guide.
- "Will it integrate with X?" → integration doc.
- "Is it secure/compliant?" → security/trust page.
Answer the objection honestly and specifically; vague reassurance converts no one. These double as sales collateral — coordinate with the `sales` collateral lane.

## Quality gates

- **Accuracy first** — verify the answer against current product behavior; a wrong help article erodes trust and creates *more* tickets.
- **No fabricated specifics** — don't invent steps, settings, or limits; mark unknowns for SME review.
- **Keep it current** — context-derived content drifts as the product changes; flag for the documentation-drift lane on releases.
- **Don't over-optimize** — write for the human with the problem first, the search engine second.

## Handoffs

- SEO optimization / keyword targeting → `seo`, `keywords`.
- Generative/answer-engine visibility → `geo`, `aeo`.
- Distribution beyond the help center → `social-media`, `syndication`.
- Sales-facing versions of objection content → `sales` collateral.
