---
name: update-memories
description: Run the memory stack as an orchestration alias over review, promote, remember, and learning sync.
argument-hint: "[project, memory goal, or note to preserve]"
allowed-tools: [Read, Write, Grep, Glob, Bash, AskUserQuestion, Skill]
---

Use skills: **memory**, **learning**, and **code-documentation**.

This command is a convenience wrapper. It does not replace the existing `si:*` commands.

1. **Review** - Run the `/si:review` flow for promotion candidates, stale entries, conflicts, and consolidation.
2. **Promote** - When the user approves a candidate, use `/si:promote` to move it to `CLAUDE.md`, `.claude/rules/`, or the global memory layer.
3. **Remember** - Use `/si:remember` for new explicit facts or preferences supplied in the command arguments.
4. **Sync learning** - Run `learning-sync` for durable lessons that should feed skills, docs, or knowledge.
5. **Report** - Summarize what changed, what stayed read-only, and which memory items still need human approval.
