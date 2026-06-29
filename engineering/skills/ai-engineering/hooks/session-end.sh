#!/usr/bin/env bash
# session-end hook for the ai-engineering skill.
# Aggregates token-usage records written during the session into a single
# tally, so the cost of an AI-engineering session is visible after it ends.
#
# Producers (SDK wrappers, scripts) should append JSONL lines of the form:
#   {"model":"claude-sonnet-4-6","input_tokens":1200,"output_tokens":340}
# to $AI_USAGE_LOG (default below).

set -euo pipefail

USAGE_LOG="${AI_USAGE_LOG:-${CLAUDE_PROJECT_DIR:-$PWD}/.ai/usage.jsonl}"

if [ ! -f "$USAGE_LOG" ]; then
    echo "[ai-engineering] no token-usage log at $USAGE_LOG; nothing to report." >&2
    exit 0
fi

if command -v python3 >/dev/null 2>&1; then
    python3 - "$USAGE_LOG" >&2 <<'PY'
import json, sys
from collections import defaultdict

path = sys.argv[1]
by_model = defaultdict(lambda: {"in": 0, "out": 0, "calls": 0})
with open(path, encoding="utf-8") as fh:
    for line in fh:
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        m = rec.get("model", "unknown")
        by_model[m]["in"] += int(rec.get("input_tokens", 0))
        by_model[m]["out"] += int(rec.get("output_tokens", 0))
        by_model[m]["calls"] += 1

print("[ai-engineering] Token usage this session:")
total_in = total_out = 0
for model, t in sorted(by_model.items()):
    total_in += t["in"]
    total_out += t["out"]
    print(f"  {model}: {t['calls']} calls, "
          f"{t['in']:,} in / {t['out']:,} out tokens")
print(f"  TOTAL: {total_in:,} in / {total_out:,} out "
      f"({total_in + total_out:,} tokens)")
PY
else
    echo "[ai-engineering] python3 unavailable; raw usage log at $USAGE_LOG" >&2
fi

exit 0
