# Railway Playbook

## Contents

- Scope and identity
- Command habits
- Discovery and inventory
- Deploy and provision
- Environment variables and secrets
- Databases and plugins
- Domains and environments
- Logs and troubleshooting
- Usage and cost

## Scope and Identity

```bash
railway whoami
railway link
railway status
railway environment
```

Confirm project and environment (`production`, `staging`, per-PR) explicitly with `railway environment` before writing — Railway projects commonly hold several environments side by side, and `railway link` binds the local directory to one project/service/environment combination that's easy to lose track of.

## Command Habits

- Read first with `railway status`, `railway list`, `railway logs`.
- Use `railway variables` to inspect config before `railway variables --set` to avoid clobbering an existing value.
- Confirm the linked service (`railway service`) before any deploy or variable command in multi-service projects — a project can hold several services (web, worker, database) that share a project but not config.

## Discovery and Inventory

```bash
railway list
railway status
railway service
railway variables
railway logs
```

## Deploy and Provision

```bash
railway init
railway link
railway up                 # deploy current directory
railway up --detach        # deploy without streaming logs
railway redeploy           # redeploy the last build
railway rollback <deployment-id>
```

Railway deploys either via `railway up` (CLI push) or GitHub-integration auto-deploy on a connected repo — confirm which one the project already uses. Rollback targets a prior deployment directly, similar to Vercel and Heroku's release rollback.

## Environment Variables and Secrets

```bash
railway variables
railway variables --set KEY=value
railway variables --set KEY=value --service <service>
```

Variables are scoped per environment and per service — set them against the right combination rather than assuming project-wide. Railway also supports variable references (`${{ServiceName.VARIABLE}}`) to wire config between services in the same project without copying secrets manually; prefer that over duplicating a value across services.

## Databases and Plugins

```bash
railway add                       # add a database or plugin (Postgres, MySQL, Redis, Mongo)
railway connect <service>
railway run <command>             # run a command with the linked environment's variables injected
```

Railway provisions managed Postgres/MySQL/Redis/MongoDB as first-class services inside the project, each with its own `DATABASE_URL`-style connection variable auto-injected into dependent services. Confirm backup/snapshot behavior on the current plan before a destructive database operation — Railway's backup guarantees vary by plan tier, unlike Heroku's `pg:backups` which is available on paid Postgres add-ons by default.

## Domains and Environments

```bash
railway domain
railway environment
railway environment new <name>
```

`railway domain` generates a `*.up.railway.app` domain or attaches a custom one. PR/branch environments (when configured) work like Vercel previews and Heroku review apps — prefer them over a hand-maintained staging project.

## Logs and Troubleshooting

```bash
railway logs
railway logs --deployment <deployment-id>
```

Check the deployment's build logs first for failed builds; use `railway logs` (runtime) once a deploy succeeds but the service misbehaves. `railway run <command>` is useful for reproducing a runtime issue locally with the exact environment variables the deployed service would see.

## Usage and Cost

- Railway bills by resource usage (compute, memory, egress) per environment rather than fixed dyno/instance tiers — check current usage (`railway status`, dashboard) before assuming a change is cheap, since cost scales continuously rather than in discrete plan steps.
- Each additional environment (staging, per-PR) multiplies running resource usage — confirm the project's environment count before assuming cost stays flat as environments are added.
- Verify current plan limits and pricing via web search or the Railway docs before committing to a design; pricing model and limits change over time (see the "Research First" note in [`../../cloud-architecture/references/provider-selection.md`](../../cloud-architecture/references/provider-selection.md)).
