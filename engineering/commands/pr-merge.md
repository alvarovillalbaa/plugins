---
name: pr-merge
description: Prepare and perform a local PR landing merge with explicit gates. Does not push by default.
argument-hint: "[PR number, branch, or local branch] [--base main]"
allowed-tools: [Read, Grep, Glob, Bash, AskUserQuestion, Skill]
---

Use skills: **prs**, **quality-assurance**, and **code-documentation**.

1. **Resolve target** - Determine the PR number or branch and the base branch. Default base is `main`.
2. **Check landing gates** - Inspect PR status, review state, diff risk, tests, docs, and local dirty state.
3. **Fetch and merge locally** - Merge into the local base branch only after gates are satisfied or the user accepts listed risks.
4. **Do not push** - Stop after the local merge unless the user explicitly asks to push.
5. **Return landing state** - Report merged commit, checks run, unresolved risks, and any follow-up commands.
