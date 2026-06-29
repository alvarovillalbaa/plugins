---
name: hyperframes
description: >-
  Use for video concepting, storyboarding, sequencing, asset planning, review
  loops, and platform-specific video direction. Child skill of `video`; route here from the parent router when this lane is the
  narrowest owner.
---

# Hyperframes

This child skill owns video concepting, storyboarding, sequencing, asset planning, review loops, and platform-specific video direction. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about video concepting, storyboarding, sequencing, asset planning, review loops, and platform-specific video direction.
- The parent router [`../video/SKILL.md`](../video/SKILL.md) selects this child.
- The work needs this lane's references, scripts, examples, hooks, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `scripts/` contains executable helpers owned by this lane.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.
- `hooks/` contains hook entrypoints only when this lane owns hook behavior.

## Chain Rules

- Chain to `content`, `social-media`, `images`, `slides` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `animate-text`: Use text animation patterns for motion-heavy content and video scenes. Install: `python scripts/install-external-skills.py --skill animate-text --agent codex`.
- `transitions-dev`: Use transition patterns for purposeful UI and page motion. Install: `python scripts/install-external-skills.py --skill transitions-dev --agent codex`.
- `review-animations`: Review animation timing, easing, and intent against expert motion guidance. Install: `python scripts/install-external-skills.py --skill review-animations --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
