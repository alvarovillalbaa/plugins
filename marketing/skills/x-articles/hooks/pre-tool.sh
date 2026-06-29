#!/usr/bin/env bash
set -euo pipefail

tool_name="${1:-unknown}"

echo "[x-articles] PreToolUse: ${tool_name}" >&2

if [[ "${tool_name}" == "Write" || "${tool_name}" == "Edit" ]]; then
  echo "[x-articles] X long-form: 1500–3000 words optimal. Must have a strong first paragraph." >&2
  echo "[x-articles] Structure: Hook → Why this matters → The substance → Takeaways → CTA" >&2
fi
