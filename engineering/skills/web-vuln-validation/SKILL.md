---
name: web-vuln-validation
description: Use for authorized web vulnerability validation, scanner result verification, client-side testing, and browser-exposed attack paths. Child of `pentest`.
---

# Web Vuln Validation

This child skill owns authorized web vulnerability validation, scanner result verification, client-side testing, and browser-exposed attack paths. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about authorized web vulnerability validation, scanner result verification, client-side testing, and browser-exposed attack paths.
- The parent router [`../pentest/SKILL.md`](../pentest/SKILL.md) selects this child.
- The work needs this lane's references, examples, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.

This lane intentionally has no bundled scanner. Use evidence from the actual
authorized target and current specialist tools. Route passive source, secrets,
and dependency review to `quality-assurance/security`; a local regex scanner or
frozen CVE table is not a substitute for live vulnerability validation.

## Chain Rules

- Chain to `quality-assurance/security`, `cloud`, `backend` when the task crosses this child's boundary.
- This skill owns authorized validation of browser- and network-exposed attack
  paths. It does not own passive source scanning or dependency advisory lookup.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
