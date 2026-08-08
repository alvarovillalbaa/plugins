#!/usr/bin/env bash
# Validate plugin structure and components.
# From the source root, delegate to the canonical Python validators.
# From a department plugin root, validate the local portable plugin surface.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

if [ -f ".claude-plugin/marketplace.json" ] && [ -f "COMPANY.md" ] && [ -d "scripts" ]; then
  echo "🔍 Validating plugin source root"
  echo ""
  python3 scripts/validate_skills.py .
  exit $?
fi

PLUGIN_NAME="Department Plugin"
if [ -f ".claude-plugin/plugin.json" ]; then
  PLUGIN_NAME=$(python3 - <<'PY'
import json
from pathlib import Path

try:
    print(json.loads(Path(".claude-plugin/plugin.json").read_text()).get("name", "Department Plugin"))
except Exception:
    print("Department Plugin")
PY
)
fi

echo "🔍 Validating $PLUGIN_NAME"
echo ""

ERRORS=0
WARNINGS=0

# Check plugin.json exists
if [ -f ".claude-plugin/plugin.json" ]; then
  echo "✅ Plugin manifest found"
else
  echo "❌ Missing .claude-plugin/plugin.json"
  ERRORS=$((ERRORS + 1))
fi

if [ -f ".codex-plugin/plugin.json" ]; then
  echo "✅ Codex manifest found"
else
  echo "❌ Missing .codex-plugin/plugin.json"
  ERRORS=$((ERRORS + 1))
fi

if [ -f ".cursor-plugin/plugin.json" ]; then
  echo "✅ Cursor manifest found"
else
  echo "❌ Missing .cursor-plugin/plugin.json"
  ERRORS=$((ERRORS + 1))
fi

if [ -f "profile.yaml" ]; then
  echo "✅ Profile found"
else
  echo "❌ Missing profile.yaml"
  ERRORS=$((ERRORS + 1))
fi

# Check skills (only folders with SKILL.md count)
SKILL_COUNT=0
for skill in skills/*/; do
  [ -d "$skill" ] || continue
  [ -f "${skill}SKILL.md" ] && SKILL_COUNT=$((SKILL_COUNT + 1))
done
echo "✅ Found $SKILL_COUNT skills"

# Check commands
CMD_COUNT=$(find commands -maxdepth 1 -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
echo "✅ Found $CMD_COUNT commands"

# Check agents
AGENT_COUNT=$(find agents -maxdepth 1 -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
echo "✅ Found $AGENT_COUNT agents"

# Check department plugin structure
if [ -f "mcp.json" ]; then
  echo "✅ MCP declaration found"
else
  echo "❌ Missing mcp.json"
  ERRORS=$((ERRORS + 1))
fi

if [ -d "rules" ]; then
  echo "✅ Rules directory found"
else
  echo "❌ Missing rules/"
  ERRORS=$((ERRORS + 1))
fi

if [ -d "hooks" ]; then
  if [ -f "hooks/hooks.json" ]; then
    echo "✅ Plugin hook registration found"
  else
    echo "❌ hooks/ exists without hooks/hooks.json"
    ERRORS=$((ERRORS + 1))
  fi
  while IFS= read -r hook_file; do
    case "$hook_file" in
      *.json) ;;
      *)
        echo "❌ Hook handlers belong in scripts/, not $hook_file"
        ERRORS=$((ERRORS + 1))
        ;;
    esac
  done < <(find hooks -type f 2>/dev/null)
fi

if [ -d "scripts" ] && [ ! -d "hooks" ]; then
  echo "❌ Plugin-root scripts/ is reserved for registered hook handlers"
  ERRORS=$((ERRORS + 1))
fi

# Check skill structure: only SKILL.md with name + description required
echo ""
echo "📋 Checking skill structure..."
for skill in skills/*/; do
  [ -d "$skill" ] || continue
  name=$(basename "$skill")

  if [ ! -f "$skill/SKILL.md" ]; then
    echo "  ❌ Missing SKILL.md: $name"
    ERRORS=$((ERRORS + 1))
    continue
  fi

  if grep -q "^name:" "$skill/SKILL.md" && grep -q "^description:" "$skill/SKILL.md"; then
    echo "  ✅ $name"
  else
    echo "  ❌ Missing name/description frontmatter in SKILL.md: $name"
    ERRORS=$((ERRORS + 1))
  fi

  # Optional: references, templates, examples (inform only, no error)
  [ -f "$skill/references.md" ] || [ -d "$skill/references" ] || true
  [ -d "$skill/templates" ] && [ -n "$(ls -A "$skill/templates" 2>/dev/null)" ] || true
  [ -d "$skill/examples" ] && [ -n "$(ls -A "$skill/examples" 2>/dev/null)" ] || true
done

# Summary
echo ""
echo "═══════════════════════════════════════"
if [ $ERRORS -eq 0 ]; then
  if [ -x "${SOURCE_ROOT}/scripts/skillctl.py" ]; then
    echo "✅ Local shell validation passed ($WARNINGS warnings)"
  else
    echo "✅ Validation passed ($WARNINGS warnings)"
  fi
  exit 0
else
  echo "❌ Validation failed ($ERRORS errors, $WARNINGS warnings)"
  exit 1
fi
