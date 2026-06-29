# Quickstart

## Install

- **Claude Code marketplace:** add the root marketplace and install one department plugin, for example `engineering@agent-company`.
- **Local Claude development:** `claude --plugin-dir /path/to/plugins/engineering`.
- **Codex:** point Codex at one department directory, for example `/path/to/plugins/engineering`.
- **Portable skills:** install or symlink individual folders from `<department>/skills/<skill-name>/`.

Prefer a source-tracked local clone for skills that agents may improve later:

```bash
git clone https://github.com/alvarovillalbaa/plugins.git ~/.agent-sources/plugins
cd ~/.agent-sources/plugins
python3 scripts/skillctl.py install system/skills/auto-improve --agent codex --mode symlink
```

## Personalize

Initialize local overlays on first use:

```bash
python3 scripts/skillctl.py personalize init --skill system/skills/auto-improve
```

Update learned preferences only in the overlay:

```bash
python3 scripts/skillctl.py personalize update \
  --skill system/skills/auto-improve \
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

From repo root you can run `./scripts/update.sh` to auto-detect and update, or
`./scripts/update-from-upstream.sh` for a direct git-based update.
