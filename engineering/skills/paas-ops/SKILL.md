---
name: paas-ops
description: >-
  Use for Vercel, Heroku, and Railway platform operations — deploys,
  environment/config management, custom domains, previews, add-ons and
  integrations, logs, and platform-specific CLI workflows. Child skill of
  `cloud`; route here from the parent router when this lane is the
  narrowest owner.
---

# PaaS Platform Ops

This child skill owns Vercel, Heroku, and Railway platform operations — deploys, environment/config management, custom domains, previews, add-ons and integrations, logs, and platform-specific CLI workflows. It is the PaaS counterpart to `aws-ops`, `azure-ops`, and `gcp-ops`, for repos that run on managed application platforms instead of, or alongside, the hyperscalers.

## Use When

- The request is primarily about Vercel, Heroku, or Railway operations: deploys, env vars, domains, previews, add-ons, logs, or CLI troubleshooting.
- The parent router [`../cloud/SKILL.md`](../cloud/SKILL.md) selects this child.
- The work needs this lane's references, scripts, examples, or templates.
- The repo mixes a PaaS provider with a hyperscaler (e.g. Vercel frontend + AWS backend) — this skill owns the PaaS side while `aws-ops`/`azure-ops`/`gcp-ops` own the rest; see [`../cloud-architecture/references/provider-selection.md`](../cloud-architecture/references/provider-selection.md) for how the concerns split.

## Assets

- `references/vercel-cli-playbook.md`, `references/heroku-cli-playbook.md`, `references/railway-cli-playbook.md` — per-provider CLI operating guides.
- `references/paas-selection-guide.md` — when a PaaS provider is the right call versus AWS, Azure, or GCP.
- `scripts/` contains executable helpers owned by this lane.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.

## Chain Rules

- Chain to `quality-assurance`, `agentic-development/release-landing`, `backend`, `ai-engineering`, `pentest` when the task crosses this child's boundary.
- Chain to `backend/databases` for migration mechanics and schema/data changes; this skill only owns the platform-side deploy/rollout of a service, not the database migration itself.
- Chain to `cloud-architecture` when the request is choosing between a PaaS provider and a hyperscaler, or planning a migration between them, rather than operating an already-chosen platform.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
