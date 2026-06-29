#!/usr/bin/env bash
set -euo pipefail

tool_name="${1:-unknown}"

echo "[lessons] PreToolUse: ${tool_name}" >&2

if [[ "${tool_name}" == "Write" || "${tool_name}" == "Edit" ]]; then
  echo "[lessons] Adding a lesson: ensure it has an ID, category, and generalized form." >&2
  echo "[lessons] Lessons must be durable — remove any time-specific or person-specific details." >&2
fi
