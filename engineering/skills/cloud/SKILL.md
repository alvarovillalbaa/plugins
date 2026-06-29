---
name: cloud
description: Router for cloud resources, deployment, incidents, provider operations, and architecture.
---

# Cloud Router

## Children

- [`resources`](../resources/SKILL.md) - Resources work.
- [`cicd`](../cicd/SKILL.md) - Cicd work.
- [`cloud-incidents`](../cloud-incidents/SKILL.md) - Cloud Incidents work.
- [`aws-ops`](../aws-ops/SKILL.md) - Aws Ops work.
- [`azure-ops`](../azure-ops/SKILL.md) - Azure Ops work.
- [`gcp-ops`](../gcp-ops/SKILL.md) - Gcp Ops work.
- [`cloud-architecture`](../cloud-architecture/SKILL.md) - Cloud Architecture work.

## Route

| Request | Use |
| --- | --- |
| resources requests | [`resources`](../resources/SKILL.md) |
| cicd requests | [`cicd`](../cicd/SKILL.md) |
| cloud incidents requests | [`cloud-incidents`](../cloud-incidents/SKILL.md) |
| aws ops requests | [`aws-ops`](../aws-ops/SKILL.md) |
| azure ops requests | [`azure-ops`](../azure-ops/SKILL.md) |
| gcp ops requests | [`gcp-ops`](../gcp-ops/SKILL.md) |
| cloud architecture requests | [`cloud-architecture`](../cloud-architecture/SKILL.md) |

## Chain Rules

Chain to these skills when the task crosses this skill's boundary:

- `quality-assurance`
- `agentic-development/release-landing`
- `backend`
- `ai-engineering`
- `pentest/cloud-container-pentest`

## Operating Rules

- Keep this parent compact; use children for lane-specific execution depth.
- Prefer the child skill's bundled resources when a child owns the request.
- Preserve local skill rules, repo facts, safety gates, product/channel constraints, and explicit local exceptions over external guidance when they conflict.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `clous-remote-mcp-integration`: Use Clous-owned remote MCP integration guidance for tool-server integrations. Install: `python scripts/install-external-skills.py --skill clous-remote-mcp-integration --agent codex`.
- `clous-platform-operation`: Use Clous-owned platform operation guidance for runtime and workspace operations. Install: `python scripts/install-external-skills.py --skill clous-platform-operation --agent codex`.
- `clous-mcp-use`: Use Clous-owned MCP usage guidance for connected tool workflows. Install: `python scripts/install-external-skills.py --skill clous-mcp-use --agent codex`.
- `browserbase-cli`: Use Browserbase CLI guidance for local setup and operational commands. Install: `python scripts/install-external-skills.py --skill browserbase-cli --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
