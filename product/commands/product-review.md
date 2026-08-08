---
name: product-review
description: Review a product surface with engineering, design, or combined lenses and produce prioritized findings.
argument-hint: "[surface, PRD, screenshot, branch, or flow] [--lens=engineering|design|both]"
allowed-tools: [Read, Write, Grep, Glob, Bash, AskUserQuestion, Skill]
---

Use skill: **critique** — `skills/critique/SKILL.md`.

Use skills by lens:

- **engineering**: `architecture`, `quality-assurance`, `frontend`, and `code-documentation`
- **design**: `design`, `critique`, `polish`, and `product-development`
- **both**: run engineering first for feasibility and risk, then design for user experience and interaction quality

1. **Resolve the lens** - Default to `both` unless `$ARGUMENTS` specifies `--lens=engineering` or `--lens=design`.
2. **Collect product context** - Read the PRD, screenshots, code, metrics, or user notes needed for the chosen lens.
3. **Review the surface** - Evaluate user outcome, workflow completeness, edge cases, implementation risk, and design quality.
4. **Prioritize** - Separate blockers, important issues, and improvements. Tie each issue to evidence.
5. **Deliver** - Return findings, recommended fixes, verification, and docs/spec updates.

## Boundary

This command reviews an existing product artifact or experience. It does not create roadmap commitments, a new PRD, or implementation unless the user separately requests that work.
