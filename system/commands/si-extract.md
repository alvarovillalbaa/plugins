---
name: si:extract
description: Turn a proven recurring pattern or debugging solution into a standalone portable skill. The skill will work in any project with no hardcoded paths or project-specific values.
argument-hint: "[pattern description, MEMORY.md entry, or 'last debugging session']"
allowed-tools: [Agent, Read, Glob]
---

Extract a proven pattern into a standalone reusable skill.

## Steps

1. **Gather context** — read the argument. If it references a MEMORY.md entry, read that entry plus any related entries. If it says "last debugging session", read the most recent entries in MEMORY.md and today's log.

2. **Check reusability** — confirm the pattern is genuinely reusable across projects. If it is project-specific (references this repo's paths or conventions), tell the user and stop. Suggest saving it to `.claude/rules/` instead.

3. **Spawn skill-extractor** — pass the agent:
   - The problem description (extracted from the argument and context)
   - The solution (the fix, with exact commands if available)
   - Known edge cases
   - The trigger condition ("Use when...")

4. **Review output** — confirm the generated SKILL.md passes the quality checklist:
   - No project-specific paths
   - Includes exact error messages for searchability
   - Runnable code examples
   - "Use when:" trigger in description

5. **Place the skill** — suggest where to save it:
   - `system/skills/<skill-name>/` if it belongs to this plugin
   - A new standalone plugin directory if the skill is more general

6. **Link back** — optionally remove the MEMORY.md entry now that a durable skill exists.
