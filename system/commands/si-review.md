---
name: si:review
description: Perform a detailed read-only review of one scoped memory store and return evidence-backed correction, consolidation, and promotion candidates.
argument-hint: "[project root or authorized memory-store path]"
allowed-tools: [Agent, Read, Glob, Skill]
---

Run a read-only review through the canonical `memory` contract.

Use skill: **memory** — `skills/memory/SKILL.md`.

## Scope first

1. Resolve exactly one project root or memory store from the argument or current
   workspace. If neither is unambiguous, ask for the scope before reading.
2. Discover the runtime's store rather than assuming a Claude-specific path.
3. Include project policy files only inside that resolved root. Read a global
   user policy or another project only when the user separately authorizes that
   source for this review.
4. Never use a wildcard that crosses project, workspace, user, or runtime
   boundaries.

## Delegate the review

Spawn the **memory-analyst** agent (`agents/memory-analyst.md`) with an explicit
input packet containing:

- resolved project root and memory-store path;
- authorized policy files or directories;
- as-of date and requested time horizon;
- excluded sources and sensitivity constraints.

The agent should return:

1. promotion candidates with durability, impact, scope, provenance, and
   freshness;
2. stale or unverifiable claims with the evidence for that judgment;
3. consolidation candidates that preserve every source and qualifier;
4. conflicts showing both claims and their precedence or unresolved status;
5. store health metrics appropriate to the discovered runtime;
6. the top three proposed actions.

The report is read-only. Present promotions, corrections, merges, and deletions
as exact candidates with targets. Offer `/si:promote` only after the user can
inspect the candidate; do not mutate memory or policy files from this command.

## Boundary

This command performs a detailed candidate-level audit. Use `si:status` for a compact health snapshot and inventory summary.
