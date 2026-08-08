# Vercel Playbook

## Contents

- Scope and identity
- Prefer the MCP tools when available
- Command habits (CLI fallback)
- Discovery and inventory
- Deploy and provision
- Environment variables and secrets
- Domains and previews
- Logs and troubleshooting
- Plans and cost

## Scope and Identity

Confirm team and project scope before writing:

```bash
vercel whoami
vercel teams ls
vercel link
vercel project ls
```

Prefer a scoped, short-lived token (`vercel login`, or a CI-scoped `VERCEL_TOKEN`) over sharing a personal token across environments. Confirm `--scope <team>` explicitly in multi-team accounts.

## Prefer the MCP Tools When Available

When operating on Vercel from inside an agent session, prefer the installed `mcp__claude_ai_Vercel__*` tools over raw CLI calls — they return structured data and avoid shell quoting issues:

- `list_teams`, `list_projects`, `get_project` — discovery, in place of `vercel teams ls` / `vercel project ls`.
- `deploy_to_vercel` — deploys, in place of `vercel deploy` / `vercel --prod`.
- `list_deployments`, `get_deployment`, `get_deployment_build_logs` — deployment status and build logs.
- `get_runtime_logs`, `get_runtime_errors` — production runtime diagnostics, in place of `vercel logs`.
- `get_project_deployment_protection`, `update_project_deployment_protection` — preview/prod access gating.
- `search_vercel_documentation` — use this before assuming current limits, pricing, or feature availability; Vercel's platform changes often enough that built-in knowledge can be stale (see the "Research First" note in [`../../cloud-architecture/references/provider-selection.md`](../../cloud-architecture/references/provider-selection.md)).
- `check_domain_availability_and_price`, `buy_domain`, `get_purchase_quote`, `buy_pro`, `buy_addon`, `buy_credits` are spend-incurring — treat as approval-worthy per [`../../cloud-architecture/references/approval-policy.md`](../../cloud-architecture/references/approval-policy.md) before calling them.

Fall back to the CLI commands below only when the MCP tools are unavailable or the task needs a capability they don't cover.

## Command Habits (CLI Fallback)

- Read first with `vercel project ls`, `vercel ls`, `vercel inspect <deployment>`.
- Use `vercel --prod` deliberately; an unqualified `vercel deploy` creates a preview, not a production deploy.
- Use `vercel env ls` before `vercel env add`/`rm` to avoid clobbering an existing value.
- Pull environment-specific config locally with `vercel env pull` before running the app against production-shaped config.

## Discovery and Inventory

```bash
vercel project ls
vercel ls <project>
vercel inspect <deployment-url>
vercel domains ls
vercel env ls
```

## Deploy and Provision

```bash
vercel link
vercel deploy                 # preview deploy
vercel deploy --prod          # production deploy
vercel rollback <deployment>  # instant rollback to a prior deployment
```

Prefer git-integration deploys (push-to-deploy on the connected repo) for steady-state rollout, and reserve `vercel deploy --prod` for out-of-band or one-off deploys. Every deployment is immutable and independently addressable — rollback is a routing change, not a rebuild, which makes it low-risk.

## Environment Variables and Secrets

```bash
vercel env ls
vercel env add <name> <environment>     # development | preview | production
vercel env rm <name> <environment>
vercel env pull .env.local
```

Scope variables per environment explicitly (`development`/`preview`/`production`) rather than adding one value for all three. Treat production secret changes as requiring a redeploy to take effect and confirm that with the user before assuming it's live.

## Domains and Previews

```bash
vercel domains ls
vercel domains add <domain>
vercel domains inspect <domain>
vercel alias ls
vercel alias set <deployment> <alias>
```

Every PR/branch push on a linked repo gets its own preview deployment and URL by default — use this for review instead of standing up separate staging infrastructure. Treat custom domain and DNS changes as approval-worthy per the parent approval policy.

## Logs and Troubleshooting

```bash
vercel logs <deployment-url>
vercel inspect <deployment-url> --logs
```

Prefer `get_runtime_logs`/`get_runtime_errors` (MCP) or `get_deployment_build_logs` for structured output. Check build logs first for failed deploys; check runtime logs for failures after a deploy succeeds but the app misbehaves.

## Plans and Cost

- Confirm the account plan (Hobby/Pro/Enterprise) before assuming a feature (team seats, protection bypass, advanced analytics, higher function limits) is available.
- Serverless/Edge Function usage, bandwidth, and image optimization are the usual cost drivers past the free tier — flag before enabling anything that scales with traffic.
- `buy_addon`/`buy_pro`/`buy_credits`/domain purchases are real spend — always confirm with the user first.
