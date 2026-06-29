#!/usr/bin/env bash
# pre-tool hook for the backend-testing skill.
# Invoked before a tool runs. $1 is the tool name.
# Checks whether a test database is reachable so integration tests don't fail
# halfway through with a confusing connection error.

set -euo pipefail

TOOL_NAME="${1:-unknown}"

case "$TOOL_NAME" in
    Bash|bash|Shell|Run) ;;
    *) exit 0 ;;
esac

# Resolve a test DB URL from the usual env var names.
DB_URL="${TEST_DATABASE_URL:-${DATABASE_URL_TEST:-${DATABASE_URL:-}}}"

if [ -z "$DB_URL" ]; then
    echo "[backend-testing] NOTE: no TEST_DATABASE_URL/DATABASE_URL set." >&2
    echo "[backend-testing]   Integration tests that need a database will fail until one is configured." >&2
    exit 0
fi

# Best-effort reachability check; never block, just warn.
if echo "$DB_URL" | grep -Eq '^postgres'; then
    if command -v pg_isready >/dev/null 2>&1; then
        if pg_isready -d "$DB_URL" >/dev/null 2>&1; then
            echo "[backend-testing] Test Postgres reachable." >&2
        else
            echo "[backend-testing] WARNING: Postgres at TEST_DATABASE_URL not reachable. Start it before integration tests." >&2
        fi
    fi
elif echo "$DB_URL" | grep -Eq '^mysql'; then
    echo "[backend-testing] MySQL test URL detected; ensure the server is up before integration tests." >&2
fi

# Remind to use a *test* database, never the dev/prod one.
if echo "$DB_URL" | grep -Eqv '(test|_test|localhost|127\.0\.0\.1)'; then
    echo "[backend-testing] CAUTION: test DB URL does not look like a dedicated test database. Tests may truncate real data." >&2
fi

exit 0
