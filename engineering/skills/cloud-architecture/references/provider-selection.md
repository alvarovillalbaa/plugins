# Provider Selection

## Contents

- What to collect first
- Research first
- Decision framework
- Multi-cloud rule set
- Workload mapping
- Service topology cues
- Managed-service bias
- Existing estate versus greenfield
- Cloud migration
- Multi-runtime backend example

## What to Collect First

- repo shape: static site, API, monolith, worker fleet, websocket or realtime service, scheduled jobs, or k8s-heavy app
- current ownership: Terraform, Bicep, CloudFormation, Pulumi, Helm, raw manifests, or ad hoc shell
- current providers already in use for runtime, database, cache, storage, secrets, DNS, CDN, email, and observability
- environment expectations: dev only, staging plus prod, HA, compliance, latency, residency, or private networking
- team reality: operator familiarity, CI system, identity model, and change cadence
- cost posture: cost-sensitive dev default or production-grade availability

## Research First

Provider capabilities, pricing, and limits change often enough that built-in knowledge can be stale by the time a decision matters. Before recommending or committing to a provider, service, or migration:

- Verify current pricing, plan tiers, and feature availability rather than asserting a remembered number.
- For Vercel, prefer the `search_vercel_documentation` MCP tool when available.
- For any other provider, use a web search against the provider's current docs or pricing page when the decision is cost-sensitive, close to a plan-tier boundary, or hinges on a specific feature or limit.
- Treat this as mandatory, not optional, when the choice is expensive to reverse (a migration, a committed spend, or a service with lock-in) or when the user's request implies the offering may have changed since this guidance was written.

## Decision Framework

Score providers by concern instead of picking one winner globally:

1. Existing footprint
   - Is the concern already owned cleanly by one provider?
2. Workload fit
   - Does the repo want managed containers, serverless, Kubernetes, or VMs?
3. Operational simplicity
   - Which option minimizes bespoke networking, secrets drift, and deployment friction?
4. Latency and data gravity
   - Can runtime stay close to its database and cache?
5. Security and identity
   - Can CI and runtime use short-lived or federated identity cleanly?
6. Cost
   - Which option avoids always-on clusters, needless NAT, or premium services for the target environment?

Prefer the provider already operating that concern unless the improvement from moving is clear and material.

## Multi-Cloud Rule Set

- Do not assume one provider for everything.
- Treat multi-cloud as a real, first-class target shape, not just a DR/failover posture: different concerns (runtime, data, storage, DNS, secrets, observability) can each live on the provider best suited to them, permanently, by design — for example a Vercel-hosted frontend in front of an AWS-hosted API and database.
- Model runtime, data, storage, DNS, secrets, and observability independently when the estate is mixed.
- Keep stateful services close to the runtime unless the user explicitly wants split-cloud data paths.
- Keep one system of record for DNS per environment.
- Keep one system of record for secrets per environment.
- Keep one explicit CI identity flow per provider and environment.
- Reuse the provider already operating a concern when the switching cost is higher than the improvement.
- Avoid partial migrations that leave DNS, data, or credentials stranded across providers without an explicit operating model.
- Design for interchangeability where it's cheap (stateless runtime behind a provider-agnostic build, config sourced from one secrets system) and accept lock-in where fighting it isn't worth it (a provider's native database, edge network, or queueing primitive) — do not add abstraction layers purely to keep every provider swappable when no swap is planned.

## Default Service Mapping by Workload

| Workload | AWS default | Azure default | GCP default | PaaS default |
| --- | --- | --- | --- | --- |
| Static site or SPA | S3 + CloudFront | Static Web Apps or Storage + Front Door | Cloud Storage + Cloud CDN | Vercel |
| Containerized web API | ECS Fargate + ALB | Container Apps | Cloud Run | Railway or Heroku |
| Web plus worker plus websocket | ECS services split by role | Container Apps split by role | Cloud Run services or GKE if long-running workers need more control | Railway or Heroku, one service per role |
| Event-driven jobs | Lambda or ECS tasks + EventBridge + SQS | Functions or Container Apps Jobs + Event Grid or Service Bus | Cloud Run Jobs or Functions + Pub/Sub + Cloud Scheduler | Vercel Functions (short-lived) or a Railway/Heroku worker + third-party queue |
| Stateful relational DB | RDS PostgreSQL or MySQL | Azure Database for PostgreSQL or MySQL | Cloud SQL | Heroku Postgres or Railway Postgres |
| Cache or broker | ElastiCache | Azure Cache for Redis | Memorystore | Heroku Redis or Railway Redis |
| Registry | ECR | ACR | Artifact Registry | N/A — PaaS providers build from source or a Dockerfile directly |
| Secrets | Secrets Manager or Parameter Store | Key Vault | Secret Manager | Provider-native env vars/config vars (Vercel/Heroku/Railway) |
| K8s-heavy repo | EKS | AKS | GKE | Not a fit — see [`../paas-ops/references/paas-selection-guide.md`](../../paas-ops/references/paas-selection-guide.md) |

See [`../paas-ops/references/paas-selection-guide.md`](../../paas-ops/references/paas-selection-guide.md) for when the PaaS default is the right call versus a hyperscaler, and per-provider operating detail in [`../paas-ops/SKILL.md`](../../paas-ops/SKILL.md).

## Service Topology Cues

- public web traffic and internal workers usually deserve separate runtimes
- websocket or realtime traffic often wants its own service, timeout policy, and scaling rules
- schedulers and admin-only surfaces should be isolated from user-facing ingress
- if the repo already runs several long-lived responsibilities inside one image, keep the runtime split explicit even when the build artifact is shared
- if migrations run during steady-state startup, treat every rollout as higher-risk and prefer moving to a one-off migration job when the repo permits it

## Managed-Service Bias

- Prefer managed containers over VMs for modern apps unless the repo depends on VM-specific behavior.
- Prefer provider-native schedulers and queues over cron inside a long-running app container.
- Prefer one registry plus rolling or revision-based service updates over SSH-based deploys.
- Prefer dev-sized single-zone or single-region defaults until the user asks for production-ready HA.
- Prefer Kubernetes only when the repo already needs ingress controllers, custom networking, node tuning, sidecars, daemon workloads, or service mesh patterns.

## Concern-by-Concern Guidance

### Runtime

- API or web service: ECS Fargate, Container Apps, or Cloud Run
- background workers: separate service or job, not a second command stuffed into the web process
- websocket or realtime: separate service with the right ingress behavior
- static frontend: object storage plus CDN or provider-native static hosting

### Data

- relational first: managed PostgreSQL or MySQL
- cache or broker: managed Redis or provider-native async services
- object files: provider-native object storage

### Identity and Secrets

- CI: OIDC, federated credentials, or workload identity
- runtime: task role, managed identity, or service account
- secrets: provider-native secret store over repo or pipeline secrets where possible

### Network and Edge

- Keep public ingress explicit.
- Prefer private access from runtime to database and cache.
- Keep DNS ownership centralized per environment.

## Existing Estate vs Greenfield

- Greenfield: choose the simplest cohesive provider-native path and keep the stack boring.
- Existing estate: extend the current account, subscription, or project footprint unless there is a clear reason to split or migrate.
- Migration: do not split data, secrets, DNS, or identity across providers without a deliberate steady-state design.

## Cloud Migration

Use this when the task is moving a workload from one provider to another, including hyperscaler-to-hyperscaler, hyperscaler-to-PaaS, and PaaS-to-hyperscaler moves.

### Migration Types

- **Lift-and-shift**: move the same architecture shape (e.g. containers to containers) to a new provider with minimal redesign. Fastest, least risky, usually leaves optimization on the table.
- **Replatform**: adopt the destination provider's managed-service equivalents (e.g. self-managed Postgres on a VM to RDS/Cloud SQL, or a hand-rolled container deploy to Vercel/Railway/Heroku) while keeping the application mostly unchanged.
- **Provider-to-provider (same shape)**: AWS ECS to Azure Container Apps or GCP Cloud Run, using the [service selection matrix](./service-selection-matrix.md) to map equivalents.
- **PaaS to hyperscaler**: usually driven by scale, compliance, or a specific service the PaaS provider doesn't offer — see [`../paas-ops/references/paas-selection-guide.md`](../../paas-ops/references/paas-selection-guide.md) for the trigger conditions before recommending this.
- **Hyperscaler to PaaS**: usually driven by wanting to shed operational overhead for a workload that doesn't need hyperscaler-specific features — verify the workload actually fits a PaaS provider's model first (see the same guide).

### Migration Phases

1. **Assess**: inventory what's moving (runtime, data, DNS, secrets, CI identity), confirm the destination's service mapping via the [service selection matrix](./service-selection-matrix.md), and confirm current provider pricing/limits for the destination (see "Research First" above).
2. **Plan**: decide cutover strategy (big-bang vs. gradual), who owns DNS during the transition, and the rollback path if the migration needs to be reversed.
3. **Execute**: provision the destination, wire CI identity, move non-stateful config first, then data.
4. **Cutover**: switch DNS/traffic, verify, keep the source environment intact until the destination is confirmed healthy.
5. **Decommission**: tear down the source only after a confirmed observation window; do not delete source infrastructure at cutover time.

### Data and Database Migration Posture

This skill does not own migration mechanics — chain to `backend/databases` for schema design, migration script authoring, and backfill patterns. At the cloud-orchestration layer:

- Default to a **hard cut, not a backfill**, when the project has no live users or customers yet: provision the destination database empty (or with a one-time snapshot restore), point the app at it, and decommission the source. Dual-write, compatibility shims, and gradual backfill infrastructure are unnecessary complexity for a pre-launch project.
- If the project has live production data and users, treat the migration as requiring an explicit decision from the user before assuming a hard cut is safe — the same default `databases` itself uses.
- Always snapshot the source database immediately before cutover, regardless of user count — this is cheap insurance, not backfill work.
- See the "Database Migrations and Backfills" section of [`approval-policy.md`](./approval-policy.md) for the approval gate this triggers.

### Migration Execution Ownership

- Chain to `aws-ops`, `azure-ops`, `gcp-ops`, or [`paas-ops`](../../paas-ops/SKILL.md) for the destination provider's actual deploy/provisioning commands.
- Chain to `cicd` for wiring the new provider's CI identity and deploy pipeline.
- Chain to `cloud-incidents` if the migration itself needs an incident-style rollback during cutover.

## Multi-Runtime Backend Example

For a Django or API backend with worker queues, websocket traffic, Redis, PostgreSQL, file storage, and scheduled jobs:

- split runtime roles into `web`, `worker`, and `socket` or `realtime`
- use managed PostgreSQL, managed Redis, object storage, registry, and a secrets system
- keep migrations separate from steady-state rollout
- default mappings:
  - AWS: ECS Fargate + RDS + ElastiCache + S3 + ECR + Secrets Manager + EventBridge
  - Azure: Container Apps + PostgreSQL Flexible Server + Azure Cache for Redis + Blob Storage + ACR + Key Vault + Event Grid or Service Bus
  - GCP: Cloud Run + Cloud SQL + Memorystore + Cloud Storage + Artifact Registry + Secret Manager + Pub/Sub or Cloud Scheduler

## Read Before Changing

- approval rules and cost hotspots: [approval-policy.md](./approval-policy.md)
- automatic deploy design: [cicd-and-auto-deploy.md](../../cicd/references/cicd-and-auto-deploy.md)
- inventory and incident loops: [inventory-optimization-remediation.md](../../resources/references/inventory-optimization-remediation.md)
