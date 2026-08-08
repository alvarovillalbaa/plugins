# Upstream Merge Policy

This policy belongs to explicitly requested canonical source maintenance through
`plugins-management`. `auto-improve` is local-only and must not enter this flow.

## Classifications

| Class | Goes upstream? | Examples |
| --- | --- | --- |
| Upstream-safe | Yes | generic SKILL.md guidance, scripts, references, evals |
| Personalization-template | Yes | placeholders, schemas, example values |
| Local/private | No | company data, local paths, customer context, credentials |
| Generated/runtime | No | rendered output, logs, caches, runtime installs |

Only upstream-safe and personalization-template changes can be proposed upstream.

## Flow

1. Locate nearest `.skillmeta.yml`.
2. Trace target path to source owner.
3. Classify changed files.
4. Fail closed if forbidden paths or likely private data appear.
5. Generate a patch bundle by default.
6. Open a PR only when the user has authenticated GitHub tooling and explicitly
   selects PR mode.

Installed-component updates use a separate no-loss merge flow: compare the
managed copy to its recorded base, fast-forward unchanged copies, three-way
merge disjoint edits, retain local content on conflicts, and stage the incoming
version under `.agents/.updates/`. Local personalization remains outside managed
source and is never part of an upstream proposal.

An installed-project conflict can be exported explicitly with:

```bash
scripts/plugins reconcile --project /path/to/project [selectors] \
  --output .agents/.updates/reconcile/manual-review
```

This is separate from `skillctl propose-upstream`. It creates a deterministic,
provider-neutral review bundle containing `manifest.json`, `REVIEW.md`, and the
available base/local/incoming conflict artifacts. Legacy managed-block entries
without recoverable base content are marked base-unavailable. Export mode never
invokes AI, applies a patch, mutates managed targets or lock state, clears a
conflict, or persists secrets. The bundle itself is never upstream evidence.

After a human reviews and manually applies a component resolution, the separate
repeatable `--accept-local <conflict-id>` mode may adopt its current local value.
It validates selected staged/base digests, requires confirmation or `--yes`, and
atomically clears only selected conflict metadata and saved artifacts without
editing the target or invoking AI. This runtime metadata adoption lets future
updates preserve the local customization against the latest accepted upstream
base; it is not an upstream proposal. Managed document blocks cannot be adopted:
restore generated content inside the markers and keep customization outside.

```bash
python3 scripts/skillctl.py trace-origin system/skills/plugins-management
python3 scripts/skillctl.py diff-classify --base origin/main --head HEAD --fail-on-private
python3 scripts/skillctl.py propose-upstream --mode patch --title "Maintain plugins-management skill"
```

## Branches

Use branch names like:

```text
plugin-maintenance/<skill-name>/<short-topic>
```

Use git worktrees for long-running or risky improvements so the main checkout
stays reviewable.
