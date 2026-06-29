#!/bin/bash
# Logs engineering metrics analysis commands
# Usage: log-metrics.sh <command>

COMMAND="$1"
LOG_DIR="${HOME}/.claude/agent-company/logs"
LOG_FILE="${LOG_DIR}/metrics-analysis.log"

# Create log directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Only log git-related commands that indicate metrics analysis
if [[ "$COMMAND" =~ (git\ log|git\ diff|git\ shortlog|git\ blame) ]]; then
  TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
  echo "[$TIMESTAMP] Metrics analysis: $COMMAND" >> "$LOG_FILE"
fi

exit 0
