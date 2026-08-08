---
name: video
description: Route programmatic and generated video work to official external framework skills and local cross-media specialists.
---

# Video Router

## Route

| Request | Use |
| --- | --- |
| HyperFrames video composition and generation | Official external `hyperframes` skill |
| Remotion video creation and React video best practices | Official external `remotion-best-practices` skill installed through registry key `remotion` |

## Chain Rules

Chain to these skills when the task crosses this skill's boundary:

- `content`
- `social-media`
- `images`
- `slides`

## Operating Rules

- Keep this router framework-neutral; use the official external framework skill for implementation depth.
- Preserve local skill rules, repo facts, safety gates, product/channel constraints, and explicit local exceptions over external guidance when they conflict.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `manim-video`: Use Manim video guidance for generated explainer videos. Install: `python3 scripts/install-external-skills.py --skill manim-video --agent codex`.
- `animate-text`: Use text animation patterns for motion-heavy content and video scenes. Install: `python3 scripts/install-external-skills.py --skill animate-text --agent codex`.
- `transitions-dev`: Use transition patterns for purposeful UI and page motion. Install: `python3 scripts/install-external-skills.py --skill transitions-dev --agent codex`.
- `review-animations`: Review animation timing, easing, and intent against expert motion guidance. Install: `python3 scripts/install-external-skills.py --skill review-animations --agent codex`.
- `hyperframes`: Use HeyGen's official HyperFrames skill. Install: `python3 scripts/install-external-skills.py --skill hyperframes --agent codex`.
- `remotion-best-practices`: Use Remotion's official skill through the `remotion` registry key. Install: `python3 scripts/install-external-skills.py --skill remotion --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
