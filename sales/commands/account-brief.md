---
name: account-brief
description: Produce a focused account or prospect research brief using prospect, without drafting full outreach sequences.
argument-hint: "[account, prospect, URL, or research goal]"
allowed-tools: [Read, Write, AskUserQuestion, Skill]
---

Use skill: **productivity/prospect** from the Productivity plugin.

1. **Gather inputs** – Ask for URLs, notes, CRM data, or the account and persona to focus on.
2. **Build the brief** – Use `prospect` to produce the research artifact with evidence, fit, and recommended next motion.
3. **Keep it research-first** – Do not expand into a full outreach sequence unless the user asks.
4. **Deliver** – Output the brief and suggest `outreach` if the user wants messaging next.

## Boundary

This command produces one sales-ready account brief without drafting outreach. Use Productivity `research` for broader investigations and the Sales `outreach` skill for messages or sequences.
