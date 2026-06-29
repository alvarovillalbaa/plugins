---
name: video
description: Router for programmatic and generated video workflows.
---

# Video Router

## Children

- [`hyperframes`](../hyperframes/SKILL.md) - Hyperframes work.
- [`remotion`](../remotion/SKILL.md) - Remotion work.

## Route

| Request | Use |
| --- | --- |
| hyperframes requests | [`hyperframes`](../hyperframes/SKILL.md) |
| remotion requests | [`remotion`](../remotion/SKILL.md) |

## Chain Rules

Chain to these skills when the task crosses this skill's boundary:

- `content`
- `social-media`
- `images`
- `slides`

## Operating Rules

- Keep this parent compact; use children for lane-specific execution depth.
- Prefer the child skill's bundled resources when a child owns the request.
- Preserve local skill rules, repo facts, safety gates, product/channel constraints, and explicit local exceptions over external guidance when they conflict.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `manim-video`: Use Manim video guidance for generated explainer videos. Install: `python scripts/install-external-skills.py --skill manim-video --agent codex`.
- `animate-text`: Use text animation patterns for motion-heavy content and video scenes. Install: `python scripts/install-external-skills.py --skill animate-text --agent codex`.
- `transitions-dev`: Use transition patterns for purposeful UI and page motion. Install: `python scripts/install-external-skills.py --skill transitions-dev --agent codex`.
- `review-animations`: Review animation timing, easing, and intent against expert motion guidance. Install: `python scripts/install-external-skills.py --skill review-animations --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
