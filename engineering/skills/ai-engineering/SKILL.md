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

- [`agent-system-architecture`](../agent-system-architecture/SKILL.md) - agent architectures, multi-agent topology, agent lifecycles, handoff patterns, and orchestration contracts
- [`prompt-tool-design`](../prompt-tool-design/SKILL.md) - system prompts, tool schemas, tool descriptions, constrained generation, and prompt/tool reliability
- [`context-memory-rag`](../context-memory-rag/SKILL.md) - context assembly, memory tiers, retrieval, RAG, vector stores, compaction, and grounding contracts
- [`ai-evals-observability`](../ai-evals-observability/SKILL.md) - AI eval architecture, traces, metrics, score monitoring, regression thresholds, and production AI observability
- [`ai-governance-safety`](../ai-governance-safety/SKILL.md) - agent governance, safety gates, scope isolation, autonomy limits, prompt-injection posture, and side-effect controls
- [`data-ml-pipelines`](../data-ml-pipelines/SKILL.md) - data pipelines, ML feature pipelines, model evaluation, fine-tuning datasets, and DataOps workflows
- [`computer-vision-systems`](../computer-vision-systems/SKILL.md) - computer vision architectures, detection, segmentation, video inference, model optimization, and production deployment

## Route

| User asks for | Use |
| --- | --- |
| agent architectures, multi-agent topology, agent lifecycles, handoff patterns, and orchestration contracts | [`agent-system-architecture`](../agent-system-architecture/SKILL.md) |
| system prompts, tool schemas, tool descriptions, constrained generation, and prompt/tool reliability | [`prompt-tool-design`](../prompt-tool-design/SKILL.md) |
| context assembly, memory tiers, retrieval, RAG, vector stores, compaction, and grounding contracts | [`context-memory-rag`](../context-memory-rag/SKILL.md) |
| AI eval architecture, traces, metrics, score monitoring, regression thresholds, and production AI observability | [`ai-evals-observability`](../ai-evals-observability/SKILL.md) |
| agent governance, safety gates, scope isolation, autonomy limits, prompt-injection posture, and side-effect controls | [`ai-governance-safety`](../ai-governance-safety/SKILL.md) |
| data pipelines, ML feature pipelines, model evaluation, fine-tuning datasets, and DataOps workflows | [`data-ml-pipelines`](../data-ml-pipelines/SKILL.md) |
| computer vision architectures, detection, segmentation, video inference, model optimization, and production deployment | [`computer-vision-systems`](../computer-vision-systems/SKILL.md) |

## Chain Rules

- `quality-assurance/ai-evals-testing`
- `quality-assurance/passive-security-review`
- `backend`
- `cloud-management`
- `auto-improve`
- `second-brain`

## Operating Rules

- Keep this `SKILL.md` small and routing-focused.
- Do not recreate the old broad parent behavior here; put execution depth in child assets.
- If no child matches, handle only shared methodology/default workflow or document the missing lane.
- Every child and parent skill must keep `examples/`, `hooks/`, `references/`, `scripts/`, and `templates/`.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
