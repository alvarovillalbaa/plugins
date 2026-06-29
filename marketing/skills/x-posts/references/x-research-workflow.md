# X Research Workflow

A data-driven system for improving X posts before publishing, based on personal performance history and topic market research.

Source tool: `github.com/ashemag/x-writing-system-skill`

---

## When to Use This Workflow

Run the research pipeline when:
- Drafting a post on a competitive topic where examples matter
- A post isn't performing and you want to understand why
- You're entering a new topic area and need to calibrate tone and format
- You want to refine a draft against what's actually working in the market right now

Skip it for:
- Time-sensitive reactions (news, events)
- Personal updates or milestone posts
- Quick replies and engagement responses

---

## Setup

Requires:
- [Bun](https://bun.sh) runtime
- X Bearer token set in `.env` as `X_BEARER_TOKEN`
- Repo cloned: `git clone https://github.com/ashemag/x-writing-system-skill`

```bash
cd x-writing-system-skill
bun install
```

Optional global env: `~/.config/env/global.env`

---

## The Four-Stage Pipeline

### Stage 1 — Baseline Constraints
Apply the Matt Gray writing guidelines as non-negotiable constraints.
See: `references/x-writing-guidelines.md`

### Stage 2 — Personal Calibration
Fetch your top-performing posts from the last 30 days to identify what's working for your specific account and voice.

```bash
bun run x-search.ts fetch \
  --username YOUR_HANDLE \
  --days 30 \
  --max-results 100 \
  --out data/recent_posts.json
```

Outputs: JSON with posts + engagement metrics (likes, reposts, replies, impressions).

### Stage 3 — Market Research
Run adaptive topic searches to find high-performing posts in your niche.

```bash
bun run x-search.ts research \
  --topics "topic1,topic2,topic3" \
  --topic-days 7 \
  --performant-like-threshold 50
```

The tool broadens search terms across attempts until it finds strong samples. Posts exceeding the threshold (default: 50 likes) are flagged as market winners.

### Stage 4 — Synthesis and Authoring
Run the full advisory pipeline against your draft.

```bash
bun run x-search.ts advise \
  --draft-file ./draft.txt \
  --username YOUR_HANDLE \
  --save \
  --out-markdown advice.md
```

Output includes:
- Trending topics at time of research
- High-performing sample posts with engagement metrics
- Your personal top posts from the period
- Three targeted, grounded recommendations
- Five LLM-authored alternative post versions

---

## Interpreting the Output

The output is evidence, not instructions. Use it to:

1. **Validate your hook** — Do top-performing posts on this topic share a hook pattern? Match or contrast deliberately
2. **Calibrate specificity** — Are market winners more/less specific than your draft? Adjust
3. **Check format** — Is the market responding to threads or single posts on this topic right now?
4. **Identify gaps** — What angle are high-performers NOT covering? That's your differentiation
5. **Borrow voice signals** — Note the vocabulary, rhythm, and structure of winners; don't copy, but internalize

The five generated versions are starting points. Rewrite from evidence, not templates.

---

## Quick Mode

For faster iteration with lower API cost:

```bash
bun run x-search.ts advise \
  --draft-file ./draft.txt \
  --username YOUR_HANDLE \
  --quick
```

Use quick mode during drafting. Run the full pipeline for final polish before publishing high-stakes posts.

---

## Rate Limits

- 450 recent search requests per 15 minutes
- Caching is enabled by default (360-minute TTL)
- Avoid repeated runs on the same topics within the cache window

---

## Without API Access

If no X Bearer token is available, apply the framework manually:

1. Manually search X for your topic — filter "Top" results in the last week
2. Note the top 5–10 posts: hook structure, format, specificity level, CTA type
3. Identify your own last 5 posts on a similar topic and check their engagement
4. Apply `x-writing-guidelines.md` rules to your draft
5. Use `x-post-formats.md` to validate your structure choice
