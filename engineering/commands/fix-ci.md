---
name: fix-ci
description: "Identify failing CI checks for the current branch, diagnose each failure, and apply targeted fixes — then re-watch CI to confirm resolution."
argument-hint: "[--max-iterations N] [--check <check-name>]"
allowed-tools: [Agent, Bash, Read, Grep]
hide-from-slash-command-tool: "true"
---

# Fix CI

Diagnose and fix failing CI checks for the current branch. Operates in a watch → identify → fix → re-watch loop.

## Step 1: Watch and classify

Invoke the ci-watcher agent to get the current CI status:
- Run `gh pr checks` for a snapshot; use `gh run view --log-failed` for failure logs.
- Classify each failure as FLAKY, REAL, or INFRA.
- Re-trigger FLAKY checks first (`gh run rerun <id> --failed`); wait for result before touching code.

## Step 2: Identify root cause

For each REAL failure:
1. Read the full failure log — do not guess from the check name alone.
2. Map the failure to a file, line, and rule.
3. Check if the failure exists locally: run the same check command that CI uses.
4. If the failure does not reproduce locally, it is likely an env/infra issue — surface to human.

## Step 3: Apply targeted fix

Fix only what the log points to. Do not refactor surrounding code. Do not fix more than one check failure in a single commit.

After each fix:
- Run the failing check locally to confirm it passes.
- Run a broader gate (full test suite or typecheck) if the touched surface is high-fanout.
- Commit with a conventional message referencing the check name.

## Step 4: Re-watch

After pushing the fix, run ci-watcher again to confirm the targeted check passes and no new failures were introduced.

## Completion criterion

All checks are PASS or INFRA (where INFRA items have been surfaced to the human). No regressions in checks that were passing before.

## Reference

- CI feedback loop patterns: `skills/agent-harness/references/harness-engineering.md` § 5
- ci-watcher agent: `skills/agent-harness/references/agents/ci-watcher.yaml`
