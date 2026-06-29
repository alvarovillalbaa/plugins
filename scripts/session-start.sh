#!/bin/bash
# Emit team config and house rules if present.

set -euo pipefail

ROOT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
FILES=(
  "$ROOT/.claude/plugins.local.md"
  "$ROOT/.claude/agent-company.local.md"
  "$ROOT/.claude/house-rules.md"
)

for file in "${FILES[@]}"; do
  if [ -f "$file" ]; then
    echo "--- $file ---"
    cat "$file"
    echo
  fi
done
