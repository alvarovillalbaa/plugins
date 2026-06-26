---
name: x-engagement-posts
description: >-
  Use for X posts, replies, quote posts, engagement prompts, thread hooks, and
  daily interaction writing. Child skill of `social-media-management`; route
  here from the parent router when this lane is the narrowest owner.
---

# X Engagement Posts

This child skill owns X posts, replies, quote posts, engagement prompts, thread hooks, and daily interaction writing. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about X posts, replies, quote posts, engagement prompts, thread hooks, and daily interaction writing.
- The parent router [`../social-media-management/SKILL.md`](../social-media-management/SKILL.md) selects this child.
- The work needs this lane's references, scripts, examples, hooks, or templates.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `unslop`: Remove generic AI-writing tells from X posts and threads. Install: `python scripts/install-external-skills.py --skill unslop --agent codex`.
- `stop-slop`: Apply stricter prose cleanup before publishing or scheduling. Install: `python scripts/install-external-skills.py --skill stop-slop --agent codex`.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `scripts/` contains executable helpers owned by this lane.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.
- `hooks/` contains hook entrypoints only when this lane owns hook behavior.

## Chain Rules

- Chain to `content-writing/repurposing-syndication`, `product-marketing/positioning-messaging`, `go-to-market/launch-gtm`, `code-as-images`, `video-generation` when the task crosses this child's boundary.
- Chain to `unslop` and `stop-slop` for prose cleanup instead of maintaining local AI-writing detector lists.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
