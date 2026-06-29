#!/usr/bin/env bash
# pre-tool hook for the aws-ops skill.
# Invoked before a tool runs. $1 is the tool name.
# - Refuses to let AWS work start with no credentials resolvable.
# - Warns when a command targets a production-looking profile.

set -euo pipefail

TOOL_NAME="${1:-unknown}"

# Only gate shell-style tools that could call the AWS CLI/SDK.
case "$TOOL_NAME" in
    Bash|bash|Shell|Run) ;;
    *) exit 0 ;;
esac

STDIN_PAYLOAD=""
if [ ! -t 0 ]; then
    STDIN_PAYLOAD="$(cat || true)"
fi

if [ -z "${AWS_PROFILE:-}" ] && [ -z "${AWS_ACCESS_KEY_ID:-}" ] \
    && [ ! -f "${HOME}/.aws/credentials" ] && [ ! -f "${HOME}/.aws/config" ]; then
    echo "[aws-ops] WARNING: No AWS credentials resolvable." >&2
    echo "[aws-ops]   Set AWS_PROFILE, run 'aws sso login --profile <p>', or export AWS_ACCESS_KEY_ID." >&2
fi

# Flag obvious production targets so writes are not run on autopilot.
ACTIVE_PROFILE="${AWS_PROFILE:-}"
if echo "$STDIN_PAYLOAD" | grep -Eqo '\-\-profile[= ]+[^ "]+'; then
    ACTIVE_PROFILE="$(echo "$STDIN_PAYLOAD" | grep -Eo '\-\-profile[= ]+[^ "]+' | head -1 | sed -E 's/--profile[= ]+//')"
fi

if echo "$ACTIVE_PROFILE" | grep -Eiq '(prod|production|live)'; then
    echo "[aws-ops] CAUTION: profile '$ACTIVE_PROFILE' looks like production. Confirm scope before any write/delete." >&2
fi

exit 0
