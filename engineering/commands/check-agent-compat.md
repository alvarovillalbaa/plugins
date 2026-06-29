---
name: check-agent-compat
description: "Run a full repo compatibility pass — scanner score, docs reliability, startup path, and validation efficiency — and produce a P0/P1/P2 finding list before extending agent autonomy."
argument-hint: "[REPO ROOT]"
allowed-tools: [Agent, Read, Bash]
hide-from-slash-command-tool: "true"
---

# Check Agent Compatibility

Run the four-phase compatibility scan before extending agent autonomy on a repo or starting a long harness loop. Produces a structured finding list with concrete remediation steps.

## What this does

Invokes the `compatibility-scanner` agent to orchestrate four focused passes:

| Pass | What it checks |
|---|---|
| Compatibility scan | All 13 harness dimensions (P0/P1/P2 score) |
| Docs reliability | Setup and run commands verified against actual repo state |
| Startup review | Cold-start bootstrap path — one command to working state |
| Validation efficiency | Local binary gate exists and runs in < 60s |

## Usage

```
/check-agent-compat [repo-root]
```

If `repo-root` is omitted, defaults to `.`.

## Steps

1. Read `$ARGUMENTS` for the repo root, defaulting to `.`.
2. Invoke the compatibility-scanner agent workflow (see `skills/agent-harness/references/agents/compatibility-scanner.yaml`).
3. Emit the unified compatibility report to stdout.
4. If any P0 items were found, stop here — do not start a dev-loop or harness-loop until P0s are resolved.
5. If P1s remain, recommend `/harness-loop` to resolve them before long autonomous passes.

## Output

Structured compatibility report with SCORE SUMMARY and prioritized finding list. See the compatibility-scanner agent for the full output format.

## Reference

- Full audit dimensions and improvement patterns: `skills/agent-harness/references/harness-engineering.md`
- Prioritization order: harness-engineering.md § Prioritization
