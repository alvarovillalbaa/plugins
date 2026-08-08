# Source And Runtime Skill Model

`alvarovillalbaa/plugins` is the canonical upstream source for this package.
Agent runtime directories are install targets, not upstream owners.

## Layers

| Layer | Example | Rule |
| --- | --- | --- |
| Source | `system/skills/<name>` in this repo | Explicit `plugins-management` source maintenance happens here. |
| Preferred project install | `.agents/{skills,commands,rules,agents}` | Flat managed runtime; trace provenance through `.agents/.plugin-lock.json`. |
| Runtime-specific install | `~/.codex/skills`, `~/.cursor`, `~/.openclaw` | Secondary compatibility path; trace provenance before using as evidence. |
| Runtime cache | Claude plugin/cache folders | Never treat as source of truth. |
| Local overlay | `.overlays/`, `personalize.local.yml` | Private and ignored. |
| Generated output | `.generated/`, `.skill-improvements/` | Review artifacts, not upstream content. |
| Reconciliation review | `.agents/.updates/reconcile/<bundle-id>/` | Local provider-neutral conflict context; never source, lock authority, or proof of resolution. |

## Update Rule

Use the first-party project installer by default. Copy mode writes lockfile
provenance and base state for no-loss three-way updates; symlink mode is an
advanced source-development option. If a runtime only supports its own copy or
cache install, trace improvements back to the source path in `.skillmeta.yml`.

Every source skill must have `.skillmeta.yml`. Runtime copies, `.agents`
materializations, and cache folders must not become source owners even when an
agent improves them locally.

## Installed Update Reconciliation

`scripts/plugins reconcile --project <path> [selectors] [--output <dir>]`
exports recorded base, current local, and incoming conflict artifacts when they
exist, plus a manifest and provider-neutral review prompt. Legacy support-lock
entries that predate recoverable base content remain explicitly
base-unavailable.

Export mode never invokes AI, applies a patch, changes managed targets or locks,
or persists secrets. Reconciliation bundles remain local generated output. A
person reviews and manually applies any component suggestion first.

After that review and application, repeatable `--accept-local <conflict-id>` is
a separate confirmation-gated runtime metadata action. It validates the
selected staged incoming and saved base artifacts, never edits the component
target, and atomically removes only those conflict/staged/base records. Future
updates compare the current local customization against the latest accepted
upstream base. Managed document blocks are not adoptable: restore the generated
block and keep project content outside its markers.

## Source Contributors

This is a separate, explicitly requested `plugins-management` workflow.
`auto-improve` never performs these steps. Contributors without GitHub write
access can prepare source changes as follows:

1. Edit the canonical source in the explicitly scoped maintenance checkout.
2. Classify the diff with `skillctl diff-classify`.
3. Keep private overlays local.
4. Generate a patch bundle with `skillctl propose-upstream --mode patch`.
5. Submit that patch through their preferred review channel or create a PR.
