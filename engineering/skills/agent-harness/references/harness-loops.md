# Harness Loops

External owner boundary:

- Use `codex-loop` for Codex PRD/story loops.
- Use `claude-loop` for Claude PRD/story loops.
- Do not duplicate their `prd.json`, fresh-subagent, wave, worktree, progress, archive, or `<promise>COMPLETE</promise>` protocols here.

This local reference only covers this plugin's stop-hook based in-session loops.

## Local loop tooling

This skill ships two commands built on `hooks/check-completion.sh`.

### `/dev-loop`

```text
/dev-loop TASK [--max-iterations N] [--completion-promise TEXT] [--verify-cmd CMD] [--spec-file PATH]
```

Use it for one supervised task that benefits from repeated attempts in the same checkout. The command writes `.agentic/agentic-dev-loop.local.md`; the stop hook reinjects the task until the final assistant message contains the configured promise.

### `/harness-loop`

```text
/harness-loop [repo-root] [--max-iterations N]
```

Use it for harness-readiness work. It runs `harness_audit.py`, fixes the highest-priority P0/P1 harness finding per iteration, and stops when no P0/P1 item remains.

## When local loops are appropriate

- one independently provable task can be completed per iteration
- a spec, checklist, or prioritized state file already exists on disk
- `--max-iterations` and a binary verification command are available
- a human can inspect, stop, or rescope the run
- the loop is not a PRD/story backlog for Codex or Claude workers

## When to chain externally instead

Use `codex-loop` or `claude-loop` when the user asks to:

- run a PRD/story loop
- process `prd.json`
- implement all stories
- fan out story work in waves
- use one fresh agent per story
- archive a completed loop run

## Local safety rules

- Always set `--max-iterations`.
- Keep the state file small and disk-backed.
- Use `--verify-cmd` when a reliable gate exists.
- Use `--spec-file` when compaction or drift is likely.
- Stop if the loop repeats the same failing fix without new evidence.
- Do not push, deploy, run destructive migrations, or modify secrets from a loop without explicit approval.

## Completion promise

The local stop hook exits only when the assistant emits the exact configured promise in a `<promise>` tag, for example:

```text
<promise>DONE</promise>
```

This is separate from the external loop skills' completion contract.
