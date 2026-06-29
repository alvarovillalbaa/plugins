#!/usr/bin/env bash
# buyer-psychology pre-tool hook
# Warns when psychology analysis is about to run without grounding research.
# Receives the tool name as $1. Advisory only: never blocks.
set -euo pipefail

TOOL="${1:-}"

case "$TOOL" in
  Write|Edit|MultiEdit|NotebookEdit) ;;
  *) exit 0 ;;
esac

if ! find . -maxdepth 4 \
      \( -iname "*customer*research*" -o -iname "*interview*" \
         -o -iname "*voice-of-customer*" -o -iname "*persona*" -o -iname "*survey*" \) \
      -not -path "*/node_modules/*" -not -path "*/.git/*" -print -quit 2>/dev/null | grep -q .; then
  echo "[buyer-psychology] No customer research detected (interviews, personas, VoC, surveys)." >&2
  echo "[buyer-psychology] Motivators/fears/objections are strongest when grounded in real quotes, not assumptions." >&2
fi

exit 0
