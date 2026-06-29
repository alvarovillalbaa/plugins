# Learning — Routing Guide

Router for capturing and routing learnings from agent sessions. Routes to the appropriate storage skill.

## Learning Type Decision Matrix

| Learning Type | Description | Destination |
|--------------|-------------|-------------|
| Lesson | Non-obvious insight with a trigger and action | `lessons` |
| Fix | Bug fix or workaround with a specific symptom | memory rules |
| Fact | Stable fact about the codebase, team, or product | `facts/` directory |
| Raw source | Unprocessed content to be absorbed | `ingestion` |
| Knowledge | Synthesized domain knowledge | `knowledge-base` |
| Memory rule | Runtime behavior rule for the agent | `memory` |

## Routing Decision Tree

```
Is this a non-obvious insight the agent should remember next time?
  → lessons

Is this a fact about the codebase, team, or product?
  → facts/ (via brain)

Is this a raw document or content that needs processing?
  → ingestion

Is this synthesized domain knowledge?
  → knowledge-base

Is this a rule about how the agent should behave?
  → memory
```

## Learning Capture Standards

- **Specificity**: Vague learnings are useless. "Be careful with migrations" is not a lesson; "When adding a NOT NULL column, always provide a DEFAULT in the same migration" is.
- **Trigger condition**: Every lesson needs a trigger — the exact situation where it applies.
- **Action**: Every lesson needs an action — what to do when the trigger fires.
- **Source reference**: Link to the session, commit, or document where the learning originated.
- **Expiry check**: Review lessons quarterly; remove ones that are no longer applicable.

## Promotion Matrix

See the shared [promotion matrix](../../../../references/docs/promotion-matrix.md) for canonical routing rules across the full knowledge system.
