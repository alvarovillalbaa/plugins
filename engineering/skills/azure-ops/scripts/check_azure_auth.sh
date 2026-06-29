#!/usr/bin/env bash
# Verify az CLI login status and report the active subscription/identity.
# Exit codes: 0 = logged in, 1 = az CLI missing, 2 = not logged in.
#
# Usage:
#   ./check_azure_auth.sh
#   ./check_azure_auth.sh --json

set -euo pipefail

JSON=0
[ "${1:-}" = "--json" ] && JSON=1

if ! command -v az >/dev/null 2>&1; then
    echo "ERROR: az CLI not found. Install: https://learn.microsoft.com/cli/azure/install-azure-cli" >&2
    exit 1
fi

if ACCOUNT_JSON="$(az account show --output json 2>/dev/null)"; then
    if [ "$JSON" -eq 1 ]; then
        echo "$ACCOUNT_JSON"
    else
        NAME="$(echo "$ACCOUNT_JSON" | sed -n 's/.*"name": *"\([^"]*\)".*/\1/p' | head -1)"
        SUB_ID="$(echo "$ACCOUNT_JSON" | sed -n 's/.*"id": *"\([^"]*\)".*/\1/p' | head -1)"
        TENANT="$(echo "$ACCOUNT_JSON" | sed -n 's/.*"tenantId": *"\([^"]*\)".*/\1/p' | head -1)"
        USER="$(echo "$ACCOUNT_JSON" | sed -n 's/.*"user": *{[^}]*"name": *"\([^"]*\)".*/\1/p' | head -1)"
        echo "Logged in."
        echo "  Subscription: ${NAME}"
        echo "  Sub ID:       ${SUB_ID}"
        echo "  Tenant:       ${TENANT}"
        echo "  Identity:     ${USER:-managed-identity}"
    fi
    exit 0
fi

echo "NOT logged in. Try one of:" >&2
echo "  az login                 # interactive" >&2
echo "  az login --use-device-code" >&2
echo "  az login --identity      # on a host with managed identity" >&2
echo "  az login --service-principal -u <app-id> -p <secret> --tenant <tenant>" >&2
exit 2
