#!/usr/bin/env bash
set -euo pipefail

tool_name="${1:-unknown}"

echo "[initial] PreToolUse: ${tool_name}" >&2

if [[ "${tool_name}" == "Write" || "${tool_name}" == "Edit" ]]; then
  echo "[initial] Before writing outreach: confirm ICP match score, personalization data (recent activity, company news), and channel (email/LinkedIn/X)." >&2
fi
