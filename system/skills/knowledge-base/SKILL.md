---
name: knowledge-base
description: Use for knowledge-base improvement, dedupe proposals, canonical page health, missing source promotion, and knowledge drift repair. Child of `plugins-management`.
---

# Knowledge Base Improve

This child skill owns knowledge-base improvement, dedupe proposals, canonical page health, missing source promotion, and knowledge drift repair. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about knowledge-base improvement, dedupe proposals, canonical page health, missing source promotion, and knowledge drift repair.
- The parent router [`../plugins-management/SKILL.md`](../plugins-management/SKILL.md) selects this child.
- The work needs this lane's references, examples, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.

## Chain Rules

- Chain to `memory`, `brain`, `code-documentation`, `agentic-development/agent-harness`, `personalize/voice` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

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
