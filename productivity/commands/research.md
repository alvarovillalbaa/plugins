---
name: research
description: Run a scoped business research job — competitor intelligence, diligence, ICP, account brief, customer answer, or synthesis. Returns a decision artifact with dated evidence, visible logic, and a next action.
argument-hint: "<topic or question> [--lane=competitor|diligence|icp|account|customer] [--shape=brief|comparison|ranked|memo|people-slate]"
allowed-tools: [Bash, Read, Write, WebSearch, WebFetch, AskUserQuestion]
---

Invoke the `research` skill with the user's arguments: $ARGUMENTS

Before sourcing, run the query quality pre-flight from the skill:

1. Parse the question for scope mismatch or keyword traps.
2. Infer the primary lane from the argument or ask one clarifying question if
   the lane is genuinely ambiguous.
3. Infer the artifact shape (brief, comparison, ranked universe, memo, account
   brief, people slate, follow-up queue, synthesis memo, or customer answer).

If `--lane` was provided, route directly to that lane without asking.
If `--shape` was provided, use that artifact shape without asking.

Run the research skill's full operating loop and return the artifact.
Apply the output contract: inline Markdown citations with descriptive link text, no trailing
`Sources:` block, post-synthesis self-check before output.
