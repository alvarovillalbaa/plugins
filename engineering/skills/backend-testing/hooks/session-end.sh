#!/usr/bin/env bash
# session-end hook for the backend-testing skill.
# Reports the latest known coverage figure and, if a baseline was recorded,
# the delta — so a session that touched tests leaves a coverage signal.

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$REPO_ROOT" 2>/dev/null || exit 0

extract_total() {
    # Try common coverage report formats; echo a percentage number or nothing.
    local pct=""
    if [ -f coverage/coverage-summary.json ]; then
        pct="$(grep -o '"pct":[0-9.]*' coverage/coverage-summary.json | head -1 | cut -d: -f2)"
    elif [ -f coverage.xml ]; then
        pct="$(grep -o 'line-rate="[0-9.]*"' coverage.xml | head -1 | sed 's/[^0-9.]//g')"
        [ -n "$pct" ] && pct="$(awk -v r="$pct" 'BEGIN{printf "%.1f", r*100}')"
    elif [ -f .coverage ] && command -v coverage >/dev/null 2>&1; then
        pct="$(coverage report 2>/dev/null | awk '/^TOTAL/{gsub("%","",$NF); print $NF}')"
    fi
    echo "$pct"
}

CURRENT="$(extract_total)"
BASELINE_FILE=".backend-testing-coverage-baseline"

if [ -z "$CURRENT" ]; then
    echo "[backend-testing] No coverage report found (looked for coverage-summary.json, coverage.xml, .coverage)." >&2
    exit 0
fi

if [ -f "$BASELINE_FILE" ]; then
    BASELINE="$(cat "$BASELINE_FILE")"
    DELTA="$(awk -v c="$CURRENT" -v b="$BASELINE" 'BEGIN{printf "%+.1f", c-b}')"
    echo "[backend-testing] Coverage: ${CURRENT}% (baseline ${BASELINE}%, delta ${DELTA}pp)" >&2
    if awk -v d="$DELTA" 'BEGIN{exit !(d < 0)}'; then
        echo "[backend-testing] WARNING: coverage decreased this session." >&2
    fi
else
    echo "[backend-testing] Coverage: ${CURRENT}% (no baseline recorded)" >&2
fi

# Record current as the new baseline for next session's delta.
echo "$CURRENT" > "$BASELINE_FILE"
exit 0
