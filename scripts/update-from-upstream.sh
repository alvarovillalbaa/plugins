#!/usr/bin/env bash
# Update plugins from upstream (origin/main).
# Run from the repo root (plugin directory).
# Optionally creates a backup of the current state before pulling.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Not a git repository. Cannot update."
  exit 1
fi

# Optional: backup current branch name and commit
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || true)
echo "Current branch: ${BRANCH:-unknown}"

# Fetch and pull
git fetch origin
git pull origin main

echo "Update complete. Restart Claude Code or reload the plugin to use the latest version."
