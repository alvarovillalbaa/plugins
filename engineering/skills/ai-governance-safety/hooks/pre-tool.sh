#!/usr/bin/env bash
# pre-tool hook for the ai-governance-safety skill.
# Invoked before a tool runs. $1 is the tool name.
# Enforces a declared authorization scope: high-impact actions are blocked
# unless the project ships a scope file that permits them.
#
# Scope file (default .ai-governance/scope.yml or $AI_GOV_SCOPE) lists allowed
# capabilities, one per line, e.g.:
#   allow: filesystem-write
#   allow: network
#   allow: shell

set -euo pipefail

TOOL_NAME="${1:-unknown}"
SCOPE_FILE="${AI_GOV_SCOPE:-${CLAUDE_PROJECT_DIR:-$PWD}/.ai-governance/scope.yml}"

# Map the tool to the capability it exercises.
capability=""
case "$TOOL_NAME" in
    Bash|bash|Shell|Run) capability="shell" ;;
    Write|Edit|NotebookEdit) capability="filesystem-write" ;;
    WebFetch|WebSearch) capability="network" ;;
    *) exit 0 ;;  # read-only / unmapped tools are always allowed
esac

if [ ! -f "$SCOPE_FILE" ]; then
    echo "[ai-governance] WARNING: no scope file at $SCOPE_FILE." >&2
    echo "[ai-governance] '$capability' (via $TOOL_NAME) is unaudited; declare scope to authorize it." >&2
    exit 0
fi

if grep -qE "^[[:space:]]*allow:[[:space:]]*${capability}[[:space:]]*$" "$SCOPE_FILE"; then
    exit 0
fi

echo "[ai-governance] BLOCKED: '$capability' (via $TOOL_NAME) is not in the authorized scope." >&2
echo "[ai-governance] Add 'allow: $capability' to $SCOPE_FILE if this is intended." >&2
exit 1
