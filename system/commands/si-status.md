---
name: si:status
description: Show a compact read-only health snapshot for one scoped memory store, including provenance, freshness, conflicts, and capacity.
argument-hint: "[project root or authorized memory-store path]"
allowed-tools: [Read, Bash, Glob, Skill]
---

Generate a read-only memory health dashboard through the canonical `memory`
skill.

Use skill: **memory** — `skills/memory/SKILL.md`.

## Steps

1. Resolve exactly one project root or authorized store. Do not wildcard across
   projects, runtimes, user profiles, or a home directory.
2. Discover the store adapter and index used by the current runtime. If the
   user supplied a local root, `memory/scripts/inventory_memory.py ROOT` may be
   used to list candidate metadata without reading contents.
3. Read only the resolved index and directly relevant records. Count records,
   index entries, bytes or lines, and topic files only when those measures are
   meaningful for that store.
4. Sample or inspect provenance, dates, scope, freshness, conflicts, and
   orphaned index links. Clearly state which records were not evaluated.
5. Apply capacity thresholds only when the store documents them. Never invent
   a universal line limit or assume a Claude-specific layout.

## Output

```text
Memory Health Dashboard — YYYY-MM-DD

Scope
  Store:             [resolved handle]
  Project/user:      [exact scope]
  As of:             [date]

Inventory
  Indexed records:   [N]
  Topic records:     [N]
  Capacity measure:  [documented metric or not specified]

Evidence health
  Current:           [N]
  Stale:             [N]
  Conflicting:       [N]
  Missing provenance:[N]
  Not evaluated:     [N]

Recommendations
  1. [read-only recommendation]
  2. [read-only recommendation]
  3. Run /si:review with this same scope for a detailed report
```

Do not mutate records from this command. Any correction, promotion,
consolidation, or deletion becomes a separately approved candidate.

## Boundary

This command summarizes store health without candidate-level analysis. Use `si:review` for a detailed audit and proposed actions.
