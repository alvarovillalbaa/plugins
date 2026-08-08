---
name: ar:run
description: Run a single iteration of an autoresearch experiment. Reads state, decides one change, commits, evaluates, and keeps or discards.
argument-hint: "[domain/experiment-name]"
allowed-tools: [Agent, Read, Bash, Skill]
---

Run one iteration of an autoresearch experiment.

Use skill: **loops** — `skills/loops/SKILL.md`.

## Steps

1. **Validate** — confirm `.autoresearch/{domain}/{name}/config.cfg` exists. If no argument, list available experiments from `.autoresearch/`.

2. **Checkout experiment branch**:
   ```bash
   git checkout autoresearch/{domain}/{name} 2>/dev/null || git checkout -b autoresearch/{domain}/{name}
   ```

3. **Spawn experiment-runner** agent (`agents/experiment-runner.md`) with the experiment path as context.

4. **Runner gate** — the agent must call:
   ```bash
   python system/skills/loops/scripts/run_experiment.py --experiment {domain}/{name} --single --description "<one change>"
   ```
   The runner commits and evaluates only the configured target file, then keeps
   or discards the experiment commit.

5. **Report** — after the agent completes one iteration, show:
   - Result: KEEP / DISCARD / CRASH
   - Metric value and delta from best
   - Commit hash (if kept)
   - Suggestion for next run

To run autonomously in a loop: `/ar:loop {domain}/{name}`

## Boundary

This command runs exactly one configured experiment iteration; it does not create the experiment or start an unattended loop.
