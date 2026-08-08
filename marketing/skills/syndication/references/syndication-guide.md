# Syndication Guide

Reference for adapting finished content for channel-specific distribution: reposting, newsletters, social, and campaign syndication. Syndication = republishing the same core content on additional platforms to extend reach. Done right, it grows audience; done wrong, it splits SEO equity or triggers duplicate-content issues. Pull channel and brand facts from repo-local docs.

## Core concepts

- **Canonical URL** — the single authoritative version of a piece. Every syndicated copy should point search engines back to it so the original keeps the ranking credit.
- **First-publish vs. syndicate** — publish on the property you most want to rank (usually your owned domain), *then* syndicate elsewhere.
- **Adaptation** — even when reusing the same content, tailor the framing, intro, and CTA to each platform's audience.

## Syndication targets

| Target | Reach character | Canonical handling |
| --- | --- | --- |
| **Owned blog/domain** | SEO home base; publish first | Is the canonical |
| **Medium** | Built-in audience, discovery | Use Medium's import tool → sets `rel=canonical` to your URL |
| **Dev.to / Hashnode** | Developer reach | Native canonical-URL field — always set it |
| **LinkedIn article/newsletter** | Professional reach, subscribers | No true canonical; publish a teaser + link, or accept it as a distinct version |
| **Substack / newsletter** | Owned subscriber list, email | Newsletter section links to canonical |
| **Reddit / community forums** | Niche, high-intent (post natively, link sparingly) | Value-first; link only where allowed |
| **Industry publications / guest posts** | Authority + backlinks | Request `rel=canonical` or a do-follow link to your original |
| **Content aggregators / partner networks** | Volume reach | Ensure canonical or at least attribution |

## Canonical & SEO discipline

- **Always set `rel=canonical`** on syndicated copies pointing to your original. This tells Google which version to rank and avoids duplicate-content dilution.
- If a platform won't let you set canonical, prefer publishing a **distinct version** (different intro, trimmed, reframed) rather than a verbatim copy.
- **Publish-then-syndicate with a delay** — let search engines index your original first (days, not minutes) before copies appear.
- **Link back** from every syndicated copy to the original (drives referral traffic + signals source).
- Never syndicate content you don't want competing with your own ranking without a canonical.

## Per-channel adaptation

Even "the same" content gets channel-fit treatment:
- **Intro/hook** — rewrite the opening for the platform's audience and scroll behavior.
- **Length** — trim for attention-spans (full article on blog, condensed on Medium, teaser on LinkedIn).
- **Formatting** — match native conventions (Markdown on dev.to, rich text on LinkedIn, plain on Reddit).
- **CTA** — platform-appropriate (subscribe in newsletter, comment on social, read-more link to canonical).
- **Tags/metadata** — use each platform's tagging system for discovery.

## Newsletter syndication

- Repurpose published content into newsletter sections; link to the canonical for the full piece.
- Lead with a personal/contextual intro — newsletters are intimate; don't paste a cold article.
- Segment if the list spans audiences; tailor framing.
- Consistent cadence and a clear theme retain subscribers better than volume.

## Campaign syndication

When pushing one campaign across many channels at once:
1. Define the **core message + canonical asset**.
2. Build a **per-channel matrix**: channel × format × hook × CTA × timing.
3. **Stagger** posting so the campaign sustains over days, not a single spike.
4. **Track** with UTM parameters per channel to attribute traffic.
5. Keep the message consistent but the packaging native to each channel.

## Reposting your own content

- **Evergreen recycling** — re-syndicate timeless pieces every few months with a fresh hook.
- **Vary the angle** — same content, new framing, so it doesn't read as a repeat to overlapping audiences.
- **Repost native formats** (carousels, threads) rather than links where platforms reward on-platform content.

## Quality & compliance gates

- **Respect canonical/attribution** — misattributed or canonical-less duplication harms SEO and looks like scraping.
- **Honor platform rules** — some forbid verbatim cross-posting or links; read the room (especially Reddit/communities).
- **No spammy blasting** — syndication is targeted reach, not spray. Match the audience to the platform.
- **Keep facts intact** — adaptation changes framing, not truth.
- **Publishing is human-gated** — present the syndication plan and drafts; a human posts.

## Handoffs

- Producing the channel variants → `repurposing`.
- Channel-native drafting → `linkedin-posts/articles`, `x-posts/articles`, `social-media`.
- Search optimization of the canonical → `seo`, `technical-seo`.
- Paid amplification → coordinate with `sales`/paid and `finances` for budget.
