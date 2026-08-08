# Marketing — Operating Defaults & Routing Rules

Runtime-neutral policy for the Marketing plugin. These rules apply to every marketing skill and agent. Platform safety requirements and the user's explicitly authorized scope take precedence; narrower skills may add compatible channel detail but may not relax the authorization gates or contradict the ownership boundaries below.

## Department boundary

Marketing owns content creation, adaptation, distribution, SEO/AEO/GEO discoverability, social publishing, marketing-channel experiments, and growth visuals (slides, images, video). Product owns positioning, packaging, and pricing strategy; Finances validates pricing economics; Sales owns one-to-one prospect outreach and deal execution. Marketing communicates approved decisions and optimizes channel performance without taking over those decisions.

## Routing constraints

Route to the **narrowest** owning skill. The `content` router selects writing children; chain across creation → discoverability → distribution.

| Request shape | Route to |
| --- | --- |
| Net-new article, blog, narrative | `content`, `copywrite` |
| Make AI/stiff prose sound human | `humanizing` |
| Turn tickets/FAQs/objections into briefs | `context-to-content` |
| Turn source material into a structured course | `coursify` |
| One asset → many channel variants | `repurposing` |
| Republish/adapt finished content per channel | `syndication` |
| Keyword/topic research, SERP intent | `keywords`, `seo`, `technical-seo` |
| Answer-engine / generative-engine visibility | `aeo`, `geo`, `discoverability` |
| Social publishing strategy and routing | `social-media` |
| Platform posts | `x-posts`, `linkedin-posts` through `social-media` |
| Platform long-form | `x-articles`, `linkedin-articles` through `social-media` |
| Marketing-channel A/B tests, playbooks, and scorecards | `growth-engine` |
| Visuals, decks, motion | `images`, `slides`, `video`, `visualization`; `video` routes to official external framework skills |

Default chain for a campaign: `context-to-content` → `content`/`copywrite` → `humanizing` → channel skill → `syndication`. Default course chain: `coursify` → the minimum required teaching, content, media, or code-production skills.

## Operating defaults

- **Voice first.** Pull tone, audience, brand, and approved positioning facts from user-provided or workspace-local sources. Never invent positioning or claims.
- **No fabricated proof.** Do not cite stats, customers, awards, or quotes that are not in source material. Mark placeholders explicitly.
- **Match the channel.** Respect each platform's length, formatting, and hook conventions (see the per-channel reference docs).
- **Lead with the hook.** Earn the first line; cut throat-clearing intros and AI tells.
- **One CTA per asset** unless the format expects more.
- **Repurpose, don't duplicate.** When syndicating, set the canonical source and adapt the framing per channel rather than reposting verbatim.

## Authorization gates

The request may authorize content creation and local asset production. Confirm final content, account, audience, and timing at the point of action before publishing, sending, scheduling, or spending.

- **Publishing and sending**: draft by default. Posting to a public account, scheduling, or pushing to a CMS/newsletter requires explicit authorization for the final asset and destination.
- **Claims about the product, customers, security, or compliance**: must be verifiable and approved before they ship.
- **Competitor or comparison claims**: keep factual and sourced; flag anything that could be disparaging or legally sensitive.
- **Third-party tools**: uploading drafts or assets to external renderers/pastebins publishes them — confirm nothing sensitive is included.
- **Paid spend**: confirm the exact budget and destination and coordinate financial guardrails with the Finances plugin before committing spend.

## Quality bar

- Specific beats generic — concrete examples, numbers, and nouns over adjectives.
- Cut filler, hedges, and em-dash-laden AI cadence; read the asset aloud before shipping.
- Every distribution asset names its audience and intended action.
- Keep formatting clean for the target surface (no markdown artifacts where the platform won't render them).
