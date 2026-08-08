---
name: data-ml-pipelines
description: Use for data pipelines, ML feature pipelines, model evaluation, fine-tuning datasets, and DataOps workflows. Child of `ai-engineering`.
---

# Data Ml Pipelines

This child skill owns data pipelines, ML feature pipelines, model evaluation, fine-tuning datasets, and DataOps workflows. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about data pipelines, ML feature pipelines, model evaluation, fine-tuning datasets, and DataOps workflows.
- The parent router [`../ai-engineering/SKILL.md`](../ai-engineering/SKILL.md) selects this child.
- The work needs this lane's references, scripts, examples, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `scripts/` contains executable helpers owned by this lane.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.

## Chain Rules

- Chain to `quality-assurance/ai-evals`, `quality-assurance/security`, `backend`, `cloud`, `plugins-management`, `brain` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
