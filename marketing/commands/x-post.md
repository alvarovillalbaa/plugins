---
name: x-post
description: Draft an original X post or thread from scratch using the research-driven writing framework — hooks, formats, and optional topic research.
argument-hint: "[topic, idea, or draft to improve]"
allowed-tools: [Read, Write, Bash, AskUserQuestion, Skill]
---

Use skill: **x-posts** — `skills/x-posts/SKILL.md`.
Reference: `skills/x-posts/references/x-writing-guidelines.md`
Reference: `skills/x-posts/references/x-post-formats.md`
Reference: `skills/x-posts/references/x-research-workflow.md`

1. **Clarify the brief** — If the input is thin, ask for: the core insight, desired outcome (reach / saves / replies / clicks), and audience posture. Use `templates/x-post-brief.md` as the scoping guide.
2. **Select the format** — Match goal to format using `x-post-formats.md`. Default to single post unless the topic needs a thread.
3. **Check for research opportunity** — If an X Bearer token is available and the topic is competitive, suggest running `bun run x-search.ts advise` before drafting. Proceed with guidelines if no token.
4. **Apply the writing framework** — Use `x-writing-guidelines.md`: strong hook, specific body, banger endings, one clear CTA.
5. **Draft the output** — Produce the post or full thread. For threads, use `templates/x-thread-plan.md` structure.
6. **Add variants** — Provide 2–3 alternative hooks or tone variants when useful.
7. **Deliver** — Output the draft(s) with a one-line rationale for the chosen format and hook angle.

If the user provides a draft to improve rather than create from scratch, analyze it against the writing guidelines and rewrite with specific improvements explained.
