# Humanizing Patterns Reference

Reference for rewriting AI-like or stiff prose into human, specific, voice-aligned writing while preserving meaning. The goal is not to "trick detectors" — it's to make writing genuinely better: specific, varied, and honest. Pull the target voice from repo-local voice/personalization docs.

## AI tells (what to hunt and cut)

### Vocabulary tics
Overused AI words and phrases — replace with plain language:
- "delve," "leverage," "utilize," "robust," "seamless," "elevate," "unlock," "harness," "navigate the landscape," "in today's fast-paced world," "ever-evolving," "game-changer," "tapestry," "testament to," "realm," "foster," "pivotal," "crucial," "comprehensive."
- "It's not just X, it's Y" construction (over-used antithesis).
- "Whether you're a beginner or an expert…" filler enumerations.

### Structural tics
- **Uniform sentence length** — AI defaults to medium, even rhythm. Real writing varies wildly (3 words. Then a long, winding one.).
- **The rule-of-three everywhere** — "fast, reliable, and scalable" on every line.
- **Hedging overload** — "can," "may," "often," "generally," "tends to" stacked together.
- **Listicle reflex** — bulleting things that should flow as prose.
- **Symmetric paragraphs** — every paragraph the same shape and length.
- **Conclusion that restates the intro** — "In conclusion, as we've seen…"
- **Empty topic sentences** — "Communication is an important aspect of business."
- **Em-dash overuse** and perfectly balanced clauses.

### Tone tics
- Relentless positivity / no opinion or stake.
- Generic, audience-less voice ("for anyone looking to…").
- Over-explaining the obvious.
- No concrete detail — adjectives instead of nouns and numbers.

## Humanizing moves

### 1. Add specificity
Generic → concrete is the single highest-leverage move.
- "improved performance significantly" → "cut p95 latency from 800ms to 120ms."
- "many customers" → "the 40-odd teams on the design-partner plan."
- Use real names, numbers, dates, and examples. Specificity is the thing AI can't fake and humans trust.

### 2. Vary rhythm (burstiness)
Mix sentence lengths deliberately. Short punch. Then a longer sentence that develops the idea with a subordinate clause or two. Fragment for emphasis. Read aloud — if it's metronomic, break it.

### 3. Inject a point of view
Humans take positions. Add a stance, a preference, a "here's what most people get wrong." Mild contrarianism and honest tradeoffs read as human because models hedge.

### 4. Cut the throat-clearing
Delete the warm-up. Start at the most interesting point. "In today's digital landscape, businesses must…" → just say the thing.

### 5. Use plain, direct language
- Prefer the simple word: "use" not "utilize," "help" not "facilitate," "about" not "regarding."
- Active voice over passive.
- Contractions where the voice allows (don't, you'll, it's) — they read conversational.

### 6. Show the seams
Real writing has texture: an aside, a parenthetical, a concrete anecdote, an admission of a limit. Add one genuine, grounded detail.

### 7. Match the voice
Pull tone, vocabulary, formality, and signature phrases from the voice doc. Humanizing toward a *specific* voice beats a generic "casual" rewrite.

## Preserve meaning

Humanizing changes the *prose*, not the *facts*.
- Do not add claims, stats, or examples that aren't true. Specificity must be *real* specificity — invented detail is worse than generic copy.
- Keep technical accuracy intact; don't oversimplify into wrongness.
- Preserve the original intent, CTA, and key points.
- If a fact is needed to make a sentence concrete and you don't have it, flag a placeholder — don't fabricate.

## Before / after pattern

> **Before (AI):** In today's fast-paced digital landscape, leveraging robust analytics solutions can help businesses unlock valuable insights and elevate their decision-making to drive seamless growth.
>
> **After (human):** Most teams already have the data. What they're missing is one number they check every Monday. Pick that number first — the dashboards can come later.

## Self-check before shipping

- [ ] Read it aloud — does it sound like a person talking?
- [ ] Sentence lengths vary (not all medium)?
- [ ] At least one concrete number/name/example per section?
- [ ] No words from the AI-tells list survived?
- [ ] There's a clear point of view, not just balanced hedging?
- [ ] Intro starts at the interesting part, not the warm-up?
- [ ] Every fact is true (no invented specifics)?
- [ ] It matches the target voice doc?
