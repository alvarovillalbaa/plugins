---
name: cancel-dev-loop
description: "Cancel an active agentic development loop by removing its state file."
allowed-tools: ["Bash(test -f .agentic/agentic-dev-loop.local.md:*)", "Bash(test -f .claude/agentic-dev-loop.local.md:*)", "Bash(rm .agentic/agentic-dev-loop.local.md)", "Bash(rm .claude/agentic-dev-loop.local.md)", "Read(.agentic/agentic-dev-loop.local.md)", "Read(.claude/agentic-dev-loop.local.md)"]
hide-from-slash-command-tool: "true"
---

# Cancel Dev Loop

1. Check if an active loop exists:
   ```bash
   test -f .agentic/agentic-dev-loop.local.md && echo "EXISTS" || \
     test -f .claude/agentic-dev-loop.local.md && echo "LEGACY_EXISTS" || echo "NOT_FOUND"
   ```

2. **If NOT_FOUND**: say "No active dev loop found."

3. **If EXISTS or LEGACY_EXISTS**:
   - Prefer `.agentic/agentic-dev-loop.local.md`; fall back to legacy `.claude/agentic-dev-loop.local.md`.
   - Read the state file to get the current `iteration:` value from the frontmatter.
   - Remove the state file:
     ```bash
     STATE_FILE=.agentic/agentic-dev-loop.local.md
     test -f "$STATE_FILE" || STATE_FILE=.claude/agentic-dev-loop.local.md
     rm "$STATE_FILE"
     ```
   - Report: "Cancelled agentic dev loop (was at iteration N)."
