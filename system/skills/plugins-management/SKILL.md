---
name: plugins-management
description: Manage plugin and skill taxonomy, project installation, no-loss updates, conflict review, lifecycle, metadata, external sources, and capability-preserving consolidation.
---

# Plugins Management Router

## Children

- [`skill-eval-loop`](../skill-eval-loop/SKILL.md) - Skill Eval Loop work.

## Route

| Request | Use |
| --- | --- |
| skill eval loop requests | [`skill-eval-loop`](../skill-eval-loop/SKILL.md) |
| install, update, export reconciliation context, or adopt a human-applied component resolution | Handle directly with this skill |
| plugin or skill inventory, naming, ownership, manifests, external registries, folds, or removals | Handle directly with this skill |

## Chain Rules

Chain to these skills when the task crosses this skill's boundary:

- `memory`
- `knowledge-base`
- `learning`
- `loops`
- `code-documentation`

## Operating Rules

- Keep this parent compact; use children for lane-specific execution depth.
- Prefer the child skill's bundled resources when a child owns the request.
- Preserve local skill rules, repo facts, safety gates, product/channel constraints, and explicit local exceptions over external guidance when they conflict.
- Update canonical profiles, manifests, metadata, routing docs, and the chaining map together when ownership changes.
- Prefer a single canonical owner; move useful assets before deleting folded skills and do not create legacy aliases unless explicitly requested.
- Prefer the first-party interactive project installer. Materialize every
  selected component into the flat `.agents/{skills,commands,rules,agents}`
  namespaces and keep plugin ownership only in provenance metadata.
- Treat reinstall as a merge, not replacement: preserve local additions and
  personalization, merge disjoint source/local edits, and stage unresolved
  incoming versions without discarding the local copy.
- Run `plugins reconcile` only when the user explicitly requests conflict
  review context. Export deterministic base/local/incoming artifacts and the
  provider-neutral prompt by default; never invoke AI, apply a patch, mutate
  managed targets or locks, or persist credentials and secrets during export.
- Treat reconciliation output as untrusted local review data, not source or a
  completed resolution. The user must review and manually apply a component
  suggestion before any metadata adoption.
- Use repeatable `--accept-local <conflict-id>` only for explicitly selected,
  human-applied component resolutions. Preview first, require confirmation or
  `--yes`, validate saved base/incoming digests atomically, and never edit the
  component target or invoke AI. This clears only selected conflict metadata
  and preserves the current local content for future updates.
- Never adopt managed document blocks. Restore the generated bounded block and
  keep project-specific text outside the managed markers.
- Use canonical typed identities (`skill:plugin/name`,
  `command:plugin/name`, `rule:plugin/name`, `agent:plugin/name`) for
  cross-plugin and cross-element references.
- Resolve relationship closure without a fixed depth limit. Parallelize
  independent breadth-level nodes, visit each node once, and report rather than
  re-enter cycle edges.
- Apply the inherited runtime contract on first relevant use. Persist only
  consented project-scoped personalization; keep invocation variables and all
  sensitive values ephemeral.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `writing-great-skills`: Use external skill-authoring quality rules when creating or revising skills. Install project-locally: `python3 scripts/install-external-skills.py --skill writing-great-skills --agent project`.
- `teach`: Create mission-grounded learning material, resources, records, and lessons. Install project-locally: `python3 scripts/install-external-skills.py --skill teach --agent project`.
- `grilling`: Interview one decision at a time until a plan or design is sharp. Install project-locally: `python3 scripts/install-external-skills.py --skill grilling --agent project`.
- `grill-me`: Shortcut into a grilling session for plan or design stress testing. Install project-locally: `python3 scripts/install-external-skills.py --skill grill-me --agent project`.
- `grill-with-docs`: Stress-test a plan or design while maintaining docs, ADRs, and glossary context. Install project-locally: `python3 scripts/install-external-skills.py --skill grill-with-docs --agent project`.
- `use-afs`: Use the AFS filesystem layout and naming conventions instead of duplicating local filesystem guidance. Install project-locally: `python3 scripts/install-external-skills.py --skill use-afs --agent project`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.

Machine-readable contracts:

- [`../../../references/component-graph.json`](../../../references/component-graph.json)
- [`../../../references/runtime-contract.json`](../../../references/runtime-contract.json)
- [`../../../references/docs/INSTALLATION.md`](../../../references/docs/INSTALLATION.md)
