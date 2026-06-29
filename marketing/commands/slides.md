---
name: slides
description: Create a code-based or HTML slide deck from scratch, a brief, or a PPTX using the slides skill.
argument-hint: "[topic or title]"
allowed-tools: [Read, Write, AskUserQuestion, Skill]
---

Use skill: **slides** — `skills/slides/SKILL.md`. Creates viewport-fitting HTML or code-based presentations, including PPTX-to-web rebuilds.

1. **Gather scope** – Ask for topic, title, number of slides, delivery format, and whether the user wants direct preset selection or style previews if not already provided.
2. **Read the skill** – Load `skills/slides/SKILL.md` and respect viewport fitting and content density limits.
3. **Plan** – Optionally produce a short deck plan using `skills/slides/templates/`.
4. **Implement** – Generate the presentation in the chosen mode: single-file HTML, multi-file HTML, React/TS, or PPTX conversion output.
5. **Deliver** – Output the slide deck files and how to open or run them.

If the user only gave a topic, ask for title and approximate slide count before generating.
