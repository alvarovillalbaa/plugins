# Agent guidance

This repository is the canonical source for the Agent Company plugin catalog.
Before changing a component, identify its source owner in `catalog.json`, its
relationships in `references/component-graph.json` plus
`scripts/component_graph.py`, and its repository rules in the owning plugin.

## Installation contract

- Prefer `./scripts/plugins install`, which is interactive when selectors are
  omitted.
- Install target projects only into the flat
  `.agents/{skills,commands,rules,agents}` namespaces.
- Never create `.agents/<plugin-name>/`; plugin names are provenance, not
  runtime namespaces.
- Treat reinstall/update as a no-loss merge. Preserve personalization, local
  additions, and user edits; stage unresolved incoming content rather than
  overwriting it.

## Runtime contract

- Personalization is inherited from `references/runtime-contract.json`.
- Ask for a missing value only on the first workflow where it is relevant.
- Persist project-scoped values only with consent. Keep invocation values and
  all credentials or secrets ephemeral.
- Resolve component relationships without a fixed depth cap. Parallelize safe
  breadth-level work, visit each node once, and report rather than re-enter
  cycle edges.

## Source changes

- Keep profiles, manifests, skills, commands, agents, rules, the chaining map,
  and generated discovery artifacts aligned.
- Preserve user work in a dirty checkout and keep changes scoped to the actual
  owner.
- Run `python3 scripts/run_skill_tests.py .`,
  `python3 scripts/component_graph.py build --check`, and
  `python3 scripts/generate_discovery_catalog.py --check` before claiming the
  relevant contracts are current.
