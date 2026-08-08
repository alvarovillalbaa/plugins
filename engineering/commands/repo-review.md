---
name: repo-review
description: Review a repository or subsystem's current state and return prioritized quality, maintainability, and operational findings.
argument-hint: "[repository root, subsystem, or review goal]"
allowed-tools: [Read, Write, AskUserQuestion, Skill]
---

Use skills: **quality-assurance** and optional **visualization** if a shareable review page would help.

1. **Set the review scope** – Ask for the repository root, files, or subsystem to review if the target is unclear.
2. **Run the review** – Follow `quality-assurance` to reconstruct intent, inspect risk, and produce findings-first output.
3. **Verify if appropriate** – Run focused verification commands when the scope and environment make that practical.
4. **Package visually when useful** – If the review is dense or needs stakeholder sharing, use `visualization` to create a companion review page.
5. **Deliver** – Output the findings, residual risks, and any artifact paths.

## Boundary

This command audits current repository state. Use `review-pr` for a branch, diff, or pull request and `review-architecture` when the lens is architecture only.
