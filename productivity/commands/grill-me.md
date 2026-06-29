---
name: grill-me
description: Relentlessly interview the user about a plan or design, walking every branch of the decision tree one question at a time until reaching full shared understanding.
argument-hint: "[plan file, feature description, or design to stress-test]"
allowed-tools: [Read, Grep, Glob, Bash, AskUserQuestion]
---

Use skill: **grill** — `skills/grill/SKILL.md`.

Optional external skill chain: **grill-me** or **grilling** from `references/external-skills.yaml`. If the external skill is not installed, report the install command instead of copying its guidance inline.

1. **Load context** — Read any plan file or design document the user points to. Scan repo instructions, TODOs, and relevant code before asking the first question.
2. **Start the grill workflow** — Ask one decision-sharpening question at a time. Include a recommended answer when choices are useful.
3. **Walk every branch** — Continue until the important assumptions, constraints, risks, and tradeoffs are explicit.
4. **Deliver a decision summary** — Output the decisions made, open questions, rejected options, and next action.
