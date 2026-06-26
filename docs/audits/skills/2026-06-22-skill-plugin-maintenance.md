# Skill & Plugin Maintenance Audit - 2026-06-22

## Summary

- Target repos checked: `/Users/alvipe/Desktop/plugins` and `/Users/alvipe/Desktop/SOFTWARE/CLOUS/plugins`.
- Declared target paths missing: `/Users/alvipe/Desktop/alvarovillalbaa/plugins`, `/Users/alvipe/Desktop/clous-ai/plugins`.
- Source directories checked: `/Users/alvipe/Desktop/agents-fs`, `/Users/alvipe/Desktop/SOFTWARE/CLOUS/agents-fs`.
- Codex session sources found: `/Users/alvipe/.codex/sessions`, `/Users/alvipe/.codex/archived_sessions`, `/Users/alvipe/.codex/memories`, `/Users/alvipe/Library/Application Support/Codex`, `/Users/alvipe/Library/Application Support/OpenAI/Codex`.
- Skills inspected: 129 personal plugin skills, 28 Clous plugin skills, and 6 source `.agents/skills` in each agents-fs repo.
- Skills updated: 0 in this personal plugin repo; 4 in the Clous plugin repo.
- Skills unchanged: all personal plugin skills.
- Skills proposed: 1 future candidate.
- Subagents proposed: 1 future candidate.
- Elevations: 2.

## Repo Status

| Repo | Branch | Dirty Before | Dirty After | Notes |
|---|---:|---:|---:|---|
| `/Users/alvipe/Desktop/plugins` | `main` | yes | yes | Large pre-existing skill-fragmentation diff preserved; only audit/changelog docs were added. |
| `/Users/alvipe/Desktop/SOFTWARE/CLOUS/plugins` | `main` | no | yes | Four Clous skills updated plus audit/changelog docs added. |
| `/Users/alvipe/Desktop/agents-fs` | `codex/research-maintenance-2026-06-17` | yes | unchanged | Source `.agents/skills` inspected only. |
| `/Users/alvipe/Desktop/SOFTWARE/CLOUS/agents-fs` | `main` | yes | unchanged | Source brain docs inspected only. |

## Source Mapping

| Source | Target | Status | Notes |
|---|---|---|---|
| `/Users/alvipe/Desktop/agents-fs/.agents/skills` | `/Users/alvipe/Desktop/plugins` | conflict-preserved | Source files are older monolithic skills; target has newer router/child split. |
| `/Users/alvipe/Desktop/SOFTWARE/CLOUS/agents-fs` | `/Users/alvipe/Desktop/SOFTWARE/CLOUS/plugins` | source-informed | Source brain evidence was applied to existing Clous skills. |
| `/Users/alvipe/Desktop/alvarovillalbaa/plugins` | n/a | missing | Inferred current equivalent: `/Users/alvipe/Desktop/plugins`. |
| `/Users/alvipe/Desktop/clous-ai/plugins` | n/a | missing | Inferred current equivalent: `/Users/alvipe/Desktop/SOFTWARE/CLOUS/plugins`. |

## Skills Inventory

| Skill | Repo | Status | Action | Reason |
|---|---|---|---|---|
| `research` | personal | target-newer | unchanged | Target has router/specialized-child architecture and output-contract improvements absent from source. |
| `review` | personal | target-newer | unchanged | Target is the router split; source remains old monolith. |
| `second-brain` | personal | target-newer | unchanged | Target routes to `raw-ingestion`; source remains old broad skill. |
| `auto-improve` | personal | target-newer | unchanged | Target routes to eval, memory, knowledge, style, and doc-drift children. |
| `content-writing` | personal | target-newer | unchanged | Target routes to specialized content children; source remains old monolith. |
| `memory-management` | personal | target-improved | unchanged | Target has detailed memory-stack workflow; source is a minimal stub. |
| `remote-mcp-integration` | Clous | source-informed | updated | Added MCP schema/scope/resource traceability and least-privilege guidance. |
| `knowledge-retrieval` | Clous | source-informed | updated | Added retrieval contract for source ids, date gaps, interpretation boundaries, and sensitive HR escalation. |
| `people-reporting` | Clous | source-informed | updated | Added AI/automation ROI measurement guardrails. |
| `capability-planning` | Clous | source-informed | updated | Added skills-intelligence and validated-evidence rules. |

## Codex Session Patterns

| Pattern | Frequency | Existing Coverage | Action |
|---|---:|---|---|
| Test gap review | 60 June session hits | `quality-assurance`, `test-strategy-coverage` | no-action |
| Backward compatibility hard cuts | 58 June session hits | `agentic-development`, `tech-debt-management` | no-action |
| Decentralized logic/canonical owners | 55 June session hits | `tech-debt-management` | no-action |
| Dead-code/orphan cleanup | 54 June session hits | `tech-debt-management` | no-action |
| Bug audits/finding | 52 June session hits | `quality-assurance`, `code-diff-review` | no-action |
| Frontend/backend integration | 21 June session hits | repo-local automations | propose future contract checker only after owner confirmation |
| Documentation updates | 12 June session hits | `code-documentation` | no-action |
| Performance regressions | 11 June session hits | `performance-testing` | no-action |
| Release notes | 10 June session hits | `release-landing` | no-action |
| Research maintenance | 8 June session hits | `research`, `second-brain` | no-action |

## Updates Made

### Skill: none in personal plugin repo

- Repo: `/Users/alvipe/Desktop/plugins`
- Files changed: this audit and changelog only.
- Problem: The source `.agents` skills are older than the current target router split.
- Change: No active personal skill file was overwritten.
- Why: Replacing router parents with monolithic source files would undo the current plugin architecture.
- Validation: `git diff --check` passed; `python scripts/validate_skills.py` still fails on a pre-existing `html-visual` frontmatter/path mismatch.

## New Skill Candidates

| Candidate | Reason | Evidence | Recommendation |
|---|---|---|---|
| `frontend-backend-contract-checker` | Repeated cross-repo integration checks appear in June sessions. | 21 `frontend-backed-integration` session hits. | Proposal only; do not create until owner repo and output contract are confirmed. |

## New Subagent Candidates

| Candidate | Reason | Evidence | Recommendation |
|---|---|---|---|
| `contract-check-investigator` | Could independently inspect route and payload drift and return a bounded report. | Same integration pattern. | Proposal only; do not add during the current dirty fragmentation state. |

## Docs Updated

| File | Reason |
|---|---|
| `docs/audits/skills/2026-06-22-skill-plugin-maintenance.md` | Record inspection, source conflicts, session patterns, and elevations. |
| `docs/changelog/skills/2026-06-22-skill-plugin-maintenance.md` | Record personal repo no-overwrite decision and cross-repo Clous skill updates. |

## Validation Results

| Check | Result | Notes |
|---|---|---|
| Source `.agents/skills` discovery | pass | Six source skills found in both agents-fs repos. |
| Personal skill inventory | pass | 129 personal plugin skills found. |
| Personal `git diff --check` | pass | No whitespace errors in current diff. |
| Personal `python scripts/validate_skills.py` | fail | Pre-existing `marketing/skills/html-visual/SKILL.md` frontmatter name does not match folder. |
| Personal `bash scripts/validate-plugin.sh` | fail | Script expects a root `.claude-plugin/plugin.json`; this repo is department-plugin structured. |

## Elevations

### 1. Declared target paths are missing

- Context: The prompt names `/Users/alvipe/Desktop/alvarovillalbaa/plugins` and `/Users/alvipe/Desktop/clous-ai/plugins`.
- Why I am not deciding automatically: The local machine has `/Users/alvipe/Desktop/plugins` and `/Users/alvipe/Desktop/SOFTWARE/CLOUS/plugins`, which appear to be the current equivalents.
- Options:
  1. Update the automation prompt to the discovered paths.
  2. Recreate the declared paths as separate checkouts.
- Recommendation: Update the automation prompt to the discovered paths.
- Cost of not deciding: Future runs will repeatedly resolve the same path mismatch.

### 2. Source `.agents` skills are stale relative to the router split

- Context: Source `research`, `review`, `second-brain`, `auto-improve`, and `content-writing` are monolithic; target files are installable router parents with child skills.
- Why I am not deciding automatically: Reverting target files would undo the current plugin architecture.
- Options:
  1. Keep target as authoritative and backport router split into source `.agents`.
  2. Revert target to source monoliths.
- Recommendation: Keep target authoritative and schedule a source backport only if agents-fs should continue exporting skills.
- Cost of not deciding: `skills-lock.json` and source `.agents` will remain stale relative to the plugin repo.

## Final Recommendation

Keep the personal plugin router split intact. The next useful maintenance action is to decide whether agents-fs `.agents/skills` should be backported from the plugin repo or treated as old installed snapshots.
