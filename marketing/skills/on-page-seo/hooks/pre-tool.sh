#!/usr/bin/env bash
# on-page-seo pre-tool hook: an on-page audit needs the live page. Remind the
# agent to confirm the URL is reachable and renders the content (not a JS shell)
# before auditing headings, internal links, and snippet readiness.
set -euo pipefail

TOOL_NAME="${1:-unknown}"

case "$TOOL_NAME" in
  WebFetch|Read|Bash)
    cat >&2 <<'MSG'
[on-page-seo/pre-tool] Before the on-page audit:
  - Confirm the URL returns HTTP 200 and the main content is in the HTML
    (server-rendered), not injected by client JS that a crawler may miss.
  - Have the target query / search intent for the page in hand.
  - Capture the current title, meta description, and H1 as the before-state.
MSG
    ;;
esac

exit 0
