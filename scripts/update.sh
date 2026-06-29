#!/usr/bin/env bash
# Update plugins from upstream. Detects install context and runs the appropriate update.
# Run from the plugins repo root (e.g. ~/.agent-sources/plugins or ./skills/plugins).

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Not a git repository. Cannot update."
  exit 1
fi

# If we're inside a clone that looks like a plugin dir (has .claude-plugin and agents/), do git pull
if [ -f "${REPO_ROOT}/.claude-plugin/marketplace.json" ] && [ -f "${REPO_ROOT}/COMPANY.md" ]; then
  echo "Detected plugins source clone. Pulling latest..."
  git fetch origin
  git pull origin main
  echo "Update complete. Re-render overlays and reload runtime agents as needed."
  exit 0
fi

if [ -f "${REPO_ROOT}/.claude-plugin/plugin.json" ] && [ -d "${REPO_ROOT}/skills" ]; then
  echo "Detected department plugin install. Pulling latest..."
  git fetch origin
  git pull origin main
  echo "Update complete. Restart or reload the plugin to use the latest version."
  exit 0
fi

# If we're in a bare skills clone (only skills/ matters to the user), still try git pull
if [ -d "${REPO_ROOT}/skills" ]; then
  echo "Detected skills tree. Pulling latest..."
  git fetch origin
  git pull origin main
  echo "Update complete. Restart or reload your runtime (OpenClaw, etc.) if needed."
  exit 0
fi

# Unknown layout: print one-liners for each install method
echo "Could not detect install type. Use one of the following:"
echo ""
echo "  Canonical clone:              cd ~/.agent-sources/plugins && git pull"
echo "  npx skills add:               npx skills add alvarovillalbaa/plugins"
echo "  OpenClaw:                    cd <path-to-clone> && git pull"
exit 1
