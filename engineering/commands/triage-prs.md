---
name: triage-prs
description: "Intent-first PR triage. Processes a list of PRs, issues, or a whole queue. Recovers plain-language intent, judges whether the implementation solves the real problem, and routes each item to close, escalate, or continue. Follows the triage protocol from prs."
argument-hint: "[PR# | branch | --queue] [--repo owner/repo]"
allowed-tools: ["Bash", "Read", "Grep", "Agent", "Skill"]
---

# PR Triage

Use agent: **pr-triage** — `agents/pr-triage.md`

Use skill: **prs** — `skills/prs/SKILL.md` and `skills/prs/references/triage-protocol.md`

## Input resolution

1. If `$ARGUMENTS` contains PR numbers or branch names, triage those items.
2. If `--queue` is given (or no argument), fetch the open PR list: `gh pr list --limit 50 --json number,title,headRefName,updatedAt`.
3. If `--repo` is given, pass `--repo owner/repo` to all `gh` calls.

## Processing order

For queue mode, process in this priority:
1. PRs with P0/P1 CI failures on the main branch
2. PRs blocked on conflicts for > 2 days
3. PRs aging > 3 business days without activity
4. Remaining open PRs by `updatedAt` descending

## Triage workflow

Follow `triage-protocol.md` exactly for each item.

Do not start review and CI work on items that will be closed or escalated — stop at Step 3 for those.

## Output

For each item, produce the standard decision record and draft the comment template from `triage-protocol.md`. Post, close, label, assign, or otherwise mutate the remote item only when the request explicitly authorizes that exact external action.

Queue summary at the end:

```
## Triage Summary

- ✅ Ready for landing: <count> PRs — [list]
- ⚠️  Needs judgment: <count> PRs — [list with what decision is needed]
- ❌ Closed: <count> PRs — [list with close reason]
- 🔄 Continuing: <count> PRs — [list]
- 📊 Queue health: avg age <N> days, <N> PRs blocked on conflicts, <N> PRs with CI failures
```

## Usage examples

```
/triage-prs 142 155 160
# Triage specific PRs

/triage-prs --queue
# Triage the full open PR queue

/triage-prs --repo <owner>/<repository> --queue
# Triage queue for a specific repo
```
