---
name: video
description: Generate a programmatic video from a brief using the video (Remotion) skill. Gather scope, produce a plan and code.
argument-hint: "[topic or scope]"
allowed-tools: [Read, Write, AskUserQuestion, Skill]
---

Use skill: **video** — `skills/video/SKILL.md`. Route Remotion implementation through `skills/remotion/SKILL.md`.

1. **Gather scope** – Ask the user for topic, duration, style, and any assets (images, audio, captions) if not provided in the argument.
2. **Read the skill** – Load `skills/video/SKILL.md`, `skills/remotion/SKILL.md`, and the relevant Remotion `rules/*.md` and `templates/`.
3. **Plan** – Produce a short video plan (scenes, timing, assets) and confirm with the user if needed.
4. **Implement** – Write Remotion composition(s) and related code; use the skill’s rules for compositions, audio, captions, and assets. For any text reveal or headline animation, read `skills/remotion/references/rules/text-animations.md` and pick a named pattern by ID; do not invent timing numbers.
5. **Deliver** – Output the video project (or key files) and brief instructions to run/render.

If the user only gave a high-level topic, ask 1–2 clarifying questions (e.g. duration, aspect ratio, tone) before planning.
