#!/usr/bin/env bash
# keywords pre-tool hook: keyword research depends on a data source. Remind the
# agent which providers are wired up (Ahrefs MCP / GSC) and to fall back to
# SERP + PAA scraping when no API is available — never invent volume numbers.
set -euo pipefail

TOOL_NAME="${1:-unknown}"

case "$TOOL_NAME" in
  WebFetch|WebSearch|Bash)
    cat >&2 <<'MSG'
[keywords/pre-tool] Before keyword research, confirm a data source:
  - Ahrefs MCP tools (keywords-explorer-*, gsc-keywords) — preferred for volume/difficulty.
  - Google Search Console — for existing-ranking and query data.
  - If neither is available: use SERP + "People Also Ask" + autocomplete and
    clearly label metrics as ESTIMATED. Do NOT fabricate exact volume numbers.
  Capture seed terms, target geo, and language before pulling data.
MSG
    ;;
esac

exit 0
