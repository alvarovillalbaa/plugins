#!/usr/bin/env bash
set -euo pipefail

tool_name="${1:-unknown}"

echo "[loops] PreToolUse: ${tool_name}" >&2

if [[ "${tool_name}" == "Bash" ]]; then
  echo "[loops] Running a loop: confirm branch is an autoresearch branch (autoresearch/{domain}/{name}) to isolate failed experiments." >&2
fi

if [[ "${tool_name}" == "Write" || "${tool_name}" == "Edit" ]]; then
  echo "[loops] Modifying loop state: use .autoresearch/{domain}/{name}/ as state directory. Do not write loop state to working tree." >&2
fi
