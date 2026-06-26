---
name: video-generation
description: >-
  Router for video strategy/storyboarding through Hyperframes and Remotion
  implementation/rendering workflows.
---

# Video Generation Router

This parent is a router. Select the narrowest child and load that child before using lane-specific assets.

## Children

- [`hyperframes`](../hyperframes/SKILL.md) - video concepting, storyboarding, sequencing, asset planning, review loops, and platform-specific video direction
- [`remotion`](../remotion/SKILL.md) - Remotion implementation, compositions, timing rules, rendering, media handling, captions, audio, and export verification

## Route

| User asks for | Use |
| --- | --- |
| video concepting, storyboarding, sequencing, asset planning, review loops, and platform-specific video direction | [`hyperframes`](../hyperframes/SKILL.md) |
| Remotion implementation, compositions, timing rules, rendering, media handling, captions, audio, and export verification | [`remotion`](../remotion/SKILL.md) |

## Chain Rules

- `content-writing`
- `social-media-management`
- `code-as-images`
- `code-slides`

## Operating Rules

- Keep this `SKILL.md` small and routing-focused.
- Do not recreate the old broad parent behavior here; put execution depth in child assets.
- If no child matches, handle only shared methodology/default workflow or document the missing lane.
- Every child and parent skill must keep `examples/`, `hooks/`, `references/`, `scripts/`, and `templates/`.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
