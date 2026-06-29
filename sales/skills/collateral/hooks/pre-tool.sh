#!/usr/bin/env bash
set -euo pipefail

tool_name="${1:-unknown}"

echo "[collateral] PreToolUse: ${tool_name}" >&2

if [[ "${tool_name}" == "Write" || "${tool_name}" == "Edit" ]]; then
  echo "[collateral] Reminder: Brand guidelines and voice profile must be loaded before creating collateral." >&2
  echo "[collateral] Confirm: What is the collateral type? (one-pager, battlecard, case study, deck slide)" >&2
fi
