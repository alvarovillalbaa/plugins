---
name: ingest
description: Capture one source into a brain's raw layer and optionally compile only that source into canonical knowledge.
argument-hint: "[URL, tweet ID, file path, or paste raw text]"
allowed-tools: [Read, Write, Bash, WebFetch, AskUserQuestion, Skill]
---

Use skill: **brain** — `skills/brain/SKILL.md`. Route source-specific extraction through `skills/ingestion/SKILL.md`.
Also read:
- `skills/brain/references/brain_contract.md` for the active brain boundary and folder mapping.
- `skills/ingestion/references/ingest_sources.md` for source-specific fetch and parse instructions.

## Steps

1. **Confirm the brain boundary**

   Count `BRAIN.md` files under the target root before writing:
   - 0: do not write canonical knowledge unless the user asked to bootstrap a brain.
   - 1: use that directory as the active brain root.
   - More than 1: stop and ask which brain to target.

   Use the active `BRAIN.md` to identify raw, knowledge, Memory, log, and index paths. Default to `knowledge/` only when no local mapping exists.

2. **Classify the source**

   Detect what was provided:
   - Twitter/X URL or tweet ID → use `xurl` per the ingest_sources playbook
   - YouTube URL → use `yt-dlp --skip-download --write-auto-sub`
   - LinkedIn URL → use `defuddle` or `agent-browser`
   - Any other web URL → use `defuddle parse <URL> --md`
   - Local file path (`.pdf`, `.md`, `.txt`, `.srt`, `.vtt`, `.json`, `.csv`, image, archive, office file) → use the matching source rule
   - Pasted raw text → save directly to `raw/`

3. **Fetch or extract the content**

   Use the appropriate tool from `skills/ingestion/references/ingest_sources.md`. If the tool is unavailable, fall back to the next option in that section and note the fallback used.

   If the source yields only metadata, a preview, a login wall, deleted media, unsupported binary data, or unreadable text, save or update the raw entry with `status: blocked` and `blocked_reason`. Do not promote it to canonical knowledge.

4. **Save to raw/**

   Write the result to the brain's raw intake folder using the naming convention `use-afs` defines (or the local equivalent from `BRAIN.md`), with the standard frontmatter:
   ```
   source: <type>
   url: <original URL or ID>
   fetched: YYYY-MM-DD
   status: unprocessed
   ```

5. **Immediate compile (optional)**

   If the user wants the content compiled now rather than queued:
   - Read `BRAIN.md` to learn the brain's structure.
   - Run the ingest mode from `references/operational_modes.md`.
   - Update relevant canonical pages under `knowledge/` or the mapped canonical knowledge path.
   - Refresh `INDEX.md` and the current dated log or local equivalent.
   - Mark the raw file as `status: processed`.

6. **Report**

   Tell the user:
   - What was fetched and from where.
   - Where the raw file was saved.
   - If compiled: which canonical pages were created or updated and what contradictions or open threads were found.
   - If blocked: which source could not be extracted and the exact reason.
   - If queued: confirm the file is ready for the next `compile-raw` pass.

## Boundary

This command captures one new source. Use `compile-raw` for a queue or corpus of sources already present in the raw layer.
