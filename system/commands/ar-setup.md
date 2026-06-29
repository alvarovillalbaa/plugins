---
name: ar:setup
description: Set up a new autoresearch experiment interactively. Creates the .autoresearch/ directory structure with config, program.md, and optionally a starter evaluator.
argument-hint: "[domain/experiment-name] [--target path] [--eval command] [--metric name] [--direction lower|higher]"
allowed-tools: [Read, Write, Bash, AskUserQuestion]
---

Set up a new autoresearch experiment.

## If arguments are provided

Parse them:
- `--target` — the file to optimize
- `--eval` — the command that outputs a metric (must print `metric_name: value` to stdout)
- `--metric` — the metric name to look for in eval output
- `--direction` — `lower` or `higher` (is lower or higher better?)
- `--scope` — `project` (default, stored in repo) or `user` (stored in `~/.autoresearch/`)

## If arguments are missing

Ask the user:
1. What domain? (engineering / marketing / content / prompts / custom)
2. What experiment name? (slug, lowercase, hyphens)
3. What file to optimize? (the target)
4. How do we measure success? (the evaluation command)
5. What is the metric name in the output?
6. Is lower or higher better?

## What to create

**Project-scoped** (default):
```
.autoresearch/
├── config.yaml
├── .gitignore                    # ignores results.tsv, *.log
└── {domain}/{experiment-name}/
    ├── program.md                # objectives, constraints, strategy
    ├── config.cfg                # target, eval cmd, metric, direction
    └── results.tsv               # experiment log (starts with header row)
```

**config.cfg format:**
```ini
target = src/path/to/file.py
evaluate_cmd = pytest bench.py --tb=no -q
metric = p50_ms
metric_direction = lower
time_budget_minutes = 5
```

**results.tsv header:**
```
commit	metric	status	description
```

**program.md template:**
```markdown
# Experiment: {name}

## Objective
Improve `{metric}` ({direction} is better) for `{target}`.

## Constraints
- Do not change the evaluator
- No new dependencies
- Keep changes to one variable per experiment

## Strategy
- Runs 1-5: Low-hanging fruit (obvious improvements)
- Runs 6-15: Systematic exploration (vary one parameter at a time)
- Runs 16-30: Structural changes (algorithm swaps)
- Runs 30+: Radical experiments (different approaches)

## Notes
[Update after every 10 experiments with what is working and what is not]
```

**.gitignore additions:**
```
.autoresearch/*/results.tsv
.autoresearch/*/*.log
```

## Proactive checks before finishing

- **Verify target exists** — if not, `git init && git add . && git commit -m 'initial'` if needed
- **Test the eval command once** — run it, verify it prints `metric_name: value` to stdout
- **Confirm metric direction** — ask if unclear
- **Check git repo** — experiments require git for keep/discard mechanism

## Output

Report:
1. Experiment created at `.autoresearch/{domain}/{name}/`
2. Eval command verified: [output sample]
3. Metric: `{metric}` ({direction} is better)
4. Ready to run: `/ar:run {domain}/{name}` or `/ar:loop {domain}/{name}`
