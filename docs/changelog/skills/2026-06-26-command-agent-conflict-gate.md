# Command and Agent Conflict Gate - 2026-06-26

## Added

- Added `python3 scripts/skillctl.py conflicts check --root .` to validate
  flat skill, command, and agent naming; profile/file consistency; command and
  agent skill references; command frontmatter shape; direct skill-agent
  activation tokens; plugin manifest drift; chain-map references; external
  skill registry shape; explicit external install/optional-chain references;
  and skill README install paths; backtick command-skill references; local
  skill-path references in active docs; and local Markdown links in active
  skills, commands, agents, READMEs, root docs, the skills chaining map, and
  audit/changelog documentation.
- Added TEAM/profile drift validation for department `TEAM.md` headings and
  profile-listed team members.
- Added command agent-tool validation: commands that explicitly invoke or spawn
  agents must declare `Agent`, and stale `Task` tool aliases are rejected.
- Added agent command-reference validation so agent `## Commands` sections must
  point at existing command names.
- Added agent frontmatter validation for `tools` and `disallowedTools`, plus
  spawned-by slash-command references in agent descriptions.
- Wired the conflict gate into `python3 scripts/validate_skills.py`.
- Added unit coverage for colonized command names, stale skill README paths, and
  unknown command skill references.
- Added unit coverage for broken local Markdown links in active skill
  references and for Markdown-like code fences.
- Added unit coverage for backtick command-skill references, active-doc
  skill-path references, and non-plugin `/skills/` path fragments.
- Added unit coverage for external registry required fields, duplicate install
  names, unknown optional external chains, and registered `--skill` install
  references.

## Fixed

- Corrected `finances/skills/finances/README.md` install and source paths.
- Corrected `productivity/skills/prospect/README.md` install and source paths.
- Updated `engineering/commands/repo-review.md` to reference the existing
  `visualization` skill instead of missing `visualizer`.
- Added missing `name: research` frontmatter to
  `productivity/commands/research.md`.
- Normalized `productivity/commands/research.md` to bracketed `allowed-tools`
  syntax.
- Normalized current `visualization` skill prompts and references away from the
  stale `visualizer` install name.
- Fixed stale cross-skill handoff links for onboarding-flow implementation,
  product experiments, and the no-use-effect performance reference.
- Fixed stale parent-router links in active child `SKILL.md` files.
- Fixed current source-reference links for frontend implementation, conversion
  copy, UX copy, performance testing, memory-source, and no-use-effect
  references.
- Fixed moved-owner reference links across evals, prompt/tool design, cloud
  runbooks, web vuln validation, E2E testing, SEO, content audit, and product
  design-system references.
- Normalized `productivity/commands/research.md` citation contract wording so
  it does not look like a literal local Markdown link.
- Fixed department team docs so headings and profile-listed members match the
  current department taxonomy.
- Normalized command `allowed-tools` for agent-spawning workflows, including
  `review-pr`, `triage-prs`, `check-agent-compat`, `orchestrate`, `fix-ci`,
  and `launch-virality`.
- Fixed the live system agent and memory-hook headings away from stale
  learning-system naming.
- Renamed `references/docs/agent-suite-integration.md` to
  `references/docs/agent-company-integration.md`.
- Added `engineering/skills/frontend-e2e/references/typescript-e2e/postgres/docker-setup.md`.
- Aligned architecture, quickstart, and naming docs with the current
  seven-department taxonomy, conflict gate, and agent naming model.
- Updated `scripts/validate-plugin.sh` for source-root and department-root
  validation in the current plugin layout.
- Added explicit conflict-gate steps to the publish and PR-check workflows.
- Registered `office-hours` in `references/external-skills.yaml` so
  `productivity/commands/office-hours.md` does not point at an undeclared
  optional external chain.

## Validation

- Pass: `python3 scripts/skillctl.py conflicts check --root .`
- Pass: `python3 scripts/validate_skills.py`
- Pass: `python3 -m unittest scripts.tests.test_skillctl` (`Ran 29 tests`)
- Pass: `python3 -m py_compile marketing/skills/visualization/scripts/scaffold_visualizer.py scripts/skillctl.py scripts/validate_skills.py`
- Pass: conflict-gate Markdown link and local skill-path scan over active
  skills, commands, agents, READMEs, root docs, the skills chaining map, and
  audit/changelog docs with fenced code ignored
- Pass: `bash scripts/validate-plugin.sh`
- Pass: `cd engineering && bash ../scripts/validate-plugin.sh`
- Pass: `git diff --check`
