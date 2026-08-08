---
name: agent-harness
description: Use for repo agent-readiness, harness loops, instruction files, hooks, scratch space, CI feedback loops, and execution reliability. Child of `agentic-development`.
hooks:
  Stop:
    - hooks:
        - type: command
          command: python3
          args:
            - "${CLAUDE_PLUGIN_ROOT}/skills/agent-harness/scripts/completion-gate.py"
          timeout: 10
---

# Agent Harness Improvement

This child skill owns repo agent-readiness, harness loops, instruction files, hooks, scratch space, CI feedback loops, and execution reliability. It carries the detailed assets for this lane after the corrected fragmentation split.

The instructions and completion gate are portable. Claude activates the gate
through the skill-scoped `Stop` registration above. Other runtimes can invoke
`scripts/completion-gate.py` only when their local hook system supplies the same
JSON event contract; this package does not claim automatic activation for them.

The shared stop hook defaults to one completion gate. Multi-iteration behavior is active only when `/dev-loop` or `/harness-loop` creates loop state.

## Use When

- The request is primarily about repo agent-readiness, harness loops, instruction files, hooks, scratch space, CI feedback loops, and execution reliability.
- The parent router [`../agentic-development/SKILL.md`](../agentic-development/SKILL.md) selects this child.
- The work needs this lane's references, scripts, examples, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `scripts/` contains executable helpers owned by this lane.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.
- `scripts/completion-gate.py` is the registered Claude hook handler and the
  optional manual integration point for compatible runtimes.

## Chain Rules

- Chain to `frontend`, `backend`, `quality-assurance`, `code-documentation`, `cloud`, `prs`, `plugins-management` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `codex-loop`: Run Codex PRD/story loops with one fresh subagent per story. Install: `python3 scripts/install-external-skills.py --skill codex-loop --agent codex`.
- `claude-loop`: Run Claude PRD/story loops with one fresh subagent per story. Install: `python3 scripts/install-external-skills.py --skill claude-loop --agent codex`.
- `ralph`: Use Ralph-style autonomous execution loops for scoped implementation plans. Install: `python3 scripts/install-external-skills.py --skill ralph --agent codex`.
- `no-mistakes`: Gate explicit ship, push, PR, or validate flows through the no-mistakes pipeline. Install: `python3 scripts/install-external-skills.py --skill no-mistakes --agent codex`.
- `use-afs`: Use the AFS filesystem layout and naming conventions instead of duplicating local filesystem guidance. Install: `python3 scripts/install-external-skills.py --skill use-afs --agent codex`.
- `clous-agent-runs`: Use Clous-owned agent run guidance for operating and inspecting agent executions. Install: `python3 scripts/install-external-skills.py --skill clous-agent-runs --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
