---
name: review-architecture
description: Review architecture, ownership boundaries, and maintainability risks for a repo area, plan, branch, or proposed design.
argument-hint: "[repo area, branch, diff, plan, or design]"
allowed-tools: [Read, Write, Grep, Glob, Bash, AskUserQuestion, Skill]
---

Use skills: **architecture**, **quality-assurance**, and **code-documentation**.

Optional external chains: **codebase-design**, **improve-codebase-architecture**, and **grill-with-docs** from `references/external-skills.yaml`.

1. **Resolve scope** - Identify the code, diff, plan, or subsystem under review. Ask for scope only if the target is unclear.
2. **Map owners** - Find the canonical modules, APIs, data contracts, and documentation owners before judging the design.
3. **Review structure** - Check coupling, layering, boundaries, data ownership, failure modes, and testability.
4. **Stress decisions** - Use focused questions for weak assumptions or missing tradeoffs.
5. **Report findings** - Lead with architecture risks, affected files, recommended fixes, and verification or doc updates.

## Boundary

This command produces evidence-led architecture findings. Use `grill-with-docs` when the primary need is an interactive decision interview.
