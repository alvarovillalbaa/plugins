---
name: harness-loop
description: "Run a harness engineering improvement loop — audits the repo each iteration, picks the highest-priority finding, enforces it as a CI gate or structural test, and stops when no P0 or P1 findings remain."
argument-hint: "[REPO ROOT or scope] [--max-iterations N]"
allowed-tools: ["Bash(${CLAUDE_PLUGIN_ROOT}/skills/agent-harness-improvement/scripts/setup-dev-loop.sh:*)", "Bash", "Read"]
hide-from-slash-command-tool: "true"
---

# Harness Loop

Initialize a structured harness engineering loop. Determine the repo root from `$ARGUMENTS` or default to `.`, then run:

```!
"${CLAUDE_PLUGIN_ROOT}/skills/agent-harness-improvement/scripts/setup-dev-loop.sh" \
  "Improve the agentic harness for this repo. Each iteration: run the harness audit, pick the highest-priority P0 or P1 finding, implement it as an enforced rule (CI gate, linter, structural test, or subsystem AGENTS.md), verify the enforcement actually catches the problem, commit the change. Stop only when a fresh harness audit shows zero P0 and P1 items." \
  --completion-promise "NO_P0_P1_FINDINGS" \
  --verify-cmd "python ${CLAUDE_PLUGIN_ROOT}/skills/agent-harness-improvement/scripts/harness_audit.py ." \
  $ARGUMENTS
```

## Harness loop discipline per iteration

1. **Audit** — run `harness_audit.py` to get the current findings list. Do not skip this step.
2. **P0 first, then P1** — never skip a higher-priority finding to work on a lower one.
3. **Enforce, don't just document** — prefer CI gates, linters, and structural tests over prose updates alone. Documentation can describe the rule; CI must reject the violation.
4. **Verify the enforcement** — confirm the new gate actually catches the problem class it was designed for (e.g., write a test that would fail without the gate).
5. **Commit and record** — commit with a conventional message; include the resolved finding dimension in the commit body.
6. **Re-audit before declaring done** — run the audit again before the next iteration to confirm the finding is resolved and no regressions were introduced.

## Completion criterion

Output `<promise>NO_P0_P1_FINDINGS</promise>` only when a fresh harness audit reports zero P0 and zero P1 findings. P2 and P3 items may remain open.

## Reference

Read `skills/agent-harness-improvement/references/harness-engineering.md` for the full audit dimensions, improvement patterns, and prioritization framework.
