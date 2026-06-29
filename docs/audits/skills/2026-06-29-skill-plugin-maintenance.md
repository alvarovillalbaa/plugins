# Skill & Plugin Maintenance Audit - 2026-06-29

## Summary

- Target repos checked: `/Users/alvipe/Desktop/plugins`, `/Users/alvipe/Desktop/SOFTWARE/CLOUS/plugins`
- Source directories checked: `/Users/alvipe/Desktop/agents-fs`, `/Users/alvipe/Desktop/SOFTWARE/CLOUS/agents-fs`
- Codex session sources found: `/Users/alvipe/.codex/session_index.jsonl`, `/Users/alvipe/.codex/history.jsonl`, `/Users/alvipe/.codex/sqlite/logs_2.sqlite`, `/Users/alvipe/.codex/sqlite/codex-dev.db`, `/Users/alvipe/.codex/archived_sessions/`
- Skills inspected: 6 source skills in each `agents-fs`; 143 personal target skills; 28 Clous target skills
- Skills updated: `clous-use/skills/agent-runs` in the Clous fallback repo
- Skills unchanged: personal target skills; Clous skills without new source drift
- Skills proposed: none
- Subagents proposed: none
- Elevations: stale configured target paths; personal plugin repo dirty-tree rewrite

## Repo Status

| Repo | Branch | Dirty Before | Dirty After | Notes |
|---|---:|---:|---:|---|
| `/Users/alvipe/Desktop/plugins` | `main` | yes | yes | Fallback personal target; heavily dirty router/plugin rewrite. No skill files changed; this run added reports and a narrow `.gitignore` exception for those reports. |
| `/Users/alvipe/Desktop/SOFTWARE/CLOUS/plugins` | `main` | yes | yes | Fallback Clous target; existing 2026-06-22 skill/doc changes plus this run's `agent-runs` update and reports. |
| `/Users/alvipe/Desktop/agents-fs` | `codex/research-maintenance-2026-06-17` | yes | yes | Source tree dirty outside `.agents/skills`; no `.agents/skills` commits or status changes since last run. |
| `/Users/alvipe/Desktop/SOFTWARE/CLOUS/agents-fs` | `main` | yes | yes | Source tree dirty in knowledge/research areas; no `.agents/skills` commits or status changes since last run. |

## Source Mapping

| Source | Target | Status | Notes |
|---|---|---|---|
| `/Users/alvipe/Desktop/agents-fs` | `/Users/alvipe/Desktop/alvarovillalbaa/plugins` | configured target missing | Used fallback `/Users/alvipe/Desktop/plugins` based on prior automation memory and filesystem evidence. |
| `/Users/alvipe/Desktop/SOFTWARE/CLOUS/agents-fs` | `/Users/alvipe/Desktop/clous-ai/plugins` | configured target missing | Used fallback `/Users/alvipe/Desktop/SOFTWARE/CLOUS/plugins`, the current workspace. |
| `/Users/alvipe/Desktop/agents-fs/.agents/skills` | `/Users/alvipe/Desktop/SOFTWARE/CLOUS/agents-fs/.agents/skills` | aligned | `diff -qr` found no differences between the two source skill trees. |

## Skills Inventory

| Skill | Repo | Status | Action | Reason |
|---|---|---|---|---|
| `auto-improve` | source trees | aligned | no target overwrite | Source unchanged since 2026-06-22. |
| `content-writing` | source trees | aligned | no target overwrite | Source unchanged since 2026-06-22. |
| `memory-management` | source trees | aligned | no target overwrite | Source unchanged since 2026-06-22. |
| `research` | source trees | aligned | no target overwrite | Source unchanged since 2026-06-22. |
| `review` | source trees | aligned | no target overwrite | Source unchanged since 2026-06-22. |
| `second-brain` | source trees | aligned | no target overwrite | Source unchanged since 2026-06-22. |
| Personal target skill set | `/Users/alvipe/Desktop/plugins` | target-only / dirty | intentionally unchanged | The target repo is in a broad router-fragmentation rewrite; overwriting would risk user work. |
| Clous target skill set | `/Users/alvipe/Desktop/SOFTWARE/CLOUS/plugins` | target-only | inspected | The Clous repo has product-specific skills rather than exact matches for the six source `.agents/skills`. |
| `agent-runs` | Clous target | under-specified | updated | Recent sessions repeatedly inspect agent runs, test failures, pending approvals, and evidence chains. |
| `remote-mcp-integration` | Clous target | already changed | left unchanged | 2026-06-22 hardening still matches current source/session evidence. |
| `knowledge-retrieval` | Clous target | already changed | left unchanged | 2026-06-22 retrieval contract still covers current knowledge/session evidence. |
| `people-reporting` | Clous target | already changed | left unchanged | 2026-06-22 AI/automation reporting rule still applies. |
| `capability-planning` | Clous target | already changed | left unchanged | 2026-06-22 skills-intelligence rule still applies. |
| `mcp-use` | Clous target | local change observed | preserved | A local MCP safety addition appeared during the run; it was not overwritten. |

## Codex Session Patterns

| Pattern | Frequency | Existing Coverage | Action |
|---|---:|---|---|
| Test gaps / test quality | 12 automation runs; 4 thread catalog entries | personal `quality-assurance`, `test-strategy-coverage`; Clous agent-run summaries | no new skill; record pattern |
| Docs lessons/fixes and documentation updates | 6 automation runs after last plugin run | personal `code-documentation`; source `auto-improve` | no new skill; report only |
| Agents-FS to plugins/docs maintenance | 6 automation runs after last plugin run | personal `skills-management`; automation memory | no new skill; report only |
| Raw-to-knowledge processing | 2 automation runs | source `second-brain`; personal `brain` / `ingestion`; Clous `knowledge-retrieval` | no Clous source overwrite |
| Bug finder / bug fixer | 4 automation runs | personal QA/debt skills | no new skill; report only |
| UI reuse, wrong abstractions, dead-code/orphaned | 6 automation runs | personal `tech-debt`, frontend/QA skills | no new skill; report only |
| Backward compatibility / decentralized logic / frontend-backend integration | 5 automation runs | personal engineering skills | no Clous skill update |
| Agent run inspection and evidence summaries | recurring across test/bug/docs automations | Clous `agent-runs` was too terse | update existing skill |

## Updates Made

### Skill: `agent-runs`

- Repo: `/Users/alvipe/Desktop/SOFTWARE/CLOUS/plugins`
- Files changed: `clous-use/skills/agent-runs/SKILL.md`
- Problem: The skill named run creation and polling but did not spell out how to inspect existing runs without losing identifiers, artifacts, approvals, raw errors, or verification gaps.
- Change: Added a compact run inspection contract and guardrails.
- Why: Recent Codex history repeatedly requires evidence-preserving run/test/failure inspection.
- Validation: Static diff review and `git diff --check`.

### Repo docs visibility

- Repo: `/Users/alvipe/Desktop/plugins`
- Files changed: `.gitignore`
- Problem: The personal repo's current dirty rewrite ignored all of `docs/`, hiding the required audit/changelog outputs from git status.
- Change: Replaced the blanket `docs/` ignore with narrow exceptions for `docs/audits/skills/*.md` and `docs/changelog/skills/*.md`.
- Why: Keep required maintenance artifacts visible without unignoring unrelated docs output.
- Validation: `git diff --check`.

## New Skill Candidates

| Candidate | Reason | Evidence | Recommendation |
|---|---|---|---|
| none | Existing skills cover current repeated workflows. | Source skills unchanged; recent sessions map to current QA/docs/brain/agent-run lanes. | Do not create new skills this run. |

## New Subagent Candidates

| Candidate | Reason | Evidence | Recommendation |
|---|---|---|---|
| none | No new bounded role had stronger evidence than updating existing skill contracts. | Repeated workflows are already routed through automation threads and existing skills. | Do not create subagents this run. |

## Docs Updated

| File | Reason |
|---|---|
| `docs/audits/skills/2026-06-29-skill-plugin-maintenance.md` | Required audit artifact for this maintenance run. |
| `docs/changelog/skills/2026-06-29-skill-plugin-maintenance.md` | Required changelog artifact for this maintenance run. |
| `/Users/alvipe/Desktop/plugins/.gitignore` | Makes the required personal audit/changelog artifacts visible while keeping other docs ignored. |

## Validation Results

| Check | Result | Notes |
|---|---|---|
| Core path preflight | partial | Prompt target repos are missing; fallback repos exist. |
| Source skill status | pass | No `.agents/skills` changes in either source tree since the last run. |
| Source skill diff | pass | Personal and Clous source `.agents/skills` trees are identical. |
| Codex session discovery | pass | Found local `.codex` JSONL, SQLite, and archived session sources. |
| Personal `git diff --check` | pass | Whitespace check passed; broader validation skipped because repo is heavily dirty and no personal skill files were changed. |
| Clous static diff review | pass | Changed Clous skill text is narrow and contract-only. |
| Clous `git diff --check` | pass | Whitespace check passed after edits. |
| Clous marketplace/root validator | pass | `python3 scripts/validate_plugins.py`; `tsc` was unavailable, so TypeScript typecheck was skipped by the validator. |
| Clous plugin validators | pass | `check-development-plugin.py`, `check-use-plugin.py`, and `check-hr-plugin.py` passed. |

## Elevations

### 1. Configured target plugin paths are stale

- Context: The prompt targets `/Users/alvipe/Desktop/alvarovillalbaa/plugins` and `/Users/alvipe/Desktop/clous-ai/plugins`, but both are missing locally.
- Why I am not deciding automatically: The fallback paths are inferred from prior automation memory and filesystem evidence, but the automation definition still points elsewhere.
- Options:
  1. Update the automation prompt to the fallback paths.
  2. Recreate the configured paths as canonical repos.
- Recommendation: Update the automation prompt to `/Users/alvipe/Desktop/plugins` and `/Users/alvipe/Desktop/SOFTWARE/CLOUS/plugins`.
- Cost of not deciding: Every run starts with path drift and has to infer the real targets.

### 2. Personal plugin repo is still too dirty for source overwrites

- Context: `/Users/alvipe/Desktop/plugins` has a broad router-fragmentation rewrite, deleted legacy plugin areas, new skills, manifests, and docs.
- Why I am not deciding automatically: Source-to-target sync could overwrite or duplicate user-owned restructuring.
- Options:
  1. Finish and commit the rewrite, then rerun source sync.
  2. Provide a narrower list of personal skills to update while dirty.
- Recommendation: Finish the rewrite first; then run a focused source-mapping pass for the six source `.agents/skills`.
- Cost of not deciding: The personal target remains intentionally not overwritten by this automation.

## Final Recommendation

Keep the Clous `agent-runs` update, review the unrelated local `mcp-use` change before commit, and fix the automation's stale target paths before the next scheduled run.
