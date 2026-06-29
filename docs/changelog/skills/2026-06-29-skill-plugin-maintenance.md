# Skill & Plugin Maintenance Changelog - 2026-06-29

## Changed

- Added a run-inspection contract to `clous-use/skills/agent-runs/SKILL.md` in the Clous fallback repo so run summaries preserve endpoint family, ids, status, artifacts, approvals, errors, retries, and verification gaps.
- Updated the personal plugin repo `.gitignore` with narrow exceptions for skill maintenance audits and changelogs.

## Added

- Added the 2026-06-29 skill/plugin maintenance audit report.
- Added this dated changelog.

## Deprecated

- Nothing deprecated or deleted.

## Docs

- Recorded that configured target paths are stale and fallback targets were used.
- Recorded that the personal plugin repo remains too dirty for safe source overwrites.
- Recorded recent Codex workflow patterns from local session and automation metadata.
- Recorded why the personal `.gitignore` needed report-specific exceptions.

## Validation

- Confirmed both source `.agents/skills` trees have no status/log changes since the prior run.
- Confirmed personal and Clous source `.agents/skills` directories are identical.
- Ran `git diff --check` in both fallback plugin repos.
- Ran Clous marketplace/root validation and the three Clous plugin validators; all passed, with `tsc` unavailable and skipped by the root validator.

## Follow-ups

- Update the automation prompt to the actual fallback target paths or recreate the configured target repos.
- Re-run personal source sync only after the personal plugin rewrite is settled.
- Review the unrelated local `clous-use/skills/mcp-use/SKILL.md` change before committing.
