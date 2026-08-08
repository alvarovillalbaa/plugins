---
name: retro
description: Analyze recent engineering work, PRs, quality signals, and lessons to produce follow-up actions.
argument-hint: "[time window, branch, repo area, or project]"
allowed-tools: [Read, Write, Grep, Glob, Bash, AskUserQuestion, Skill]
---

Use skills: **agentic-development**, **prs**, **quality-assurance**, **reporting**, **learning**, and **code-documentation**.

1. **Define the window** - Resolve the dates, branch range, PR set, or project area.
2. **Gather evidence** - Inspect commits, PRs, failures, review comments, incidents, docs changes, and repeated defects.
3. **Find patterns** - Separate one-off events from recurring delivery, quality, process, or ownership issues.
4. **Promote lessons** - Route durable lessons through `learning`, `memory`, or `code-documentation` based on the promotion matrix.
5. **Deliver actions** - Output decisions, lessons, owner actions, and verification tasks.

## Boundary

This command analyzes a completed time window or workstream. Use `repo-review` for current-state defects and `learning-sync` for one lesson-capture operation.
