---
name: agent-harness-improvement
description: >-
  Use for repo agent-readiness, harness loops, instruction files, hooks,
  scratch space, CI feedback loops, and execution reliability. Child skill
  of `agentic-development`; route here from the parent router when this lane
  is the narrowest owner.
---

# Agent Harness Improvement

This child skill owns repo agent-readiness, harness loops, instruction files, hooks, scratch space, CI feedback loops, and execution reliability. It carries the detailed assets for this lane after the corrected fragmentation split.

The skill instructions and scripts are portable across harnesses. Hook activation is runtime-specific and explicit:

- Claude: `hooks/runtimes/claude-stop.sh`
- Cursor: `hooks/runtimes/cursor-stop.sh`
- Codex: `hooks/runtimes/codex-stop.sh`, only if the local Codex runtime supports stop hooks

The shared stop hook defaults to one completion gate. Multi-iteration behavior is active only when `/dev-loop` or `/harness-loop` creates loop state.

## Use When

- The request is primarily about repo agent-readiness, harness loops, instruction files, hooks, scratch space, CI feedback loops, and execution reliability.
- The parent router [`../agentic-development/SKILL.md`](../agentic-development/SKILL.md) selects this child.
- The work needs this lane's references, scripts, examples, hooks, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `scripts/` contains executable helpers owned by this lane.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.
- `hooks/` contains the shared hook implementation and runtime wrappers.

## Chain Rules

- Chain to `frontend`, `backend`, `quality-assurance`, `code-documentation`, `cloud-management`, `pr-management`, `auto-improve` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `codex-loop`: Run Codex PRD/story loops with one fresh subagent per story. Install: `python scripts/install-external-skills.py --skill codex-loop --agent codex`.
- `claude-loop`: Run Claude PRD/story loops with one fresh subagent per story. Install: `python scripts/install-external-skills.py --skill claude-loop --agent codex`.
- `no-mistakes`: Gate explicit ship, push, PR, or validate flows through the no-mistakes pipeline. Install: `python scripts/install-external-skills.py --skill no-mistakes --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
