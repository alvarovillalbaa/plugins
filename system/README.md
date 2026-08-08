# System

Owns plugins management, skill evaluation, durable memory, knowledge bases, lessons, brain ingestion, personalization, evidence-backed work explanations, and repeatable improvement loops.

Use the narrowest owner:

- `memory` discovers available stores, retrieves scoped prior context with provenance and freshness checks, and gates every write, promotion, or deletion.
- `explain-yourself` produces plan, status, decision, handoff, and postmortem explanations from observable actions and evidence without exposing hidden chain-of-thought.
- `plugins-management`, `learning`, `brain`, `personalize`, and `loops` route their established maintenance lanes.

Department-wide routing and safety policy lives in [`rules/defaults.md`](rules/defaults.md).

## Agents

| Agent | Spawned by | What it does |
|-------|-----------|-------------|
| `system-steward.md` | Direct multi-surface requests | Coordinates plugin maintenance, knowledge flows, personalization policy, evaluation, and improvement, then hands narrow work to the command-bound specialists below. |
| `memory-analyst.md` | `/si:review` | Read-only analysis of one explicitly scoped memory store. Identifies provenance-rich promotion candidates, stale claims, consolidation opportunities, and policy conflicts. |
| `skill-extractor.md` | `/si:extract` | Transforms a proven pattern into a portable standalone skill. Generates SKILL.md with proper frontmatter and quality checks. |
| `experiment-runner.md` | `/ar:run`, `/ar:loop` | Autonomous experimenter for the autoresearch loop. Reads experiment state, makes one change, commits, evaluates, keeps or discards. |

The command-bound specialist agents are spawned via the `Agent` tool. The
system steward is the direct route for work that genuinely spans multiple
system capabilities. The experiment runner uses
`skills/loops/scripts/run_experiment.py`, requires the matching
`autoresearch/{domain}/{name}` branch, and refuses unrelated working-tree
changes.
