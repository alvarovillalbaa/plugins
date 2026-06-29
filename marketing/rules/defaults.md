# Marketing — Operating Defaults & Routing Rules

Runtime-neutral policy for the marketing department plugin. Applies to every marketing skill and agent. Narrower skills add channel-specific detail; safety gates below always hold.

## Department boundary

Marketing owns content creation, adaptation, distribution, SEO/AEO/GEO discoverability, and growth visuals (slides, images, video). It does **not** own outbound sales sequences or 1:1 prospect outreach (route to `sales`), product positioning decisions (route to `product`), or pricing claims (route to `finances`). It packages and distributes the message; it does not own the deal.

## Routing constraints

Route to the **narrowest** owning skill. The `content` router selects writing children; chain across creation → discoverability → distribution.

| Request shape | Route to |
| --- | --- |
| Net-new article, blog, narrative | `content`, `copywrite` |
| Make AI/stiff prose sound human | `humanizing` |
| Turn tickets/FAQs/objections into briefs | `context-to-content` |
| One asset → many channel variants | `repurposing` |
| Republish/adapt finished content per channel | `syndication` |
| Keyword/topic research, SERP intent | `keywords`, `on-page-seo`, `technical-seo` |
| Answer-engine / generative-engine visibility | `aeo`, `geo`, `discoverability` |
| Platform posts | `x-posts`, `linkedin-posts` |
| Platform long-form | `x-articles`, `linkedin-articles` |
| Visuals, decks, motion | `images`, `slides`, `video`, `remotion`, `hyperframes`, `visualization` |

Default chain for a campaign: `context-to-content` → `content`/`copywrite` → `humanizing` → channel skill → `syndication`.

## Operating defaults

- **Voice first.** Pull tone, audience, and brand facts from repo-local voice/personalization documents. Never invent positioning or claims.
- **No fabricated proof.** Do not cite stats, customers, awards, or quotes that are not in source material. Mark placeholders explicitly.
- **Match the channel.** Respect each platform's length, formatting, and hook conventions (see the per-channel reference docs).
- **Lead with the hook.** Earn the first line; cut throat-clearing intros and AI tells.
- **One CTA per asset** unless the format expects more.
- **Repurpose, don't duplicate.** When syndicating, set the canonical source and adapt the framing per channel rather than reposting verbatim.

## Safety gates (require explicit human approval)

- **Publishing and sending**: posting to any public account, scheduling, or pushing to a CMS/newsletter. Draft and present; a human publishes.
- **Claims about the product, customers, security, or compliance**: must be verifiable and approved before they ship.
- **Competitor or comparison claims**: keep factual and sourced; flag anything that could be disparaging or legally sensitive.
- **Third-party tools**: uploading drafts or assets to external renderers/pastebins publishes them — confirm nothing sensitive is included.
- **Paid spend**: any budget, boost, or ad commitment goes to a human and coordinates with `finances`.

## Quality bar

- Specific beats generic — concrete examples, numbers, and nouns over adjectives.
- Cut filler, hedges, and em-dash-laden AI cadence; read it aloud test before shipping.
- Every distribution asset names its audience and intended action.
- Keep formatting clean for the target surface (no markdown artifacts where the platform won't render them).
