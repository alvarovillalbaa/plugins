---
name: social-media-management
description: >-
  Router for X engagement posts, X viral launch systems, and LinkedIn
  engagement/DM workflows.
---

# Social Media Management Router

This parent is a router. Select the narrowest child and load that child before using lane-specific assets.

## Children

- [`x-engagement-posts`](../x-engagement-posts/SKILL.md) - X posts, replies, quote posts, engagement prompts, thread hooks, and daily interaction writing
- [`x-viral-launch`](../x-viral-launch/SKILL.md) - viral X launch systems, launch threads, controversy research, sequence planning, and performance-oriented post variants
- [`linkedin-engagement-dms`](../linkedin-engagement-dms/SKILL.md) - LinkedIn comments, connection requests, DM replies, follow-up sequences, and professional engagement writing

## Route

| User asks for | Use |
| --- | --- |
| X posts, replies, quote posts, engagement prompts, thread hooks, and daily interaction writing | [`x-engagement-posts`](../x-engagement-posts/SKILL.md) |
| viral X launch systems, launch threads, controversy research, sequence planning, and performance-oriented post variants | [`x-viral-launch`](../x-viral-launch/SKILL.md) |
| LinkedIn comments, connection requests, DM replies, follow-up sequences, and professional engagement writing | [`linkedin-engagement-dms`](../linkedin-engagement-dms/SKILL.md) |

## Chain Rules

- `content-writing/repurposing-syndication`
- `product-marketing/positioning-messaging`
- `go-to-market/launch-gtm`
- `code-as-images`
- `video-generation`

## Operating Rules

- Keep this `SKILL.md` small and routing-focused.
- Do not recreate the old broad parent behavior here; put execution depth in child assets.
- If no child matches, handle only shared methodology/default workflow or document the missing lane.
- Every child and parent skill must keep `examples/`, `hooks/`, `references/`, `scripts/`, and `templates/`.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
