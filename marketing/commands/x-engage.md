---
name: x-engage
description: Draft public X replies, quote posts, or short conversation sequences using the X publishing skill.
argument-hint: "[post, thread, topic, or goal]"
allowed-tools: [Read, Write, AskUserQuestion, Skill]
---

Use skill: **x-posts** — `skills/x-posts/SKILL.md`.
Reference: `skills/x-posts/references/x-writing-guidelines.md`

1. **Gather context** – Ask for the target post URL or text, conversation summary, and desired outcome if the prompt is thin.
2. **Choose the interaction type** – Reply, quote post, or short public engagement sequence.
3. **Draft the output** – Produce a concise, platform-native draft with a strong angle. Apply the hook and specificity rules from `x-writing-guidelines.md` even in replies.
4. **Add variants if useful** – Include alternative tones: sharper, warmer, or more neutral. At least one variant should take a contrarian angle if the topic allows.
5. **Deliver** – Output the drafts and a one-line rationale for why the angle fits the target conversation.

## Boundary

This command owns public X engagement. Route direct messages and one-to-one sales follow-up to the Sales `outreach` skill or its `x-dms` child; use `x-post` for a net-new standalone post or thread.
