---
name: web-vuln-validation
description: >-
  Use for authorized web vulnerability validation, scanner result
  verification, client-side testing, and browser-exposed attack paths. Child
  skill of `pentest`; route here from the parent router when this lane is
  the narrowest owner.
---

# Web Vuln Validation

This child skill owns authorized web vulnerability validation, scanner result verification, client-side testing, and browser-exposed attack paths. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about authorized web vulnerability validation, scanner result verification, client-side testing, and browser-exposed attack paths.
- The parent router [`../pentest/SKILL.md`](../pentest/SKILL.md) selects this child.
- The work needs this lane's references, scripts, examples, hooks, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `scripts/` contains executable helpers owned by this lane.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.
- `hooks/` contains hook entrypoints only when this lane owns hook behavior.

## Chain Rules

- Chain to `quality-assurance/passive-security-review`, `cloud-management`, `backend` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
