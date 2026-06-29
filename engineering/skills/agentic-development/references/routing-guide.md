# Agentic Development — Routing Guide

This skill is the entry point for agentic development work. Use this guide to route requests to the correct child skill.

## Child Skills

| Child | Owns |
|-------|------|
| `agent-harness` | Harness design, dev-loop configuration, session management, CLAUDE.md setup |
| `agent-system-architecture` | Multi-agent topology, orchestrator patterns, A2A communication design |
| `architecture` | System architecture review, ADRs, tech decisions |
| `cicd` | CI/CD pipeline changes triggered by agentic dev |

## When to Use This Skill Directly

- Evaluating whether a task should be agentic at all.
- Choosing between harness, tool-use, or direct prompting patterns.
- Designing the boundary between human oversight and agent autonomy.

## Routing Decision Tree

```
Is this about building/configuring an agent harness or dev-loop?
  → YES → agent-harness

Is this about designing multi-agent systems (orchestrators, sub-agents)?
  → YES → agent-system-architecture

Is this about code architecture (not agent-specific)?
  → YES → architecture

Is this about CI/CD that an agent will run or trigger?
  → YES → cicd

Is this about evaluating/testing agent outputs?
  → YES → ai-evals
```

## Agentic Development Principles

- **Harness-first**: Build the harness before the agent. Define done, define tools, define approval gates.
- **Fail loud**: Agents should surface uncertainty rather than silently choosing wrong paths.
- **Human-in-the-loop by default**: Default to requiring approval for irreversible or high-blast-radius actions.
- **Minimal tool surface**: Give each agent only the tools it needs for its scope.
- **Observability**: Every agent run should produce a trace that answers "what happened and why."
