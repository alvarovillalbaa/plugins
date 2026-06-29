---
name: loops
description: Run and maintain repeatable improvement, evaluation, memory, and experimentation loops.
---

# Loops

Use this skill for the named lane in the current taxonomy. Route to sibling skills when the request crosses ownership boundaries, and preserve local rules over external guidance when they conflict.

Autoresearch-style loops use `.autoresearch/{domain}/{name}/` state plus
`system/skills/loops/scripts/run_experiment.py`. Run them on matching
`autoresearch/{domain}/{name}` branches so failed experiments can be discarded
without touching unrelated work.

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `codex-loop`: Run Codex PRD/story loops with one fresh subagent per story. Install: `python scripts/install-external-skills.py --skill codex-loop --agent codex`.
- `claude-loop`: Run Claude PRD/story loops with one fresh subagent per story. Install: `python scripts/install-external-skills.py --skill claude-loop --agent codex`.
- `ralph`: Use Ralph-style autonomous execution loops for scoped implementation plans. Install: `python scripts/install-external-skills.py --skill ralph --agent codex`.
- `no-mistakes`: Gate explicit ship, push, PR, or validate flows through the no-mistakes pipeline. Install: `python scripts/install-external-skills.py --skill no-mistakes --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).
