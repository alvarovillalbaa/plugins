#!/usr/bin/env bash
# Verify AWS authentication is configured and report the resolved identity.
# Exit codes: 0 = authenticated, 1 = aws CLI missing, 2 = not authenticated.
#
# Usage:
#   ./check_aws_credentials.sh
#   ./check_aws_credentials.sh --profile my-dev
#   ./check_aws_credentials.sh --json

set -euo pipefail

PROFILE_ARG=()
JSON=0
for arg in "$@"; do
    case "$arg" in
        --profile) shift; PROFILE_ARG=(--profile "${1:-}");;
        --profile=*) PROFILE_ARG=(--profile "${arg#*=}");;
        --json) JSON=1;;
    esac
done

if ! command -v aws >/dev/null 2>&1; then
    echo "ERROR: aws CLI not found. Install: https://docs.aws.amazon.com/cli/" >&2
    exit 1
fi

if ID_JSON="$(aws sts get-caller-identity "${PROFILE_ARG[@]}" --output json 2>/dev/null)"; then
    if [ "$JSON" -eq 1 ]; then
        echo "$ID_JSON"
    else
        ACCOUNT="$(echo "$ID_JSON" | sed -n 's/.*"Account": *"\([^"]*\)".*/\1/p')"
        ARN="$(echo "$ID_JSON" | sed -n 's/.*"Arn": *"\([^"]*\)".*/\1/p')"
        echo "Authenticated."
        echo "  Account: ${ACCOUNT}"
        echo "  ARN:     ${ARN}"
        echo "  Profile: ${AWS_PROFILE:-${PROFILE_ARG[*]:-default}}"
        echo "  Region:  ${AWS_REGION:-${AWS_DEFAULT_REGION:-$(aws configure get region "${PROFILE_ARG[@]}" 2>/dev/null || echo unset)}}"
    fi
    exit 0
fi

echo "NOT authenticated. Try one of:" >&2
echo "  aws sso login --profile <profile>" >&2
echo "  export AWS_PROFILE=<profile>" >&2
echo "  export AWS_ACCESS_KEY_ID=... AWS_SECRET_ACCESS_KEY=..." >&2
exit 2
