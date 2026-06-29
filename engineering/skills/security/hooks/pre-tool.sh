#!/usr/bin/env bash
# pre-tool hook for the security skill (passive review).
# Invoked before a tool runs. $1 is the tool name.
# - This lane is review-only. It blocks anything that looks like active
#   exploitation and steers such work to the `pentest` skill instead.
# - Surfaces dependency manifests and secret-scanning tools for review work.

set -euo pipefail

TOOL_NAME="${1:-unknown}"
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

case "$TOOL_NAME" in
    Bash|bash|Shell|Run) ;;
    *) exit 0 ;;
esac

STDIN_PAYLOAD=""
if [ ! -t 0 ]; then
    STDIN_PAYLOAD="$(cat || true)"
fi

# Passive review must not turn into active attack. Flag offensive tooling.
OFFENSIVE='(sqlmap|nikto|nmap[[:space:]]|nuclei|metasploit|msfconsole|hydra|\bffuf\b|gobuster|wpscan)'
if echo "$STDIN_PAYLOAD" | grep -Eiq "$OFFENSIVE"; then
    echo "[security] BLOCKED: '$TOOL_NAME' invokes offensive tooling, but this is the passive-review lane." >&2
    echo "[security] Active exploitation belongs in the 'pentest' skill with a signed scope. Switch skills." >&2
    exit 2
fi

# Surface dependency manifests for review.
MANIFESTS="$(find "$REPO_ROOT" -maxdepth 3 \
    \( -name 'package.json' -o -name 'requirements*.txt' -o -name 'go.mod' \
       -o -name 'pom.xml' -o -name 'Gemfile' -o -name 'Cargo.toml' \) \
    -not -path '*/node_modules/*' -not -path '*/.git/*' 2>/dev/null | head -8 || true)"
if [ -n "$MANIFESTS" ]; then
    echo "[security] Dependency manifests to review for known-vuln packages:" >&2
    echo "$MANIFESTS" | sed 's/^/  - /' >&2
fi

# Note available audit tooling.
for t in npm pip-audit osv-scanner gitleaks trivy; do
    command -v "$t" >/dev/null 2>&1 && echo "[security] Available: $t" >&2
done

exit 0
