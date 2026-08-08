---
name: brain
description: Route and maintain BRAIN.md-bounded second-brain workflows — raw ingestion, folder adaptation, memory-to-knowledge compilation, and canonical knowledge updates.
---

# Brain Router

## Children

- [`ingestion`](../ingestion/SKILL.md) - Ingestion work.

## Route

| Request | Use |
| --- | --- |
| ingestion requests | [`ingestion`](../ingestion/SKILL.md) |

## Chain Rules

Chain to these skills when the task crosses this skill's boundary:

- `knowledge-base`
- `memory`
- `research`
- `reporting`

## Operating Rules

- Keep this parent compact; use children for lane-specific execution depth.
- Read [`references/brain_contract.md`](references/brain_contract.md) before any write-bearing brain run.
- Count `BRAIN.md` files before creating or updating canonical knowledge. Work inside exactly one brain boundary.
- Preserve the user's existing company or workspace standard when `BRAIN.md` defines one; otherwise use the strict AFS defaults.
- Prefer the child skill's bundled resources when a child owns the request.
- Preserve local skill rules, repo facts, safety gates, product/channel constraints, and explicit local exceptions over external guidance when they conflict.

## References

- [`references/brain_contract.md`](references/brain_contract.md) - brain boundaries, AFS/native adaptation, canonical paths, and raw/memory evidence rules.
- [`references/operational_modes.md`](references/operational_modes.md) - concrete brain modes such as ingest, query, reconcile, health, work, and compound.
- [`references/page_model.md`](references/page_model.md) - canonical page responsibilities and provenance model.
- [`references/compound_loop.md`](references/compound_loop.md) - closing loop for durable learnings.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `writing-great-skills`: Use external skill-authoring quality rules when creating or revising skills. Install: `python3 scripts/install-external-skills.py --skill writing-great-skills --agent codex`.
- `teach`: Create mission-grounded learning material, resources, records, and lessons. Install: `python3 scripts/install-external-skills.py --skill teach --agent codex`.
- `grilling`: Interview one decision at a time until a plan or design is sharp. Install: `python3 scripts/install-external-skills.py --skill grilling --agent codex`.
- `grill-me`: Shortcut into a grilling session for plan or design stress testing. Install: `python3 scripts/install-external-skills.py --skill grill-me --agent codex`.
- `grill-with-docs`: Stress-test a plan or design while maintaining docs, ADRs, and glossary context. Install: `python3 scripts/install-external-skills.py --skill grill-with-docs --agent codex`.
- `use-afs`: Use the AFS filesystem layout and naming conventions instead of duplicating local filesystem guidance. Install: `python3 scripts/install-external-skills.py --skill use-afs --agent codex`.
- `clous-knowledge-retrieval`: Use Clous-owned retrieval guidance for knowledge lookup and source-grounded context. Install: `python3 scripts/install-external-skills.py --skill clous-knowledge-retrieval --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
