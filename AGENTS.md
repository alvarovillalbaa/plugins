# Agent guidance

Last updated: 2026-10-10

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

## Knowledge workspace and AFS profile

This repository uses partial AFS mode, with its documentation shell in `docs/`.
Select this repository as the explicit workspace. Read root guidance and the
nearest applicable subsystem `AGENTS.md`; nested guidance does not create an
ambiguous second brain. Sibling repositories are separate source owners unless
the user explicitly includes them. Runtime installs, caches, and generated
bundles are evidence, not canonical source.

| Responsibility | Repo path |
| --- | --- |
| Skill source | `<department>/skills/<skill>/` |
| Commands | `<department>/commands/*.md` |
| Agents | `<department>/agents/*.md` |
| Skill taxonomy | `skills-chaining-map.md` |
| External skill registry | `references/external-skills.yaml` |
| Skill audits | `docs/audits/YYYY/MM-DD/skills/` |
| Skill changelog | `docs/changelog/skills/` |
| Technical owner docs | `references/docs/`, cataloged in `REFERENCES.md` |
| Generated improvement bundles | `.skill-improvements/` |

Read the installed `use-afs` skill before AFS work; explicit user instructions
take precedence over an older installed revision. Local ownership rules are in
[`references/docs/afs-profile.md`](references/docs/afs-profile.md). Use the
[`promotion matrix`](references/docs/promotion-matrix.md) before making a
learning, fact, fix, rule, source, or generated artifact durable.

Preserve raw intake in the ownership-appropriate private Drive account and
record its provenance in `SOURCES.md`. `REFERENCES.md` is the reference catalog;
`GAPS.md` records unresolved evidence. Knowledge contains unique generalized
synthesis. Repo operations belong to their technical guides. Research uses
living unit folders with ordered questions, hypotheses, reasoning, method,
evidence, status, and next action. Goals remain canonical in Notion, linked from
`ROADMAP.md` where relevant. Keep logs to at most two lines per change; link
longer evidence from dated results or audits. Templates stay with their skill or
content owner; never introduce a global template intake directory.
