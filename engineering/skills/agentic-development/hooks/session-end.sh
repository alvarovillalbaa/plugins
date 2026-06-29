#!/usr/bin/env bash
# session-end hook for the agentic-development skill.
# Summarizes the tool-call trace produced by pre-tool.sh into a human-readable
# session summary, so a finished agentic run leaves an auditable record.

set -euo pipefail

TRACE_DIR="${AGENTIC_TRACE_DIR:-${CLAUDE_PROJECT_DIR:-$PWD}/.agentic/traces}"
SESSION_ID="${AGENTIC_SESSION_ID:-${CLAUDE_SESSION_ID:-default}}"
TRACE_FILE="$TRACE_DIR/${SESSION_ID}.jsonl"
SUMMARY_FILE="$TRACE_DIR/${SESSION_ID}.summary.md"

if [ ! -f "$TRACE_FILE" ]; then
    echo "[agentic-dev] no trace found for session '$SESSION_ID'; nothing to summarize." >&2
    exit 0
fi

if command -v python3 >/dev/null 2>&1 && [ -f "$(dirname "$0")/../scripts/trace_agent_session.py" ]; then
    python3 "$(dirname "$0")/../scripts/trace_agent_session.py" \
        --trace "$TRACE_FILE" --format markdown > "$SUMMARY_FILE"
else
    TOTAL="$(wc -l < "$TRACE_FILE" | tr -d ' ')"
    {
        echo "# Agentic Session Summary: $SESSION_ID"
        echo
        echo "- Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
        echo "- Total tool calls: $TOTAL"
        echo
        echo "## Tool usage"
        grep -o '"tool": *"[^"]*"' "$TRACE_FILE" \
            | sed 's/.*"tool": *"//; s/"//' \
            | sort | uniq -c | sort -rn \
            | awk '{printf "- %s: %s\n", $2, $1}'
    } > "$SUMMARY_FILE"
fi

echo "[agentic-dev] session summary written to $SUMMARY_FILE" >&2
exit 0
