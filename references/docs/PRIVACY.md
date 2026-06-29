# Privacy And Data Handling

This repository is designed as a local source package for agent skills and
department plugins. It does not transmit data externally by itself.

## Personalization

Personalization must be overlay-only:

- `personalize.local.yml`
- `*.local.yml`
- `.overlays/**`
- `.company/**`
- `.user/**`
- `.generated/**`

Do not commit user, company, customer, credential, local-path, or private
workflow data. Generic placeholders, schemas, templates, examples, and rendering
scripts may go upstream after diff classification.

## Runtime Installs

Runtime folders such as `~/.codex/skills`, `~/.cursor/skills`,
`~/.openclaw/skills`, and Claude plugin/cache paths are install targets, not
source owners. Trace provenance through `.skillmeta.yml` or a lockfile before
using runtime changes as upstream proposals.

## Tools And MCP

Department `mcp.json` files are source declarations. Any actual tool or MCP
server call is controlled by the runtime configuration and user action. Do not
hardcode secrets in this repo.
