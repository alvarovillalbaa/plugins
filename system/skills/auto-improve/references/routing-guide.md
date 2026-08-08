# Auto Improve — Routing Guide

Route project-local improvement of agent context, Markdown, personalization,
and installed components. Never use this workflow to modify a canonical plugin
source checkout or prepare an upstream contribution.

## Child Skills

| Child | Owns |
|-------|------|
| `skill-eval-loop` | Evaluating skill quality and running improvement loops |
| `memory` | Curating and promoting agent memories |
| `brain` | Improving knowledge from second-brain sources |
| `ingestion` | Ingesting raw content into the knowledge system |
| `personalize` | Personalizing skills for a user or company |
| `loops` | Designing repeatable improvement loops |
| `code-documentation` | Improving Markdown and agent instruction files |

## Routing Decision Tree

```
Is this an installed skill under the current project's .agents tree?
  → skill-eval-loop, local copy only

Is this a canonical plugin source checkout?
  → stop; route an explicit source-maintenance request to plugins-management

Is this about cleaning up, promoting, or reconciling agent memories?
  → memory

Is this about improving the knowledge base from raw content?
  → brain → ingestion (if raw source needs processing first)

Is this about making a skill or agent more tailored to a specific user?
  → auto-improve → personalize on the first relevant workflow

Is this about improving Markdown or agent instructions?
  → code-documentation

Is this about setting up a recurring improvement process?
  → loops
```

## Auto Improvement Principles

- **Local-only plugins**: Improve only installed `.agents` copies. Treat source
  plugin checkouts as read-only and never prepare commits, patches, PRs, or pushes.
- **Source separation**: Installed skills, memories, Markdown, knowledge, and
  personalization keep their own canonical owners. Do not blend their stores.
- **Evidence-driven**: Improvements must be grounded in eval results, session learnings, or explicit user feedback — not arbitrary changes.
- **Just-in-time personalization**: Use inherited variables and ask only for
  relevant missing values when a component first needs them.
- **Eval before keep**: Run an appropriate check before and after installed skill
  changes to confirm improvement.
- **Idempotent loops**: Improvement loops must be safe to run multiple times without degrading quality.
