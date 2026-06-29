#!/usr/bin/env bash
# pre-tool hook for the web-vuln-validation skill.
# Invoked before a tool runs. $1 is the tool name.
# - Requires an authorization/scope file before web vulnerability testing.
# - Warns when a request targets a host not present in the scope list.

set -euo pipefail

TOOL_NAME="${1:-unknown}"
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

# Gate actions that can issue requests or run tooling.
case "$TOOL_NAME" in
    Bash|bash|Shell|Run|WebFetch|browser_navigate) ;;
    *) exit 0 ;;
esac

STDIN_PAYLOAD=""
if [ ! -t 0 ]; then
    STDIN_PAYLOAD="$(cat || true)"
fi

# Authorization gate.
AUTH_FILE=""
for candidate in \
    "${PENTEST_SCOPE_FILE:-}" \
    "$REPO_ROOT/SCOPE.md" \
    "$REPO_ROOT/SCOPE.txt" \
    "$REPO_ROOT/scope/authorization.md" \
    "$REPO_ROOT/.pentest/scope.md"; do
    [ -n "$candidate" ] && [ -f "$candidate" ] && { AUTH_FILE="$candidate"; break; }
done

if [ -z "$AUTH_FILE" ]; then
    echo "[web-vuln-validation] BLOCKED: no authorization/scope file found." >&2
    echo "[web-vuln-validation] Validating vulnerabilities against a target requires written authorization." >&2
    echo "[web-vuln-validation] See pentest/templates/pentest-scope-document.md." >&2
    exit 2
fi
echo "[web-vuln-validation] Authorized by: $AUTH_FILE" >&2

# Best-effort target scope check using the parent skill's helper if present.
TARGET_URL="$(printf '%s' "$STDIN_PAYLOAD" | grep -Eo 'https?://[^"[:space:]]+' | head -1 || true)"
CHECK="$REPO_ROOT/engineering/skills/pentest/scripts/check_scope.sh"
if [ -n "$TARGET_URL" ] && [ -x "$CHECK" ] && [ -f "$REPO_ROOT/SCOPE.txt" ]; then
    if ! SCOPE_FILE="$REPO_ROOT/SCOPE.txt" "$CHECK" "$TARGET_URL" >/dev/null 2>&1; then
        echo "[web-vuln-validation] WARNING: '$TARGET_URL' may be outside scope. Verify before testing." >&2
    fi
fi

exit 0
