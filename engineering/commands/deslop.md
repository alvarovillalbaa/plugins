---
name: deslop
description: Remove AI-code residue and local maintainability noise without changing product behavior.
argument-hint: "[file, folder, diff, or repo area]"
allowed-tools: [Read, Write, Grep, Glob, Bash, AskUserQuestion, Skill]
---

Use skills: **quality-assurance** and **prs**.

Optional external chain: **deslop** from `references/external-skills.yaml`.

1. **Set the cleanup boundary** - Identify the files or diff to clean. Avoid unrelated refactors.
2. **Preserve behavior** - Read tests and call sites before editing. Do not change public contracts unless the user explicitly asks.
3. **Remove residue** - Tighten vague names, redundant comments, dead branches, needless wrappers, duplicated logic, and low-signal generated prose.
4. **Verify narrowly** - Run the smallest relevant checks for the touched surface.
5. **Report exact changes** - Summarize behavior preservation, cleanup choices, and residual risks.
