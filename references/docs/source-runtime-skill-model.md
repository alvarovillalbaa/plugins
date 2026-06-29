# Source And Runtime Skill Model

`alvarovillalbaa/plugins` is the canonical upstream source for this package.
Agent runtime directories are install targets, not upstream owners.

## Layers

| Layer | Example | Rule |
| --- | --- | --- |
| Source | `system/skills/auto-improve` in this repo | Safe upstream edits happen here. |
| Runtime install | `~/.codex/skills`, `~/.cursor`, `~/.openclaw` | Trace provenance before using as evidence. |
| Runtime cache | Claude plugin/cache folders | Never treat as source of truth. |
| Local overlay | `.overlays/`, `personalize.local.yml` | Private and ignored. |
| Generated output | `.generated/`, `.skill-improvements/` | Review artifacts, not upstream content. |

## Update Rule

Use symlink installs from a local clone when possible. If a runtime only supports
copy or cache installs, write lockfile provenance and route improvements back
to the source path in `.skillmeta.yml`.

Every source skill must have `.skillmeta.yml`. Runtime copies and cache folders
must not become source owners even when an agent improves them locally.

## External Users

External users should be able to improve skills without GitHub write access:

1. Run improvement locally.
2. Classify the diff with `skillctl diff-classify`.
3. Keep private overlays local.
4. Generate a patch bundle with `skillctl propose-upstream --mode patch`.
5. Submit that patch through their preferred review channel or create a PR.
