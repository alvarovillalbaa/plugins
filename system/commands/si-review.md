---
name: si:review
description: Analyze auto-memory for promotion candidates, stale entries, consolidation opportunities, and conflicts with CLAUDE.md. Produces a prioritized report without modifying any files.
allowed-tools: [Agent]
---

Spawn the **memory-analyst** agent (`agents/memory-analyst.md`) to analyze:

- `~/.claude/projects/*/memory/MEMORY.md` and all topic files in the same directory
- `./CLAUDE.md`, `~/.claude/CLAUDE.md`, and all files in `.claude/rules/`

The agent should produce a structured report with:
1. Promotion candidates (scored ≥ 6 on durability × impact × scope)
2. Stale entries (referencing deleted files, outdated versions, or removed patterns)
3. Consolidation groups (overlapping entries to merge)
4. Conflicts (memory entries that contradict existing CLAUDE.md rules)
5. Health metrics (MEMORY.md line count vs. 200-line limit, CLAUDE.md line count)
6. Top 3 recommended actions

After the report is delivered, offer to run `/si:promote` on the highest-scoring candidate.
