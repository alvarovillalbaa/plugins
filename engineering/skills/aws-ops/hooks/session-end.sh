#!/usr/bin/env bash
# session-end hook for the aws-ops skill.
# Appends a record of AWS CLI commands run this session to a local audit log,
# so cloud-touching work leaves a reviewable trail.

set -euo pipefail

LOG_DIR="${AWS_OPS_LOG_DIR:-.aws-ops-logs}"
mkdir -p "$LOG_DIR"
LOG_FILE="${LOG_DIR}/aws-commands.log"
STAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

{
    echo "=== session ended ${STAMP} ==="
    # Best-effort extraction of aws commands from shell history if available.
    if [ -n "${HISTFILE:-}" ] && [ -f "$HISTFILE" ]; then
        grep -E '(^| )aws ' "$HISTFILE" 2>/dev/null | tail -50 || true
    elif [ -f "${HOME}/.zsh_history" ]; then
        grep -E '(^| )aws ' "${HOME}/.zsh_history" 2>/dev/null | tail -50 || true
    elif [ -f "${HOME}/.bash_history" ]; then
        grep -E '(^| )aws ' "${HOME}/.bash_history" 2>/dev/null | tail -50 || true
    else
        echo "(no shell history available to scan)"
    fi
    echo ""
} >> "$LOG_FILE"

echo "[aws-ops] Session AWS commands appended to ${LOG_FILE}" >&2
exit 0
