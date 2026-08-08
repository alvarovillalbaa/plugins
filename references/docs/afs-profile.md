# AFS Profile

Last updated: 2026-08-07

AFS (the Agentic File System) is defined **externally** and is deliberately not restated here or in
any skill in this repo. Duplicating it caused drift; this file exists so there is exactly one place
for the parts AFS does not define.

- Skill: `use-afs` (registered in [`../external-skills.yaml`](../external-skills.yaml))
- Canonical: [afs-livid.vercel.app](https://afs-livid.vercel.app) · [github.com/alvarovillalbaa/afs](https://github.com/alvarovillalbaa/afs)

## AFS gate (blocking)

Before any AFS-pathed read, write, move, or scaffold, confirm `use-afs` is installed and read it for
the layout, folder taxonomy, naming conventions, and timestamp format.

If it is not installed, **stop and report**:

```bash
python3 scripts/install-external-skills.py --skill use-afs --agent codex
```

Do not infer, reconstruct, or improvise the taxonomy from memory, from neighboring files, or from
folders that happen to exist in the target repo. A missing `use-afs` blocks AFS-pathed work; it does
not license a guess.

This does not block non-AFS documentation work: inline docs, in-folder docs, and edits to files that
already exist in known locations proceed normally.

## Local profile

Everything below is a local decision or a local extension. AFS owns everything else.

### Installation profile

AFS defines installation profiles by repo shape. For the developer repos this repo's skills operate
on, select the **application-repository profile**: the AFS shell lives in `docs/`.

Consequences:

- Regular documentation goes under `docs/` inside the repo.
- Root UPPERCASE instruction docs stay at the **repo root**, not in `docs/`.
- In-folder documentation stays beside the code it describes (see below) and is never relocated
  into `docs/`.

Follow the target repo's existing convention when it already has one. Detect the profile before
writing; do not migrate a repo between profiles without an explicit request.

### In-folder documentation contract

This contract is **not part of AFS** — it is owned here. Outside the AFS shell, every meaningful
code folder can carry its own documentation.

**Core** — consider first:

- `README.md` — entry point, purpose, usage, links to neighboring docs
- `ARC.md` — internals, boundaries, flows, and design decisions

**Conditional** — add only when the folder actually needs them:

- `SETUP.md` — non-obvious environment and initialization steps
- `RUNBOOK.md` — local operational workflow for this folder
- `CHANGELOG.md` — user-facing or package-facing release history
- `SECURITY.md` — security boundaries, secrets handling, abuse cases, review expectations

**Rare** — use when the domain justifies them:

- `OVERVIEW.md` — concept-first orientation when README would become too dense
- `FAQ.md` — repeated questions and troubleshooting
- `DECISIONS.md` — folder-local decisions that do not justify standalone ADRs
- `DEPENDENCIES.md` — dependency map, contracts, and upgrade notes

Use the smallest set that makes the folder legible.

### Living-doc freshness

Every living documentation file carries:

```markdown
Last updated: YYYY-MM-DD
```

Place it directly under the H1 or immediately after frontmatter, and refresh it whenever the file is
touched. Which folders are living versus timestamped is an AFS question — ask `use-afs`.

### Repo-local exceptions

These apply to this plugins repo only:

- Skill audits stay directly under `docs/audits/skills/` with date-prefixed filenames. Do not create
  a parallel root `audits/` tree here.
- Skill changelogs stay under `docs/changelog/skills/`.
- Generated improvement bundles live in `.skill-improvements/` and are evidence, not durable memory.

See [`../../BRAIN.md`](../../BRAIN.md) for this repo's brain boundary and canonical paths, and
[`promotion-matrix.md`](promotion-matrix.md) for choosing an owner when a signal becomes durable.
