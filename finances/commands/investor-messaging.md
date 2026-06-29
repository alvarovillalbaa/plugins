---
name: investor-messaging
description: Generate the investor narrative, tailored hooks, and FAQ rebuttals from fundraising materials using the fundraising skill.
argument-hint: "[deck, model, stage, or investor context]"
allowed-tools: [Read, Write, AskUserQuestion, Skill]
---

Use skill: **finances** — `skills/finances/SKILL.md`, focusing on **Mode 4:
Fundraising**, but only the **Investor-Ready Messaging** section.

1. **Gather inputs** – Ask for the deck, model, stage, target investors, and any existing narrative or constraints.
2. **Read the fundraising context** – Extract the business, traction, and positioning inputs needed for the narrative.
3. **Produce messaging** – Generate the core narrative, tailored hooks, and top FAQ rebuttals with inline source references where possible.
4. **Keep the scope narrow** – Do not expand into materials audit or pipeline diagnostics unless the user asks.
5. **Deliver** – Output the messaging pack and suggest `materials-audit` or a broader fundraising diagnostics pass if that is the next need.
