#!/usr/bin/env bash
# pre-tool hook for the agentic-development skill.
# Invoked before a tool runs. $1 is the tool name.
# Appends a structured trace line per tool call so an agentic dev session can
# be reconstructed and analyzed later (see scripts/trace_agent_session.py).

set -euo pipefail

TOOL_NAME="${1:-unknown}"

TRACE_DIR="${AGENTIC_TRACE_DIR:-${CLAUDE_PROJECT_DIR:-$PWD}/.agentic/traces}"
mkdir -p "$TRACE_DIR"

SESSION_ID="${AGENTIC_SESSION_ID:-${CLAUDE_SESSION_ID:-default}}"
TRACE_FILE="$TRACE_DIR/${SESSION_ID}.jsonl"
TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Capture tool input if the harness pipes it on stdin (kept short).
PAYLOAD=""
if [ ! -t 0 ]; then
    PAYLOAD="$(head -c 2000 || true)"
fi

# Emit one JSON line. Use python for safe escaping if available, else degrade.
if command -v python3 >/dev/null 2>&1; then
    python3 - "$TS" "$TOOL_NAME" "$PAYLOAD" >> "$TRACE_FILE" <<'PY'
import json, sys
ts, tool, payload = sys.argv[1], sys.argv[2], sys.argv[3]
print(json.dumps({"ts": ts, "event": "pre_tool", "tool": tool,
                  "input_preview": payload[:500]}))
PY
else
    printf '{"ts":"%s","event":"pre_tool","tool":"%s"}\n' "$TS" "$TOOL_NAME" >> "$TRACE_FILE"
fi

exit 0
