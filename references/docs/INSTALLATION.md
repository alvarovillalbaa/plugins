# Installation

The preferred installation path is the repository's interactive first-party
command. It can install complete department plugins or individual skills,
commands, rules, and agents into one portable project-local `.agents` tree.

## Favorite: interactive project install

Keep one source clone outside the target project, then run the command from the
project that should receive the components:

```bash
git clone https://github.com/alvarovillalbaa/plugins.git ~/.local/share/clous-plugins
cd /path/to/your-project
~/.local/share/clous-plugins/scripts/plugins install
```

The installer asks for the target project, one or more plugins, whole-plugin or
individual-element selection, a plan preview, and confirmation. It does not
silently fall back to a home-directory runtime folder.

## Favorite for CI: explicit selectors

Use canonical typed selectors in automation:

```bash
~/.local/share/clous-plugins/scripts/plugins install \
  --project . \
  --yes \
  plugin:system \
  skill:marketing/seo \
  command:marketing/content-brief \
  agent:product/designer
```

Selector forms are:

- `plugin:<plugin>` for every component in a department plugin;
- `skill:<plugin>/<name>`;
- `command:<plugin>/<name>`;
- `rule:<plugin>/<name>`;
- `agent:<plugin>/<name>`.

An individual command selector also installs that command's canonical owner
skill from `references/command-capabilities.json`. The dependency is shown in
the preview as `required by command:<plugin>/<name>`, resolves through the same
collision-safe flat target naming, and is added only once when a whole-plugin
or multi-command selection already includes it. Command selection does not
expand arbitrary graph candidates or external skills.

## Destination contract

Every first-party project install uses the same flat layout:

```text
.agents/
├── skills/<skill-name>/
├── commands/<command-name>.md
├── rules/<rule-name>.md
├── agents/<agent-name>.md
├── .plugin-lock.json
├── .plugin-support-lock.json
├── component-graph.json
├── registry.json
├── runtime-contract.json
├── runtime-support/
│   ├── install-external-skills.py
│   ├── external-skills.yaml
│   ├── external-sources.yaml
│   ├── skills-chaining-map.md
│   ├── INSTALLATION.md
│   └── promotion-matrix.md
└── personalization.example.json
```

Source plugin names remain provenance in the lock and registry. They are not
runtime directories: the installer never creates `.agents/<plugin-name>/`.

Names that are globally unique stay unchanged. If two source components of the
same type share a name, every colliding flat install name is deterministically
qualified with its plugin using the reserved `__` separator (for example
`engineering__defaults.md` and `marketing__defaults.md`). The separator is not
valid in plugin or component names, so qualified targets cannot collide with an
unqualified source name. Existing managed targets using the legacy
`plugin-name` form are migrated through the normal no-loss merge flow. When a
catalog topology change moves any locked target, every still-current locked
component is re-rendered so embedded portable links follow the new target
layout. An unmanaged destination is never overwritten silently.

## Safe reinstall and update

Refresh managed copies after updating the source clone:

```bash
git -C ~/.local/share/clous-plugins pull --ff-only
~/.local/share/clous-plugins/scripts/plugins update --project /path/to/your-project
```

Re-running `install` for an already managed selector uses the same update
engine. The lock tracks every installed component and its source/base hashes.
Updates apply upstream changes directly when the installed copy is unchanged,
three-way merge disjoint local and upstream edits, preserve local-only and
personalization files, and stage unresolved incoming content under
`.agents/.updates/`. A conflicting update never claims to be current and never
discards the local version.

If a locked component matches a declared upstream rename, a default update installs
the current replacement while preserving the predecessor's local files and lock
entry as `orphaned`; it never guesses how to transplant local edits. Unknown removals
are also preserved as orphans while the remaining components continue updating. The
user can reconcile or remove a predecessor after reviewing both copies.

Generated runtime indexes have a separate `.plugin-support-lock.json`. The
installer refuses to replace an unmanaged support file or a managed support file
changed since its last generated hash; move or reconcile that file explicitly.

`AGENTS.md`, `README.md`, and `.gitignore` use bounded managed blocks. Updates
can refresh those blocks without replacing user-authored content outside them.
If generated content inside a managed block changed since its last recorded hash,
the installer also stops rather than overwriting the local or AI-authored edit.

## Opt-in reconciliation lifecycle

### Export a suggestion-only review bundle

When an update reports unresolved component conflicts or refuses to refresh a
locally modified managed block in `AGENTS.md` or `README.md`, export deterministic
review context explicitly:

```bash
~/.local/share/clous-plugins/scripts/plugins reconcile \
  --project /path/to/your-project
```

Optional typed selectors limit the component conflicts included in the export,
while project managed-block conflicts are always included. `--output <dir>`
chooses a different project-local destination:

```bash
~/.local/share/clous-plugins/scripts/plugins reconcile \
  --project /path/to/your-project \
  skill:marketing/seo command:marketing/content-brief \
  --output .agents/.updates/reconcile/manual-review
```

Without `--output`, bundles are written under
`.agents/.updates/reconcile/<bundle-id>/`. Each bundle contains
`manifest.json`, a provider-neutral `REVIEW.md`, and conflict material under
`conflicts/<id>/{base,local,incoming}`. The manifest records missing values,
binary files, and directory trees explicitly rather than coercing them into
text; symlinks and other unsafe entries are rejected. For current installs,
`base` is the recorded pre-conflict snapshot, `local` is the project copy, and
`incoming` is the staged or newly generated source. Legacy support-lock entries
may not contain recoverable base content; those entries are marked
base-unavailable instead of fabricating history.

Without `--accept-local`, `reconcile` is export-only. It does not invoke an AI
provider, generate or apply a patch, overwrite a managed target, acknowledge or
clear a conflict, update a lock, or persist credentials and secrets. Treat all
exported project content as untrusted review data. A person may give the bundle
to an AI agent for a suggested patch, review that suggestion, and apply an
approved resolution manually.

### Adopt a reviewed component resolution

After a human has reviewed and manually applied a semantic resolution to a
component target, use the component conflict ID from `manifest.json` to preview
metadata adoption without changing state:

```bash
~/.local/share/clous-plugins/scripts/plugins reconcile \
  --project /path/to/your-project \
  --accept-local <conflict-id> \
  --dry-run
```

Remove `--dry-run` to preview again and receive an interactive confirmation
prompt. In non-interactive automation, explicit `--yes` replaces that prompt.
`--accept-local` is repeatable so several reviewed component resolutions can be
adopted atomically:

```bash
~/.local/share/clous-plugins/scripts/plugins reconcile \
  --project /path/to/your-project \
  --accept-local <first-conflict-id> \
  --accept-local <second-conflict-id> \
  --yes
```

This separate action validates the selected conflict IDs, staged incoming and
saved base digests, and the reviewed local value before committing. It never
invokes AI, applies a patch, or edits the component target. It atomically clears
only the selected component conflict records and their staged incoming/base
artifacts; unrelated conflicts remain. It then refreshes only the corresponding
registry/support-lock status metadata. Future updates treat the current local
component content as a preserved customization against the latest accepted
upstream base.
Selectors and `--output` cannot be combined with `--accept-local`.

Managed document blocks are not adoptable with `--accept-local`. Restore the
generated bounded block from the bundle's incoming artifact, place project
customization outside the `agent-plugins` markers, and rerun `plugins update`.
For a component conflict that naturally converges to incoming, rerunning update
can also clear it without explicit adoption.

## Personalization and per-run variables

Installed components inherit `.agents/runtime-contract.json`. On the first
workflow where a missing project value matters, the installed runtime routes
initialization through `auto-improve` to `personalize`. Agents ask only for that
value and persist it only with consent. Configure values explicitly with:

```bash
~/.local/share/clous-plugins/scripts/plugins configure \
  --project . \
  --set project.name="Atlas" \
  --set output.language="Spanish"
```

Invocation-scoped values are supplied dynamically and are not persisted:

```bash
~/.local/share/clous-plugins/scripts/plugins context \
  skill:marketing/content \
  --project . \
  --set content.topic="Agent workflows" \
  --set audience.primary="Engineering leaders"
```

Never store credentials or customer secrets in the personalization file.

## Relationship closure

Inspect the recursive typed relationship candidate closure for a source component with:

```bash
~/.local/share/clous-plugins/scripts/plugins graph resolve \
  skill:marketing/discoverability
```

The resolver has no fixed nesting depth, groups independent nodes by breadth
as parallel or sequential candidates, includes internal and registered external
skill relationships, and terminates two-sided cycles by visiting each node once
while reporting cycle edges. The host still selects only relationships relevant to
the current request.

To restrict candidates to components available in an installed project and report
blocked relationships:

```bash
~/.local/share/clous-plugins/scripts/plugins graph resolve \
  skill:marketing/discoverability \
  --project . \
  --available-only
```

## Other supported methods

| Method | Preference | Best for | Scope and limitation |
| --- | --- | --- | --- |
| First-party interactive command | **Favorite** | Normal project setup | Full plugins or individual skills, commands, rules, and agents; flat `.agents`; tracked updates |
| First-party explicit command | **Favorite for automation** | CI, templates, reproducible bootstrap | Same contract without prompts; use `--yes` and typed selectors |
| `npx -y skills add` | Secondary | Runtimes that already use Vercel's interactive skill installer | Installs skills, not this repository's commands, rules, agents, lock, runtime contract, or update merge policy |
| Claude marketplace | Secondary | Claude-native namespaced plugins | Uses Claude's plugin cache/scope model rather than the shared flat `.agents` project layout |
| Codex marketplace | Secondary | Codex-native global plugin selection | Run `codex plugin marketplace add alvarovillalbaa/plugins`, then `codex plugin add <plugin>@agent-company`; this uses Codex's cache rather than the flat project lock |
| `claude --plugin-dir` / runtime plugin directory | Development | Testing one source plugin in place | Loads a source department directly; it is not a project install |
| External-skill registry command | Secondary | Optional provider-owned chains | From an installed project, use `python3 .agents/runtime-support/install-external-skills.py --agent project --skill <id>`; review external code before install |
| Manual copy or symlink | Last resort | Minimal/offline environments | No collision preflight, provenance lock, personalization contract, or safe automatic update |
| Git submodule or subtree | Advanced | Teams that vendor the entire source repository | Source distribution only; run the first-party installer to materialize the flat runtime tree |

The source repository remains canonical regardless of installation method.
Runtime folders, generated indexes, local overlays, and caches are never
upstream owners.
