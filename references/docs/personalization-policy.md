# Component Personalization Policy

Personalization is an overlay/context step. It must not mutate upstream or
managed installed component files with user, company, customer, path,
credential, or private workflow data.

The inherited project contract applies by default to installed skills,
commands, rules, and agents. Component-specific variables are declared in
[`../runtime-contract.json`](../runtime-contract.json), so most components do
not need duplicated personalization boilerplate.

## Source-Maintenance Templates

These template types are valid only during an explicitly requested canonical
source-maintenance workflow owned by `plugins-management`. They are not write
targets for `auto-improve`.

- Placeholder templates in `left-to-personalize/**`
- `personalization.schema.json`
- `personalize.example.yml` using placeholder values
- Generic rendering scripts and examples

## Local-Only Personalization

- `personalize.local.yml`
- `*.local.yml`
- `.overlays/**`
- `.company/**`
- `.user/**`
- rendered files in `.generated/**`
- private credentials, customer data, internal process details, and local paths

## Rendering Contract

Render overlays into an explicit output directory. Do not render in place unless
the output path is ignored and clearly marked as generated.

## First Use

In installed projects, agents read `.agents/runtime-contract.json` and
`.agents/personalization.local.json`. On the first workflow where a missing
value is relevant, ask only for that value and store it only with consent:

```bash
/path/to/plugins/scripts/plugins configure \
  --project . \
  --set organization.name="Example Inc"
```

An installed component may be personalized explicitly through the same local
project store:

```bash
/path/to/plugins/scripts/plugins configure \
  --project . \
  --set user.role="Engineering lead"
```

`auto-improve` coordinates this just-in-time step and delegates the value capture
to `personalize`. It never edits a canonical plugin source checkout.

## Continuous Personalization

When an agent learns a stable user or company preference, it may update the
local project store only, with consent:

```bash
/path/to/plugins/scripts/plugins configure \
  --project . \
  --set organization.name="Example Inc"
```

Continuous personalization must not write to installed `SKILL.md`, references,
examples, scripts, templates, or any canonical source checkout.

## Dynamic invocation values

Invocation-scoped inputs are never stored in the project overlay. Supply them
when resolving or running the component:

```bash
/path/to/plugins/scripts/plugins context skill:marketing/content \
  --project . \
  --set content.topic="Agent workflows"
```

Resolution order is invocation, session, project, then declared default.
Required unresolved values fail closed in non-interactive flows. Sensitive
values are always ephemeral.
