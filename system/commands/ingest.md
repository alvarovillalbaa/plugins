---
name: ingest
description: Preserve one source in private Drive, catalog its provenance, and optionally compile readable evidence into maintained owner pages.
argument-hint: "[URL, tweet ID, file path, or paste raw text]"
allowed-tools: [Read, Write, Bash, WebFetch, AskUserQuestion, Skill]
---

Last updated: 2026-10-10

Use skill: **brain** — `skills/brain/SKILL.md`. Route source-specific extraction through `skills/ingestion/SKILL.md`.
Also read:
- `skills/brain/references/brain_contract.md` for the active brain boundary and folder mapping.
- `skills/ingestion/references/ingest_sources.md` for source-specific fetch and parse instructions.

## Steps

1. **Confirm the brain boundary**

   Select the requested workspace; read root and applicable scoped `AGENTS.md`,
   indexes, and owner pages. Nested instructions do not create competing roots.
   Resolve the source's ownership and verify the connected private Drive account
   and destination. If that access is missing, report the exact blocker and keep
   the source untouched.

2. **Classify the source**

   Detect what was provided:
   - Twitter/X URL or tweet ID → use `xurl` per the ingest_sources playbook
   - YouTube URL → use `yt-dlp --skip-download --write-auto-sub`
   - LinkedIn URL → use `defuddle` or `agent-browser`
   - Any other web URL → use `defuddle parse <URL> --md`
   - Local file path (`.pdf`, `.md`, `.txt`, `.srt`, `.vtt`, `.json`, `.csv`, image, archive, office file) → use the matching source rule
   - Pasted raw text → capture in temporary staging, then preserve in Drive

3. **Fetch or extract the content**

   Use the appropriate tool from `skills/ingestion/references/ingest_sources.md`. If the tool is unavailable, fall back to the next option in that section and note the fallback used.

   If the source yields only metadata, a preview, a login wall, deleted media, unsupported binary data, or unreadable text, save or update the raw entry with `status: blocked` and `blocked_reason`. Do not promote it to canonical knowledge.

4. **Preserve in private Drive and catalog**

   Preserve the original and extracted content with the authorized Drive
   connector. Verify the uploaded bytes by remote download and SHA256 before
   removing an explicitly migrated original. Record stable artifact URL, member
   path, size, checksum, and reading status in `SOURCES.md`. Never create a
   repository raw folder or commit a temporary path or signed URL. Extraction
   metadata uses:
   ```
   source: <type>
   url: <original URL or ID>
   fetched: YYYY-MM-DD
   status: unprocessed
   ```

5. **Immediate compile (optional)**

   If the user wants the content compiled now rather than queued:
   - Read `AGENTS.md` to learn the workspace's structure.
   - Run the ingest mode from `references/operational_modes.md`.
   - Update the existing owner: unique generalized synthesis belongs in
     `knowledge/`; facts, decisions, repo procedures, and research use their
     appropriate maintained surfaces. Copied source summaries stay source material.
   - Refresh `INDEX.md` and the current dated log or local equivalent.
   - Mark the source catalog entry `status: processed` after successful writes;
     retain the preserved Drive artifact.

6. **Report**

   Tell the user:
   - What was fetched and from where.
   - The stable Drive artifact and source catalog location.
   - If compiled: which canonical pages were created or updated and what contradictions or open threads were found.
   - If blocked: which source could not be extracted and the exact reason.
   - If queued: confirm the file is ready for the next `compile-raw` pass.

## Boundary

This command captures one new source. Use `compile-raw` for a queue or corpus of sources already present in the raw layer.
