---
name: skill-eval-loop
description: Use for skill evaluation loops, regression checks for skill behavior, prompt/skill mutation proposals, and explicit improvement gates. Child of `plugins-management`.
---

# Skill Eval Loop

This child skill owns skill evaluation loops, regression checks for skill behavior, prompt/skill mutation proposals, and explicit improvement gates. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about skill evaluation loops, regression checks for skill behavior, prompt/skill mutation proposals, and explicit improvement gates.
- The parent router [`../plugins-management/SKILL.md`](../plugins-management/SKILL.md) selects this child.
- The work needs this lane's references, examples, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.

## Chain Rules

- Chain to `memory`, `brain`, `code-documentation`, `agentic-development/agent-harness`, `personalize/voice` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.
- When routed from `auto-improve`, evaluate and edit only the installed component
  under the current project's `.agents` tree. Do not classify or package an
  upstream diff, create a source commit or branch, open a PR, or push.
- For upstream proposals, locate `.skillmeta.yml`, classify the diff with
  `scripts/skillctl.py diff-classify`, and keep private overlays out of
  source-tracked files. This path is available only for an explicit canonical
  source-maintenance request routed directly through `plugins-management`, not
  through `auto-improve`.
- In that direct source-maintenance flow, generate patch bundles by default with
  `scripts/skillctl.py propose-upstream --mode patch`; use PR mode only when the
  user has authenticated GitHub tooling and has chosen an upstream PR flow.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `writing-great-skills`: Use external skill-authoring quality rules when creating or revising skills. Install: `python3 scripts/install-external-skills.py --skill writing-great-skills --agent codex`.
- `teach`: Create mission-grounded learning material, resources, records, and lessons. Install: `python3 scripts/install-external-skills.py --skill teach --agent codex`.
- `grilling`: Interview one decision at a time until a plan or design is sharp. Install: `python3 scripts/install-external-skills.py --skill grilling --agent codex`.
- `grill-me`: Shortcut into a grilling session for plan or design stress testing. Install: `python3 scripts/install-external-skills.py --skill grill-me --agent codex`.
- `grill-with-docs`: Stress-test a plan or design while maintaining docs, ADRs, and glossary context. Install: `python3 scripts/install-external-skills.py --skill grill-with-docs --agent codex`.
- `use-afs`: Use the AFS filesystem layout and naming conventions instead of duplicating local filesystem guidance. Install: `python3 scripts/install-external-skills.py --skill use-afs --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
