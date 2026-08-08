---
name: ar:loop
description: Start an autonomous experiment loop. The experiment-runner agent runs iterations continuously, keeping improvements and discarding failures, until interrupted or the goal is met.
argument-hint: "[domain/experiment-name] [--interval 10m|1h|daily]"
allowed-tools: [Agent, Read, Bash, Skill]
---

Start an autonomous autoresearch loop.

Use skill: **loops** — `skills/loops/SKILL.md`.

## Steps

1. **Validate** — confirm the experiment exists in `.autoresearch/`. If no argument, list available experiments.

2. **Parse interval** (optional):
   - `10m` — run every 10 minutes (active loop)
   - `1h` — run every hour
   - `daily` — run once per day
   - No interval → run continuously until interrupted

3. **Checkout or create experiment branch**:
   ```bash
   git checkout autoresearch/{domain}/{name} 2>/dev/null || git checkout -b autoresearch/{domain}/{name}
   ```

4. **Spawn experiment-runner** agent (`agents/experiment-runner.md`) in loop mode. The agent will run indefinitely until:
   - The user interrupts
   - Context limit is reached (results.tsv and git log persist for the next `/ar:loop` run)
   - The goal in `program.md` is met
   - 5 consecutive crashes

5. **Before spawning** — remind the user:
   - The experiment is running on branch `autoresearch/{domain}/{name}`
   - Results are logged to `.autoresearch/{domain}/{name}/results.tsv`
   - To check progress mid-loop: `/ar:status {domain}/{name}`
   - To pause and review: interrupt, then rerun `/ar:loop {domain}/{name}` to continue

## Safety rules enforced by the agent

- Never modifies the evaluator (`evaluate.py`)
- Never pushes to remote
- Runs only on the matching `autoresearch/{domain}/{name}` branch
- Refuses unrelated working-tree changes
- 5 consecutive crashes → stops automatically
- One change per experiment

## Boundary

This command repeats a configured metric-driven experiment. Use `ar:run` for one iteration, `dev-loop` for general task convergence, and `harness-loop` for repository-harness hardening.
