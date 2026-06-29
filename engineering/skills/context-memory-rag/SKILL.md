---
name: context-memory-rag
description: >-
  Use for context assembly, memory tiers, retrieval, RAG, vector stores,
  compaction, and grounding contracts. Child skill of `ai-engineering`;
  route here from the parent router when this lane is the narrowest owner.
---

# Context Memory RAG

This child skill owns context assembly, memory tiers, retrieval, RAG, vector stores, compaction, and grounding contracts. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about context assembly, memory tiers, retrieval, RAG, vector stores, compaction, and grounding contracts.
- The parent router [`../ai-engineering/SKILL.md`](../ai-engineering/SKILL.md) selects this child.
- The work needs this lane's references, scripts, examples, hooks, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `scripts/` contains executable helpers owned by this lane.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.
- `hooks/` contains hook entrypoints only when this lane owns hook behavior.

## Chain Rules

- Chain to `quality-assurance/ai-evals`, `quality-assurance/security`, `backend`, `cloud`, `skills-management`, `brain` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `clous-knowledge-retrieval`: Use Clous-owned retrieval guidance for knowledge lookup and source-grounded context. Install: `python scripts/install-external-skills.py --skill clous-knowledge-retrieval --agent codex`.
- `use-afs`: Use the AFS filesystem layout and naming conventions instead of duplicating local filesystem guidance. Install: `python scripts/install-external-skills.py --skill use-afs --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
