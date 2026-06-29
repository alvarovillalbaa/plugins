# Brain Contract

Use this reference before any second-brain run that may write, reorganize, or compile knowledge. It defines the storage contract that the `brain` and `ingestion` skills must preserve.

Use the repo's shared promotion matrix for target selection across memory, facts, fixes, lessons, raw sources, generated artifacts, and living docs: `../../../../references/docs/promotion-matrix.md`.

## Boundary Rule

A target repo, codebase, workspace, or database has one active brain. The active brain is the directory governed by `BRAIN.md`.

Before canonical writes:

1. Count `BRAIN.md` files inside the requested target root.
2. If none exist, stay read-only unless the user explicitly asks to bootstrap a brain.
3. If exactly one exists, use that file's directory as the brain root.
4. If more than one exists, fail closed and ask which brain to target. Do not merge, dedupe, or infer across multiple brains.
5. Work inside the selected boundary only. Paired or sibling brains may be inspected read-only only when the request requires it.

If the user targets a subdirectory inside a larger workspace, count from the requested target root first. If the task would cross a higher-level `BRAIN.md`, stop and clarify the intended boundary.

## AFS External Reference

The canonical Agentic File System (AFS) definition lives outside this skill. Prefer the external source over the summaries below to avoid drift:

- **Skill**: `use-afs` — install with `python scripts/install-external-skills.py --skill use-afs --agent codex`. When installed, defer to it for the full AFS layout, naming conventions, and responsibility mapping.
- **Reference site**: `afs-livid.vercel.app`
- **Source repo**: `github.com/alvarovillalbaa/afs`

The adaptation modes below are summaries. When `use-afs` is installed, it is authoritative and wins over these summaries on any conflict.

## Adaptation Modes

`BRAIN.md` may define the mode in plain English, tables, YAML, or another local format. Follow the local contract over these defaults.

### strict-afs

Use when no meaningful local standard exists. Create or follow the final Agentic File System:

- Memory: `logs/`, `lessons/`, `facts/`, `fixes/`, `steers/`, `models/`, `reflections/`
- Operational: `audits/`, `raw/`, domain folders, `plans/`, `specs/`, `sources/`, `lib/`, `objects/`, `templates/`
- Source of truth: `references/`, `cookbook/`, `knowledge/`, `runbooks/`, `research/`

Timestamped Memory and operational-history content uses the local date convention from `BRAIN.md`; if unspecified, use `YYYY/MM-DD/`.

### partial-afs

Use when the workspace already has some AFS roles but not the full tree. Map the AFS responsibility to the existing folder instead of forcing a migration.

Examples:

- `knowledge/` exists but `facts/` does not: compile canonical knowledge into `knowledge/` and leave facts in the closest Memory equivalent.
- A repo has one continuous `research/continuous-research.md`: update that owner instead of creating a parallel research tree.
- A repo has a source-material page: archive provenance there instead of scattering duplicate source pages.

### native

Use when the company or user already has a standard that covers the same responsibilities. Follow that standard fully while preserving the responsibilities: raw intake, compiled knowledge, source provenance, logs, open threads, and indexes.

Native mode is not permission to skip provenance or boundary checks. It only changes paths and naming.

## Canonical Knowledge Paths

Default canonical knowledge lives under:

```text
knowledge/<domain>/<subject>/<topic>/<case>/
```

Omit empty levels. Use the smallest path that stays navigable. Do not create deep empty trees. If a topic is a single page in a folder, use the local naming convention (`README.md`, `index.md`, or `<topic>.md`) from nearby files or `BRAIN.md`.

No-timestamped source-of-truth directories such as `knowledge/`, `references/`, `cookbook/`, `runbooks/`, `research/`, and `specs/` are living surfaces. Rewrite them into current truth. Timestamped Memory folders preserve history and evidence.

## Inputs That May Compile Into Knowledge

Compilation is not limited to `raw/`.

Default evidence inputs:

- `raw/` source material
- `logs/`
- `lessons/`
- `facts/`
- `fixes/`
- `steers/`
- `models/`
- `reflections/`

Treat these Memory folders as evidence and experience, not as automatically canonical truth. Search `knowledge/` first, then rewrite existing owner pages and append evidence according to the page model.

Do not read global agent memory outside the repo unless the user explicitly asks or `BRAIN.md` opts in.

## Raw Status Contract

Every raw entry should resolve to one of:

- `status: unprocessed` - ready for classification or extraction.
- `status: processed` - successfully absorbed into canonical owner pages.
- `status: blocked` - not currently extractable or not readable enough to promote.

Use `blocked_reason` for blocked files. Common blockers include missing transcript, login wall, deleted source, OCR needed, encrypted file, unsupported binary, tool unavailable, or metadata-only access.

Promote only readable primary content. Do not infer durable claims from URL metadata, previews, search snippets, landing pages, or missing media.

Cleanup rule:

- Mark raw files as processed by default.
- If `BRAIN.md` says to remove processed queue pointers, remove only the exact processed pointer.
- Never bulk-delete unresolved raw material while processing a neighboring readable source.

## Evidence Labels

Keep confidence visible when source quality differs. Useful labels include:

- primary source
- official documentation
- research paper
- transcript
- practitioner commentary
- anecdotal evidence
- sponsored directional evidence
- case-pattern evidence
- metadata-only or unreadable

Weaker sources can still be useful, but they must not be flattened into benchmark claims or high-confidence facts.

## Required Write Discipline

For each compile pass:

1. Read `BRAIN.md`, index pages, and likely owner pages before writing.
2. Search for an existing canonical owner before creating a page.
3. Rewrite the compiled/current-truth section for changed knowledge.
4. Append dated evidence or timeline notes for provenance.
5. Record contradictions and open threads explicitly.
6. Refresh indexes/logs that the local brain uses.
7. Report processed files, blocked files, pages created, pages updated, contradictions, and open questions.
