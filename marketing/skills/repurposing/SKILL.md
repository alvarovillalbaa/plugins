---
name: repurposing
description: >-
  Use for turning one source asset into channel-specific posts, newsletters,
  articles, and distribution packs. Child skill of `content`; route
  here from the parent router when this lane is the narrowest owner.
---

# Repurposing Syndication

This child skill owns turning one source asset into channel-specific posts, newsletters, articles, and distribution packs. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about turning one source asset into channel-specific posts, newsletters, articles, and distribution packs.
- The parent router [`../content/SKILL.md`](../content/SKILL.md) selects this child.
- The work needs this lane's references, scripts, examples, hooks, or templates.

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `scripts/` contains executable helpers owned by this lane.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.
- `hooks/` contains hook entrypoints only when this lane owns hook behavior.

## Chain Rules

- Chain to `discoverability/geo`, `seo-and-geo/on-page-seo`, `social-media`, `product-marketing` when the task crosses this child's boundary.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
