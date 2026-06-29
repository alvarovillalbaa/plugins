#!/usr/bin/env bash
# Scaffold a dev-loop working directory for an agentic execution run.
# Creates the plan/log/artifact structure the loop reads and writes during
# plan -> code -> test -> verify cycles.
#
# Usage:
#   setup_dev_loop.sh [target-dir]    # defaults to ./.agentic/dev-loop

set -euo pipefail

TARGET="${1:-.agentic/dev-loop}"

if [ -e "$TARGET" ] && [ -n "$(ls -A "$TARGET" 2>/dev/null || true)" ]; then
    echo "Error: '$TARGET' already exists and is not empty. Refusing to overwrite." >&2
    exit 1
fi

mkdir -p "$TARGET"/{plans,logs,artifacts,checkpoints}

cat > "$TARGET/PLAN.md" <<'EOF'
# Dev Loop Plan

## Goal
<One sentence: what "done" looks like.>

## Acceptance criteria
- [ ] <observable, testable condition>

## Stories
1. <smallest shippable slice>
2. <next slice>

## Out of scope
- <explicitly deferred>
EOF

cat > "$TARGET/STATE.json" <<EOF
{
  "created_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "current_story": 1,
  "status": "planned",
  "iterations": 0
}
EOF

cat > "$TARGET/README.md" <<'EOF'
# Dev Loop Workspace

- `PLAN.md` — the source of truth for goal, acceptance criteria, and stories.
- `STATE.json` — machine-readable loop state (current story, status, iterations).
- `plans/` — per-story plan snapshots.
- `logs/` — per-iteration logs (plan, diff, test output, verify result).
- `artifacts/` — generated outputs worth keeping (reports, screenshots).
- `checkpoints/` — known-good states to roll back to.

Each iteration: read PLAN.md -> implement the current story -> run tests ->
verify against acceptance criteria -> update STATE.json -> log the result.
EOF

echo "Dev loop scaffolded at: $TARGET"
echo "Next: edit $TARGET/PLAN.md with the goal and stories."
