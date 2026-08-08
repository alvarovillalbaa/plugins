---
name: linkedin-engage
description: Draft public LinkedIn comments, replies, or repost copy using the LinkedIn publishing skill.
argument-hint: "[post, conversation context, or public engagement goal]"
allowed-tools: [Read, Write, AskUserQuestion, Skill]
---

Use skill: **linkedin-posts** — `skills/linkedin-posts/SKILL.md`.

1. **Gather context** – Ask for the post, public conversation, audience, and goal if the request is underspecified.
2. **Choose the format** – Decide whether this is a comment, reply, or repost with commentary.
3. **Draft the message** – Produce a personalized, platform-native draft with the right tone and ask.
4. **Add variants if useful** – Include softer or more direct versions when the user would benefit from choice.
5. **Deliver** – Output the draft and a one-line rationale for the angle.

## Boundary

This command owns public LinkedIn engagement. Route connection requests, direct messages, and sales follow-ups to the Sales `outreach` skill or its `linkedin-dms` child.
