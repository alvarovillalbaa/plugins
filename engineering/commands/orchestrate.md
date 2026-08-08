---
name: orchestrate
description: Decompose a large goal into bounded agent workstreams, coordinate dependencies, and verify the integrated result with one controller.
argument-hint: "<goal> [--max-workers N] [--verify CMD]"
allowed-tools: [Agent, Read, Bash, AskUserQuestion, Skill]
hide-from-slash-command-tool: "true"
---

Use skill: **multi-agent** — `skills/multi-agent/SKILL.md`.
Read `skills/multi-agent/references/orchestrate-roles.md` for role, handoff, and escalation contracts.

1. **Pre-flight** — Require a concrete goal, acceptance checks, explicit authority boundary, reliable verification command, and non-overlapping write scopes.
2. **Select the runtime adapter** — Use the current runtime's agent/delegation mechanism or a project-local orchestration CLI. Do not require a particular vendor, API key, messaging service, or cloud-agent product.
3. **Plan dependencies** — Route simple independent work to bounded delegation and dependency-shaped work to `agentic-graphs`. Keep one controller responsible for integration.
4. **Dispatch safely** — Give each worker a disjoint scope, minimum context, deliverable, allowed actions, and verification requirement. Bound concurrency, cost, time, and retries.
5. **Collect handoffs** — Require artifact paths, evidence, checks run, assumptions, and residual risks. Pause on overlapping writes, scope expansion, or approval-gated actions.
6. **Integrate and verify** — The controller reconciles conflicts, assembles the result, and reruns the original acceptance checks. Workers do not declare the whole goal complete.
7. **Report** — Return the workstream state, integrated changes, verification evidence, unresolved risks, and any unavailable runtime capability.

## Boundary

Use this command for multi-workstream orchestration. Use `dev-loop` for one bounded task and `harness-loop` for repository harness improvement.
