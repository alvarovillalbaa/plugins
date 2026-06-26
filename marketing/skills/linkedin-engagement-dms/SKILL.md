---
name: linkedin-engagement-dms
description: >-
  Use for LinkedIn comments, connection requests, DM replies, follow-up
  sequences, and professional engagement writing. Child skill of `social-
  media-management`; route here from the parent router when this lane is the
  narrowest owner.
---

# Linkedin Engagement Dms

This child skill owns LinkedIn comments, connection requests, DM replies, follow-up sequences, and professional engagement writing. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about LinkedIn comments, connection requests, DM replies, follow-up sequences, and professional engagement writing.
- The parent router [`../social-media-management/SKILL.md`](../social-media-management/SKILL.md) selects this child.
- The work needs this lane's references, scripts, examples, hooks, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `scripts/` contains executable helpers owned by this lane.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.
- `hooks/` contains hook entrypoints only when this lane owns hook behavior.

## Chain Rules

- Chain to `content-writing/repurposing-syndication`, `product-marketing/positioning-messaging`, `go-to-market/launch-gtm`, `code-as-images`, `video-generation` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
