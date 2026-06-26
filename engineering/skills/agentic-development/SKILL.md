---
name: agentic-development
description: >-
  Router for engineering execution, architecture/system design, multi-agent
  execution, release landing, agent harness improvement, and tech debt
  management.
---

# Agentic Development Router

This parent is a router. Select the narrowest child and load that child before using lane-specific assets.

This skill is portable across harnesses because it is instruction-first. Runtime hooks are explicit adapters owned by [`agent-harness-improvement`](../agent-harness-improvement/SKILL.md); do not assume a Claude, Cursor, or Codex install activates hooks automatically.

## Children

- [`architecture-system-design`](../architecture-system-design/SKILL.md) - system architecture, technical design, interface decisions, planning, and architecture tradeoff work
- [`multi-agent-execution`](../multi-agent-execution/SKILL.md) - parallel agent execution, subagent coordination, orchestration roles, and multi-agent workflow handoffs
- [`release-landing`](../release-landing/SKILL.md) - engineering release landing, merge hygiene, deployment gates, hotfixes, tags, and rollback posture
- [`agent-harness-improvement`](../agent-harness-improvement/SKILL.md) - repo agent-readiness, harness loops, instruction files, hooks, scratch space, CI feedback loops, and execution reliability
- [`tech-debt-management`](../tech-debt-management/SKILL.md) - technical-debt elimination, refactor plans, dependency cleanup, anti-pattern removal, and schedulable debt cadences

## Route

| User asks for | Use |
| --- | --- |
| system architecture, technical design, interface decisions, planning, and architecture tradeoff work | [`architecture-system-design`](../architecture-system-design/SKILL.md) |
| parallel agent execution, subagent coordination, orchestration roles, and multi-agent workflow handoffs | [`multi-agent-execution`](../multi-agent-execution/SKILL.md) |
| engineering release landing, merge hygiene, deployment gates, hotfixes, tags, and rollback posture | [`release-landing`](../release-landing/SKILL.md) |
| repo agent-readiness, harness loops, instruction files, hooks, scratch space, CI feedback loops, and execution reliability | [`agent-harness-improvement`](../agent-harness-improvement/SKILL.md) |
| technical-debt elimination, refactor plans, dependency cleanup, anti-pattern removal, and schedulable debt cadences | [`tech-debt-management`](../tech-debt-management/SKILL.md) |

## Chain Rules

- `frontend`
- `backend`
- `quality-assurance`
- `code-documentation`
- `cloud-management`
- `pr-management`
- `auto-improve`

## Operating Rules

- Keep this `SKILL.md` small and routing-focused.
- Do not recreate the old broad parent behavior here; put execution depth in child assets.
- If no child matches, handle only shared methodology/default workflow or document the missing lane.
- Every child and parent skill must keep `examples/`, `hooks/`, `references/`, `scripts/`, and `templates/`.
- Completion hooks must be wired through runtime wrappers, not by calling shared hook scripts directly.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `codex-loop`: Run Codex PRD/story loops with one fresh subagent per story. Install: `python scripts/install-external-skills.py --skill codex-loop --agent codex`.
- `claude-loop`: Run Claude PRD/story loops with one fresh subagent per story. Install: `python scripts/install-external-skills.py --skill claude-loop --agent codex`.
- `no-mistakes`: Gate explicit ship, push, PR, or validate flows through the no-mistakes pipeline. Install: `python scripts/install-external-skills.py --skill no-mistakes --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
