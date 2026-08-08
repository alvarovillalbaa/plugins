# Plugins Brain Contract

Last updated: 2026-06-26

This repo uses partial AFS mode. The repository is the active brain for plugin, skill, command, agent, and documentation-maintenance work.

## Boundary

- This `BRAIN.md` governs `/Users/alvipe/Desktop/plugins`.
- Do not infer or write into sibling repos from this brain. Paired repos such as `/Users/alvipe/Desktop/SOFTWARE/CLOUS/plugins` are separate brains unless the user explicitly targets them.
- Runtime installs, caches, and generated bundles are evidence only. They are not source owners.

## Canonical Paths

| Responsibility | Repo path |
| --- | --- |
| Skill source | `<department>/skills/<skill>/` |
| Commands | `<department>/commands/*.md` |
| Agents | `<department>/agents/*.md` |
| Skill taxonomy | `skills-chaining-map.md` |
| External skill registry | `references/external-skills.yaml` |
| Skill audits | `docs/audits/skills/` |
| Skill changelog | `docs/changelog/skills/` |
| Durable docs policy | `references/docs/` |
| Generated improvement bundles | `.skill-improvements/` |

## AFS Adaptation

- AFS is defined externally by the `use-afs` skill. This file does not restate its folder taxonomy, naming conventions, or timestamp format — read `use-afs` for those. If it is not installed, stop AFS-pathed work and report the install command.
- Local profile and exceptions: [`references/docs/afs-profile.md`](references/docs/afs-profile.md).
- This repo uses the application-repository profile: the documentation shell lives in `docs/`.
- This repo preserves the established skill-audit convention: skill audit reports live directly under `docs/audits/skills/` with date-prefixed filenames.
- Do not create a parallel root `audits/` tree for skill-audit work in this repo.
- Do not recreate retired durable-fact folder names; use the fact surfaces `use-afs` defines.

## Promotion

Use `references/docs/promotion-matrix.md` before promoting a learning, fact, fix, rule, raw source, or generated improvement artifact into a durable location.
