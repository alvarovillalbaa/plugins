#!/usr/bin/env bash
set -euo pipefail

tool_name="${1:-unknown}"

echo "[personalize] PreToolUse: ${tool_name}" >&2

# Personalize is a router — remind to delegate to the correct child skill
if [[ "${tool_name}" == "Write" || "${tool_name}" == "Edit" ]]; then
  echo "[personalize] Router reminder: delegate to the correct child skill." >&2
  echo "  - communication-style → tone, register, formality preferences" >&2
  echo "  - voice → brand voice, writing style, vocabulary" >&2
  echo "  - calibration → adjusting agent/skill behavior" >&2
  echo "  - positioning → how product is framed for market segments" >&2
  echo "  - icp → ideal customer profile definition and scoring" >&2
fi
