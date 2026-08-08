---
name: si:promote
description: Stage, review, and explicitly approve promotion of one proven memory into its canonical policy owner without losing provenance.
argument-hint: "[exact scoped record handle and proposed target]"
allowed-tools: [Read, Edit, Write, AskUserQuestion, Skill]
---

Promote one memory only through the canonical `memory` contract and
[`../../references/docs/promotion-matrix.md`](../../references/docs/promotion-matrix.md).

## Steps

1. **Resolve exact source and scope** — require one record handle in one
   authorized store. Do not choose the closest semantic match across a store or
   search adjacent projects.
2. **Verify the evidence** — preserve evidence kind, source, observation date,
   qualifiers, conflicts, and freshness. Re-check drift-prone claims against
   current state when safe. An inferred or disputed claim cannot be promoted as
   an unconditional rule.
3. **Score the candidate** — rate durability, impact, and scope from 0 to 3.
   A score of six or more permits review; it never substitutes for evidence or
   approval.
4. **Select the canonical owner** — use the promotion matrix and current
   runtime's project/user policy locations. Do not assume `CLAUDE.md`, a global
   home path, or `.claude/rules/` exists unless discovered in the authorized
   scope.
5. **Draft the exact change** — show source record, target path/handle, proposed
   text, retained scope and qualifiers, provenance note, and what would happen
   to the source record. Do not strip uncertainty merely to sound prescriptive.
6. **Obtain explicit approval** — confirmation must cover both the target write
   and any source mutation. Approval to promote does not imply approval to
   delete the original record.
7. **Apply transactionally** — after approval, write the canonical target,
   verify it, then either mark the source as superseded or leave it intact as
   approved. Prefer a reversible supersession pointer over deletion.
8. **Report** — show the target change, source-record state, approval evidence,
   validation, and any unresolved conflict. Never claim promotion if either
   write failed.

Do not promote secrets, private reasoning, unrelated personal data, temporary
task state, or unsupported sensitive inferences.

## Boundary

This command promotes one reviewed memory candidate to a canonical policy owner. It does not create a new memory candidate or perform a broad store review.
