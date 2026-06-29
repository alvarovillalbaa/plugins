#!/usr/bin/env bash
# pre-tool hook for the accessibility skill.
# Invoked before a tool runs. $1 is the tool name.
# - Warns when an accessibility audit appears to target a production URL.
# - Checks that axe-core tooling is reachable before audit-style work.

set -euo pipefail

TOOL_NAME="${1:-unknown}"

# Pull the tool input from stdin if a harness provides it; otherwise fall back
# to scanning the environment for a URL the audit might target.
STDIN_PAYLOAD=""
if [ ! -t 0 ]; then
    STDIN_PAYLOAD="$(cat || true)"
fi

CANDIDATE_URLS="$(printf '%s\n%s\n' "$STDIN_PAYLOAD" "${AUDIT_URL:-}" \
    | grep -Eo 'https?://[^"[:space:]]+' || true)"

PROD_PATTERN='(^|[./])(www\.)?(app|api|prod|production|live)\.|\.(com|io|app|dev|co)(/|$)'
LOCAL_PATTERN='(localhost|127\.0\.0\.1|0\.0\.0\.0|\.local|:300[0-9]|:8080|staging|\.test)'

while IFS= read -r url; do
    [ -z "$url" ] && continue
    if echo "$url" | grep -Eq "$LOCAL_PATTERN"; then
        continue
    fi
    if echo "$url" | grep -Eq "$PROD_PATTERN"; then
        echo "[accessibility] WARNING: '$url' looks like a production target." >&2
        echo "[accessibility] Audits inject scripts and generate load. Prefer staging or a local build." >&2
    fi
done <<< "$CANDIDATE_URLS"

# Only enforce tooling for actions that are likely to run an audit.
case "$TOOL_NAME" in
    Bash|bash|Shell|Run)
        if ! command -v node >/dev/null 2>&1; then
            echo "[accessibility] WARNING: node not found; axe-core scans require Node.js." >&2
        elif ! node -e "require.resolve('axe-core')" >/dev/null 2>&1 \
            && ! command -v axe >/dev/null 2>&1; then
            echo "[accessibility] NOTE: axe-core not installed. Install with: npm i -D axe-core @axe-core/cli" >&2
        fi
        ;;
esac

exit 0
