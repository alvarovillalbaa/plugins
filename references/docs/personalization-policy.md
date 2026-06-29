# Skill Personalization Policy

Personalization is a rendering step. It must not mutate upstream skill files
with user, company, customer, path, credential, or private workflow data.

## Upstream-Safe

- Placeholder templates in `left-to-personalize/**`
- `personalization.schema.json`
- `personalize.example.yml` using placeholder values
- Generic rendering scripts and examples

## Local-Only

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

Agents initialize local overlays instead of editing skill source files:

```bash
python3 scripts/skillctl.py personalize init --skill system/skills/auto-improve
```

The default source-checkout overlay path is `.overlays/<department>/<skill>.local.yml`.

## Continuous Personalization

When an agent learns a stable user or company preference, it may update the
local overlay only:

```bash
python3 scripts/skillctl.py personalize update \
  --skill system/skills/auto-improve \
  --set company.name="Example Inc"
```

Continuous updates must not write to `SKILL.md`, references, examples, scripts,
or templates unless the change is generic and passes upstream diff
classification.
