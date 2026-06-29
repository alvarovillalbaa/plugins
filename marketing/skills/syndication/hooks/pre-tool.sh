#!/usr/bin/env bash
set -euo pipefail

tool_name="${1:-unknown}"

echo "[syndication] PreToolUse: ${tool_name}" >&2

# Before syndicating, check canonical URL is set
if [[ "${tool_name}" == "Write" || "${tool_name}" == "Edit" ]]; then
  echo "[syndication] Reminder: Canonical URL must be set on the original article before syndicating." >&2
  echo "[syndication] Check: Does the target platform support rel=canonical? (Dev.to ✓, Medium ✓, Hashnode ✓)" >&2
fi
