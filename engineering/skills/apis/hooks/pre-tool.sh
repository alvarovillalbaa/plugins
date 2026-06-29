#!/usr/bin/env bash
# pre-tool hook for the apis skill.
# Invoked before a tool runs. $1 is the tool name.
# When API design/implementation work is underway, nudges toward a
# spec-first workflow: if the repo has no OpenAPI spec, warn so the contract is
# written before the code drifts from it.

set -euo pipefail

TOOL_NAME="${1:-unknown}"

# Only act on actions that author code/specs.
case "$TOOL_NAME" in
    Write|Edit|NotebookEdit|Bash|bash|Shell|Run) ;;
    *) exit 0 ;;
esac

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$PWD}"

# Look for any OpenAPI/Swagger spec in common locations.
SPEC_FOUND=0
while IFS= read -r candidate; do
    if [ -f "$candidate" ] && grep -qiE 'openapi:|swagger:' "$candidate" 2>/dev/null; then
        SPEC_FOUND=1
        break
    fi
done < <(find "$PROJECT_DIR" \
    -maxdepth 4 \
    \( -name 'openapi.*' -o -name 'swagger.*' -o -name 'api.yaml' -o -name 'api.yml' \) \
    -not -path '*/node_modules/*' -not -path '*/.git/*' 2>/dev/null)

if [ "$SPEC_FOUND" -eq 0 ]; then
    echo "[apis] NOTE: no OpenAPI/Swagger spec found under $PROJECT_DIR." >&2
    echo "[apis] Prefer spec-first: define the contract (openapi.yaml) before or" >&2
    echo "[apis] alongside the implementation so request/response shapes stay authoritative." >&2
fi

exit 0
