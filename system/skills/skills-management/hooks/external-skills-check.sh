#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
while [ "$ROOT" != "/" ] && [ ! -f "$ROOT/scripts/check-external-skills.py" ]; do
  ROOT="$(dirname "$ROOT")"
done

if [ ! -f "$ROOT/scripts/check-external-skills.py" ]; then
  echo "Could not locate scripts/check-external-skills.py from skill hook path." >&2
  exit 1
fi

exec python3 "$ROOT/scripts/check-external-skills.py" --offline "$@"
