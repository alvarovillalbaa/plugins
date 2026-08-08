---
name: cloud-incidents
description: Use for cloud incidents, runtime diagnostics, logs, health checks, cost anomalies, and operational recovery loops. Child of `cloud`.
---

# Cloud Ops Cost Incidents

This child skill owns cloud incidents, runtime diagnostics, logs, health checks, cost anomalies, and operational recovery loops. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about cloud incidents, runtime diagnostics, logs, health checks, cost anomalies, and operational recovery loops.
- The parent router [`../cloud/SKILL.md`](../cloud/SKILL.md) selects this child.
- The work needs this lane's references, examples, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.

## Chain Rules

- Chain to `quality-assurance`, `agentic-development/release-landing`, `backend`, `ai-engineering`, `pentest` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
