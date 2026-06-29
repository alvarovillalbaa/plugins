#!/usr/bin/env bash
# content-led pre-tool hook
# Warns when a content-led strategy is built without SEO or ICP grounding.
# Receives the tool name as $1. Advisory only: never blocks.
set -euo pipefail

TOOL="${1:-}"

case "$TOOL" in
  Write|Edit|MultiEdit|NotebookEdit) ;;
  *) exit 0 ;;
esac

HAS_SEO=0
HAS_ICP=0
find . -maxdepth 4 \( -iname "*keyword*" -o -iname "*seo*" -o -iname "*search-intent*" \) \
     -not -path "*/node_modules/*" -not -path "*/.git/*" -print -quit 2>/dev/null | grep -q . && HAS_SEO=1
find . -maxdepth 4 \( -iname "*icp*" -o -iname "*persona*" -o -iname "*ideal-customer*" \) \
     -not -path "*/node_modules/*" -not -path "*/.git/*" -print -quit 2>/dev/null | grep -q . && HAS_ICP=1

[ "$HAS_SEO" -eq 0 ] && echo "[content-led] No SEO/keyword data found — topic selection may not match search demand." >&2
[ "$HAS_ICP" -eq 0 ] && echo "[content-led] No ICP/persona data found — content may not match buyer intent. See the 'icp' skill." >&2

exit 0
