# Content — Routing Guide

Router for all content creation work. Routes to channel or format specialist skills.

## Child Skills

| Child | Owns |
|-------|------|
| `context-to-content` | Turning product/company context into content briefs |
| `copywrite` | Ad copy, landing page copy, email copy |
| `humanizing` | Making AI-generated content sound human |
| `repurposing` | Adapting content across channels |
| `syndication` | Publishing content to external platforms |
| `linkedin-posts` | LinkedIn short-form posts |
| `linkedin-articles` | LinkedIn long-form articles |
| `x-posts` | X/Twitter posts |
| `x-articles` | X/Twitter long-form posts |
| `social-media` | Other social platforms |
| `video` | Video scripts and production |
| `slides` | Slide decks |
| `visualization` | Data visualizations and charts |
| `hyperframes` | Mental models and conceptual frameworks |

## Routing Decision Tree

```
Does the request start from raw company context (no content yet)?
  → context-to-content

Is this ad copy, landing page, or email marketing copy?
  → copywrite

Is this content that needs to be de-sloppified or humanized?
  → humanizing

Is this existing content being adapted for a new channel?
  → repurposing

Is this being published to an external platform?
  → syndication

Is the target LinkedIn (short)?
  → linkedin-posts

Is the target LinkedIn (long article)?
  → linkedin-articles

Is the target X/Twitter (short)?
  → x-posts

Is the target X/Twitter (long-form)?
  → x-articles

Is the target a video?
  → video

Is the target a slide deck?
  → slides
```

## Content Quality Gates

- **Slop check**: All AI-generated content passes through humanizing before delivery.
- **Brand voice**: Check voice profile before writing any customer-facing content.
- **Factual accuracy**: Product claims reference internal source docs, not training knowledge.
- **CTA required**: Every content piece closes with a clear call to action.
