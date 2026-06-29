# Message Outreach

Messaging skill for turning research and thread context into outbound drafts, follow-ups, replies, and short sequences — from ICP scoring through copy review to mailbox delivery.

## Use this for

- scoring and tiering a prospect list before writing sequences
- building a cold email campaign from scratch (ICP definition → sequence design → copy review)
- drafting cold and warm outbound emails
- writing follow-ups, breakup notes, and re-engagement messages
- generating email, LinkedIn, and call-script variants from the same research
- replying to engaged prospects with the right tone and next step
- reviewing who needs a response or bump before drafting the outreach
- building short, evidence-backed outreach sequences
- creating mailbox-ready drafts when email tools are available
- matching the sender's actual writing voice from prior approved or sent messages
- triaging an inbox before deciding where to draft

## Install

```bash
npx -y skills add ./sales/skills/outreach
mkdir -p ~/.codex/skills
cp -R sales/skills/outreach ~/.codex/skills/
```

Codex `$skill-installer` path:

```text
https://github.com/alvarovillalbaa/plugins/tree/main/sales/skills/outreach
```

## What is bundled

- `references/icp-scoring.md` — 6-factor ICP scoring, tier definitions, capacity math
- `references/copy-rules.md` — first-sentence rules, body length limits, CTA rules, deliverability, expert panel check
- `references/gmail-workflows.md` — gws CLI commands, inbox triage, calendar scheduling
- `references/email-sequences.md` — step timing, sequence types, A/B testing, deliverability
- `references/follow-up-triage.md` — email classification, response-needed review, promise tracking
- `references/response-drafting.md` — reply-style messaging, sensitive responses, tone selection
- `references/writing-style-calibration.md` — voice learning, persistent style guide
