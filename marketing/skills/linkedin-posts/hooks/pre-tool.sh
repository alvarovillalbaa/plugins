#!/usr/bin/env bash
set -euo pipefail

tool_name="${1:-unknown}"

echo "[linkedin-posts] PreToolUse: ${tool_name}" >&2

# Remind about character limit and hook requirements
if [[ "${tool_name}" == "Write" || "${tool_name}" == "Edit" ]]; then
  echo "[linkedin-posts] Reminder: LinkedIn posts cut off at ~210 chars in feed. First line is the hook." >&2
  echo "[linkedin-posts] Optimal length: 150–300 words. One idea, one CTA." >&2
fi
