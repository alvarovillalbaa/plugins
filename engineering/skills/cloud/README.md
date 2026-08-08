# Cloud

CLI-first, multi-cloud operations router for AWS, Azure, GCP, Vercel, Heroku, and Railway.

## Use this for

- identifying which cloud estate a repo actually uses, including mixed PaaS-plus-hyperscaler estates
- designing AWS, Azure, GCP, Vercel, Heroku, or Railway target architectures before provisioning
- true multi-cloud designs where different concerns (runtime, data, DNS, secrets) live on different providers on purpose
- planning and executing cross-provider or PaaS-to-hyperscaler migrations
- deploying services or wiring CI/CD from the terminal
- inventory, optimization, and incident remediation
- cloud changes that need explicit approval gates and rollback thinking, including database migrations run as part of a deploy or cloud migration

## Install

```bash
npx -y skills add ./engineering/skills/cloud
mkdir -p ~/.codex/skills
cp -R engineering/skills/cloud ~/.codex/skills/
```

Codex `$skill-installer` path:

```text
https://github.com/alvarovillalbaa/plugins/tree/main/engineering/skills/cloud
```

## What is bundled

This skill is a thin router. The detailed references, scripts, and playbooks live in the child skills below — see [`SKILL.md`](./SKILL.md) for routing rules.

- `references/routing-guide.md` — how to route a request to the right child skill.

AWS deep-dive references live in [`../aws-ops/references/`](../aws-ops/references/):

- `aws-amplify-guide.md` — Amplify full-stack (auth, data, storage, functions, hosting, Gen 2)
- `aws-serverless-guide.md` — Lambda, API Gateway, Step Functions, EventBridge, SAM, CDK
- `aws-databases-guide.md` — RDS, Aurora, Aurora DSQL, DynamoDB, ElastiCache, connection management
- `aws-cli-playbook.md` — AWS CLI operating habits

Azure-specific references live in [`../azure-ops/references/`](../azure-ops/references/):

- `azure-diagnostics-guide.md`, `azure-resource-visualization.md`, `azure-cost-optimization-guide.md`, `azure-storage-guide.md`, `azure-compute-guide.md`, `azure-upgrade-guide.md`, `azure-compliance-guide.md`, `azure-entra-app-registration.md`, `azure-foundry-guide.md`, `azure-cli-playbook.md`

GCP-specific references live in [`../gcp-ops/references/`](../gcp-ops/references/).

Vercel, Heroku, and Railway references live in [`../paas-ops/references/`](../paas-ops/references/):

- `vercel-cli-playbook.md`, `heroku-cli-playbook.md`, `railway-cli-playbook.md`
- `paas-selection-guide.md` — when to use a PaaS provider versus a hyperscaler

Cross-cloud architecture references live in [`../cloud-architecture/references/`](../cloud-architecture/references/):

- `cloud-architecture-patterns.md`, `service-selection-matrix.md`
- `provider-selection.md` — multi-cloud rules, true multi-cloud designs, and the cloud migration playbook
- `approval-policy.md` — approval gates, cost hotspots, and the database-migration/backfill orchestration rules

Notable architecture tooling: [`../cloud-architecture/scripts/architecture_designer.py`](../cloud-architecture/scripts/architecture_designer.py).
