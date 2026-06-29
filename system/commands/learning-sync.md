---
name: learning-sync
description: Capture durable engineering lessons and update repo-local learning artifacts using the learning skill.
argument-hint: "[session summary, workstream, or learning goal]"
allowed-tools: [Read, Write, AskUserQuestion, Skill]
---

Use skill: **learning** — `skills/learning/SKILL.md`. Route lesson-specific capture through `skills/lessons/SKILL.md`.

1. **Orient to the repo memory** – Check whether `learning/` exists and initialize or scan it if needed.
2. **Gather the durable signals** – Ask for the session summary or infer it from the current work context.
3. **Update learning artifacts** – Capture items, episodes, triples, or lessons based on the strength of the signal.
4. **Promote only durable knowledge** – Update AGENTS or docs only when the learning is stable enough to outlive the current task.
5. **Deliver** – Output the files changed and the key lesson captured.
