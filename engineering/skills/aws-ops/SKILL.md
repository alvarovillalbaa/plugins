---
name: aws-ops
description: Use for AWS-specific operations for Amplify, Lambda, ECS, RDS/Aurora, DynamoDB, IAM, networking, and deployment troubleshooting. Child of `cloud`.
---

# AWS Platform Ops

This child skill owns AWS-specific operations for Amplify, Lambda, ECS, RDS/Aurora, DynamoDB, IAM, networking, and deployment troubleshooting. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about AWS-specific operations for Amplify, Lambda, ECS, RDS/Aurora, DynamoDB, IAM, networking, and deployment troubleshooting.
- The parent router [`../cloud/SKILL.md`](../cloud/SKILL.md) selects this child.
- The work needs this lane's references, scripts, examples, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `scripts/` contains executable helpers owned by this lane.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.

## Chain Rules

- Chain to `quality-assurance`, `agentic-development/release-landing`, `backend`, `ai-engineering`, `pentest` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
