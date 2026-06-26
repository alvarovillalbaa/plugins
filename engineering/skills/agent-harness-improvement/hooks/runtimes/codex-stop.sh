#!/usr/bin/env bash
set -euo pipefail

export AGENT_RUNTIME="codex"
export AGENTIC_DEV_MAX="${AGENTIC_DEV_MAX:-1}"
export AGENTIC_DEV_STATE_DIR="${AGENTIC_DEV_STATE_DIR:-.agentic}"

SCRIPT=".agents/skills/agent-harness-improvement/hooks/check-completion.sh"

if [ ! -x "$SCRIPT" ]; then
  echo "agentic-development hook skipped: $SCRIPT not found or not executable" >&2
  exit 0
fi

exec "$SCRIPT"
