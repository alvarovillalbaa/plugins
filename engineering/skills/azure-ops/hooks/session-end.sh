#!/usr/bin/env bash
# session-end hook for the azure-ops skill.
# Appends a record of az CLI operations run this session to a local audit log.

set -euo pipefail

LOG_DIR="${AZURE_OPS_LOG_DIR:-.azure-ops-logs}"
mkdir -p "$LOG_DIR"
LOG_FILE="${LOG_DIR}/azure-operations.log"
STAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

{
    echo "=== session ended ${STAMP} ==="
    if command -v az >/dev/null 2>&1; then
        SUB="$(az account show --query name -o tsv 2>/dev/null || echo 'unknown')"
        echo "subscription: ${SUB}"
    fi
    if [ -n "${HISTFILE:-}" ] && [ -f "$HISTFILE" ]; then
        grep -E '(^| )az ' "$HISTFILE" 2>/dev/null | tail -50 || true
    elif [ -f "${HOME}/.zsh_history" ]; then
        grep -E '(^| )az ' "${HOME}/.zsh_history" 2>/dev/null | tail -50 || true
    elif [ -f "${HOME}/.bash_history" ]; then
        grep -E '(^| )az ' "${HOME}/.bash_history" 2>/dev/null | tail -50 || true
    else
        echo "(no shell history available to scan)"
    fi
    echo ""
} >> "$LOG_FILE"

echo "[azure-ops] Session az operations appended to ${LOG_FILE}" >&2
exit 0
