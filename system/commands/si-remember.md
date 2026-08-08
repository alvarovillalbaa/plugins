---
name: si:remember
description: Stage and explicitly confirm one provenance-rich durable memory record in an authorized store.
argument-hint: "[exact claim to remember and intended scope]"
allowed-tools: [Read, Write, Edit, AskUserQuestion, Skill]
---

Save one important pattern, fix, decision, or preference through the canonical
`memory` contract. Invoking this command requests the workflow; it does not
authorize an inferred claim, an unreviewed normalization, or an unspecified
store.

## Steps

1. **Resolve one scope** — identify the current project or the exact store the
   user named. Use the `memory` skill to discover stores available in this
   runtime. Never wildcard across projects, runtimes, or global memory.
2. **Draft the exact claim** — preserve qualifiers, uncertainty, dates, and the
   user's wording. If the argument is vague, reconstruct only a candidate and
   label it `inferred`; do not turn it into a fact or instruction.
3. **Build the candidate record** — include:
   - type: `feedback`, `project`, `reference`, or `user`
   - evidence kind: `reported`, `observed`, or `inferred`
   - source or conversation handle and observation date
   - scope and intended consumers
   - freshness or revalidation condition
   - reason and how to apply it
   - conflicts, superseded record IDs, and sensitivity notes
4. **Preview before mutation** — show the complete candidate, exact destination,
   and whether an existing record would be created, updated, or superseded.
   Obtain explicit confirmation of that exact candidate. A vague instruction
   such as “remember what we discussed” is never sufficient on its own.
5. **Check duplicates and conflicts** — inspect the authorized store's index and
   relevant topic records only. Preserve both claims when evidence conflicts;
   never silently blend them or discard the older source.
6. **Write after confirmation** — use the store's native schema when one exists.
   For a Markdown store, use this minimum record:

```markdown
---
name: [descriptive-slug]
description: [one-line summary that preserves uncertainty]
metadata:
  type: [feedback | project | reference | user]
  evidence_kind: [reported | observed | inferred]
  source: [relocatable source or conversation handle]
  observed_at: [YYYY-MM-DD]
  scope: [project, workspace, or user scope]
  freshness: [revalidation date or trigger]
  supersedes: [record IDs or none]
---

## Claim

[Exact claim with qualifiers intact.]

## Why and how to apply

[Reason, applicability boundary, and practical use.]

## Conflicts and uncertainty

[Conflicts, alternatives, or none observed.]
```

7. **Update the index transactionally** — add or revise exactly one pointer and
   verify that the record and index agree. Do not remove an older record unless
   the confirmed operation explicitly supersedes it.
8. **Report** — state what changed, where, the approval used, provenance,
   freshness, and any unresolved conflict. If the write did not occur, say so.

Read [`../skills/memory/references/memory-contract.md`](../skills/memory/references/memory-contract.md)
before changing the schema or relaxing a gate. Never store credentials,
private reasoning, unrelated personal data, or unsupported sensitive
inferences.

## Examples

```text
/si:remember "Project scope: after editing openapi.yaml, run pnpm run generate:api; reported by the user on 2026-08-02"
/si:remember "User preference: omit trailing summaries unless the task needs a handoff; user-reported, global scope"
/si:remember "Project reference: bugs are tracked in Linear project <project-key>; revalidate if the project is renamed"
```

## Boundary

This command stages and writes one exact memory candidate after approval. It does not review a whole store or promote the candidate into policy.
