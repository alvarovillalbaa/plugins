---
name: learning-sync
description: Capture durable project or workflow lessons and update the active repository's learning artifacts.
argument-hint: "[session summary, workstream, or learning goal]"
allowed-tools: [Read, Write, AskUserQuestion, Skill]
---

Use skill: **learning** — `skills/learning/SKILL.md`. Route lesson-specific capture through `skills/lessons/SKILL.md`.

1. **Orient to the repo memory** – Check whether `learning/` exists and initialize or scan it if needed.
2. **Gather the durable signals** – Ask for the session summary or use evidence from the current authorized work context.
3. **Update learning artifacts** – Capture items, episodes, triples, or lessons based on the strength of the signal.
4. **Promote only durable knowledge** – Update AGENTS or docs only when the learning is stable enough to outlive the current task.
5. **Deliver** – Output the files changed and the key lesson captured.

## Boundary

This command captures reusable lessons in repository learning artifacts. Use `si:remember` for one exact durable memory candidate and `retro` for a multi-signal engineering retrospective.
