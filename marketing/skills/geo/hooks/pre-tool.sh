#!/usr/bin/env bash
# GEO pre-tool hook: before a Generative Engine Optimization audit, remind the
# agent to gather AI-citation signals (does the page already get quoted/cited by
# LLM answer engines, and does it have the quotable structure to be cited).
set -euo pipefail

TOOL_NAME="${1:-unknown}"

case "$TOOL_NAME" in
  WebFetch|WebSearch|Read|Bash)
    cat >&2 <<'MSG'
[geo/pre-tool] Before running a GEO audit:
  - Establish citation baseline: run scripts/check_ai_citations.py "<brand or url>".
  - Verify the page has quotable blocks (statistics, definitions, named claims).
  - Confirm authorship, freshness date, and source links exist (LLMs weight these).
  - GEO without a citation baseline is unmeasurable — capture the before-state first.
MSG
    ;;
esac

exit 0
