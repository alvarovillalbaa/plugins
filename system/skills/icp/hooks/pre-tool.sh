#!/usr/bin/env bash
set -euo pipefail

tool_name="${1:-unknown}"

echo "[icp] PreToolUse: ${tool_name}" >&2

if [[ "${tool_name}" == "Write" || "${tool_name}" == "Edit" ]]; then
  echo "[icp] Before updating ICP definition: confirm you have data to support the change." >&2
  echo "[icp] ICP changes should be based on won/lost deal analysis, not intuition alone." >&2
fi
