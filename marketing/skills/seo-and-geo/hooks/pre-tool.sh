#!/usr/bin/env bash
# seo-and-geo pre-tool hook: the 5-phase LLM SEO workflow assumes the target
# site is reachable. Remind the agent to confirm accessibility and capture a
# baseline before running phases (core SEO, LLM files, structured data, agent
# discovery, AI-referrer measurement).
set -euo pipefail

TOOL_NAME="${1:-unknown}"

case "$TOOL_NAME" in
  WebFetch|WebSearch|Bash)
    cat >&2 <<'MSG'
[seo-and-geo/pre-tool] Before the 5-phase LLM SEO workflow:
  Phase 0 (baseline) checklist:
    - Site responds (HTTP 200) and is crawlable (robots.txt not blocking).
    - You have the canonical domain (www vs apex) settled.
    - Capture current organic + AI-referrer baseline before changing anything.
  Then run, in order:
    1. core SEO   2. llms.txt / llms-full.txt   3. structured data
    4. agent discovery (agent-card.json, OpenAPI, MCP)   5. AI-referrer measurement
  Helpers: scripts/generate_llms_txt.py, scripts/check_ai_discovery.py
MSG
    ;;
esac

exit 0
