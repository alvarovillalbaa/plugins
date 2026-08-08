#!/usr/bin/env bash
# Update plugins from upstream (origin/main).
# Run from the repo root (plugin directory).

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

# Refuse non-fast-forward source rewrites. Project-local component updates use their
# own no-loss merge engine after this source clone is current.
git pull --ff-only

echo "Source update complete. Refresh a project-local install with:"
echo "  ${REPO_ROOT}/scripts/plugins update --project /path/to/project"
