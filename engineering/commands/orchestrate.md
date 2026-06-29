---
name: orchestrate
description: "Decompose a large goal into parallel cloud-agent tasks using the planner/worker/verifier model. Use when the task is too large for a single /dev-loop or benefits from parallel sub-scope execution."
argument-hint: "<goal> [--slack-token TOKEN]"
allowed-tools: [Agent, Read, Bash, AskUserQuestion]
hide-from-slash-command-tool: "true"
---

# Orchestrate

Distribute large-scope work across parallel cloud agents. This command acts as the **Dispatcher** — you remain in local IDE mode while Planner and Worker agents run in the cloud.

## Pre-flight

Before running, confirm:
- `CURSOR_API_KEY` is set (Cursor Dashboard → Integrations)
- The goal is concrete enough for a Planner to decompose without mid-flight clarifications
- The repo has a reliable local verify command workers can use to validate their handoffs

If any condition is unmet, stop and resolve it before spawning.

## Usage

```
/orchestrate "Migrate the legacy auth module to the new SDK, add test coverage, and update AGENTS.md"
```

## What happens

1. A Planner cloud agent receives your goal, writes `plan.json`, and decomposes it into parallel Worker tasks.
2. Workers execute in isolated repo clones and return structured handoffs.
3. Optional Verifiers validate acceptance criteria before the Planner marks tasks done.
4. If a Worker or Verifier triggers an Andon, the Planner pauses and surfaces the escalation to you.
5. When all tasks complete, a final compatibility audit runs and results are reported.

## Monitoring

Use the current orchestration reference in `skills/multi-agent/references/orchestrate-roles.md` to decide what state, handoff, and escalation artifacts to inspect. If a project provides its own cloud-agent CLI, use that project-local CLI; this plugin does not ship a standalone orchestration CLI.

## Discipline

- Planners own scope — they do not write code directly
- Workers operate in isolation — no cross-talk between siblings
- `plan.json` is the authoritative state — restartable from any point
- Every Andon escalation must be surfaced to you, never silently suppressed

## Reference

Read `skills/multi-agent/references/orchestrate-roles.md` for the full role model, Andon protocol, plan.json schema, and when-to-use guidance.
