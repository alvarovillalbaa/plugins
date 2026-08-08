# Quickstart

## Install

Prefer the first-party interactive installer. It supports complete plugins and
individual skills, commands, rules, and agents in the flat project-local
`.agents` layout:

```bash
git clone https://github.com/alvarovillalbaa/plugins.git ~/.local/share/clous-plugins
cd /path/to/your-project
~/.local/share/clous-plugins/scripts/plugins install
```

See [`INSTALLATION.md`](INSTALLATION.md) for explicit selectors and the supported
secondary paths: `npx skills add`, Claude/Codex marketplace installs, runtime plugin
directories, symlinks, external skill chains, and manual copies.

## Personalize

Configure known project values explicitly, or let the runtime ask only when a
missing value first becomes relevant:

```bash
~/.local/share/clous-plugins/scripts/plugins configure \
  --project . \
  --set user.role="Principal Engineer"
```

## Validate

```bash
python3 scripts/skillctl.py structure check --root .
python3 scripts/skillctl.py meta check --root . --require-all
python3 scripts/skillctl.py conflicts check --root .
python3 scripts/validate_skills.py .
```

## Update

Update the canonical clone, then merge the refreshed managed components into the
target project:

```bash
git -C ~/.local/share/clous-plugins pull --ff-only
~/.local/share/clous-plugins/scripts/plugins update --project /path/to/your-project
```

If the update cannot merge safely, export a provider-neutral review bundle only
after explicitly choosing to do so:

```bash
~/.local/share/clous-plugins/scripts/plugins reconcile \
  --project /path/to/your-project
```

The command writes base/local/incoming context when available and marks legacy
base content unavailable rather than inventing it. It does not invoke AI, apply
patches, mutate managed targets or locks, or persist secrets. Apply any reviewed
resolution manually. A component resolution that does not naturally converge
through `update` can then be adopted explicitly:

```bash
~/.local/share/clous-plugins/scripts/plugins reconcile \
  --project /path/to/your-project \
  --accept-local <conflict-id>
```

The adoption preview requires confirmation and changes only validated conflict
metadata; it never edits the component. Managed document blocks are not
adoptable—restore the generated block and keep customization outside its
markers.
