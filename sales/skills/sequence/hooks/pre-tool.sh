#!/usr/bin/env bash
set -euo pipefail

tool_name="${1:-unknown}"

echo "[sequence] PreToolUse: ${tool_name}" >&2

if [[ "${tool_name}" == "Write" || "${tool_name}" == "Edit" ]]; then
  echo "[sequence] Sequence design checklist:" >&2
  echo "  1. Define the ICP segment this sequence targets" >&2
  echo "  2. Decide the total number of touches (5–8 for cold, 3–4 for warm)" >&2
  echo "  3. Mix channels: email, LinkedIn, phone/text" >&2
  echo "  4. Set a clear exit condition (reply = stop, no reply after touch 6 = pause)" >&2
fi
