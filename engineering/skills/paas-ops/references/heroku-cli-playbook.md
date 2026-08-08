# Heroku Playbook

## Contents

- Scope and identity
- Command habits
- Discovery and inventory
- Deploy and provision
- Config vars and secrets
- Add-ons (databases, caches, logging)
- Domains and review apps
- Logs and troubleshooting
- Dynos and cost

## Scope and Identity

```bash
heroku auth:whoami
heroku apps
heroku apps:info -a <app>
heroku access -a <app>
```

Prefer team-scoped API keys or `heroku authorizations:create` for CI over sharing a personal login. Confirm `-a <app>` explicitly — Heroku has no strong per-repo binding beyond the local git remote, so it's easy to target the wrong app.

## Command Habits

- Read first with `heroku apps:info`, `heroku ps`, `heroku config`.
- Use `-a <app>` (or `--app`) on every command in multi-app accounts rather than relying on the current directory's git remote.
- Prefer the Heroku Platform API or `heroku config` over editing environment values through the dashboard, so changes stay scriptable and auditable.
- Use `heroku releases` to see the deploy/config history before rolling back.

## Discovery and Inventory

```bash
heroku apps
heroku apps:info -a <app>
heroku ps -a <app>
heroku addons -a <app>
heroku config -a <app>
heroku releases -a <app>
heroku domains -a <app>
```

## Deploy and Provision

```bash
heroku create <app-name> --team <team>
git push heroku main
heroku releases:rollback <version> -a <app>
heroku ps:scale web=1:standard-1x -a <app>
```

Heroku deploys via `git push` to the `heroku` remote (or a connected GitHub repo with automatic deploys) — confirm which path the repo already uses before introducing a second one. `heroku releases:rollback` is fast and low-risk; prefer it over a forward-fix for a bad deploy that needs to be reverted immediately.

## Config Vars and Secrets

```bash
heroku config -a <app>
heroku config:set KEY=value -a <app>
heroku config:unset KEY -a <app>
```

Setting a config var triggers a restart of all dynos by default — treat this as a deploy-equivalent event for production apps, not a free-standing change. Do not print full config output containing secrets into shared logs.

## Add-ons (Databases, Caches, Logging)

```bash
heroku addons -a <app>
heroku addons:create heroku-postgresql:standard-0 -a <app>
heroku addons:create heroku-redis:premium-0 -a <app>
heroku pg:info -a <app>
heroku pg:backups:capture -a <app>
heroku pg:backups:restore <backup> DATABASE_URL -a <app>
```

Heroku Postgres and Heroku Redis are the default managed data services — Heroku itself does not run raw compute you provision separately. Always capture a backup (`pg:backups:capture`) before a plan change, restore, or fork on a database with real data. `heroku pg:promote` changes which add-on `DATABASE_URL` points to — treat it as approval-worthy in production.

## Domains and Review Apps

```bash
heroku domains -a <app>
heroku domains:add www.example.com -a <app>
heroku pipelines:info <pipeline>
```

Review apps (one ephemeral app per PR, via a configured pipeline) are the Heroku equivalent of Vercel/Railway preview deploys — use them instead of hand-rolled staging apps when the repo has a pipeline configured. Treat custom domain and DNS changes as approval-worthy per the parent approval policy.

## Logs and Troubleshooting

```bash
heroku logs -a <app> --tail
heroku logs -a <app> --source app
heroku ps -a <app>
heroku run bash -a <app>
```

Check `heroku ps` first for crashed/restarting dynos before digging into logs. `heroku run` starts a one-off dyno for debugging — remember it bills separately and does not share state with running web/worker dynos.

## Dynos and Cost

- Dyno type and count are the primary cost driver — confirm the plan (Eco/Basic/Standard/Performance) before assuming autoscaling or zero-downtime deploys are available.
- Add-on plan tiers (especially Postgres/Redis) often cost more than the dynos themselves at scale — check `heroku addons` pricing before recommending a tier bump.
- Eco/free-tier dynos sleep after inactivity; do not use them for anything expected to serve traffic reliably.
