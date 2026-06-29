# Changelog

## [Unreleased]

### Added

- **Source/runtime skill metadata** – Every active skill now has `.skillmeta.yml` provenance for `alvarovillalbaa/plugins`, overlay-only personalization policy, upstream-safe path rules, and quality gates.
- **Skill personalization tooling** – `scripts/skillctl.py` now supports structure checks, metadata generation/checks, first-use overlay initialization, continuous overlay updates, rendering, diff classification, installs, and patch-bundle proposals.
- **Department structure contract** – Department plugins now include `mcp.json` and `rules/`, with hooks/scripts owned by skills or root tooling only.

### Changed

- **Validation** – `scripts/validate_skills.py` now runs full metadata,
  structure, and conflict checks; `scripts/validate-plugin.sh` supports both
  source-root and department-root validation; CI includes `skill-pr-check.yml`.
- **Hook/script ownership** – External-skill checks, memory error capture, and autoresearch runner moved from plugin-level folders into owning skill folders.

### Added (comprehensive plan)

- **Canonical skill layout** – Active skills are self-contained folders with
  `SKILL.md` plus `examples/`, `hooks/`, `references/`, `scripts/`, and
  `templates/` placeholders or content.
- **Router taxonomy** – Parent skills stay installable as compact routers, with
  child skills and `skills-chaining-map.md` owning routing and external-chain
  precedence.
- **Agents** – Department agents are small orchestrators with scope, primary
  skills, commands, workflow, and output contract.
- **Commands** – Command files declare stable workflow entry points with
  frontmatter names, argument hints, allowed tools, and explicit skill routing.
- **Install/update** – README and quickstart docs describe department plugin
  installs, source-tracked skill installs, personalization overlays, and
  update scripts.
- **Hooks** – Runtime hook adapters live inside owning skills; department
  plugin roots do not own active `hooks/` or `scripts/` directories.

### Changed

- README and reference docs now describe the department-plugin layout,
  source/runtime model, external skill chains, and validation commands.
- QUICKSTART documents department installs, source-tracked installs,
  personalization overlays, validation, and updates.

---

## [1.0.0] – 2025-02-22

### Added

- **Plugin manifest** – `.claude-plugin/plugin.json` for Claude Code discovery.
- **README** – Features, skills/commands/agents tables, install (Claude plugin, npx skills add, OpenClaw), configuration, quick start, update instructions.
- **Skills** – All skills use canonical layout with `SKILL.md` (frontmatter + instructions). Migrated from `v1/instruction.j2` where applicable: fundraising, competitors, industry-discovery, outreach, prospect. Filled minimal skills: accounting-reconciliation, briefings, financial-modeling, linkedin-articles, linkedin-engagement. Placeholders: email-inbox-management, x-engagement. Optional references for slides and video.
- **Agents** – content-manager, financial-manager, sales-manager, social-media-manager filled as multi-skill orchestrators with workflow and skill mapping.
- **Commands** – Department command files remain the stable workflow entry points.
- **Hooks** – Runtime hooks are explicit skill-owned adapters; active plugin-root hooks are no longer part of the source layout.
- **Docs** – QUICKSTART updated for department plugins, source-tracked installs, and personalization overlays.
- **Validation** – scripts/validate-plugin.sh updated for department plugin structure; references/templates/examples remain optional.

### Changed

- session-start.sh now loads repo-local agent-company context files when present.
