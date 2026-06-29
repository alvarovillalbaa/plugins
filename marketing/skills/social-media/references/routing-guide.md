# Social Media — Routing Guide

Router for social media content creation. Routes to platform-specific skills.

## Child Skills

| Child | Owns |
|-------|------|
| `linkedin-posts` | LinkedIn short-form posts (under 3000 chars) |
| `linkedin-articles` | LinkedIn newsletter/articles (1000–2000 words) |
| `x-posts` | X/Twitter posts and threads |
| `x-articles` | X/Twitter long-form posts |

## Routing Decision Tree

```
Is the platform LinkedIn?
  Short post (< 500 words) → linkedin-posts
  Long article/newsletter  → linkedin-articles

Is the platform X/Twitter?
  Short post or thread     → x-posts
  Long-form post           → x-articles

Is this a multi-platform content pack?
  → handle directly: generate per-platform using child skills in sequence
```

## Platform-Specific Rules

### LinkedIn
- Lead with a bold first line — it's cut off after ~3 lines, must hook.
- Use line breaks between ideas — dense paragraphs perform poorly.
- Personal stories and lessons outperform promotional content.
- Optimal post length: 150–300 words for posts, 1200+ for articles.

### X / Twitter
- Hook in the first tweet of a thread — it determines open rate.
- Threads of 5–10 tweets outperform single tweets for reach.
- Use numbers and concrete specifics ("3 ways", "in 7 days").
- Optimal thread length: 7–12 tweets for maximum engagement.

## Content Quality Standards

- **Platform-native**: Adapt content structure and language for each platform — don't copy/paste.
- **No slop**: Run through humanizing before posting.
- **One CTA per post**: Multiple asks dilute engagement.
- **Scheduling**: Batch social content 2 weeks ahead for consistency.
