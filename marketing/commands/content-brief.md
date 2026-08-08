---
name: content-brief
description: Create a working content brief from a topic, campaign, transcript, or knowledge dump, then optionally route into drafting commands.
argument-hint: "[topic, campaign, or source material]"
allowed-tools: [Read, Write, AskUserQuestion, Skill]
---

Use skill: **context-to-content** — `skills/context-to-content/SKILL.md`. Chain to **content** only when the request also includes drafting.

Create a compact working brief the rest of the content workflow can depend on.

1. **Gather scope** – Ask for topic, audience, goal, channel mix, and source material if those are not already clear.
2. **Frame the brief inline** – Produce a concise brief covering objective, reader, core message, proof points, formats, and CTA.
3. **Resolve ambiguity** – If the channel mix or positioning is still fuzzy, ask the minimum follow-up needed to sharpen it.
4. **Route to the next command if requested** – Suggest `blog-draft` for the canonical piece or `social-pack` for repurposing.
5. **Deliver** – Output the brief in a form that can be reused by a human, an agent, or a follow-on command.

## Boundary

This command creates the planning brief only. Use `blog-draft` for a finished article and `social-pack` for channel adaptations.
