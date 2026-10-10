---
name: compile-raw
description: Compile a scoped queue of previously captured raw sources into canonical knowledge with provenance and contradiction tracking.
argument-hint: "[workspace, SOURCES.md entry, or Drive artifact URL]"
allowed-tools: [Read, Write, Bash, Glob, AskUserQuestion, Skill]
---

Last updated: 2026-10-10

Use skills: **brain** and **ingestion**.
Read `skills/brain/references/brain_contract.md`, `skills/brain/references/operational_modes.md`, and `skills/ingestion/references/wiki_compiler.md` before writing.

1. **Resolve one workspace** — Select the explicit target; read root and applicable scoped `AGENTS.md`. Nested instruction files refine scope, rather than creating ambiguous brains.
2. **Read the contract** — Resolve maintained owners, navigation, logs, `SOURCES.md`, and the verified ownership-appropriate Drive account. Do not create a local raw directory.
3. **Inventory the queue** — Read source catalog entries and inspect the scoped Drive artifacts with the authorized connector. A local inventory alone does not inspect Drive. Group unprocessed, blocked, and processed entries; confirm scope only when priorities or costs are genuinely unresolved.
4. **Extract faithfully** — Use the source-specific ingestion guidance. Keep metadata-only, inaccessible, encrypted, or unsupported sources blocked with an exact reason; never synthesize claims from missing content.
5. **Absorb per source** — Update the nearest canonical owner, preserve evidence and dates, record contradictions or supersessions, and create a new page only for a durable topic. Unique generalized synthesis belongs in knowledge; operations, facts, decisions, and research have their own owners. Mark the catalog entry processed only after its write succeeds; retain the Drive original.
6. **Checkpoint and rebuild** — Rebuild the index and inspect edited pages at bounded intervals. Apply the brain's retention rule to exact processed pointers only.
7. **Report** — Return processed and blocked counts, pages created or updated, contradictions, unresolved decisions, source retention state, and verification evidence.

## Boundary

This command compiles a queued raw corpus. Use `ingest` to capture one new source, with optional immediate compilation of only that source.
