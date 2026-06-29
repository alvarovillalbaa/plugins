# System Agents

Specialized agents for the system plugin.

## Agents

| Agent | Spawned by | What it does |
|-------|-----------|-------------|
| `memory-analyst.md` | `/si:review` | Read-only analysis of auto-memory. Identifies promotion candidates, stale entries, consolidation opportunities, and conflicts with CLAUDE.md. |
| `skill-extractor.md` | `/si:extract` | Transforms a proven pattern into a portable standalone skill. Generates SKILL.md with proper frontmatter and quality checks. |
| `experiment-runner.md` | `/ar:run`, `/ar:loop` | Autonomous experimenter for the autoresearch loop. Reads experiment state, makes one change, commits, evaluates, keeps or discards. |

## Usage

Agents are spawned by commands via the `Agent` tool — you do not invoke them directly. Use the corresponding slash commands:

```
/si:review      → spawns memory-analyst
/si:extract     → spawns skill-extractor
/ar:run         → spawns experiment-runner (single iteration)
/ar:loop        → spawns experiment-runner (continuous loop)
```

The runner commits and evaluates one changed target through
`system/skills/loops/scripts/run_experiment.py`. It must run on the matching
`autoresearch/{domain}/{name}` branch and refuses unrelated working-tree
changes.
