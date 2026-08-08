# Plugins Management

Manage the repository's plugin and skill taxonomy, lifecycle, manifests, metadata, external sources, and capability-preserving consolidations.

## Use this for

- auditing plugin and skill inventories
- renaming, folding, or removing skills without losing useful assets
- resolving overlapping ownership in `skills-chaining-map.md`
- maintaining profiles, manifests, external registries, and validation rules
- routing skill evaluation work to `skill-eval-loop`

## Install

Preferred project-local install:

```bash
cd /path/to/your-project
/path/to/plugins/scripts/plugins install \
  --project . --yes skill:system/plugins-management
```

This preserves provenance and installs into
`.agents/skills/plugins-management/`. Secondary skill-only methods remain
available when a runtime cannot use the shared project layout:

```bash
npx -y skills add https://github.com/alvarovillalbaa/plugins/tree/main/system/skills/plugins-management
```
