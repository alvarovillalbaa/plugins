---
name: compile-raw
description: Process all unprocessed files in the raw/ folder and compile them into canonical knowledge base pages. Handles mixed source types — markdown, PDFs, YouTube transcripts, Twitter exports, web captures, and more.
argument-hint: "[optional: path to specific raw/ subfolder or single file]"
allowed-tools: [Read, Write, Bash, Glob, AskUserQuestion, Skill]
---

Use skill: **brain** — `skills/brain/SKILL.md`. Route source-specific extraction through `skills/ingestion/SKILL.md`.
Also read:
- `skills/brain/references/brain_contract.md` — BRAIN.md boundary, adaptation mode, canonical paths, raw status, and Memory input rules
- `skills/ingestion/references/ingest_sources.md` — per-source extraction instructions
- `skills/ingestion/references/wiki_compiler.md` — absorb, cleanup, rebuild, and reorganize loops
- `skills/brain/references/operational_modes.md` — ingest mode contract

## Steps

### 1. Confirm Boundary

Count `BRAIN.md` files under the target root before writing:

- 0: stop before canonical writes unless the user explicitly asked to bootstrap a brain.
- 1: use that directory as the active brain root.
- More than 1: stop and ask which brain to target.

Read `BRAIN.md` and record:

- adaptation mode: strict AFS, partial AFS, or native company standard
- raw path
- canonical knowledge path, defaulting to `knowledge/`
- Memory paths, if present
- raw retention rule: mark processed, archive, or remove exact processed pointer

When available, run the read-only helper for orientation:

```sh
python system/skills/ingestion/scripts/brain_inventory.py . --include-memory
```

### 2. Discover

List every file in `raw/` (or the specified path) where `status` is not `processed`. Group by source type:

```sh
grep -rL "status: processed" raw/ 2>/dev/null
```

Also inventory repo-local Memory folders when present: `logs/`, `lessons/`, `facts/`, `fixes/`, `steers/`, `models/`, and `reflections/`.

Report the count and breakdown before starting (for example, "12 raw files - 3 twitter, 4 web, 2 pdf, 3 markdown; 8 Memory candidates").

If the queue is large (>20 files), ask the user whether to run all at once or process in priority order per `skills/ingestion/references/ingest_sources.md`.

### 3. Extract

For each file:
- `source: twitter` or `.md` tweets → already text, proceed to absorb.
- `source: youtube` or `.srt` / `.vtt` → strip timestamps: `sed '/^[0-9]/d;/^$/d;s/<[^>]*>//g'`.
- `source: pdf` or `.pdf` → run `pdftotext <file> -` and append the text to the raw entry.
- `source: linkedin` or `source: web` → already markdown from defuddle, proceed to absorb.
- `.json` → parse relevant fields and flatten to markdown.
- `.csv` → convert rows to markdown list or table.
- `.html` / `.htm` → extract readable body text.
- `.png` / `.jpg` → run `tesseract` OCR if available, otherwise mark blocked.
- archive, office, audio, or video files → extract only with a source-appropriate tool; otherwise mark blocked.

For Memory entries, extract only durable learnings, procedures, facts, decisions, recurring patterns, contradictions, or open threads. Keep one-off events in Memory.

If a source is metadata-only, preview-only, deleted, login-walled, encrypted, image-only without OCR, or tool-blocked, update or record it as `status: blocked` with `blocked_reason` and do not synthesize claims from it.

### 4. Orient

Before writing anything:
- Read `BRAIN.md` to confirm the brain's folder structure and retention rule.
- Read `knowledge/INDEX.md` or the equivalent index.
- Identify which canonical pages are likely to need updates based on the source content.

### 5. Absorb (per-file loop)

For each extracted source:

1. Extract entities, concepts, claims, decisions, procedures, open questions, and dates.
2. Search for existing canonical pages that should absorb the new information.
3. Update canonical pages: rewrite the current-state or compiled-truth section, append evidence to the timeline section.
4. Create new pages only when the source introduces a durable topic with enough substance to warrant it.
5. Record contradictions, supersessions, or strengthened consensus explicitly.
6. Mark the raw file as `status: processed` after successful absorption.

Use a checkpoint every 10 files: rebuild the index, inspect the most-edited pages as whole documents, and split any page that has become a dumping ground.

### 6. Rebuild

After the full pass:

- Refresh `knowledge/INDEX.md`.
- Append a summary entry to `logs/YYYY-MM-DD.md`:
  ```
  compile-raw: N files processed, M pages created, P pages updated
  ```
- Update any synthesis or hub pages that are now stale.

Use the log path and date folder convention from `BRAIN.md` when it differs from this default.

### 7. Report

Deliver:
- Count of files processed.
- Count of Memory entries reviewed and promoted.
- Files blocked, with exact blocker.
- Canonical pages created (list with paths).
- Canonical pages updated (list with paths).
- Contradictions found and how they were handled.
- Open threads that need human judgment.
- Suggested next actions (synthesis sweeps, gap pages, health check).
