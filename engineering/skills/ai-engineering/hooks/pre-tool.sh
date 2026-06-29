#!/usr/bin/env bash
# pre-tool hook for the ai-engineering skill.
# Invoked before a tool runs. $1 is the tool name.
# Warns when AI-provider work is about to run without the expected API keys set,
# so a model call does not fail mid-task with an opaque auth error.

set -euo pipefail

TOOL_NAME="${1:-unknown}"

# Only gate actions that could actually call a provider.
case "$TOOL_NAME" in
    Bash|bash|Shell|Run) ;;
    *) exit 0 ;;
esac

# A provider is "in play" if its SDK env var OR a hint in the project is present.
declare -a MISSING=()

check_key() {
    local label="$1" var="$2"
    if [ -z "${!var:-}" ]; then
        MISSING+=("$label ($var)")
    fi
}

# Detect which providers the project likely uses.
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$PWD}"
USES_ANTHROPIC=0
USES_OPENAI=0
if grep -rqiE '@anthropic-ai|anthropic|claude-' "$PROJECT_DIR" \
    --include='*.json' --include='*.ts' --include='*.js' --include='*.py' \
    2>/dev/null; then
    USES_ANTHROPIC=1
fi
if grep -rqiE 'openai|gpt-4|gpt-3' "$PROJECT_DIR" \
    --include='*.json' --include='*.ts' --include='*.js' --include='*.py' \
    2>/dev/null; then
    USES_OPENAI=1
fi

[ "$USES_ANTHROPIC" -eq 1 ] && check_key "Anthropic" "ANTHROPIC_API_KEY"
[ "$USES_OPENAI" -eq 1 ] && check_key "OpenAI" "OPENAI_API_KEY"

if [ "${#MISSING[@]}" -gt 0 ]; then
    echo "[ai-engineering] WARNING: expected API key(s) not set:" >&2
    for entry in "${MISSING[@]}"; do
        echo "  - $entry" >&2
    done
    echo "[ai-engineering] Export them or load a .env before making model calls." >&2
fi

exit 0
