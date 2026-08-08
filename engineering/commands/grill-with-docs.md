---
name: grill-with-docs
description: Stress-test a technical plan or design while keeping documentation, ADR, glossary, or decision-log context aligned.
argument-hint: "[plan file, design, ADR, or architecture question]"
allowed-tools: [Read, Write, Grep, Glob, Bash, AskUserQuestion, Skill]
---

Use skills: **architecture**, **code-documentation**, and optional external **grill-with-docs**.

1. **Load the docs context** - Read the target plan or design, nearby README/ARCHITECTURE/ADR files, and repo instruction docs.
2. **Interview the decision** - Ask one focused question at a time until assumptions, constraints, owner boundaries, risks, and success criteria are explicit.
3. **Check documentation drift** - Identify which living docs, ADRs, glossary entries, or runbooks would need updates if the decision lands.
4. **Produce the decision log** - Summarize decisions, rejected options, remaining questions, and affected docs.
5. **Update docs when requested** - If the user wants write-back, update the closest owner docs through `code-documentation`.

## Boundary

This is an interactive decision interview that keeps supporting docs aligned. Use `review-architecture` for an evidence-led architecture audit with findings and fixes.
