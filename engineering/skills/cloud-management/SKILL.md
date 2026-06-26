---
name: cloud-management
description: >-
  Router for cloud resource optimization, deployment/CI/CD, cloud ops and
  incidents, AWS ops, Azure ops, GCP ops, and cloud architecture design.
---

# Cloud Management Router

This parent is a router. Select the narrowest child and load that child before using lane-specific assets.

## Children

- [`cloud-resources-optimization`](../cloud-resources-optimization/SKILL.md) - cloud inventory, cost optimization, resource sizing, waste cleanup, lifecycle policy, and utilization analysis
- [`cloud-deployment-cicd`](../cloud-deployment-cicd/SKILL.md) - cloud deployment strategy, CI/CD wiring, OIDC or managed identity, rollout gates, and deploy automation
- [`cloud-ops-cost-incidents`](../cloud-ops-cost-incidents/SKILL.md) - cloud incidents, runtime diagnostics, logs, health checks, cost anomalies, and operational recovery loops
- [`aws-platform-ops`](../aws-platform-ops/SKILL.md) - AWS-specific operations for Amplify, Lambda, ECS, RDS/Aurora, DynamoDB, IAM, networking, and deployment troubleshooting
- [`azure-platform-ops`](../azure-platform-ops/SKILL.md) - Azure-specific operations for Container Apps, App Service, Functions, storage, Key Vault, Entra ID, Foundry, and diagnostics
- [`gcp-platform-ops`](../gcp-platform-ops/SKILL.md) - GCP-specific operations for Cloud Run, GKE, Cloud SQL, IAM, Pub/Sub, storage, monitoring, and deployment troubleshooting
- [`cloud-architecture-design`](../cloud-architecture-design/SKILL.md) - provider selection, service selection, cloud architecture design, migration target choices, and approval-aware architecture plans

## Route

| User asks for | Use |
| --- | --- |
| cloud inventory, cost optimization, resource sizing, waste cleanup, lifecycle policy, and utilization analysis | [`cloud-resources-optimization`](../cloud-resources-optimization/SKILL.md) |
| cloud deployment strategy, CI/CD wiring, OIDC or managed identity, rollout gates, and deploy automation | [`cloud-deployment-cicd`](../cloud-deployment-cicd/SKILL.md) |
| cloud incidents, runtime diagnostics, logs, health checks, cost anomalies, and operational recovery loops | [`cloud-ops-cost-incidents`](../cloud-ops-cost-incidents/SKILL.md) |
| AWS-specific operations for Amplify, Lambda, ECS, RDS/Aurora, DynamoDB, IAM, networking, and deployment troubleshooting | [`aws-platform-ops`](../aws-platform-ops/SKILL.md) |
| Azure-specific operations for Container Apps, App Service, Functions, storage, Key Vault, Entra ID, Foundry, and diagnostics | [`azure-platform-ops`](../azure-platform-ops/SKILL.md) |
| GCP-specific operations for Cloud Run, GKE, Cloud SQL, IAM, Pub/Sub, storage, monitoring, and deployment troubleshooting | [`gcp-platform-ops`](../gcp-platform-ops/SKILL.md) |
| provider selection, service selection, cloud architecture design, migration target choices, and approval-aware architecture plans | [`cloud-architecture-design`](../cloud-architecture-design/SKILL.md) |

## Chain Rules

- `quality-assurance`
- `agentic-development/release-landing`
- `backend`
- `ai-engineering`
- `pentest/cloud-container-pentest`

## Operating Rules

- Keep this `SKILL.md` small and routing-focused.
- Do not recreate the old broad parent behavior here; put execution depth in child assets.
- If no child matches, handle only shared methodology/default workflow or document the missing lane.
- Every child and parent skill must keep `examples/`, `hooks/`, `references/`, `scripts/`, and `templates/`.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
