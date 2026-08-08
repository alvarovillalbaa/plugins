---
name: x-posts
description: Use for X posts, replies, quote posts, engagement prompts, thread hooks, and daily interaction writing. Child of `social-media`.
---

# X Engagement Posts

This child skill owns X posts, replies, quote posts, engagement prompts, thread hooks, and daily interaction writing. It carries the detailed assets for this lane after the corrected fragmentation split.

## Use When

- The request is primarily about X posts, replies, quote posts, engagement prompts, thread hooks, and daily interaction writing.
- The parent router [`../social-media/SKILL.md`](../social-media/SKILL.md) selects this child.
- The work needs this lane's references, examples, or templates.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `unslop`: Remove generic AI-writing tells while preserving meaning and voice. Install: `python3 scripts/install-external-skills.py --skill unslop --agent codex`.
- `stop-slop`: Apply stricter prose cleanup for predictable AI writing patterns. Install: `python3 scripts/install-external-skills.py --skill stop-slop --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).

## Assets

- `references/` contains lane-specific guidance moved from the original parent skill.
- `templates/` contains reusable output or implementation templates for this lane.
- `examples/` contains sample inputs, outputs, or usage artifacts.

## Chain Rules

- Chain to `content/repurposing`, `personalize/positioning`, `launches`, `images`, `video` when the task crosses this child's boundary.
- Chain to `unslop` and `stop-slop` for prose cleanup instead of maintaining local AI-writing detector lists.
- Use repo-local personalization documents for company, product, voice, cloud, QA, or finance facts instead of hardcoding them here.
- Preserve parent safety and approval rules for destructive, security-sensitive, finance-sensitive, or cloud-costly work.

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
