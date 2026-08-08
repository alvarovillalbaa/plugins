---
name: docs-pass
description: Update or create the right technical documentation for a code change, service, or workflow using the code-documentation skill.
argument-hint: "[scope, service, feature, or changed area]"
allowed-tools: [Read, Write, AskUserQuestion, Skill]
---

Use skill: **code-documentation** — `skills/code-documentation/SKILL.md`.

1. **Gather the documentation target** – Ask what changed, who the readers are, and where the docs should live if that is unclear.
2. **Choose the doc type** – README, architecture doc, tests doc, report, ADR, migration guide, or changelog.
3. **Update the docs** – Follow `code-documentation` to write or revise the most appropriate artifact close to the source.
4. **Keep the docs scoped** – Update existing docs before creating new ones unless the gap clearly requires a new file.
5. **Deliver** – Output the doc changes and note any follow-up documentation gaps.

## Boundary

This command writes or updates a bounded documentation artifact. Use the `documentation-drift` skill for a read-only drift audit and `docs-site` for a complete documentation website.
