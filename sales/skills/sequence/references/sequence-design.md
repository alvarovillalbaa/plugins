# Sequence Design Reference

Reference for designing multi-touch outbound sequences: cadence, channel mix, message progression, and personalization. A sequence is a planned series of touches across channels over time — not the same ask repeated. Outreach is human-gated; personalize from real signal and respect anti-spam norms.

## Why sequences

Most replies come after the first touch — single-touch outreach leaves the majority of responses on the table. A sequence gives multiple, varied chances to be relevant at the right moment, across the channels where the prospect actually pays attention. The art is persistence *with* respect: enough touches to be remembered, varied enough to not be annoying, with a graceful exit.

## Sequence anatomy

| Element | Decision |
| --- | --- |
| **Length** | How many touches (commonly 5–9 over 2–4 weeks) |
| **Cadence** | Spacing between touches (tighten early, widen later) |
| **Channels** | Email, LinkedIn, X, phone, video — and the mix/order |
| **Progression** | How the message/angle evolves touch to touch |
| **Personalization** | Where deep 1:1 vs. segment-level |
| **Exit** | Break-up touch + when to stop |

## Cadence

- **Front-load, then space out.** Touches closer together early (days), wider later (週). Example spacing: Day 0, +2, +4, +7, +12, +18, +25.
- **Total window**: ~2–4 weeks for most B2B sequences; longer for nurture.
- **Don't crowd channels** — avoid hitting email + LinkedIn + X on the same day repeatedly; alternate.
- **Respect timezones and work hours**; weekday mornings tend to land best.

## Channel mix

Multi-channel sequences outperform single-channel — but each channel keeps its own norms.

| Channel | Role in sequence | Notes |
| --- | --- | --- |
| **Email** | Backbone — carries detail, links, async | Subject + first line decide opens |
| **LinkedIn** | Warming + personal touch | Engage/comment before DM; respectful cadence (`linkedin-dms`) |
| **X** | Warm, casual, relationship-led | Warm up via engagement first (`x-dms`) |
| **Phone/voicemail** | High-intent, breaks through | Pair with an email "tried calling" |
| **Video** | Differentiation, personal | Short, personalized |

Order: often engage on social → email → social DM → phone → break-up, but match to where the persona is reachable (from `prospect` research).

## Message progression

Each touch should bring a **new angle or value**, never the same ask reworded.

| Touch | Angle |
| --- | --- |
| 1 | Personalized opener tied to a trigger/signal (the "why now") |
| 2 | Different value — a relevant insight, resource, or proof point |
| 3 | Social proof — a similar-company result or case study |
| 4 | New angle — a different pain or use case |
| 5 | Light nudge / pattern interrupt (short, human) |
| 6 | Break-up — "I'll stop here; reach out if timing changes" |

The break-up touch is often the highest-replying — it creates urgency and signals you'll stop.

## Personalization in sequences

- **First and last touches** deserve the deepest personalization (they decide entry and the break-up reply).
- **Middle touches** can lean on segment-level relevance (role/industry/trigger) plus a real detail.
- **Personalization tokens alone are not personalization** — reference something true about them, not just `{firstName}`.
- Tier personalization to account value: high-value accounts get fully bespoke sequences; broader segments get tailored-but-templated.

## Channel norms within a sequence

- Keep each touch native to its channel (short DMs, scannable emails) — don't paste the same copy everywhere.
- Reference earlier touches lightly ("followed up by email last week") to show continuity without nagging.
- Vary format: question, insight, proof, resource, break-up.

## Stop conditions

- **Reply received** → pull from sequence, switch to human conversation (route to `follow-up`).
- **Explicit no / unsubscribe** → stop immediately, honor it.
- **Sequence complete** (break-up sent, no response) → stop; optionally move to long-term nurture.
- Never restart a completed sequence on the same contact without a genuinely new reason.

## Quality gates

- **Each touch adds value** — no "just bumping this" filler.
- **Varied, not repetitive** — different angle each time.
- **Respectful volume and cadence** — no spammy frequency; honor disinterest.
- **Compliant** — anti-spam (CAN-SPAM/GDPR): opt-out, no deceptive subjects, no scraped-list blasting.
- **True, approved claims** — no fabricated proof.
- **Human-gated** — present the full sequence + target list; a human enrolls/sends. No fully-automated blasting.

## Handoffs

- Individual first-touch craft → `initial`.
- Reply/no-reply handling → `follow-up`.
- Channel-specific DMs → `linkedin-dms`, `x-dms`.
- Targeting and angle research → `prospect`.
- Performance/attribution → `revenue-ops`, `revenue-intelligence`.
