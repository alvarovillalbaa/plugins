# Example: Buyer Psychology Map for a SaaS Pricing Page

Context: A B2B observability tool ("Acme Traces") with a pricing page that converts at 1.8% of visitors to trial. Goal: map buyer psychology to diagnose why mid-market buyers stall on the page.

## Buyer Segment

Mid-market platform engineers and their EM, evaluating during an active incident-fatigue period.

## Motivators (jobs + desired gains)

- **Functional:** "Cut mean-time-to-resolution without rebuilding our stack."
- **Emotional:** Stop being the person paged at 3am. Look competent to leadership.
- **Social:** Adopt what respected peers (other infra teams) already trust.

## Fears / perceived risks

- Hidden per-seat or per-GB overage that explodes the bill at scale.
- Migration cost: ripping out the incumbent is weeks of work.
- Vendor lock-in on proprietary query language.

## Objections (and where they fire on the page)

| Objection | Trigger location | Counter-move |
| --- | --- | --- |
| "This will get expensive at our volume" | Pricing tiers, no volume example | Add a worked cost example at 500GB/day |
| "Will it work with our existing tools?" | Feature list, no integrations shown | Logos + "works with OpenTelemetry" above the fold |
| "Is this real or vaporware?" | No proof near CTA | Move a quantified case study beside the trial button |

## Decision triggers

- Concrete ROI math they can paste into a Slack thread for buy-in.
- A low-commitment next step (self-serve trial, no card).
- Proof that a similar-sized team succeeded.

## Recommended page changes (ranked)

1. Add a volume-based cost calculator near the tiers (kills the #1 fear).
2. Place a quantified peer case study adjacent to the primary CTA.
3. Reframe the trial CTA from "Start free trial" to "See your MTTR in 10 minutes."

## Expected effect

Reduces the dominant cost-anxiety objection and supplies the social proof + ROI math the buyer needs to advance internally. Validate with a CRO test (see the `cro` skill).
