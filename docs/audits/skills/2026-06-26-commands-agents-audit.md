# Commands and Agents Audit - 2026-06-26

## Summary

This audit reviews proposed command and agent additions against the current
department-plugin taxonomy.

Status: Done on 2026-06-26.

Recommendation: preserve the current model.

- Skills are the reusable capability units.
- Commands are stable, user-invoked workflows.
- Agents orchestrate multiple skills, commands, artifacts, or roles.
- External skills should be chained through `references/external-skills.yaml`
  and `skills-chaining-map.md`, not copied into every local command.

Current repo evidence after implementation:

- `python3 scripts/validate_skills.py` passes with `Validated 141 skill file(s).`
- `python3 scripts/skillctl.py conflicts check --root .` passes for 141 skills,
  56 commands, and 26 agents.
- The current filesystem has 56 non-legacy command files and 26 non-README
  agent files.
- `python3 scripts/check-external-skills.py --offline --all --agent codex`
  reports every configured external skill as missing from the Codex install
  target.
- The worktree is heavily dirty from the active taxonomy migration. Future
  implementation should add narrow files in canonical department directories
  and avoid restoring deleted legacy paths.

## Completion Evidence

Implemented command work:

- Fixed `productivity/commands/grill-me.md` to route to `productivity/skills/grill` plus optional external `grill-me` or `grilling`.
- Added `engineering/commands/grill-with-docs.md`.
- Added `engineering/commands/review-architecture.md`.
- Added `engineering/commands/deslop.md`.
- Added `system/commands/update-memories.md`.
- Added `engineering/commands/pr-merge.md`.
- Added `engineering/commands/retro.md`.
- Added `productivity/commands/office-hours.md`.
- Added `sales/commands/meet-with-clients.md`.
- Added `product/commands/product-review.md`.

Implemented agent work:

- Added `productivity/agents/ceo.md`.
- Added `productivity/agents/executive-assistant.md`.
- Added `engineering/agents/cto.md`.
- Added `engineering/agents/cloud-architect.md`.
- Added `engineering/agents/software-engineer.md`.
- Added `engineering/agents/ai-engineer.md`.
- Added `product/agents/product-manager.md`.
- Added `product/agents/designer.md`.
- Added `sales/agents/cso.md`.
- Added `sales/agents/gtm-engineer.md`.
- Added `sales/agents/sdr.md`.
- Added `sales/agents/account-executive.md`.
- Added `finances/agents/cfo.md`.
- Added `finances/agents/accountant.md`.

Implemented conflict remediation:

- Added `scripts/skillctl.py conflicts check --root .` for flat skill,
  command, and agent name collisions; profile/file drift; command and agent
  skill references; command frontmatter shape; direct skill-agent activation
  tokens; plugin manifest drift; chain-map references; external skill registry
  shape; explicit external install/optional-chain references; skill README
  install paths; backtick command-skill references; local skill-path references
  in active docs; and local Markdown links in active skills, commands, agents,
  READMEs, root docs, the skills chaining map, and audit/changelog
  documentation.
- Added TEAM/profile drift validation for department `TEAM.md` headings and
  profile-listed team members.
- Added command agent-tool validation: commands that explicitly invoke or spawn
  agents must declare `Agent`, and stale `Task` tool aliases are rejected.
- Added agent command-reference validation so agent `## Commands` sections must
  point at existing command names.
- Added agent frontmatter validation for `tools` and `disallowedTools`, plus
  spawned-by slash-command references in agent descriptions.
- Wired the conflict check into `python3 scripts/validate_skills.py`.
- Fixed stale install/source paths in `finances/skills/finances/README.md` and
  `productivity/skills/prospect/README.md`.
- Fixed `engineering/commands/repo-review.md` to route optional visual
  packaging to the existing `visualization` skill instead of missing
  `visualizer`.
- Added the missing `name: research` frontmatter to
  `productivity/commands/research.md`.
- Normalized `productivity/commands/research.md` to bracketed
  `allowed-tools` syntax.
- Normalized current `visualization` skill-facing surfaces away from the stale
  `visualizer` install name while preserving the scaffold script filename.
- Fixed stale handoff links across `engineering/skills/onboarding-flows`,
  `product/skills/experiments`, and `engineering/skills/performance`.
- Fixed stale parent-router links in active child `SKILL.md` files after the
  department-router split.
- Fixed current source-reference Markdown links in frontend implementation,
  conversion copy, UX copy, performance testing, memory-source, and
  no-use-effect references.
- Fixed moved-owner reference links across evals, prompt/tool design, cloud
  runbooks, web vuln validation, E2E testing, SEO, content audit, and product
  design-system references.
- Normalized `productivity/commands/research.md` citation contract wording so
  it does not masquerade as a literal local Markdown link.
- Fixed department team docs so headings and profile-listed members match the
  current department taxonomy.
- Normalized command `allowed-tools` for agent-spawning workflows, including
  `review-pr`, `triage-prs`, `check-agent-compat`, `orchestrate`, `fix-ci`,
  and `launch-virality`.
- Fixed the live system agent and memory-hook headings away from stale
  learning-system naming.
- Renamed the active integration doc from `agent-suite-integration.md` to
  `agent-company-integration.md` and updated the slides reference.
- Added the missing PostgreSQL E2E Docker setup reference linked from the
  frontend E2E knowledge index.
- Aligned `references/docs/ARCHITECTURE.md`, `references/docs/QUICKSTART.md`,
  and `references/docs/NAMING.md` with the current seven-department taxonomy,
  conflict gate, and agent naming model.
- Updated `scripts/validate-plugin.sh` so source-root validation delegates to
  the canonical validators and department-root validation checks the current
  manifest/profile/MCP/rules shape.
- Added explicit conflict-gate steps to `.github/workflows/publish_skills.yml`
  and `.github/workflows/skill-pr-check.yml`.
- Registered the optional `office-hours` external chain in
  `references/external-skills.yaml` so the `/office-hours` command routes only
  through declared external skill metadata.

Updated department profiles:

- `engineering/profile.yaml`
- `system/profile.yaml`
- `product/profile.yaml`
- `sales/profile.yaml`
- `finances/profile.yaml`
- `productivity/profile.yaml`

Validation:

- Pass: `python3 scripts/validate_skills.py`.
- Pass: `python3 scripts/skillctl.py conflicts check --root .`.
- Pass: `python3 scripts/skillctl.py meta check --root .`.
- Pass: `python3 -m unittest scripts.tests.test_skillctl` (`Ran 29 tests`).
- Pass: `python3 -m py_compile marketing/skills/visualization/scripts/scaffold_visualizer.py scripts/skillctl.py scripts/validate_skills.py`.
- Pass: conflict-gate Markdown link and local skill-path scan over active
  skills, commands, agents, READMEs, root docs, the skills chaining map, and
  audit/changelog docs with fenced code ignored.
- Pass: `bash scripts/validate-plugin.sh`.
- Pass: `cd engineering && bash ../scripts/validate-plugin.sh`.
- Pass: `git diff --check`.
- Expected offline state: `python3 scripts/check-external-skills.py --offline --all --agent codex` lists configured external skills as missing from the Codex install target.
- Pass: command and agent file-existence checks for every recommended addition.

## External Inputs

Use these as design references, not as source-of-truth replacements:

- Matt Pocock's skills repo:
  <https://github.com/mattpocock/skills>
- `grill-me`: tiny command-style skill that delegates into a grilling session:
  <https://raw.githubusercontent.com/mattpocock/skills/main/skills/productivity/grill-me/SKILL.md>
- `grill-with-docs`: grilling plus maintained docs/domain-model context:
  <https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/grill-with-docs/SKILL.md>
- Garry Tan `office-hours`: startup/builder forcing-question workflow:
  <https://raw.githubusercontent.com/garrytan/gstack/main/office-hours/SKILL.md>
- Garry Tan `retro`: weekly engineering retrospective workflow:
  <https://raw.githubusercontent.com/garrytan/gstack/main/retro/SKILL.md>

The useful pattern across these examples is not a large monolithic skill. It is
a thin trigger that routes into a sharper underlying workflow.

## Existing Model

The current taxonomy already matches the desired decomposition:

- Parent skills are compact routers.
- Child skills own lane-specific depth.
- Commands wrap stable end-to-end workflows.
- Agents coordinate multi-step or cross-functional work.
- `skills-chaining-map.md` is the canonical routing graph.
- External skills are registered in `references/external-skills.yaml`.

Important current owners:

| Surface | Current owner |
| --- | --- |
| adversarial plan critique | `productivity/skills/grill` and external `grill-me` or `grilling` |
| docs-backed grilling | `engineering/skills/architecture`, `code-documentation`, external `grill-with-docs` |
| memory updates | `system/commands/si:*`, `learning-sync`, `system/skills/memory` |
| financial modeling | `finances/commands/model-scenarios` |
| accounting reconciliation | `finances/commands/reconcile-books` |
| fundraising | `investor-messaging`, `materials-audit`, `pipeline-diagnostics` |
| PR review and triage | `engineering/commands/review-pr`, `triage-prs`, `engineering/skills/prs` |
| product/design review | `product/skills/product-development`, `product/skills/design`, `productivity/skills/design-review` |
| code cleanup/deslop | `engineering/skills/quality-assurance`, `engineering/skills/prs`, external `deslop` |

## Command Recommendations

| Proposed command | Status | Recommendation |
| --- | --- | --- |
| `/grill-me` | Done | `productivity/commands/grill-me.md` now points directly at `productivity/skills/grill` plus external `grill-me` or `grilling`. |
| `/grill-with-docs` | Done | Added `engineering/commands/grill-with-docs.md`; routes to `architecture`, `code-documentation`, and external `grill-with-docs`. |
| `/update-memories` | Done | Added `system/commands/update-memories.md`; orchestrates review, promote, remember, and learning-sync without replacing `si:*`. |
| `/financial-model` | Covered, no new file | Use `finances/commands/model-scenarios.md`; no hard rename was requested. |
| `/accounting-reconciliation` | Covered, no new file | Use `finances/commands/reconcile-books.md`; no hard rename was requested. |
| `/fundraising-*` | Covered, no wildcard | The narrower commands remain `investor-messaging`, `materials-audit`, and `pipeline-diagnostics`. |
| `/meet-with-clients` | Done | Added `sales/commands/meet-with-clients.md`; routes through `technical-sales`, `go-to-market`, `follow-up`, `outreach`, and optional `research`. |
| `/office-hours` | Done | Added `productivity/commands/office-hours.md`; uses an interview workflow for idea quality, demand reality, wedge, risks, and next decision. |
| `/pr-merge` | Done | Added `engineering/commands/pr-merge.md`; enforces local landing gates and does not push by default. |
| `/retro` | Done | Added `engineering/commands/retro.md`; analyzes recent work, PRs, quality signals, lessons, and follow-up actions. |
| `/deslop` | Done | Added `engineering/commands/deslop.md`; routes to `quality-assurance`, `prs`, and external `deslop`. |
| `/review-architecture` | Done | Added `engineering/commands/review-architecture.md`; routes to `architecture` and external architecture review chains. |
| `/product-review` | Done | Added `product/commands/product-review.md` with `--lens=engineering\|design\|both`. |

## Command Backlog

Implemented in this order:

1. Fix `/grill-me` contract because it already exists and is likely to trigger
   incorrectly.
2. Add `/grill-with-docs`, `/review-architecture`, and `/deslop` because they
   are already represented in external chains and fill current command gaps.
3. Add `/update-memories` as a high-level convenience wrapper over the existing
   memory command family.
4. Add `/pr-merge` only after deciding whether local-main merge should stage,
   commit, or only merge and stop for inspection.
5. Add `/retro` and `/office-hours` as higher-level operating workflows.
6. Add `/meet-with-clients` and `/product-review` after confirming expected
   artifact formats for sales notes and product review findings.

Avoid adding duplicate aliases for `financial-model`,
`accounting-reconciliation`, or wildcard `fundraising-*` unless the repo is
doing a hard rename. The existing finance commands are clearer and narrower.

## Agent Recommendations

The repo already has useful orchestration agents:

| Existing agent | Keep as |
| --- | --- |
| `productivity/agents/executive.md` | cross-company synthesis |
| `productivity/agents/vp-of-operations.md` | operating cadence and follow-through |
| `engineering/agents/principal-engineer.md` | senior technical orchestration |
| `engineering/agents/pr-reviewer.md` | pre-merge review |
| `engineering/agents/pr-triage.md` | PR queue triage |
| `marketing/agents/growth-lead.md` | growth and channel orchestration |
| `sales/agents/sales-prospecting.md` | prospecting and outbound |
| `finances/agents/financial-analyst.md` | finance analysis |
| `productivity/agents/deep-research.md` | deeper research synthesis |
| `system/agents/memory-analyst.md` | memory review |
| `system/agents/skill-extractor.md` | skill extraction |
| `system/agents/experiment-runner.md` | autoresearch experiments |

Role agents for missing roles are now added, without duplicating files for headcount.
Use one reusable agent plus spawn-count instructions where needed.

| Proposed role | Status | Recommendation |
| --- | --- | --- |
| CEO | Done | `productivity/agents/ceo.md`; decision framing, operating priorities, fundraising narrative, company tradeoffs. |
| Executive Assistant | Done | `productivity/agents/executive-assistant.md`; inbox, scheduling prep, meeting notes, follow-through, memory hygiene. |
| CTO | Done | `engineering/agents/cto.md`; architecture, technical strategy, staffing shape, delivery risk. |
| Cloud Architect | Done | `engineering/agents/cloud-architect.md`; cloud architecture, deployment, cost, security, reliability. |
| Software Engineer x3 | Done | `engineering/agents/software-engineer.md`; use orchestrator spawn count `x3` instead of three files. |
| Product Manager | Done | `product/agents/product-manager.md`; product contracts, discovery, PRDs, prioritization, user stories. |
| Designer | Done | `product/agents/designer.md`; design critique, direction, systems, polish, UX risk. |
| AI Engineer | Done | `engineering/agents/ai-engineer.md`; AI systems, evals, prompt/tool design, RAG/context. |
| CSO | Done | `sales/agents/cso.md`; GTM strategy, pipeline health, sales operating model. |
| GTM Engineer x2 | Done | `sales/agents/gtm-engineer.md`; use spawn count `x2` for campaign or automation work. |
| SDR x3 | Done | `sales/agents/sdr.md`; use spawn count `x3` for prospect/account queues. |
| Account Executive x2 | Done | `sales/agents/account-executive.md`; use spawn count `x2` for discovery, demos, objections, follow-up. |
| CFO | Done | `finances/agents/cfo.md`; finance strategy, fundraising readiness, planning, controls, close quality. |
| Financial Analyst | Exists | Keep `finances/agents/financial-analyst.md`. |
| Accountant | Done | `finances/agents/accountant.md`; reconciliation, close, evidence, journal-entry queue, controls. |

## Agent Backlog

Implemented role agents in department order:

1. `productivity`: CEO and Executive Assistant.
2. `engineering`: CTO, Cloud Architect, Software Engineer, AI Engineer.
3. `product`: Product Manager and Designer.
4. `sales`: CSO, GTM Engineer, SDR, Account Executive.
5. `finances`: CFO and Accountant.

Each agent file should stay small:

- frontmatter `name` and `description`
- scope
- primary skills
- relevant commands
- workflow
- output contract

Do not put full methodology into agents. Agents should point at skills and
commands.

## Implementation Rules For Follow-Up

- Do not restore deleted legacy paths such as the old monolithic `business-ops`
  plugin.
- Do not add compatibility aliases unless the user explicitly asks for a hard
  rename or migration path.
- Keep command files thin and action-oriented.
- Keep agent files as orchestrators, not skill replacements.
- External skill guidance should remain referenced through
  `references/external-skills.yaml` and `skills-chaining-map.md`.
- Before using external skills, install or refresh them explicitly; current
  offline check shows they are registered but not installed for Codex.

## Validation For Follow-Up

After report-only work:

```bash
git diff --check
```

After adding commands or agents:

```bash
python3 scripts/validate_skills.py
python3 scripts/skillctl.py conflicts check --root .
python3 -m unittest scripts.tests.test_skillctl
python3 scripts/check-external-skills.py --offline --all --agent codex
rg --files -g '*/commands/*.md' -g '!references/legacy/**'
rg --files -g '*/agents/*.md' -g '!references/legacy/**'
git diff --check
```

If external skills are required for live command execution, install only the
specific needed skills, for example:

```bash
python3 scripts/install-external-skills.py --skill grill-with-docs --agent codex
python3 scripts/install-external-skills.py --skill deslop --agent codex
python3 scripts/install-external-skills.py --skill codebase-design --agent codex
```
