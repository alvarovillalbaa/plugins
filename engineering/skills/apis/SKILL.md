---
name: apis
description: Use for API contracts, service boundaries, serializers, request/response shape, jobs, queues, and backend application design. Child of `backend`.
---

# API Service Design

This child skill owns API contracts, service boundaries, serializers, request/response shape, jobs, queues, and backend application design. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about API contracts, service boundaries, serializers, request/response shape, jobs, queues, and backend application design.
- The parent router [`../backend/SKILL.md`](../backend/SKILL.md) selects this child.
- The work needs this lane's references, scripts, examples, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `scripts/` contains executable helpers owned by this lane.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.

## Chain Rules

- Chain to `quality-assurance/testing`, `quality-assurance/security`, `quality-assurance`, `code-documentation`, `cloud`, `ai-engineering` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.
- Treat request/response shape as a contract. Reject wrong shapes at the boundary and fix the producer; do not add compatibility aliases or hidden payload transformations by default.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `clous-a2a-integration`: Use Clous-owned A2A integration guidance for agent-to-agent surfaces. Install: `python3 scripts/install-external-skills.py --skill clous-a2a-integration --agent codex`.
- `clous-api-integration`: Use Clous-owned API integration guidance for building or changing platform integrations. Install: `python3 scripts/install-external-skills.py --skill clous-api-integration --agent codex`.
- `clous-api-use`: Use Clous-owned API usage guidance for consuming platform APIs. Install: `python3 scripts/install-external-skills.py --skill clous-api-use --agent codex`.
- `clous-oauth-integration`: Use Clous-owned OAuth integration guidance for auth and consent flows. Install: `python3 scripts/install-external-skills.py --skill clous-oauth-integration --agent codex`.
- `clous-webhook-integration`: Use Clous-owned webhook integration guidance for producer-side webhook work. Install: `python3 scripts/install-external-skills.py --skill clous-webhook-integration --agent codex`.
- `clous-webhook-operations`: Use Clous-owned webhook operations guidance for consumer-side webhook work. Install: `python3 scripts/install-external-skills.py --skill clous-webhook-operations --agent codex`.
- `browserbase-browser-to-api`: Convert browser workflows into API-backed automation when appropriate. Install: `python3 scripts/install-external-skills.py --skill browserbase-browser-to-api --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
