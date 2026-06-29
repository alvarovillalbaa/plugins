#!/usr/bin/env bash
# pre-tool hook for the ai-evals skill.
# Invoked before a tool runs. $1 is the tool name.
# Before an eval run, verifies that a dataset exists and is non-empty, so a run
# does not silently "pass" against zero cases.

set -euo pipefail

TOOL_NAME="${1:-unknown}"

case "$TOOL_NAME" in
    Bash|bash|Shell|Run) ;;
    *) exit 0 ;;
esac

# Read the command/payload if the harness pipes it; only act on eval-like runs.
PAYLOAD=""
if [ ! -t 0 ]; then
    PAYLOAD="$(head -c 4000 || true)"
fi

if ! echo "$PAYLOAD" | grep -qiE 'run_evals|eval|\.jsonl'; then
    exit 0
fi

# Resolve the dataset: explicit env var, --dataset flag in the payload, or default.
DATASET="${EVAL_DATASET:-}"
if [ -z "$DATASET" ]; then
    DATASET="$(echo "$PAYLOAD" | grep -oE -- '--dataset[ =][^ ]+' | head -n1 \
        | sed -E 's/--dataset[ =]//' || true)"
fi
DATASET="${DATASET:-evals/dataset.jsonl}"

if [ ! -f "$DATASET" ]; then
    echo "[ai-evals] WARNING: eval dataset not found: $DATASET" >&2
    echo "[ai-evals] Create it or pass --dataset; an eval with no cases proves nothing." >&2
    exit 0
fi

CASES="$(grep -cve '^[[:space:]]*$' "$DATASET" || true)"
if [ "${CASES:-0}" -eq 0 ]; then
    echo "[ai-evals] WARNING: dataset '$DATASET' has 0 cases." >&2
else
    echo "[ai-evals] dataset OK: $DATASET ($CASES cases)." >&2
fi

exit 0
