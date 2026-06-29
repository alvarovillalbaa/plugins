#!/usr/bin/env bash
set -euo pipefail

tool_name="${1:-unknown}"

echo "[x-dms] PreToolUse: ${tool_name}" >&2

if [[ "${tool_name}" == "Write" || "${tool_name}" == "Edit" ]]; then
  echo "[x-dms] X DM limits: 300 chars for connection message, ~1000 chars in DM. Keep it tight." >&2
  echo "[x-dms] Confirm: Is there a genuine signal to reference? (post they wrote, reply they left, thread context)" >&2
fi
