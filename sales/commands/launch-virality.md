---
name: launch-virality
description: Run the full 6-step viral X launch system — hidden outcome, weapons check, controversy engineering, concept research, algorithm strategy, and distribution timing — for a product launch post or video.
argument-hint: "[product name, features list, or existing draft]"
allowed-tools: [Read, Write, Bash, AskUserQuestion, WebSearch, Agent, Skill]
---

Use skill: **launches** — `skills/launches/SKILL.md`. Use child skill **virality** for the X launch system.

## References (load before starting)

- `skills/virality/references/virality-playbook.md` — Full 6-step system
- `../../marketing/skills/x-posts/references/x-copy-scoring.md` — Weapons Check scoring dimensions
- `../../marketing/skills/x-posts/references/x-concept-research.md` — YouTube + X controversy research
- `../../marketing/skills/x-posts/references/x-algorithm-mechanics.md` — Sourcing vs ranking signals
- `skills/virality/templates/x-launch-brief.md` — Brief template

## Step 1 — Gather Inputs

Ask for what's missing. Minimum required:
- Product name and category
- Feature list (raw is fine — will run "so what?" recursion on it)
- Target community (who is this for, what do they already believe)
- Any existing draft, script, or positioning language

## Step 2 — Find the Hidden Outcome

Run the "so what?" recursion on every feature until hitting an emotional outcome.

**Prompt template:**
> Here is a list of features for [product]. For each one, ask "so what?" recursively until you reach an emotional outcome. Return the single strongest emotional positioning statement.

Present the strongest 2–3 emotional outcomes. Ask the user to pick or riff on one. Derive the hook from the chosen outcome. Confirm: does this describe the user's life after, not the product's feature?

## Step 3 — Research the Controversy

Using the target community, identify the most activating nerve:

**If X API key is available:**
```
Research the top posts on X in [category] using advanced search Min_Faves:1000. 
Identify the ones with the highest quote tweet ratio. What is the single most 
activating nerve in this community?
```

**If no API key:** Use WebSearch to find recent high-engagement X posts in the category. Identify the common criticism or tension that drives quote tweets.

Present the activating nerve. Propose how the product's positioning can own that criticism before critics use it. Draft the "plant line" — the one line designed to generate defensive quote tweets from the community.

## Step 4 — Concept Research

Run competitive research to find a proven viral framing to borrow:

```
Find the top performing videos in [category] across the last 30 days, 12 months, 
and all time. Identify the structural pattern behind the highest performing titles. 
What is the core concept or framing that made them work? Apply that same framing 
to [product].
```

**Tools:** Use WebSearch with YouTube-specific queries, or 1of10.com if available. Look for the 2x-channel-average outliers — those title patterns are the ceiling worth stealing.

Present the found concept and the adapted framing for this product.

## Step 5 — Write the Launch Post or Script

Combine the hidden outcome + controversy plant + borrowed concept into a full draft.

**Post structure:**
- Tweet 1: Hook from hidden outcome (+ the controversy plant line embedded)
- Retweet mechanic: "RT + comment '[keyword]' and we'll [do thing] for FREE"
- Thread body (if applicable): proof, specifics, how it works
- Final tweet: CTA

**Script structure (if video):**
- Open with the hidden outcome hook — zero context-setting
- Quick credibility setup (raise amount, users, results)
- Problem section (the world before this product)
- Solution (product moment — visceral, not feature-based)
- Proof (specific numbers, specific examples)
- CTA

## Step 6 — Run the Weapons Check

Score every line in the draft using the weapons-check agent at `../../marketing/skills/social-media/agents/weapons-check.md`.

Invoke the weapons check with the full draft. Every line must hit 10/10 on both Invention Novelty and Copy Intensity. Lines that fail get rewritten. Filler gets cut.

Output the scored + revised version.

## Step 7 — Build the Distribution Plan

Present the phased distribution strategy:

**Phase 1 (0–60 min):** Organic only. Reply to every comment.
**Phase 2 (hours 1–2):** Deploy N influencers, staggered across 30-minute windows.
**Phase 3 (real-time):** Add gas when momentum builds.
**Phase 4 (days 2–4):** Follow-up content calendar (meme → feature deep dive → company story).
**Week 2:** Results, testimonials, social proof.

Generate a starter set of 25 reply drafts for the 48-hour window:
> I'm working on a launch [insert script + product knowledge]. Write 25 potential replies to people responding — keep the conversation going, add value, sound like a real human, keep each under 280 characters.

## Deliverables

Output everything in one clean document:

1. **Hidden outcome statement** — the single positioning line
2. **Controversy plant line** — the activating nerve line
3. **Launch post / script** (weapons-checked, fully revised)
4. **Retweet mechanic** — the giveaway or engagement hook
5. **Distribution plan** — phased timeline with influencer count and stagger
6. **25 reply drafts** — for the 48-hour window
7. **Follow-up content calendar** — days 2–4 + week 2

## Optional: Visual Asset

If the launch needs a video or visual:
- Route to `video` for motion graphics
- Route to `images` for product-focused stills
- Route to `visualization` for visual landing pages
