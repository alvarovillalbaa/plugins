---
type: outbound-sequence
segment: [cold|warm|inbound|re-engage]
icp: [describe ICP here]
goal: [book call|demo|referral|re-engage]
total_touches: 6
duration_days: 21
---

# Sequence: [Name] — [ICP] ([Touch Count]-Touch, [Days] Days)

**Segment**: [Cold / Warm / Re-engage]  
**Goal**: [Book a discovery call / Schedule demo / etc.]  
**Channels**: Email (T1, T3, T5), LinkedIn (T2, T4), [Phone (T6)]

---

## Touch 1 — Email (Day 1)

**Subject**: [Specific, signal-based — not "Quick question"]

Hi {{first_name}},

[Personalization line: 1 sentence about them.]

[Value proposition: 1 sentence with a concrete metric.]

[Low-commitment CTA: "Worth a 20-minute call?"]

{{your_name}}

---

## Touch 2 — LinkedIn (Day 3)

**Connection note** (300 chars):

[Reference email. Offer an alternative channel. No pitch.]

---

## Touch 3 — Email (Day 7)

**Subject**: RE: [original subject]

Hi {{first_name}},

[Brief follow-up. Add a new piece of value — a stat, case study, or specific insight.]

[CTA: Same low-commitment ask.]

{{your_name}}

---

## Touch 4 — LinkedIn Message (Day 12)

[Direct message if connected. Reference email thread. Share a resource or observation. No pressure framing.]

---

## Touch 5 — Email (Day 16)

**Subject**: [One resource before I stop]

Hi {{first_name}},

[Last substantive value add — a case study, benchmark, or direct insight.]

[Soften: "If the timing is off, no worries."]

[CTA: Subtle — "feel free to reply if useful."]

{{your_name}}

---

## Touch 6 — Email (Day 21) — Breakup

**Subject**: Closing the loop

Hi {{first_name}},

[Acknowledge the no-response gracefully. Not passive-aggressive.]

[Leave the door open: "If timing changes, feel free to reply."]

[No CTA — this is a close, not a push.]

{{your_name}}

---

## Sequence Rules

- **Stop immediately on any reply** (positive or negative).
- Do not re-enroll the same prospect in less than 6 months.
- If 3+ email opens with no reply: switch to phone or direct LinkedIn message.
- Personalize the T1 opening line for every prospect — never blast a generic version.
- Update benchmarks and case study links every quarter.

---

## Exit Conditions

| Signal | Action |
|--------|--------|
| Replied "yes" | Remove from sequence, move to active pipeline |
| Replied "not now" | Pause 90 days, then re-enroll |
| Replied "unsubscribe" | Remove permanently |
| 3+ opens, no reply | Escalate to phone touch |
| No engagement after T6 | Archive |
