---
name: review-pr
description: "Run a comprehensive multi-lens PR review. Covers code quality, silent failures, test coverage, and comment accuracy. Defaults to the current git diff; accepts a branch, PR number, or file list."
argument-hint: "[branch | PR# | file-list] [--lens code|errors|tests|comments|types]"
allowed-tools: ["Bash", "Read", "Glob", "Grep", "Agent"]
---

# PR Review

Use agent: **pr-reviewer** — `agents/pr-reviewer.md`

Use skill: **prs** — `skills/prs/SKILL.md`

## Scope resolution

1. Parse `$ARGUMENTS` for a branch name, PR number, or explicit file paths.
2. If a PR number is given: `gh pr diff <number>` to get the diff; `gh pr view <number>` for description and context.
3. If a branch is given: `git diff origin/<base>...<branch>` to get the diff.
4. If none given: `git diff` for unstaged changes, or `git diff HEAD` for committed-but-unpushed changes.
5. If `--lens` is specified, run only the named lens(es). Otherwise run all applicable lenses.

## Review workflow

1. **Determine which lenses apply** based on diff content:
   - `code` — always
   - `errors` — if error handling, try/catch, fallback, or optional chaining in diff
   - `tests` — if new or modified functionality in diff
   - `comments` — if new or modified comments or docs in diff
   - `types` — if new types or data models in diff (typed languages only)

2. **Run each lens** per `skills/prs/references/review-specializations.md`.

3. **For diffs ≥ 200 lines changed:** run the adversarial pass per `skills/architecture/references/reviews-and-comments.md`.

4. **Synthesize** into a single report:

   ```
   # PR Review — [scope]

   ## Critical Blockers
   <lens>/<severity> <path>:<line> -- <risk> -> <fix>

   ## Important Issues
   <lens>/<severity> <path>:<line> -- <risk> -> <fix>

   ## Suggestions
   ...

   ## Strengths
   ...

   ## Recommended action
   1. Fix critical blockers
   2. Address important issues
   3. Consider suggestions
   ```

5. If no high-confidence issues: confirm explicitly with a one-line summary.

## Usage examples

```
/review-pr
# Reviews current unstaged diff

/review-pr main
# Reviews current branch against main

/review-pr 142
# Reviews PR #142

/review-pr --lens errors tests
# Runs only silent-failure and test-coverage lenses
```
