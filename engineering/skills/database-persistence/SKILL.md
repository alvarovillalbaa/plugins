---
name: database-persistence
description: >-
  Use for database schemas, migrations, persistence models, indexing,
  transactions, normalization, and data-integrity constraints. Child skill
  of `backend`; route here from the parent router when this lane is the
  narrowest owner.
---

# Database Persistence

This child skill owns database schemas, migrations, persistence models, indexing, transactions, normalization, and data-integrity constraints. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about database schemas, migrations, persistence models, indexing, transactions, normalization, and data-integrity constraints.
- The parent router [`../backend/SKILL.md`](../backend/SKILL.md) selects this child.
- The work needs this lane's references, scripts, examples, hooks, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `scripts/` contains executable helpers owned by this lane.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.
- `hooks/` contains hook entrypoints only when this lane owns hook behavior.

## Chain Rules

- Chain to `quality-assurance/backend-test-engineering`, `quality-assurance/passive-security-review`, `cloud-management`, `ai-engineering` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
