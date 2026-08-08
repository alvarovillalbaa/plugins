---
name: ar:setup
description: Create and validate the configuration for one metric-driven autoresearch experiment.
argument-hint: "[domain/experiment-name] [--target PATH] [--eval CMD] [--metric NAME] [--direction lower|higher]"
allowed-tools: [Read, Write, Bash, AskUserQuestion, Skill]
---

Use skill: **loops** — `skills/loops/SKILL.md`.

1. **Resolve the experiment** — Gather a portable slug, one target, objective, constraints, evaluation command, metric name and direction, time budget, and project- or user-scoped storage choice.
2. **Validate prerequisites** — Require a version-controlled project for keep/discard behavior, an existing target, and an evaluator that prints the named numeric metric. Do not initialize or commit a repository unless the user explicitly requests it.
3. **Create state** — Write the experiment under the scope selected by the user. Project scope uses `.autoresearch/<domain>/<name>/`; user scope uses the current runtime's documented user experiment store.
4. **Write the contract** — Create `program.md` with objective, constraints, strategy, and notes; create `config.cfg` with target, evaluation command, metric, direction, and time budget; initialize `results.tsv` with `commit`, `metric`, `status`, and `description` columns.
5. **Protect generated output** — Add only experiment result and log patterns to the nearest applicable ignore file. Preserve existing ignore rules.
6. **Test once** — Run the evaluator, confirm the metric can be parsed, and record the baseline without changing the target.
7. **Deliver** — Report the experiment path, verified evaluation command, baseline, metric direction, constraints, and the exact `ar:run` or `ar:loop` invocation.

## Boundary

This command creates experiment state only. Use `ar:run` for one iteration, `ar:loop` for repeated iterations, and `ar:status` for read-only inspection.
