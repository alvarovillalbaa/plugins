# ICP Scoring

Use this reference when building a prospect list or campaign and needing to score and tier leads before writing any copy.

## When to use

Load this reference when the user asks to:

- define or refine an ICP before drafting a sequence
- score or tier a prospect list
- build a campaign from scratch
- decide which leads to prioritize or exclude

## ICP Definition Checklist

Collect all fields before writing copy. Missing fields produce generic outreach.

### Targeting

**Titles:**
- Primary titles (high intent): e.g., VP Marketing, Head of Growth, Director of Demand Gen
- Secondary titles (acceptable, lower priority): e.g., CMO at a <50-person company
- Never target: coordinators, interns, assistants, unless specifically requested

**Industries / verticals:**
- Primary verticals (1–3 max)
- Secondary verticals (test only, not primary)
- Excluded verticals: reasons should be concrete (budget, procurement cycles, cannot serve)

**Company size:**
- Employee count range: min / max / sweet spot
- Revenue range if targeting by ARR
- Funding stage if relevant: e.g., Series A+, bootstrapped >$5M, PE-backed

**Geography:**
- Primary markets
- Excluded regions with reason: e.g., APAC requires a different sales motion

### Buying signals (trigger events)

What makes a company more likely to buy right now:

- Recent hire in a role you solve for (job posting signal)
- Funding round in the last 6 months
- Product launch or expansion in the last 90 days
- Running paid search visible via SpyFu or SemRush
- Job listings that signal a pain you solve
- New executive who owns the budget

### Anti-ICP (explicit exclusions)

Who should never receive these emails:

- Too small: below minimum employee or revenue threshold
- Already a current client
- Missing verified email (bounce risk)
- Missing firstName (personalization fails)
- On opt-out or suppression list

### Offer fit

- Primary offer: free audit / trial / demo / strategy call / report
- Why this offer for this ICP (one sentence — if you cannot answer this clearly, rethink the offer before writing copy)

### Known objections

List the top 2–3 objections this ICP typically raises. Pick the one that kills the most deals and address it once, in Step 3 or 4 of the sequence — not in Step 1.

### Personalization data available

For each lead, identify what fields are confirmed available:

- `firstName` — required; filter out leads without it before upload
- `companyName` — required
- `personalization` — custom field (funding round, recent post, job listing, product launch); source: Clay / Apollo / manual
- `industry`, `employeeCount`, `linkedInURL` — optional enrichment

If personalization cannot be set for more than 50% of the list, rewrite the sequence to not depend on it.

---

## 6-Factor ICP Scoring Model

Score each factor 0–3 for a given prospect or segment. Multiply by weight. Sum for composite score.

| Factor | Weight | What to assess |
|--------|--------|---------------|
| Product-market fit | 30% | Does this persona have the problem your product solves, at the scale it requires? |
| Outbound readiness | 25% | Is this persona reachable via cold email? Do they respond to peers reaching out? |
| Value prop clarity | 15% | Can you explain the value in one sentence that lands for this persona? |
| TAM size | 15% | Is there enough of this segment to justify the campaign investment? |
| Multi-channel willingness | 10% | Will this persona engage across email + LinkedIn or only one channel? |
| Sector fit | 5% | Does your proof point library align to this vertical? |

### Composite score thresholds

| Tier | Score | Action |
|------|-------|--------|
| Tier 1 | 2.5 and above | Prioritize — write personalized sequences for these leads first |
| Tier 2 | 1.5 to 2.4 | Qualified — include in standard sequence after Tier 1 is ready |
| Tier 3 | Below 1.5 | Deprioritize or exclude — do not spend copywrite time here |

Spend expert copywrite effort on Tier 1 only. Tier 2 can run a lighter sequence. Do not write for Tier 3.

### Scoring table format

Use this table when presenting scored leads or segments:

| Lead / Segment | PMF | Readiness | VP Clarity | TAM | Multi-ch | Sector | Score | Tier |
|----------------|-----|-----------|------------|-----|----------|--------|-------|------|

---

## Capacity math (when sequencing to a platform)

```
Sending accounts ready (warmup score ≥80, ≥14 days) × 30 emails/day = conservative daily volume
Sending accounts ready × 50 emails/day = aggressive daily volume (only after 30+ days warmup)
Daily volume × 22 working days = monthly send capacity
Monthly sends × expected reply rate = expected replies
Expected replies × qualification rate = pipeline opportunities
```

Use this before promising a list size or committing to a launch date.

---

## Warmup requirements (when using a sending platform)

- Minimum 14 days warmup before first campaign send
- Minimum warmup score of 80
- Accounts below 80 or under 14 days: do not add to active campaigns

Domain setup to verify before launch: SPF, DKIM, DMARC (p=none minimum with reporting), MX records, custom tracking subdomain.
