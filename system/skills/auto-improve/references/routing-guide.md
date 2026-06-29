# Auto Improve — Routing Guide

Router for continuous improvement of skills, memories, and knowledge. Routes to specialist system skills.

## Child Skills

| Child | Owns |
|-------|------|
| `skill-eval-loop` | Evaluating skill quality and running improvement loops |
| `memory` | Curating and promoting agent memories |
| `brain` | Improving knowledge from second-brain sources |
| `ingestion` | Ingesting raw content into the knowledge system |
| `personalize` | Personalizing skills for a user or company |
| `loops` | Designing repeatable improvement loops |

## Routing Decision Tree

```
Is this about improving the content or instructions in a skill?
  → skill-eval-loop

Is this about cleaning up, promoting, or reconciling agent memories?
  → memory

Is this about improving the knowledge base from raw content?
  → brain → ingestion (if raw source needs processing first)

Is this about making a skill or agent more tailored to a specific user?
  → personalize

Is this about setting up a recurring improvement process?
  → loops
```

## Auto Improvement Principles

- **Source separation**: Skills live in the plugin repo; memories live in the agent's memory system; knowledge lives in the brain. Don't cross these boundaries.
- **Evidence-driven**: Improvements must be grounded in eval results, session learnings, or explicit user feedback — not arbitrary changes.
- **Upstream vs local**: Improvements that benefit all users belong upstream; company/user-specific changes stay in local overlays.
- **Eval before promote**: Run an eval before and after skill changes to confirm improvement.
- **Idempotent loops**: Improvement loops must be safe to run multiple times without degrading quality.
