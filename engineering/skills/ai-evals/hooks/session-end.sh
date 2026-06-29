#!/usr/bin/env bash
# session-end hook for the ai-evals skill.
# Archives the latest eval results into a timestamped history directory and
# prints a one-line headline, so each eval session leaves a comparable record.

set -euo pipefail

RESULTS_FILE="${EVAL_RESULTS_FILE:-${CLAUDE_PROJECT_DIR:-$PWD}/evals/results.json}"
HISTORY_DIR="${EVAL_HISTORY_DIR:-${CLAUDE_PROJECT_DIR:-$PWD}/evals/history}"

if [ ! -f "$RESULTS_FILE" ]; then
    echo "[ai-evals] no results at $RESULTS_FILE; nothing to archive." >&2
    exit 0
fi

mkdir -p "$HISTORY_DIR"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
ARCHIVE="$HISTORY_DIR/results-${STAMP}.json"
cp "$RESULTS_FILE" "$ARCHIVE"

if command -v python3 >/dev/null 2>&1; then
    python3 - "$RESULTS_FILE" "$ARCHIVE" >&2 <<'PY'
import json, sys
results_path, archive = sys.argv[1], sys.argv[2]
try:
    data = json.load(open(results_path, encoding="utf-8"))
except (json.JSONDecodeError, OSError) as exc:
    print(f"[ai-evals] archived to {archive} (could not parse summary: {exc})")
    sys.exit(0)
s = data.get("summary", data)
total = s.get("total", "?")
passed = s.get("passed", "?")
acc = s.get("accuracy")
acc_str = f", accuracy={acc:.1%}" if isinstance(acc, (int, float)) else ""
print(f"[ai-evals] archived to {archive} — {passed}/{total} passed{acc_str}")
PY
else
    echo "[ai-evals] results archived to $ARCHIVE" >&2
fi

exit 0
