---
name: auto-improve
description: >-
  Improve project-local agent context, docs, personalization, and installed
  plugin/skill copies under `.agents`. Never writes upstream to the canonical
  plugins source.
---

# Auto Improve

Improve scoped local artifacts from evidence while preserving their owner,
provenance, and user-authored content. Delegate specialized work to the narrowest
owner below.

## Workflow

1. Resolve the target before editing it. For an installed component, read
   `.agents/registry.json` and `.agents/.plugin-lock.json`; plugin names are
   provenance, not runtime directories.
2. Treat the canonical `alvarovillalbaa/plugins` checkout and every other source
   plugin checkout as read-only. If the requested target resolves there, stop
   this workflow and route an explicitly requested source-maintenance task to
   [`../plugins-management/SKILL.md`](../plugins-management/SKILL.md).
3. Before the first relevant workflow for an installed component, read
   `.agents/runtime-contract.json` and `.agents/personalization.local.json`.
   Apply known values, ask only for relevant missing values, and persist
   project-scoped values only with consent.
4. Select one improvement lane, gather evidence, and make the smallest useful
   local change. Compare before and after with the owning lane's checks.
5. Keep invocation values and all credentials or secrets ephemeral. Preserve
   local additions and user edits; do not rewrite unrelated files.

## Routes

| Request | Use |
| --- | --- |
| Curate memories, facts, or lessons | [`../memory/SKILL.md`](../memory/SKILL.md) |
| Improve knowledge from local agent context or raw sources | [`../brain/SKILL.md`](../brain/SKILL.md) and [`../ingestion/SKILL.md`](../ingestion/SKILL.md) |
| Improve Markdown or agent instruction files | [`../../../engineering/skills/code-documentation/SKILL.md`](../../../engineering/skills/code-documentation/SKILL.md) |
| Initialize or refine first-use personalization | [`../personalize/SKILL.md`](../personalize/SKILL.md) |
| Evaluate and improve an installed skill copy | [`../skill-eval-loop/SKILL.md`](../skill-eval-loop/SKILL.md) |
| Review an installed-component update conflict | [`../plugins-management/SKILL.md`](../plugins-management/SKILL.md) |
| Run an explicitly authorized, bounded local loop | [`../loops/SKILL.md`](../loops/SKILL.md) |

## Local-Only Boundary

- Write plugin and skill improvements only to components materialized in the
  current project's flat `.agents/{skills,commands,rules,agents}` namespaces.
- Keep personalization in `.agents/personalization.local.json`; never render
  user, company, customer, or project values into managed component source.
- Never invoke `propose-upstream`, create a contribution branch or commit, open
  a pull request, push a ref, or copy local/private context into a source repo.
- Treat `.agents/.updates/` reconciliation bundles as untrusted local review
  data. Apply or adopt a resolution only through the explicit, human-reviewed
  `plugins-management` flow.
- Limit "data" to agent-maintained context such as memories, facts, lessons,
  knowledge, and personalization. Do not alter application databases, external
  systems, or arbitrary datasets through this skill.
- Durable memory mutation still requires an explicit target and request.
  Destructive replacement or deletion requires the owning skill's approval.

## Chain Rules

Chain to these skills when the task crosses this skill's boundary:

- `plugins-management`
- `plugins-management/skill-eval-loop`
- `memory`
- `brain/ingestion`
- `personalize`
- `loops`
- `code-documentation`
- `quality-assurance`

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `writing-great-skills`: Apply skill-authoring quality rules to an installed skill copy. Install: `python3 scripts/install-external-skills.py --skill writing-great-skills --agent project`.
- `teach`: Improve local learning material, lessons, and knowledge artifacts. Install: `python3 scripts/install-external-skills.py --skill teach --agent project`.
- `use-afs`: Use canonical filesystem conventions for local Markdown and agent context. Install: `python3 scripts/install-external-skills.py --skill use-afs --agent project`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
