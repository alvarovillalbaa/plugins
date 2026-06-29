#!/usr/bin/env bash
# content router pre-tool hook: before doing content work directly, the router
# should classify the request and delegate to the narrowest child skill.
set -euo pipefail

TOOL_NAME="${1:-unknown}"

cat >&2 <<'MSG'
[content/pre-tool] This is a ROUTER. Before generating content directly:
  - Classify the request (scripts/detect_content_type.py "<request>").
  - Delegate to the narrowest child:
      humanizing | repurposing | syndication | keywords | context-to-content | copywrite
  - Only do work here when no single child owns it.
  - Always start a piece from templates/content-brief.md.
MSG

exit 0
