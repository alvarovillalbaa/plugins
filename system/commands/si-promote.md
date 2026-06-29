---
name: si:promote
description: Graduate a proven pattern from MEMORY.md to CLAUDE.md or .claude/rules/. Distills the entry into a one-line prescriptive instruction and removes it from MEMORY.md to free space.
argument-hint: "[pattern description or MEMORY.md line number]"
allowed-tools: [Read, Edit, Write, AskUserQuestion]
---

Promote a pattern from auto-memory to the project's rule system.

## Steps

1. **Identify the entry** — read the argument. If it is a line number, read that line from MEMORY.md. If it is a description, search MEMORY.md for the closest match.

2. **Score it** — confirm the entry scores ≥ 6 on:
   - Durability (0–3): still true in 30+ days?
   - Impact (0–3): prevents mistakes or breakage?
   - Scope (0–3): applies to whole project?
   
   If score < 6, tell the user and stop.

3. **Select target** — decide where the rule belongs:
   - `./CLAUDE.md` — project-wide rules that any contributor needs to know
   - `.claude/rules/<topic>.md` — rules that only apply to specific file types
   - `~/.claude/CLAUDE.md` — personal preferences across all projects

4. **Distill** — transform the entry from descriptive to prescriptive:
   - Remove "I noticed", "it seems", "sometimes" hedges
   - Write one direct instruction: "Use X" or "Never Y"
   - Include the exact command if relevant

5. **Write** — append the distilled rule to the target file. For `.claude/rules/`, add or update the `paths` frontmatter to scope correctly.

6. **Remove** — delete or comment out the entry from MEMORY.md. If the entry is in a topic file, remove it there.

7. **Confirm** — show the user:
   - What was added to which file
   - What was removed from MEMORY.md
   - New line count for both files
