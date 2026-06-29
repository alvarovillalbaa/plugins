#!/usr/bin/env bash
# AEO pre-tool hook: before an AEO audit touches a page, remind the agent to
# confirm Schema.org markup exists. Answer engines lean heavily on structured
# data to lift content into featured snippets and AI answers.
set -euo pipefail

TOOL_NAME="${1:-unknown}"

# Only nudge on tools that read/fetch a page or run the audit script.
case "$TOOL_NAME" in
  WebFetch|Read|Bash)
    cat >&2 <<'MSG'
[aeo/pre-tool] Before auditing for answer-engine optimization:
  - Confirm the target page exposes Schema.org JSON-LD (FAQPage, Article, HowTo, Product).
  - Run scripts/check_schema_markup.py <url> to detect JSON-LD blocks and their @type.
  - Missing structured data is the most common reason a page never wins a snippet.
MSG
    ;;
esac

# Advisory only; never block the underlying tool.
exit 0
