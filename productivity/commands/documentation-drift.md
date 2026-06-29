---
name: documentation-drift
description: Review agent, repo, or workflow documentation for drift against current files and behavior.
argument-hint: "[doc path, repo area, or workflow]"
allowed-tools: [Read, Grep, Glob, Bash, AskUserQuestion, Skill]
---

Use skill: **documentation-drift** — `skills/documentation-drift/SKILL.md`.

Compare docs against current source files, identify stale instructions or missing coverage, and return a concise drift report or patch plan.
