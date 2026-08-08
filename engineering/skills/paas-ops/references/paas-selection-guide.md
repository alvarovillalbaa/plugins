# PaaS Selection Guide

Use this reference when deciding whether Vercel, Heroku, or Railway is the right fit for a workload, versus AWS, Azure, or GCP. This feeds the decision framework in [`../../cloud-architecture/references/provider-selection.md`](../../cloud-architecture/references/provider-selection.md) — read that first for the general multi-cloud decision process; this file is the PaaS-specific narrowing.

## When a PaaS Provider Is the Right Call

- The repo is a standard web app, API, or frontend framework (Next.js, Remix, Django, Rails, Express, Node worker) with no need for custom networking, node-level tuning, or compliance controls a managed platform can't satisfy.
- The team has no dedicated ops/infra function and wants deploys, previews, rollback, and basic observability to work with minimal configuration.
- Iteration speed matters more than infrastructure control — preview-per-branch, one-command rollback, and zero-config TLS/CDN are worth more than the marginal cost or feature gap versus a hand-built hyperscaler stack.
- The workload's traffic and data volume are moderate enough that PaaS pricing (which is usually a premium over raw hyperscaler compute) stays reasonable — verify current pricing rather than assuming (see "Research First" below).
- Team size is small enough that the operational simplicity trade-off dominates: fewer knobs, less IaC to maintain, no cluster or VPC to own.

## When a Hyperscaler Is the Better Call

- Compliance or data residency requirements need controls (private networking, dedicated tenancy, specific certifications) that the PaaS provider doesn't offer on an affordable plan.
- The workload needs Kubernetes-level control, custom networking, sidecars, node tuning, or GPU/specialized compute that PaaS platforms don't expose.
- Scale has grown to the point where hyperscaler compute pricing is materially cheaper than the equivalent PaaS plan tier — this is a real crossover point, not a given; verify it with current numbers before recommending a migration off PaaS.
- The team already has a mature IaC/ops practice on AWS/Azure/GCP and the marginal cost of adding one more service there is lower than standing up a second platform to operate.
- The estate needs deep integration with other hyperscaler-native services (a data warehouse, a specific managed ML service, an existing VPC-private database) that a PaaS platform can only reach over the public internet.

## Splitting Concerns (True Multi-Cloud)

PaaS and hyperscaler are not mutually exclusive on the same project. Common, legitimate splits:

- Frontend on Vercel (edge-optimized static/SSR hosting) with an API or worker fleet on AWS/Azure/GCP when the backend needs VPC-private data access or heavier compute.
- Vercel/Railway/Heroku for the primary app, with a hyperscaler-native data warehouse or ML platform for analytics/inference that the PaaS provider doesn't offer.
- A PaaS provider for early-stage/low-traffic products, with an explicit, planned migration path to a hyperscaler once traffic or compliance needs cross a known threshold.

When splitting, keep the same discipline the general multi-cloud rule set requires: one system of record for DNS per environment, one system of record for secrets per environment, and an explicit owner for each concern (runtime, data, DNS, secrets) rather than letting ownership blur across providers.

## Provider-to-Provider Differences That Affect the Choice

- **Vercel**: strongest for frontend-framework-native hosting (especially Next.js) and edge/CDN behavior; no general-purpose long-running compute — background workers and long-lived connections need a separate runtime elsewhere.
- **Heroku**: general-purpose dyno model (web, worker, one-off) with the longest-established add-on ecosystem (Postgres, Redis, logging); config var changes restart dynos, which matters for zero-downtime expectations.
- **Railway**: general-purpose service model similar to Heroku but with usage-based billing (not fixed dyno tiers) and first-class multi-service projects with variable references between services; newer platform, verify current SLA/compliance posture before recommending it for regulated workloads.

## Research First

Confirm current plan tiers, pricing, feature availability, and limits before making a recommendation — all three platforms change pricing and feature sets over time, and static built-in knowledge goes stale. Use `search_vercel_documentation` (MCP) for Vercel, or a web search against the provider's current docs/pricing page for Heroku and Railway, rather than asserting a number or limit from memory.

## Read Before Changing

- multi-cloud rules and provider decision framework: [`../../cloud-architecture/references/provider-selection.md`](../../cloud-architecture/references/provider-selection.md)
- approval rules and cost hotspots: [`../../cloud-architecture/references/approval-policy.md`](../../cloud-architecture/references/approval-policy.md)
- per-provider CLI operations: [`vercel-cli-playbook.md`](./vercel-cli-playbook.md), [`heroku-cli-playbook.md`](./heroku-cli-playbook.md), [`railway-cli-playbook.md`](./railway-cli-playbook.md)
