---
name: ai-engineering
description: >-
  Router for AI system architecture, prompt/tool design, context and memory
  RAG, AI eval observability, governance/safety, data/ML pipelines, and
  computer vision systems.
---

# AI Engineering Router

This parent is a router. Select the narrowest child and load that child before using lane-specific assets.

## Children

- [`agent-system-architecture`](../agent-system-architecture/SKILL.md) - Agent System Architecture work.
- [`prompt-tool-design`](../prompt-tool-design/SKILL.md) - Prompt Tool Design work.
- [`context-memory-rag`](../context-memory-rag/SKILL.md) - Context Memory Rag work.
- [`ai-evals-observability`](../ai-evals-observability/SKILL.md) - Ai Evals Observability work.
- [`ai-governance-safety`](../ai-governance-safety/SKILL.md) - Ai Governance Safety work.
- [`data-ml-pipelines`](../data-ml-pipelines/SKILL.md) - Data Ml Pipelines work.
- [`computer-vision-systems`](../computer-vision-systems/SKILL.md) - Computer Vision Systems work.

## Route

| Request | Use |
| --- | --- |
| agent system architecture requests | [`agent-system-architecture`](../agent-system-architecture/SKILL.md) |
| prompt tool design requests | [`prompt-tool-design`](../prompt-tool-design/SKILL.md) |
| context memory rag requests | [`context-memory-rag`](../context-memory-rag/SKILL.md) |
| ai evals observability requests | [`ai-evals-observability`](../ai-evals-observability/SKILL.md) |
| ai governance safety requests | [`ai-governance-safety`](../ai-governance-safety/SKILL.md) |
| data ml pipelines requests | [`data-ml-pipelines`](../data-ml-pipelines/SKILL.md) |
| computer vision systems requests | [`computer-vision-systems`](../computer-vision-systems/SKILL.md) |

## Chain Rules

Chain to these skills when the task crosses this skill's boundary:

- `quality-assurance/ai-evals`
- `quality-assurance/security`
- `backend`
- `cloud`
- `skills-management`
- `brain`

## Operating Rules

- Keep this `SKILL.md` small and routing-focused.
- Do not recreate the old broad parent behavior here; put execution depth in child assets.
- If no child matches, handle only shared methodology/default workflow or document the missing lane.
- Every child and parent skill must keep `examples/`, `hooks/`, `references/`, `scripts/`, and `templates/`.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `browserbase-agent-experience`: Use Browserbase guidance for browser-based agent experiences. Install: `python scripts/install-external-skills.py --skill browserbase-agent-experience --agent codex`.
- `browserbase-webmcp-gen`: Generate Web MCP wrappers from browser workflows when toolization is useful. Install: `python scripts/install-external-skills.py --skill browserbase-webmcp-gen --agent codex`.
- `browserbase-functions`: Use Browserbase function patterns for reusable browser automation tools. Install: `python scripts/install-external-skills.py --skill browserbase-functions --agent codex`.
- `clous-agent-runs`: Use Clous-owned agent run guidance for operating and inspecting agent executions. Install: `python scripts/install-external-skills.py --skill clous-agent-runs --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
