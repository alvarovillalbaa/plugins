---
name: compile-raw
description: Compile a scoped queue of previously captured raw sources into canonical knowledge with provenance and contradiction tracking.
argument-hint: "[brain root, raw subfolder, or raw file]"
allowed-tools: [Read, Write, Bash, Glob, AskUserQuestion, Skill]
---

Use skills: **brain** and **ingestion**.
Read `skills/brain/references/brain_contract.md`, `skills/brain/references/operational_modes.md`, and `skills/ingestion/references/wiki_compiler.md` before writing.

1. **Resolve one brain** — Locate the applicable `BRAIN.md`. Stop before canonical writes when none exists unless bootstrapping was requested; ask which root to use when more than one applies.
2. **Read the contract** — Record the raw, canonical knowledge, index, log, memory, and retention paths from that brain. Do not assume a repository layout when the contract defines another.
3. **Inventory the queue** — List unprocessed raw items in the requested scope, group them by source type, and report blocked or already processed items separately. Ask before processing a large queue when priority or cost is material.
4. **Extract faithfully** — Use the source-specific ingestion guidance. Keep metadata-only, inaccessible, encrypted, or unsupported sources blocked with an exact reason; never synthesize claims from missing content.
5. **Absorb per source** — Update the nearest canonical owner, preserve evidence and dates, record contradictions or supersessions, and create a new page only for a durable topic. Mark an item processed only after its canonical write succeeds.
6. **Checkpoint and rebuild** — Rebuild the index and inspect edited pages at bounded intervals. Apply the brain's retention rule to exact processed pointers only.
7. **Report** — Return processed and blocked counts, pages created or updated, contradictions, unresolved decisions, source retention state, and verification evidence.

## Boundary

This command compiles a queued raw corpus. Use `ingest` to capture one new source, with optional immediate compilation of only that source.
