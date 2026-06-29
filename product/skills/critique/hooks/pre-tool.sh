#!/usr/bin/env bash
# critique pre-tool hook
# Reminds the agent to identify the artifact under critique before writing one.
# Receives the tool name as $1. Advisory only: never blocks.
set -euo pipefail

TOOL="${1:-}"

case "$TOOL" in
  Write|Edit|MultiEdit|NotebookEdit) ;;
  *) exit 0 ;;
esac

if ! find . -maxdepth 4 \
      \( -iname "*brief*" -o -iname "*prd*" -o -iname "*spec*" -o -iname "*.fig" \
         -o -iname "*mock*" -o -iname "*design*" -o -iname "*proposal*" \) \
      -not -path "*/node_modules/*" -not -path "*/.git/*" -print -quit 2>/dev/null | grep -q .; then
  echo "[critique] No obvious artifact found to critique (brief, PRD, spec, mock, design)." >&2
  echo "[critique] Confirm WHAT is being critiqued and against WHICH goal/standard before writing the report." >&2
fi

exit 0
