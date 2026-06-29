#!/usr/bin/env bash
# pre-tool hook for the azure-ops skill.
# Invoked before a tool runs. $1 is the tool name.
# - Checks the az CLI is present and logged in before Azure work starts.
# - Warns when the active subscription looks like production.

set -euo pipefail

TOOL_NAME="${1:-unknown}"

case "$TOOL_NAME" in
    Bash|bash|Shell|Run) ;;
    *) exit 0 ;;
esac

if ! command -v az >/dev/null 2>&1; then
    echo "[azure-ops] WARNING: az CLI not found. Install: https://learn.microsoft.com/cli/azure/install-azure-cli" >&2
    exit 0
fi

# `az account show` fails fast when no login/identity is available.
if ACCOUNT_JSON="$(az account show --output json 2>/dev/null)"; then
    SUB_NAME="$(echo "$ACCOUNT_JSON" | sed -n 's/.*"name": *"\([^"]*\)".*/\1/p' | head -1)"
    if echo "$SUB_NAME" | grep -Eiq '(prod|production|live)'; then
        echo "[azure-ops] CAUTION: active subscription '$SUB_NAME' looks like production. Confirm scope before any write/delete." >&2
    else
        echo "[azure-ops] Active subscription: ${SUB_NAME:-unknown}" >&2
    fi
else
    echo "[azure-ops] WARNING: not logged in. Run 'az login' (or 'az login --identity' on a managed identity host)." >&2
fi

exit 0
