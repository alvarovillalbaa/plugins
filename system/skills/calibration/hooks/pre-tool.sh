#!/usr/bin/env bash
set -euo pipefail

tool_name="${1:-unknown}"

echo "[calibration] PreToolUse: ${tool_name}" >&2

if [[ "${tool_name}" == "Write" || "${tool_name}" == "Edit" ]]; then
  echo "[calibration] Before modifying calibration settings: confirm which agent/skill is being calibrated and what the observed issue is." >&2
  echo "[calibration] Calibration changes should be traceable — document the 'before' behavior and expected 'after' behavior." >&2
fi
