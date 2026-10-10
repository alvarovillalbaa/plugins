# Brain Contract

Last updated: 2026-10-10

Use this reference before any second-brain run that may write, reorganize, or compile knowledge. It defines the storage contract that the `brain` and `ingestion` skills must preserve.

Use the repo's shared promotion matrix for target selection across memory, facts, fixes, lessons, raw sources, generated artifacts, and living docs: `../../../../references/docs/promotion-matrix.md`.

## Boundary Rule

A run has one explicitly selected workspace. `AGENTS.md` supplies operating
rules; it is not a marker whose recursive count determines ownership.

Before canonical writes:

1. Resolve the repository or workspace explicitly targeted by the request.
2. Read its root `AGENTS.md` and the nearest applicable scoped instructions.
3. Nested `AGENTS.md` files refine scope; they do not make the workspace ambiguous.
4. Inspect navigation and existing owner pages before writes. If the request
   leaves several independent workspaces equally plausible, clarify that scope.
5. Keep writes inside the selected workspace unless cross-repo work is authorized.

For an explicit subdirectory, inherit applicable parent guidance and read its
scoped guidance. Missing instructions alone do not revoke a user's implementation
or bootstrap authorization; report the missing guidance and use the installed
AFS contract plus the current request.

## AFS Authority

The Agentic File System (AFS) is defined **externally** and is deliberately not restated here.

- **Skill**: `use-afs` — install with `python3 scripts/install-external-skills.py --skill use-afs --agent codex`. It is the authoritative and only source for the AFS layout, folder taxonomy, naming conventions, timestamp format, and responsibility mapping.
- **Reference site**: `afs-livid.vercel.app`
- **Source repo**: `github.com/alvarovillalbaa/afs`

Before any AFS-pathed write, read `use-afs`. If it is not installed, **stop and report the install command** rather than inferring or reconstructing the taxonomy from memory or from folders that happen to exist in the target repo.

Local deltas AFS does not define live in [`../../../../references/docs/afs-profile.md`](../../../../references/docs/afs-profile.md).

The adaptation modes below describe *how much* of AFS applies to a given workspace. They do not define what AFS contains.

## Adaptation Modes

`AGENTS.md` may define the mode in plain English, tables, YAML, or another local format. Follow the current request and local contract over these defaults.

### strict-afs

Use when no meaningful local standard exists. Create or follow the full AFS shell exactly as `use-afs` defines it, including its installation profile for the repo's shape — application repositories place the shell in `docs/`.

Use the current requested timestamp convention; otherwise follow the local
`AGENTS.md` or installed AFS convention.

### partial-afs

Use when the workspace already has some AFS roles but not the full tree. Map the AFS responsibility to the existing folder instead of forcing a migration.

Examples:

- `knowledge/` exists but `facts/` does not: compile canonical knowledge into `knowledge/` and leave facts in the closest Memory equivalent.
- A repo has continuous research: use living unit folders with ordered questions,
  hypotheses, reasoning, method, evidence, status, and next action. Existing
  notes become evidence without inventing a completed experiment.
- A repo has a source-material catalog: maintain `SOURCES.md` with Drive
  provenance rather than scattering duplicate source pages.

### native

Use when the company or user already has a standard that covers the same responsibilities. Follow that standard fully while preserving the responsibilities: raw intake, compiled knowledge, source provenance, logs, open threads, and indexes.

Native mode is not permission to skip provenance or boundary checks. It only changes paths and naming.

## Canonical Knowledge Paths

`use-afs` owns the knowledge surface and its internal path shape. What this contract adds:

Omit empty levels. Use the smallest path that stays navigable. Do not create deep empty trees. If a topic is a single page in a folder, use the local naming convention (`README.md`, `index.md`, or `<topic>.md`) from nearby files or `AGENTS.md`.

`knowledge/` holds unique generalized knowledge, perspectives, and synthesis.
Copied articles, book summaries, provider documentation, and source extracts
remain Drive material or generated library artifacts. Repo operating procedures
belong to technical owner guides, cookbooks, and runbooks. Facts and decisions
keep their own maintained owners; compilation is not permission to put all
information in knowledge. `REFERENCES.md` catalogs references; `SOURCES.md`
records source provenance; `GAPS.md` names unread evidence and unresolved scope.

Source-of-truth surfaces are living: rewrite them into current truth. Timestamped Memory surfaces preserve history and evidence. `use-afs` decides which is which.

## Inputs That May Compile Into Knowledge

Compilation is not limited to raw source material. Every AFS Memory surface — plus raw intake — is a valid evidence input.

Treat Memory surfaces as evidence and experience, not as automatically canonical truth. Search the knowledge surface first, then rewrite existing owner pages and append evidence according to the page model.

Do not read global agent memory outside the repo unless the user explicitly asks or `AGENTS.md` opts in.

## Raw Status Contract

Preserve raw entries in the ownership-appropriate private Drive account. Select
and verify the connected account and destination before upload. Use temporary
staging for extraction; do not create a durable repository `raw/` folder. Keep
original bytes, record size and SHA256, and verify the remote download before
removing an explicitly migrated local original. `SOURCES.md` records the stable
artifact URL, archive member path when applicable, checksum, and reading status.
Do not commit local absolute paths, signed download URLs, or authentication data.

Every source catalog entry should resolve to one of:

- `status: unprocessed` - ready for classification or extraction.
- `status: processed` - successfully absorbed into canonical owner pages.
- `status: blocked` - not currently extractable or not readable enough to promote.

Use `blocked_reason` for blocked files. Common blockers include missing transcript, login wall, deleted source, OCR needed, encrypted file, unsupported binary, tool unavailable, or metadata-only access.

Promote only readable primary content. Do not infer durable claims from URL metadata, previews, search snippets, landing pages, or missing media.

Cleanup rule:

- Mark an entry processed only after readable evidence was absorbed successfully.
- Update the catalog status; retain the original Drive artifact unless explicitly
  authorized to remove it. If `AGENTS.md` permits removing processed queue
  pointers, remove only the exact pointer while preserving its provenance.
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

1. Read `AGENTS.md`, index pages, and likely owner pages before writing.
2. Search for an existing canonical owner before creating a page.
3. Rewrite the compiled/current-truth section for changed knowledge.
4. Append dated evidence or timeline notes for provenance.
5. Record contradictions and open threads explicitly.
6. Refresh indexes/logs that the local brain uses.
7. Report processed files, blocked files, pages created, pages updated, contradictions, and open questions.
