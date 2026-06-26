# X Copy Scoring

A scoring system for every line in a launch script or post before anything gets published.
The Weapons Check runs before publishing. Both dimensions must hit 10/10.

External owner boundary:

- Use `unslop` and `stop-slop` for generic AI-writing tells, filler, passive voice, punctuation tells, and formulaic phrasing.
- This file owns X-specific scoring: invention novelty, copy intensity, platform fit, proof, and engagement potential.

---

## The Two-Dimension Weapons Check

Every line gets scored independently on two dimensions:

### Dimension 1 — Invention Novelty (1–10)
**Does it make the product feel like a genuine breakthrough?**

- 10: Makes the product sound like something that has never existed before
- 7–9: Interesting but familiar — could be said about a competitor
- 4–6: Generic product-category language
- 1–3: Could apply to any product in any category

### Dimension 2 — Copy Intensity (1–10)
**Does it make someone feel something — not just understand something?**

- 10: Visceral reaction — reader feels something immediately
- 7–9: Engaging but not emotionally charged
- 4–6: Informative but flat
- 1–3: No emotional response; purely informational

**Rule:** Both must be 10/10. A novel idea with flat copy fails. Sharp copy about a boring feature fails.

### Prompt
```
Score this line on two dimensions:
- Invention Novelty (1–10): Does it make the product feel like a genuine breakthrough?
- Copy Intensity (1–10): Does it make someone feel something — not just understand something?

If either is below 10, rewrite it and explain what was weak.
```

---

## Weak → Strong Rewrites

The transformation is always the same: replace vague with visceral, features with feelings, announcements with punches.

| Weak | Strong |
|------|--------|
| "Introducing our new AI platform" | "We built the world's first AI that makes your competitors obsolete overnight" |
| "Our tool helps you grow faster" | "The exact system that took 4 startups from zero to 1M+ views" |
| "Better customer support" | "Support that actually solves your problem — first contact, every time" |
| "AI website builder that works in seconds" | "Replace your 9-5 income" |
| "Excited to announce..." | [Delete the line entirely] |

---

## 100-Point Content Score

Start at 100. Deduct for violations. Ship when score is 90+.

| Threshold | Action |
|-----------|--------|
| 90–100 | Ship it — human-sounding, clean |
| 70–89 | Minor fixes needed |
| 50–69 | Significant rewrite required |
| 0–49 | Complete rewrite |

---

## Prose Cleanup Handoff

Before final scoring, run the draft through `unslop` or `stop-slop`.

Keep the external review focused on generic prose issues. Return here for the X-specific questions:

- Does the first line stop the scroll?
- Does each post add new information or tension?
- Does the thread have a reason to continue after each post?
- Are proof points real and specific?
- Is the CTA natural for the audience and format?

---

## Content Quality Dimensions

For full post/script scoring, use these weighted dimensions:

| Dimension | Weight | What it measures |
|-----------|--------|-----------------|
| Voice similarity | 35% | Sounds like a real person / founder, not a template |
| Specificity | 25% | Real numbers, real examples, real context |
| Prose cleanup | 20% | Use `unslop` or `stop-slop` for the generic prose gate |
| Length appropriateness | 10% | Right length for the format and platform |
| Engagement potential | 10% | Would someone share, save, or reply? |

---

## Expert Panel Approach

For high-stakes scripts, run a recursive expert panel before finalizing:

1. Assemble 7–10 domain expert personas tailored to the content
2. Always include: External Prose Gate (`unslop` or `stop-slop`, 1.5x weight) + Brand Voice Match
3. Each expert scores the draft and identifies the top 3 weaknesses
4. Revise addressing the weaknesses; repeat
5. Continue until aggregate score hits 90+ or 3 rounds exhausted
6. Ship the best version with notes if 3 rounds don't reach 90+

The external prose gate is weighted 1.5x in the aggregate; generic AI-writing detection stays owned by `unslop` and `stop-slop`.

---

## ASCII Diagram Requirement (for long-form posts)

Every long-form X post must include at least one ASCII diagram:
- Under 40 characters wide
- Must parse in under 3 seconds
- Types: system architecture, before/after, flow diagram, metrics using block chars (█ ▓ ░)

---

## Never Fabricate

Use only real data — actual business metrics, specific incidents, real decisions with documented reasoning.
"Never fabricate metrics. Use real numbers or don't use numbers."
