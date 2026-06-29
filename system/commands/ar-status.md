---
name: ar:status
description: Show experiment dashboard — progress, best metric, keep rate, and results table for one or all experiments.
argument-hint: "[domain/experiment-name] or leave blank for all experiments"
allowed-tools: [Read, Bash, Glob]
---

Show the autoresearch experiment dashboard.

## Steps

1. **Find experiments**:
   ```bash
   find .autoresearch -name "results.tsv" | sort
   ```

2. **If a specific experiment is given**, show detailed view:
   ```bash
   cat .autoresearch/{domain}/{name}/results.tsv
   ```
   Then output:
   ```
   Experiment: {domain}/{name}
   Target: {target from config.cfg}
   Metric: {metric} ({direction})
   
   Run  Status   Metric    Delta    Description
   ──────────────────────────────────────────────
   0    baseline 250ms     —        original
   1    keep     230ms     -8.0%    cached db lookups
   2    discard  260ms     +4.0%    batched queries
   ...
   
   Best: {value} (run N, {delta}% from baseline)
   Keep rate: N/M ({percent}%)
   Status: active / paused / done
   ```

3. **If no argument**, show summary across all experiments:
   ```
   DOMAIN          EXPERIMENT       RUNS  KEPT  BEST          Δ FROM START  STATUS
   engineering     api-speed         47    14   185ms         -76.9%        active
   engineering     bundle-size       23     8   412KB         -58.3%        paused
   marketing       medium-ctr        31    11   8.4/10        +68.0%        active
   ```

4. **Offer next action** based on status:
   - `active` → "Continue with `/ar:loop {name}`"
   - `paused` → "Resume with `/ar:loop {name}`"
   - `done` → "View final diff with `git diff autoresearch/{name} main -- {target}`"
