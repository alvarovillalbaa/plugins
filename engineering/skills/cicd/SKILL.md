---
name: cicd
description: >-
  Use for cloud deployment strategy, CI/CD wiring, OIDC or managed identity,
  rollout gates, and deploy automation. Child skill of `cloud`;
  route here from the parent router when this lane is the narrowest owner.
---

# Cloud Deployment Cicd

This child skill owns cloud deployment strategy, CI/CD wiring, OIDC or managed identity, rollout gates, and deploy automation. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about cloud deployment strategy, CI/CD wiring, OIDC or managed identity, rollout gates, and deploy automation.
- The parent router [`../cloud/SKILL.md`](../cloud/SKILL.md) selects this child.
- The work needs this lane's references, scripts, examples, hooks, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `scripts/` contains executable helpers owned by this lane.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.
- `hooks/` contains hook entrypoints only when this lane owns hook behavior.

## Chain Rules

- Chain to `quality-assurance`, `agentic-development/release-landing`, `backend`, `ai-engineering`, `pentest/cloud-container-pentest` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `clous-cli-integration`: Use Clous-owned CLI integration guidance for command-line workflows. Install: `python scripts/install-external-skills.py --skill clous-cli-integration --agent codex`.
- `clous-cli-use`: Use Clous-owned CLI usage guidance for platform command-line operations. Install: `python scripts/install-external-skills.py --skill clous-cli-use --agent codex`.
- `clous-sdk-release`: Use Clous-owned SDK release guidance for package and release workflows. Install: `python scripts/install-external-skills.py --skill clous-sdk-release --agent codex`.
- `browserbase-cli`: Use Browserbase CLI guidance for local setup and operational commands. Install: `python scripts/install-external-skills.py --skill browserbase-cli --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
