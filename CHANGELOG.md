# Changelog

## [Unreleased]

### Added

- **First-party project installer** – `scripts/plugins install` now interactively
  selects whole plugins or individual skills, commands, rules, and agents,
  installs them into a flat project-local `.agents` tree, and records a no-loss,
  rollback-capable component-and-lock transaction with conflict staging and
  collision migration.
- **Suggestion-only reconciliation bundles** – `scripts/plugins reconcile` now
  exports deterministic component and managed-document conflict context with
  available base/local/incoming artifacts and a provider-neutral review prompt.
  Export remains the default and never invokes AI, applies patches, mutates
  managed targets or locks, or treats a suggestion as a resolved update.
- **Explicit reviewed-resolution adoption** – Repeatable
  `reconcile --accept-local <conflict-id>` now previews and confirmation-gates
  atomic adoption of human-applied component resolutions. It validates saved
  conflict artifacts and clears only selected metadata without editing targets;
  managed document blocks remain bounded and non-adoptable.
- **Runtime personalization and variables** – Installed projects receive a
  shared first-use personalization contract, consent-based local store,
  invocation/session/project/default value resolution, and agent runtime rule.
- **Typed component graph** – Plugin, skill, command, rule, agent, and external
  skill relationships now resolve iteratively as conditional candidates at
  arbitrary finite depth, with installed-aware filtering, breadth-level parallel
  groups, cycle reporting, and a checked-in generated full graph.
- **LLM and agent discovery** – Added deterministic `catalog.json`, `llms.txt`,
  `llms-full.txt`, `context7.json`, CodeMeta, citation metadata, and drift tests.
- **Agentic execution skills** – Engineering now includes dynamic councils,
  bounded execution loops, dependency-aware work graphs, and persistent goal
  pursuit under the existing multi-agent owner.
- **World-class AI eval guidance** – The canonical `ai-evals` skill now covers
  composable operations and variables, strict manifests and gates, calibrated
  graders, scenarios, statistics, and capability-gated GEPA/FAPO/GA-style
  optimization without exposing hidden chain-of-thought.
- **Personal operating skills** – Productivity now includes evidence-led
  improvement, consensual roasting, performance reviews, and end-to-end single
  or multi-meeting workflows.
- **Course production and transparency** – Marketing adds `coursify` for
  multimodal course design and skill chaining; System adds
  `explain-yourself` and restores the canonical runtime-neutral `memory`
  owner.
- **Source/runtime skill metadata** – Every active skill now has `.skillmeta.yml` provenance for `alvarovillalbaa/plugins`, overlay-only personalization policy, upstream-safe path rules, and quality gates.
- **Skill personalization tooling** – `scripts/skillctl.py` now supports structure checks, metadata generation/checks, first-use overlay initialization, continuous overlay updates, rendering, diff classification, installs, and patch-bundle proposals.
- **Department structure contract** – Department plugins now include `mcp.json` and `rules/`, with hooks/scripts owned by skills or root tooling only.
- **Hook/script audit** – Added a generated 146-skill coverage matrix and a
  validator for registrations, executable contracts, documentation coverage,
  duplicate ownership, placeholders, and portability.

### Changed

- **Plugin presentation metadata** – All Codex manifests now include validated
  publisher, discoverability, interface, capability, and starter-prompt fields;
  the external skill installer defaults to project-local `.agents/skills`.
- **Canonical skill ownership** – Renamed `skills-management` to
  `plugins-management`, `computer-vision-systems` to `computer-vision`,
  `context-memory-rag` to `context-engineering`, `prompt-tool-design` to
  `prompt-engineering`, and `seo-and-geo` to `seo`.
- **Consolidated routers** – Added `testing` as the canonical owner for test
  strategy, coverage, backend testing, frontend E2E, flakes, and authorized
  business-logic/race testing; added `simplify` under `quality-assurance`; and
  folded specialist material into `pentest`, `reporting`, `growth`, `seo`, and
  `discovery`.
- **Official video skills** – `video` now routes HyperFrames and Remotion work
  to their official external repositories through the live skill registry.
- **Contract-test CI** – PR and publish workflows now discover and run every
  bundled Python skill test, including orchestration state machines, eval
  contracts, course manifests, and explanation rendering.
- **Validation** – `scripts/validate_skills.py` now runs full metadata,
  structure, and conflict checks; `scripts/validate-plugin.sh` supports both
  source-root and department-root validation; CI includes `skill-pr-check.yml`.
- **Hook/script ownership** – Hooks now mean registered automatic lifecycle
  behavior; deterministic tools live in `scripts/`, and advisory checklists
  live in skill instructions or references. The agent-harness Stop gate is the
  only automatic skill hook.
- **Generalized deterministic tooling** – Experiment sample floors, ICP
  scoring criteria, repositories, cache paths, and channel inventories are now
  caller-supplied, discovered, or environment-configured instead of tied to a
  person or company.

### Removed

- Removed the local `hyperframes` and `remotion` copies and the folded legacy
  skill directories; no alias or compatibility skill directories remain.
- Removed inert hook files, placeholder hook/script READMEs, duplicate
  cross-skill implementations, a canned user-story demo, and a
  schema-specific marketing/recruiting pacing monitor. Removed two overlapping
  dependency scanners with frozen CVE tables and the duplicate passive scanner
  from the active web-validation lane.

### Added (comprehensive plan)

- **Canonical skill layout** – Active skills are self-contained folders with
  `SKILL.md` plus only the optional references, examples, templates, and
  executable assets they actually use.
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
- **Hooks** – Skill-scoped lifecycle behavior is registered in `SKILL.md`
  frontmatter and its handler lives in the owning skill's `scripts/` directory;
  department plugin roots do not own unregistered hook files.

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
