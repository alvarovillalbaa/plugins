---
name: dev-loop
description: "Start an agentic development loop in the current session — re-injects your task prompt each iteration until the completion promise is output or max iterations is reached."
argument-hint: "TASK [--max-iterations N] [--completion-promise TEXT] [--verify-cmd CMD] [--spec-file PATH]"
allowed-tools: ["Bash(${CLAUDE_PLUGIN_ROOT}/skills/agent-harness/scripts/setup-dev-loop.sh:*)", "Skill"]
hide-from-slash-command-tool: "true"
---

# Dev Loop

Use skill: **agent-harness** — `skills/agent-harness/SKILL.md`.

Execute the setup script to initialize the agentic dev loop:

```!
"${CLAUDE_PLUGIN_ROOT}/skills/agent-harness/scripts/setup-dev-loop.sh" $ARGUMENTS
```

Then begin working on the task. Each time you try to exit, the stop hook re-injects your original task prompt. File changes and git history persist across iterations, letting you converge on a correct, verified solution.

## Loop discipline per iteration

1. **Orient** — check `git status`, re-read the spec file if one was provided, and understand where the last iteration left off.
2. **Pick one action** — the single highest-priority item that can be implemented and proven in this iteration. Do not try to do everything at once.
3. **Implement narrowly** — change only the files required for that action.
4. **Verify** — run the verification command. Do not claim success without fresh evidence.
5. **Commit if clean** — if all gates pass, commit with a conventional commit message. Do not batch multiple unrelated changes into one commit.
6. **Output the promise** — only output `<promise>COMPLETION_PROMISE</promise>` when the task is genuinely complete, all gates pass, and the git state is clean.

## Critical rule

Only output the completion promise when the statement is completely and unequivocally TRUE. Do not lie to exit the loop, even if you think you are stuck. If genuinely blocked, document the blocker clearly and let the loop continue so the context is preserved for the next iteration.

This loop converges on one user task. Use `harness-loop` only for repeated repository-harness hardening and `ar:loop` only for measured experiments with keep/discard evaluation.
