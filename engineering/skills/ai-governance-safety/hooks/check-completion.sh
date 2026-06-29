#!/usr/bin/env bash
# check-completion hook for the ai-governance-safety skill.
# Runs as a completion gate: scans recently changed / generated files for PII
# before work is considered done. Blocks (nonzero exit) if PII is detected.
#
# Scans git-tracked changes when in a repo; otherwise scans $AI_GOV_OUTPUT_DIR.

set -euo pipefail

SELF_DIR="$(cd "$(dirname "$0")" && pwd)"
SCANNER="$SELF_DIR/../scripts/pii_scanner.py"

# Collect candidate files.
files=()
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    while IFS= read -r f; do
        [ -n "$f" ] && [ -f "$f" ] && files+=("$f")
    done < <(git diff --name-only HEAD 2>/dev/null; git ls-files --others --exclude-standard 2>/dev/null)
elif [ -n "${AI_GOV_OUTPUT_DIR:-}" ] && [ -d "$AI_GOV_OUTPUT_DIR" ]; then
    while IFS= read -r f; do
        files+=("$f")
    done < <(find "$AI_GOV_OUTPUT_DIR" -type f)
fi

if [ "${#files[@]}" -eq 0 ]; then
    echo "[ai-governance] no changed files to scan for PII." >&2
    exit 0
fi

if ! command -v python3 >/dev/null 2>&1 || [ ! -f "$SCANNER" ]; then
    echo "[ai-governance] WARNING: pii_scanner.py unavailable; skipping PII gate." >&2
    exit 0
fi

# Only scan text-like files; skip binaries.
scan_targets=()
for f in "${files[@]}"; do
    if file "$f" 2>/dev/null | grep -qiE 'text|json|xml|csv|empty'; then
        scan_targets+=("$f")
    fi
done

if [ "${#scan_targets[@]}" -eq 0 ]; then
    exit 0
fi

if python3 "$SCANNER" --fail-on-match "${scan_targets[@]}"; then
    echo "[ai-governance] PII gate passed: no PII detected in changed files." >&2
    exit 0
else
    echo "[ai-governance] BLOCKED: potential PII found in output. Redact before completing." >&2
    exit 1
fi
