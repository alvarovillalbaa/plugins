---
name: si:remember
description: Explicitly save a pattern, fix, or preference to auto-memory with proper frontmatter. Use immediately after finding a debugging solution, confirming a preference, or identifying a workflow that should persist.
argument-hint: "[what to remember — be specific and prescriptive]"
allowed-tools: [Read, Write, Edit]
---

Save an important pattern to auto-memory immediately.

## Steps

1. **Read the argument** — this is what the user wants saved. If vague ("what we just discussed"), infer from context the concrete actionable fact.

2. **Classify the entry type**:
   - `feedback` — behavior instruction, preference, or correction ("always X", "never Y", "user prefers Z")
   - `project` — project context, decision, or constraint ("we use pnpm", "auth is in src/auth/")
   - `reference` — pointer to where something lives ("bugs tracked in Linear INGEST project")
   - `user` — fact about the user's role, background, or goals

3. **Check for duplicates** — read the memory index at `~/.claude/projects/<project>/memory/MEMORY.md`. If the fact is already there, update the existing entry instead of creating a new one.

4. **Distill to prescriptive form**:
   - Remove hedges: "I noticed", "it seems", "sometimes"
   - Write one direct instruction or fact
   - For debugging solutions: include the exact error and exact fix command

5. **Write the memory file**:

```markdown
---
name: [descriptive-slug]
description: [one-line summary]
metadata:
  type: [feedback | project | reference | user]
---

[The fact, rule, or solution — for feedback/project: lead with the rule, then **Why:** and **How to apply:** lines]
```

Save to `~/.claude/projects/<project>/memory/<slug>.md`.

6. **Update MEMORY.md index** — add a pointer line:
   ```
   - [Title](./slug.md) — one-line hook
   ```

7. **Confirm** — report: what was saved, where, and the new MEMORY.md line count.

## Examples of good entries

```
/si:remember "always run pnpm run generate:api after editing openapi.yaml — types won't match otherwise"
/si:remember "user prefers no trailing summaries — they find them redundant"
/si:remember "bugs are tracked in Linear project INGEST"
/si:remember "restart dev server after any .env change — hot reload doesn't pick up env vars"
```
