# Personalization, Variables, And Relationships

The installed runtime is intentionally separate from source plugin folders. Every
selected element lands in a flat project-local namespace under `.agents/`; its source
plugin remains recorded only as provenance in `.agents/.plugin-lock.json` and
`.agents/registry.json`.

## Inherited personalization

The canonical contract is [`../runtime-contract.json`](../runtime-contract.json).
Personalization is enabled by default for skills, commands, rules, and agents, so it
does not require boilerplate in every component. An individual component can opt out
or declare additional variables in the contract.

On the first workflow where a missing value is actually relevant, the installed
runtime rule routes initialization through `auto-improve` to the `personalize`
owner. The host asks only for that value and—only with consent—stores project-
scoped values in `.agents/personalization.local.json`. The first-party `context`
command also prompts for required invocation values on an interactive terminal.
The file is local-only and must never contain credentials or customer secrets.
Invocation values stay ephemeral.

## Variable resolution

Values resolve in the following order:

1. explicit invocation input, including values already present in the request;
2. current session context;
3. project personalization;
4. a declared default.

The contract supports project, session, and invocation scopes, required values,
prompts, types, and sensitive-value handling. Components use canonical typed IDs such
as `skill:marketing/content` or `command:marketing/blog-draft`.

The same command can render canonical dotted placeholders and raw invocation input:

```bash
scripts/plugins context skill:marketing/content --project . \
  --set content.topic="Agent workflows" \
  --render path/to/template.md --output path/to/rendered.md \
  --arguments="the original invocation text"
```

Named placeholders use `{{content.topic}}`; `$ARGUMENTS` receives the explicitly
supplied raw invocation string. Unresolved canonical placeholders fail closed.

## Relationship resolution

The component graph supports plugin, skill, command, rule, agent, and external-skill
nodes. Its resolver produces a relationship candidate closure, not an unconditional
execution plan: the host selects only task-relevant edges. Resolution has no fixed
nesting depth. Independent candidates at the same breadth level form a possible
parallel group, while sequential edges remain ordered. Cycles are legal: the resolver
visits each node once per resolution and reports edges that would re-enter an already
visited node.

Project graphs mark availability. Installed-aware resolution excludes nodes marked
`installed: false` and reports the blocked relationships and unavailable nodes. This
makes two-sided relationships useful without allowing an execution loop or claiming
an unavailable component ran.
