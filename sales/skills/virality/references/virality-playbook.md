# X Viral Launch Playbook

A 6-step system behind product launches that hit #1 trending on X.
Source: proven across Moda (4.3M views), Durable (1.7M), HockeyStack (1.5M+), Slash Series C (1.7M).

---

## Step 1 — Find Your Hidden Outcome

Most founders pitch features. Nobody cares about features.

**The only question that matters:** What does a user's life look like after using your product?

Examples:
- Durable was not "an AI website builder" — it was "a way to replace your 9-5 income"
- HockeyStack was not "a revenue analytics platform" — it was "the system that breaks through the noise"
- Moda was not "an AI design tool" — it was "the world's first design agent with taste"

One positioning decision is the difference between 100K views and millions.

### The "So What?" Recursion

Run this before writing a single word:

1. Write down every feature your product has
2. After each one, ask "so what?" out loud
3. Keep asking until you hit an emotion
4. That emotion is your positioning
5. Write one sentence describing the user's life after using it — that sentence is your hook

**Claude Code prompt:**
```
Here is a list of features for [product]. For each one, ask "so what?" 
recursively until you reach an emotional outcome. Return the single 
strongest emotional positioning statement.
```

**Weak → Strong:**
- "AI website builder that works in seconds" → "Replace your 9-5 income"
- "Revenue analytics platform" → "Break through the noise and close more deals while you sleep"
- "AI design tool" → "The world's first design agent with taste. Anti-slop, by design."

---

## Step 2 — Score Every Line to 10/10

Every video script and launch post gets scored on two independent dimensions.

**Do not write "good enough." Both must hit 10/10 before anything gets filmed.**

See `references/x-copy-scoring.md` for the full scoring system and rewrite protocol.

**Claude Code prompt:**
```
Score this line on two dimensions:
- Invention Novelty (1–10): Does it make the product feel like a genuine breakthrough?
- Copy Intensity (1–10): Does it make someone feel something — not just understand something?

If either is below 10, rewrite it and explain what was weak.
```

Lines that score below 10 on either dimension get rewritten automatically.
Pure filler gets cut entirely.

---

## Step 3 — Engineer Controversy as Distribution

The most counterintuitive step. Your biggest haters become your distribution.

**The mechanism:** Quote tweets are an engagement signal. Every quote tweet (including negative ones) tells X's algorithm to show the post to more users. Critics distribute your content while complaining about it.

### How Moda did it

Moda was launching an AI design tool — to designers who despise AI design tools.

Instead of ignoring the hate or using standard product marketing language, they owned the criticism first: **"The world's first design agent with taste. Anti-slop, by design."**

Every designer who disagreed quote tweeted it. Every quote tweet fed the algorithm.

### How to find your activating nerve

**Claude Code prompt (requires X API key):**
```
Research the top posts on X in [category] sorted by engagement using 
advanced search Min_Faves:1000. Identify the ones with the highest 
quote tweet ratio. What is the core criticism or controversy that made 
people react? Summarize the single most activating nerve in this community.
```

### How to engineer it

1. Find the most common criticism of your product category
2. Acknowledge it directly in your positioning
3. Make your product the solution to that exact criticism
4. Plant one line that a specific community can't help but react to
5. Watch them distribute your content while complaining

Communities that activate easily: SEO, design, UGC creators, finance, dev tools.

---

## Step 4 — Borrow Proven Viral Concepts

Find a concept that's already proven viral on another platform and apply it to your product.

**HockeyStack raised $50M.** Their positioning: "an AI revenue agent that closes business while you sleep." The proven concept: action happening while you're passive (sleeping, offline). This concept already had millions of views in fitness, finance, and real estate content.

### The Research Process

Before writing, run 15 keyword searches across YouTube filtered three ways:
- All time
- Last 12 months
- Last 30 days

For each keyword, find the highest-performing video. That's the ceiling.
Collect patterns downward until there's a major drop-off in views.
The titles at the ceiling are the patterns worth stealing.

**Claude Code prompt:**
```
Find the top performing videos in [category] across the last 30 days, 
12 months, and all time. Identify the structural pattern behind the 
highest performing titles. What is the core concept or framing that 
made them work? Now apply that same framing to [product].
```

**Use:** YouTube API or [1of10.com](https://1of10.com)

### The key question

What does this product actually help you do?
Is there a proven viral concept built on that same idea?
Can you borrow the concept and let the product speak through it?

Spend the entire production budget on finding the right framing before filming anything.

---

## Step 5 — Understand What the Algorithm Actually Measures

The algorithm does not measure "engagement" as a single number. It measures two completely separate signals.

### Signal 1: Sourcing
**Does the algorithm show your post at all?**

Primary signal: **retweets**.

No retweets = post never enters the For You feed. Ever.
This is why giveaways requiring a retweet work — they're gaming sourcing.

### Signal 2: Ranking
**How high does your post appear once sourced?**

Primary signal: **reply chains where the original author responds back**.

Each reply you post creates a new chain. Each chain tells the algorithm this is a real conversation worth showing to more people.

**More chains = higher ranking = more visibility = more replies.**

This is the single highest-leverage mechanic on the platform.

### The 48-Hour Reply Protocol

You'll know whether your post will live or die within the first 3 hours.

Exact schedule:
1. Post goes live
2. Let it breathe for 30–60 minutes — organic audience only
3. Reply to every single comment immediately
4. Deploy connections and influencers when organic velocity is confirmed
5. Continue replying to every comment for 48 hours
6. Never stop. Not for meetings. Not for sleep. Not for anything.

Launches where founders follow this exactly outperform by 2–3x.

**Claude Code prompt for drafting replies:**
```
I'm working on a launch [Insert video script + knowledge base about 
the product]. Write 25 potential replies to people responding to my 
launch — keep the conversation going, add value, sound like a real 
human responding, and keep each under 280 characters, preferably less.
```

---

## Step 6 — Strategic Distribution Timing

Never blast every connection at once. Never use influencers who don't disclose.
(Non-disclosure violates FTC rules — make it mandatory for every influencer to disclose.)

If the algorithm sees a sudden artificial spike with no organic foundation, it reads as inauthentic and kills the post within an hour.

### The Phased Sequence

**Phase 1 — Minutes 0–60: Organic only**
- Let the post breathe
- Algorithm tests with your core audience first
- Reply to every question thoughtfully
- Monitor engagement velocity

**Phase 2 — Hours 1–2: Deploy influencers**
- Only if organic velocity is strong
- Deploy 10–20 influencers
- Stagger posts across 30-minute windows (never all at once)

**Phase 3 — Real-time adjustment**
- Watch engagement live
- Add gas when momentum is building
- Hold if organic velocity is weak

**Phase 4 — Next 24 hours**
- Follow-up content while the algorithm is still hot
- Day 1: Main video / launch post
- Day 2: Meme your product
- Day 3: Deep dive on one specific feature
- Day 4: Tell your company story
- Week 2: Results, testimonials, social proof

---

## Metrics That Signal Success

| Signal | Threshold | Meaning |
|--------|-----------|---------|
| Retweets in first hour | 10+ | Post will enter For You feed |
| Reply chain depth | 5+ | Algorithm ranking boost |
| Quote tweet ratio | >5% of engagements | Controversy is working |
| Views in 3 hours | >10K | Post has velocity |

---

## What This Is Not

- This is not luck. Every viral launch followed this system.
- This is not organic reach. It's engineered distribution with organic triggers.
- This is not about follower count. It's about algorithm signals and positioning.
- Founders spend years building the product and 30 minutes thinking about the launch. The launch makes or breaks the business.
