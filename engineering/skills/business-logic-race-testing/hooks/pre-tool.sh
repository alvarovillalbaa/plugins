#!/usr/bin/env bash
# pre-tool hook for the business-logic-race-testing skill.
# Invoked before a tool runs. $1 is the tool name.
# - Confirms a load/concurrency tool is available (k6, wrk, locust, hey, ab).
# - Reminds that this lane requires explicit authorization and a non-prod target.

set -euo pipefail

TOOL_NAME="${1:-unknown}"

case "$TOOL_NAME" in
    Bash|bash|Shell|Run) ;;
    *) exit 0 ;;
esac

FOUND=""
for tool in k6 wrk locust hey ab vegeta; do
    if command -v "$tool" >/dev/null 2>&1; then
        FOUND="${FOUND:+$FOUND }$tool"
    fi
done

if [ -n "$FOUND" ]; then
    echo "[race-testing] Concurrency tools available: $FOUND" >&2
else
    echo "[race-testing] No concurrency tool found. Install one of:" >&2
    echo "[race-testing]   k6 (brew install k6) | wrk | locust (pip install locust) | hey" >&2
    echo "[race-testing]   The bundled scripts/race_detector.sh falls back to curl + xargs if none are present." >&2
fi

echo "[race-testing] REMINDER: only run against systems you are explicitly authorized to test, and prefer staging." >&2
exit 0
