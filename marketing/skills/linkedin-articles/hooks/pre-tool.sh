#!/usr/bin/env bash
set -euo pipefail

tool_name="${1:-unknown}"

# Before writing a LinkedIn article, verify a brief or topic exists
if [[ "${tool_name}" == "Write" || "${tool_name}" == "Edit" ]]; then
  if [[ -z "${LINKEDIN_ARTICLE_BRIEF:-}" ]]; then
    echo "[linkedin-articles] No article brief set. Recommend confirming: topic, angle, target audience, and CTA before writing." >&2
  fi
fi

echo "[linkedin-articles] PreToolUse: ${tool_name}" >&2
