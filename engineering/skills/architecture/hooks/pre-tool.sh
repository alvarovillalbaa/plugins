#!/usr/bin/env bash
# pre-tool hook for the architecture skill.
# Invoked before a tool runs. $1 is the tool name.
# - Locates an ADR (Architecture Decision Record) directory or suggests one.
# - Surfaces existing architecture docs so new design work builds on them.

set -euo pipefail

TOOL_NAME="${1:-unknown}"
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

# Only run discovery for actions that tend to start design or write work.
case "$TOOL_NAME" in
    Write|Edit|Bash|bash|Shell|Run|str_replace_editor|create_file) ;;
    *) exit 0 ;;
esac

ADR_DIR=""
for candidate in \
    "$REPO_ROOT/docs/adr" \
    "$REPO_ROOT/docs/adrs" \
    "$REPO_ROOT/docs/decisions" \
    "$REPO_ROOT/architecture/decisions" \
    "$REPO_ROOT/adr"; do
    if [ -d "$candidate" ]; then
        ADR_DIR="$candidate"
        break
    fi
done

if [ -n "$ADR_DIR" ]; then
    ADR_COUNT="$(find "$ADR_DIR" -maxdepth 1 -name '*.md' 2>/dev/null | wc -l | tr -d ' ')"
    echo "[architecture] ADR directory: $ADR_DIR ($ADR_COUNT records). Add a new ADR for any non-trivial decision." >&2
else
    echo "[architecture] No ADR directory found. Consider 'docs/adr/' to record design decisions (see templates/)." >&2
fi

# Surface existing architecture docs so work extends them instead of duplicating.
EXISTING_DOCS="$(find "$REPO_ROOT" \
    -maxdepth 3 \
    -type f \
    \( -iname 'architecture*.md' -o -iname 'design*.md' -o -iname 'ARCHITECTURE*' \) \
    -not -path '*/node_modules/*' \
    -not -path '*/.git/*' 2>/dev/null | head -10 || true)"

if [ -n "$EXISTING_DOCS" ]; then
    echo "[architecture] Existing architecture docs to review before designing:" >&2
    echo "$EXISTING_DOCS" | sed 's/^/  - /' >&2
fi

exit 0
