#!/usr/bin/env bash
# cro pre-tool hook
# Warns when CRO analysis runs without accessible analytics/funnel data.
# Receives the tool name as $1. Advisory only: never blocks.
set -euo pipefail

TOOL="${1:-}"

case "$TOOL" in
  Write|Edit|MultiEdit|NotebookEdit) ;;
  *) exit 0 ;;
esac

if ! find . -maxdepth 4 \
      \( -iname "*analytics*" -o -iname "*funnel*" -o -iname "*conversion*" \
         -o -iname "*ga4*" -o -iname "*events*.csv" -o -iname "*sessions*" \) \
      -not -path "*/node_modules/*" -not -path "*/.git/*" -print -quit 2>/dev/null | grep -q .; then
  echo "[cro] No analytics/funnel data found. CRO recommendations should be grounded in real conversion data." >&2
  echo "[cro] Without baselines you cannot size tests or estimate impact — confirm data access first." >&2
fi

exit 0
