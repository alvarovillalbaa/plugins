#!/usr/bin/env bash
# technical-seo pre-tool hook: a technical audit is meaningless if crawlers
# can't reach the site. Remind the agent to confirm crawlability fundamentals
# (robots.txt, status codes, sitemap) before the deeper audit.
set -euo pipefail

TOOL_NAME="${1:-unknown}"

case "$TOOL_NAME" in
  WebFetch|WebSearch|Bash)
    cat >&2 <<'MSG'
[technical-seo/pre-tool] Before the technical SEO audit, confirm crawlability:
  - robots.txt exists and does not block important paths (Disallow: /).
  - Homepage + key templates return 200 (not 4xx/5xx, no redirect chains).
  - sitemap.xml exists, is referenced in robots.txt, and is fresh.
  - You know the canonical host (apex vs www) and HTTPS is enforced.
  A blocked or unreachable site invalidates every downstream finding.
MSG
    ;;
esac

exit 0
