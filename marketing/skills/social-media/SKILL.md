---
name: social-media
description: Router for LinkedIn and X social publishing workflows.
---

# Social Media Router

## Children

- [`x-posts`](../x-posts/SKILL.md) - X Posts work.
- [`linkedin-posts`](../linkedin-posts/SKILL.md) - Linkedin Posts work.
- [`x-articles`](../x-articles/SKILL.md) - X Articles work.
- [`linkedin-articles`](../linkedin-articles/SKILL.md) - Linkedin Articles work.

## Route

| Request | Use |
| --- | --- |
| x posts requests | [`x-posts`](../x-posts/SKILL.md) |
| linkedin posts requests | [`linkedin-posts`](../linkedin-posts/SKILL.md) |
| x articles requests | [`x-articles`](../x-articles/SKILL.md) |
| linkedin articles requests | [`linkedin-articles`](../linkedin-articles/SKILL.md) |

## Chain Rules

Chain to these skills when the task crosses this skill's boundary:

- `content/repurposing`
- `personalize/positioning`
- `launches/virality`
- `images`
- `video`

## Operating Rules

- Keep this parent compact; use children for lane-specific execution depth.
- Prefer the child skill's bundled resources when a child owns the request.
- Preserve local skill rules, repo facts, safety gates, product/channel constraints, and explicit local exceptions over external guidance when they conflict.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `unslop`: Remove generic AI-writing tells while preserving meaning and voice. Install: `python scripts/install-external-skills.py --skill unslop --agent codex`.
- `stop-slop`: Apply stricter prose cleanup for predictable AI writing patterns. Install: `python scripts/install-external-skills.py --skill stop-slop --agent codex`.
- `animate-text`: Use text animation patterns for motion-heavy content and video scenes. Install: `python scripts/install-external-skills.py --skill animate-text --agent codex`.
- `visual-explainer`: Use visual explanation guidance for diagrams, concepts, and teachable visuals. Install: `python scripts/install-external-skills.py --skill visual-explainer --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
