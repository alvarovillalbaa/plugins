---
name: si:extract
description: Turn a proven recurring pattern or debugging solution into a standalone portable skill. The skill will work in any project with no hardcoded paths or project-specific values.
argument-hint: "[pattern description, exact memory record, or current-session pattern]"
allowed-tools: [Agent, Read, Glob, Skill]
---

Extract a proven pattern into a standalone reusable skill.

Use skill: **plugins-management** — `skills/plugins-management/SKILL.md`.

## Steps

1. **Resolve scope and gather context** — require one project or memory-store scope. If the argument references a memory record, read that exact record plus directly linked evidence inside the authorized store. If it says "last debugging session", inspect only the current project's scoped records and logs. Do not wildcard across projects or runtimes.

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

6. **Link back** — propose a supersession link from the source record to the new skill. Update or remove the memory only after a separate explicit approval that identifies the exact record; prefer a reversible supersession pointer over deletion.

## Boundary

This command packages an already proven reusable pattern. It does not capture new memory, promote policy, or extract project-specific conventions into a portable skill.
