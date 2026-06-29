#!/usr/bin/env bash
set -euo pipefail

tool_name="${1:-unknown}"

echo "[learning] PreToolUse: ${tool_name}" >&2

if [[ "${tool_name}" == "Write" || "${tool_name}" == "Edit" ]]; then
  echo "[learning] Capturing a lesson: confirm it's generalized (not task-specific). Ask: will this apply in 6 months?" >&2
fi
