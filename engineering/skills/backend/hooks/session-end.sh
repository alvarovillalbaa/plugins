#!/usr/bin/env bash
# session-end hook for the backend skill.
# Summarizes backend-relevant changes made this session (routes, models,
# migrations, services) so the next step / reviewer has a quick orientation.

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$REPO_ROOT" 2>/dev/null || exit 0

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    exit 0
fi

CHANGED="$(git status --porcelain 2>/dev/null \
    | awk '{print $2}' \
    | grep -Ei '(route|controller|service|model|schema|migration|api|handler|repository|serializer)' \
    || true)"

echo "[backend] Session summary:" >&2
if [ -n "$CHANGED" ]; then
    echo "$CHANGED" | sed 's/^/  changed: /' >&2
    if echo "$CHANGED" | grep -qi 'migration'; then
        echo "[backend] Migrations touched — confirm they run forward AND backward before shipping." >&2
    fi
    if echo "$CHANGED" | grep -Eqi '(route|controller|api|handler)'; then
        echo "[backend] API surface changed — update contract docs/specs and add/extend tests." >&2
    fi
else
    echo "  no backend-shaped files changed this session" >&2
fi

exit 0
