---
name: docs-site
description: Research a software project and build a complete documentation website using the project's existing stack or a justified portable default.
argument-hint: "[project root] [--framework existing|auto] [--deploy]"
allowed-tools: [Read, Write, Edit, Bash, Agent, AskUserQuestion, Skill]
---

Use skill: **code-documentation** — `skills/code-documentation/SKILL.md`.
Read `skills/code-documentation/references/project-research.md` and `skills/code-documentation/references/docs-site.md` for the detailed workflow.

1. **Resolve constraints** — Identify the project root, audience, existing docs stack, required outputs, and deployment intent. Preserve an existing documentation framework unless the user asks to replace it.
2. **Research the project** — Read source, entry points, manifests, tests, examples, and existing docs. Build an evidence-backed feature inventory; do not invent unsupported APIs or behavior.
3. **Design coverage** — Map every user-facing feature to getting started, concepts, guides, reference, examples, or changelog pages. Record genuine gaps as gaps.
4. **Implement the site** — Reuse the existing stack. If none exists, choose a portable static-docs option that fits the repository and explain the choice before adding dependencies.
5. **Verify** — Run the site's link check and production build. Exercise navigation and the quick start. Fix failures before reporting completion.
6. **Deploy only when authorized** — Treat deployment as an optional shared-state action. Use the hosting target the user or repository specifies; do not assume a vendor or account.
7. **Deliver** — Report page coverage, build command, validation evidence, artifact paths, deployment state, and unresolved documentation gaps.

## Boundary

This command creates or rebuilds a complete documentation website. Use `docs-pass` for a bounded documentation change.
