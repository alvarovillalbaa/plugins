# Email Sequences

Use this reference when the user asks for more than one touch.

## Inputs to collect

- sequence type
- goal
- audience and relationship stage
- desired number of touches
- cadence preferences
- sender identity and proof points
- CTA destination or next step
- suppression or exit rules
- sending platform (Instantly, Outreach, Apollo, manual) if relevant

## Default outreach sequence types

### Cold outbound

- **Length:** 5–6 steps maximum; diminishing returns after 6
- **Arc:** initial hook → new angle → proof or resource → softer ask → bump → respectful close

**Default step timing:**

| Step | Delay | Purpose |
|------|-------|---------|
| 1 | Day 0 | Hook + value + soft CTA |
| 2 | Day 2 | New angle or supporting asset |
| 3 | Day 4–7 | Proof point or case study |
| 4 | Day 7 | Sharper framing or harder ask (if engagement signals exist) |
| 5 | Day 7–14 | Bump — "Still relevant?" style, 1–2 sentences |
| 6 | Day 7–14 after Step 5 | Breakup — leave something useful, leave the door open |

Do not exceed 6 steps. Do not send Steps 5–6 within the same week as Steps 3–4.

### Warm follow-up

- **Length:** 2–3 touches over 7–10 days
- **Arc:** reference shared context → clarify value → close the loop

### Re-engagement

- **Length:** 2–4 touches over 2–3 weeks
- **Arc:** acknowledge the gap → share a new reason to reconnect → final lightweight check-in

### Post-event or post-meeting

- **Length:** 2–3 touches over 5–7 days
- **Arc:** recap context → send value → propose next step

## Per-touch requirements

For each touch provide:

- subject line options (2 variants for Step 1 only — see A/B testing below)
- purpose
- full body copy
- CTA
- timing (day relative to previous step)
- conditions for sending or skipping

## Sequence logic

Define:

- **Branching:** what changes after a reply, meeting booked, or engagement signal
- **Exit conditions:** reply or meeting booked stops the sequence immediately; no further steps
- **Suppression rules:** unsubscribe, opt-out list, existing client, or missing firstName should prevent any step from going out

## A/B testing

- Test subject line variants on **Step 1 only** — one variable at a time
- Minimum 100 sends per variant before calling a winner
- Do not A/B test body copy in early campaigns; isolate the subject line variable first
- After Step 1 winner is confirmed, run the full sequence before testing other variables

Good subjects for later tests (only after Step 1 is confirmed):

- CTA wording in Step 2
- Send timing (Day 2 vs Day 4)
- Personalization depth in the opening line

## Deliverability

Apply these rules to every step:

- Plain text only — no HTML, no images, no tracking pixels
- Subject lines: 3–7 words, no exclamation points, no all-caps
- No links in Step 1; max 1 link in Steps 2–3 only if genuinely useful
- Avoid spam trigger words: "free", "guarantee", "no risk", "limited time", "act now", "click here"
- Sending platform: verify SPF, DKIM, DMARC, and custom tracking subdomain before launch

If the sequence is going into a sending platform, load `references/icp-scoring.md` for send limit and warmup requirements before committing to a launch date.

## Weekly performance targets (cold outbound baseline)

| Metric | Good | Great |
|--------|------|-------|
| Open rate | 40%+ | 60%+ |
| Reply rate | 3%+ | 7%+ |
| Positive reply rate | 1%+ | 3%+ |
| Meeting rate | 0.5%+ | 1.5%+ |

Adjust targets based on niche and offer type.

## Deliverable shape

Return:

1. overview table (step / delay / purpose / CTA / exit condition)
2. full drafts for each step
3. branching and exit notes
4. A/B test suggestions (Step 1 subject lines only unless specified)
5. metrics to watch
