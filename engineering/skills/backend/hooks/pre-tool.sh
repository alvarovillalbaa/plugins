#!/usr/bin/env bash
# pre-tool hook for the backend skill.
# Invoked before a tool runs. $1 is the tool name.
# Detects the backend framework/runtime from manifest files and surfaces it so
# work follows the project's existing stack instead of guessing.

set -euo pipefail

TOOL_NAME="${1:-unknown}"

case "$TOOL_NAME" in
    Write|Edit|Bash|bash|Shell|Run|str_replace_editor|create_file) ;;
    *) exit 0 ;;
esac

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
DETECTED=""

add() { DETECTED="${DETECTED:+$DETECTED, }$1"; }

if [ -f "$REPO_ROOT/package.json" ]; then
    PKG="$REPO_ROOT/package.json"
    grep -q '"express"' "$PKG" && add "Express (Node)"
    grep -q '"@nestjs/core"' "$PKG" && add "NestJS (Node)"
    grep -q '"fastify"' "$PKG" && add "Fastify (Node)"
    grep -q '"koa"' "$PKG" && add "Koa (Node)"
    grep -q '"next"' "$PKG" && add "Next.js API routes"
fi

if [ -f "$REPO_ROOT/requirements.txt" ] || [ -f "$REPO_ROOT/pyproject.toml" ]; then
    PYREQ="$REPO_ROOT/requirements.txt"
    PYPROJ="$REPO_ROOT/pyproject.toml"
    for f in "$PYREQ" "$PYPROJ"; do
        [ -f "$f" ] || continue
        grep -qi 'django' "$f" && add "Django (Python)"
        grep -qi 'djangorestframework' "$f" && add "DRF (Python)"
        grep -qi 'fastapi' "$f" && add "FastAPI (Python)"
        grep -qi 'flask' "$f" && add "Flask (Python)"
    done
fi

[ -f "$REPO_ROOT/go.mod" ] && add "Go module"
[ -f "$REPO_ROOT/Cargo.toml" ] && add "Rust/Cargo"
{ [ -f "$REPO_ROOT/pom.xml" ] || [ -f "$REPO_ROOT/build.gradle" ]; } && add "JVM (Maven/Gradle)"
[ -f "$REPO_ROOT/Gemfile" ] && grep -qi 'rails' "$REPO_ROOT/Gemfile" 2>/dev/null && add "Rails (Ruby)"

if [ -n "$DETECTED" ]; then
    echo "[backend] Detected backend stack: $DETECTED" >&2
    echo "[backend] Match existing conventions (routing, validation, error shape) before adding new patterns." >&2
else
    echo "[backend] No backend framework detected from manifests. Confirm the stack before scaffolding." >&2
fi

exit 0
