## Quick Start

### 1. Keep a source clone

```bash
git clone https://github.com/alvarovillalbaa/plugins.git ~/.local/share/clous-plugins
```

### 2. Run the favorite interactive installer

```bash
cd /path/to/your-project
~/.local/share/clous-plugins/scripts/plugins install
```

Choose one or more of `system`, `marketing`, `sales`, `engineering`, `product`,
`finances`, and `productivity`. For each plugin, install everything or select
individual skills, commands, rules, and agents. The command previews the flat
`.agents` plan before writing.

For a non-interactive install:

```bash
~/.local/share/clous-plugins/scripts/plugins install \
  --project . --yes \
  plugin:system skill:marketing/seo command:marketing/content-brief
```

### 3. Optional platform-native methods

#### Claude

Use the root marketplace when you specifically want Claude's namespaced plugin
and cache model:

```text
/plugin marketplace add <owner>/<repo>
/plugin install engineering@agent-company
```

For local plugin development:

```bash
claude --plugin-dir "$(pwd)/engineering"
```

#### Codex

Use Codex's marketplace flow when you specifically want its global plugin cache
and native plugin selector:

```bash
codex plugin marketplace add alvarovillalbaa/plugins
codex plugin add engineering@agent-company
```

For a durable project install, prefer step 2 so commands, rules, agents,
personalization, provenance, and safe updates are installed with the skills.

#### Cursor

Use the department directory that contains `.cursor-plugin/plugin.json`.

### 4. Update without losing local work

```bash
git -C ~/.local/share/clous-plugins pull --ff-only
~/.local/share/clous-plugins/scripts/plugins update --project /path/to/your-project
```

If the update reports a conflict, explicitly export a review-only bundle:

```bash
~/.local/share/clous-plugins/scripts/plugins reconcile \
  --project /path/to/your-project
```

The default bundle lives under `.agents/.updates/reconcile/` and contains the
available base, local, and incoming context plus a provider-neutral review
prompt. The command never invokes AI, applies a suggestion, or changes managed
targets. Review and apply any proposed resolution manually. If a semantic
component merge does not naturally converge through `update`, explicitly adopt
its current local value after review:

```bash
~/.local/share/clous-plugins/scripts/plugins reconcile \
  --project /path/to/your-project \
  --accept-local <conflict-id>
```

This previews the metadata change and asks for confirmation; it never edits the
component. Managed `AGENTS.md` and `README.md` blocks cannot be adopted this
way—restore their generated content and keep customization outside the markers.

### 5. Company-level entry points

- [Complete installation guide](references/docs/INSTALLATION.md)
- [Company model](COMPANY.md)
- [Architecture](references/docs/ARCHITECTURE.md)
- [Machine-readable catalog](catalog.json)
- [Full LLM catalog](llms-full.txt)
- [Claude marketplace](.claude-plugin/marketplace.json)
