#!/usr/bin/env bash
# design-systems pre-tool hook
# Warns when component work proceeds without design-system docs/tokens present.
# Receives the tool name as $1. Advisory only: never blocks.
set -euo pipefail

TOOL="${1:-}"

case "$TOOL" in
  Write|Edit|MultiEdit|NotebookEdit) ;;
  *) exit 0 ;;
esac

if ! find . -maxdepth 5 \
      \( -iname "tokens*.json" -o -iname "*design-system*" -o -iname "*tailwind.config*" \
         -o -iname "theme*.*" -o -iname "*tokens*.css" -o -iname "*.stories.*" \) \
      -not -path "*/node_modules/*" -not -path "*/.git/*" -print -quit 2>/dev/null | grep -q .; then
  echo "[design-systems] No design-system source found (tokens, theme, tailwind config, stories)." >&2
  echo "[design-systems] New components should extend existing tokens/patterns, not invent them. Locate the system first." >&2
fi

exit 0
