---
name: inbox-triage
description: Triage inbound email threads, summarize next actions, and draft replies using the productivity command workflow.
argument-hint: "[thread, inbox batch, or reply goal]"
allowed-tools: [Read, Write, AskUserQuestion, Skill]
---

Use this command workflow directly. Chain to **review** for risk or escalation decisions and **reporting** when the user needs an inbox summary.

1. **Gather the inbox context** – Ask for email content, thread summaries, sender context, and the goal for the inbox pass.
2. **Triage the messages** – Categorize them into reply now, delegate, follow up later, reference, or archive.
3. **Draft replies where needed** – Produce concise drafts for the messages that matter.
4. **Highlight risk and urgency** – Make deadlines, blockers, and escalation cases explicit.
5. **Deliver** – Output the triage list, reply drafts, and any repeatable inbox rules the user should keep.

## Boundary

This command triages user-supplied or explicitly authorized inbound messages. It drafts replies by default and does not send, archive, label, or open a private inbox without separate authorization.
