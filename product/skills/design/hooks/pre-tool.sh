#!/usr/bin/env bash
# design pre-tool hook
# Warns when design work starts without a design brief to anchor it.
# Receives the tool name as $1. Advisory only: never blocks.
set -euo pipefail

TOOL="${1:-}"

case "$TOOL" in
  Write|Edit|MultiEdit|NotebookEdit) ;;
  *) exit 0 ;;
esac

if ! find . -maxdepth 4 \
      \( -iname "*brief*" -o -iname "*prd*" -o -iname "*requirements*" -o -iname "*design-doc*" \) \
      -not -path "*/node_modules/*" -not -path "*/.git/*" -print -quit 2>/dev/null | grep -q .; then
  echo "[design] No design brief / PRD found. Design without a brief drifts from the problem and success criteria." >&2
  echo "[design] Generate or confirm a brief first (see templates/design-brief.md)." >&2
fi

exit 0
