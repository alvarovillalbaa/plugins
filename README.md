# Agent Company

This repository is a company package with department-level plugins for Claude, Codex, and Cursor.

This repo is structured so people can use it in multiple ways:

- As a Claude Code plugin system through the root marketplace plus department plugins
- As a skill collection via Vercel's `npx skills`
- In Codex
- In OpenClaw
- By cloning the repo and loading it manually
- By copying only the folders you want with shell scripts
- By installing only individual skills, agents, or commands

The active departments are:

- `learning-system`
- `marketing`
- `sales`
- `engineering`
- `product`
- `business-ops`

The active agents are:

- `sales-prospecting`
- `executive`
- `deep-research`
- `financial-analyst`
- `growth-lead`
- `principal-engineer`
- `vp-of-operations`

## Install

### Install matrix

| Method | Best for | Installs |
|--------|----------|----------|
| Claude Code marketplace + department plugin | Full repo with department plugins, teams, and shared references | Marketplace plus department plugin |
| `npx skills` | Cross-agent skill install | Skills only |
| Codex manual install | One skill or a small set of skills | Skills only |
| Codex `$skill-installer` | Direct GitHub skill install inside Codex | Individual skills |
| OpenClaw manual install | Local runtime skill folders | Skills, optionally agents/commands |
| Git clone | Local development, forking, direct loading | Everything |
| Symlink / shell copy | Selective local installs | Individual folders |
| Sparse checkout | Pull only specific folders from Git | Individual folders |

### Portable skills and runtime hooks

Skills in this repo are portable across supported harnesses. Hook activation is not assumed to be portable.

Each runtime must explicitly wire its own wrapper:

- Claude: `engineering/skills/agent-harness-improvement/hooks/runtimes/claude-stop.sh`
- Cursor: `engineering/skills/agent-harness-improvement/hooks/runtimes/cursor-stop.sh`
- Codex: `engineering/skills/agent-harness-improvement/hooks/runtimes/codex-stop.sh`, only if the local Codex runtime supports stop hooks

The shared stop hook defaults to one completion gate. Multi-iteration loops are explicit and start through `/dev-loop` or `/harness-loop`, which write loop state under `.agentic/`.

### External skill chains

Some internal skills intentionally chain to external owner skills instead of
duplicating their full methodology. The live registry is
[`references/external-skills.yaml`](references/external-skills.yaml).
These external installs track the configured upstream branch, usually `main`,
not pinned commits.

Check local availability without mutating anything:

```bash
python scripts/check-external-skills.py --offline --all --agent codex
```

Install or refresh all external skills for Codex:

```bash
python scripts/install-external-skills.py --all --agent codex --force
```

Preview an install first:

```bash
bash scripts/install-external-skills.sh --dry-run --all --agent codex
```

The optional hook wrapper is `hooks/external-skills/check.sh`. It reports
missing external skills by default. It installs missing skills only when
`AGENT_COMPANY_AUTO_INSTALL_EXTERNAL_SKILLS=1` is set by the runtime or project.

### 1. Claude Code plugin

Use this when you want the full repo: root marketplace, department plugins, teams, references, commands, hooks, agents, and skills.

Claude now installs departments through the root marketplace at [`.claude-plugin/marketplace.json`](/Users/alvipe/Desktop/plugins/.claude-plugin/marketplace.json).

#### Local development

Run Claude against the department you want to work with:

```bash
claude --plugin-dir /absolute/path/to/repo/engineering
claude --plugin-dir /absolute/path/to/repo/marketing
claude --plugin-dir /absolute/path/to/repo/business-ops
```

#### Persistent install

Clone the repo once, then add the marketplace and install the department plugin you want:

```bash
mkdir -p ~/.claude/plugins
git clone https://github.com/alvarovillalbaa/plugins.git ~/.claude/plugins/agent-company
```

Inside Claude:

```text
/plugin marketplace add /absolute/path/to/repo
/plugin install engineering@agent-company
/plugin install sales@agent-company
```

If the repo is hosted on GitHub, the flow is:

```text
/plugin marketplace add alvarovillalbaa/plugins
/plugin install engineering@agent-company
/plugin install sales@agent-company
```

#### Update

```bash
cd ~/.claude/plugins/agent-company && git pull
```

### 2. Vercel `npx skills`

Use this when you want portable skill installation across supported agents.

Because the repo is now department-scoped, install from a department path or from a published skill repo that mirrors one skill.

#### Install from a local department path

```bash
npx -y skills add ./engineering
npx -y skills add ./marketing
```

#### Install all skills from selected departments globally

```bash
npx -y skills add -g ./engineering
npx -y skills add -g ./business-ops
```

#### Install for a specific agent

```bash
npx -y skills add -a codex ./engineering
npx -y skills add -a claude-code ./marketing
```

#### Install only selected skills

If your `npx skills` workflow accepts direct folder targets, point it at the skill folder:

```bash
npx -y skills add ./marketing/skills/seo-and-geo
npx -y skills add ./sales/skills/prospect-research
```

#### Install from a cloned local path

```bash
git clone https://github.com/alvarovillalbaa/plugins.git
cd plugins
npx -y skills add ./engineering
```

### 3. Codex

You still have the same three practical options: install via `npx skills`, install an individual skill manually, or use Codex `$skill-installer`.

#### Option A: install through `npx skills`

```bash
npx -y skills add -a codex ./engineering
npx -y skills add -a codex ./marketing
```

#### Option B: install a single skill manually

Copy a skill folder into your local Codex skills directory.

```bash
mkdir -p ~/.codex/skills
cp -R marketing/skills/seo-and-geo ~/.codex/skills/
cp -R engineering/skills/agentic-development ~/.codex/skills/
cp -R business-ops/skills/finances ~/.codex/skills/
```

#### Option C: install a single skill with Codex's skill installer

Inside Codex, use `$skill-installer` for repository-backed installs.

```text
$skill-installer
```

If you want a skill from this repo, prompt the installer to fetch the skill from its new department path:

```text
https://github.com/alvarovillalbaa/plugins/tree/main/engineering/skills/agentic-development
https://github.com/alvarovillalbaa/plugins/tree/main/marketing/skills/seo-and-geo
https://github.com/alvarovillalbaa/plugins/tree/main/business-ops/skills/finances
```

### 4. OpenClaw

OpenClaw users can still clone the repo and point the runtime at the specific department `skills/` directory, or copy individual skill folders.

#### Full clone

```bash
mkdir -p ~/.openclaw/skills
git clone https://github.com/alvarovillalbaa/plugins.git ~/.openclaw/skills/agent-company
```

From there, point OpenClaw at one or more department skill roots:

```text
~/.openclaw/skills/agent-company/engineering/skills
~/.openclaw/skills/agent-company/marketing/skills
```

#### Individual skill copy

```bash
mkdir -p ~/.openclaw/skills
cp -R marketing/skills/code-slides ~/.openclaw/skills/
cp -R sales/skills/prospect-research ~/.openclaw/skills/
```

Reload the runtime after install.

### 5. Git clone

Use this when you want the repo locally for development, inspection, or manual loading in any AI OS.

```bash
git clone https://github.com/alvarovillalbaa/plugins.git
cd plugins
```

From there you can:

- Load one department as a plugin if your runtime supports plugins
- Point your runtime at one or more `<department>/skills/` directories
- Copy only selected `agents/`, `commands/`, or skills
- Symlink folders into a local skill registry

### 6. Install with shell scripts

Use plain `sh` commands if you want repeatable installs without a marketplace.

#### Copy one skill

```bash
mkdir -p "$HOME/.codex/skills"
cp -R marketing/skills/seo-and-geo "$HOME/.codex/skills/"
```

#### Copy several skills

```sh
mkdir -p ~/.codex/skills
cp -R marketing/skills/seo-and-geo ~/.codex/skills/
cp -R sales/skills/prospect-research ~/.codex/skills/
cp -R business-ops/skills/research ~/.codex/skills/
```

#### Symlink for local development

```sh
mkdir -p "$HOME/.codex/skills"
ln -s "$(pwd)/engineering/skills/agentic-development" "$HOME/.codex/skills/agentic-development"
```

### 7. Install only individual skills

Every folder under `<department>/skills/` is installable on its own.

Examples:

```bash
cp -R business-ops/skills/finances ~/.codex/skills/
cp -R marketing/skills/code-slides ~/.openclaw/skills/
npx -y skills add ./sales/skills/message-outreach
```

### 8. Install only individual agents

If your runtime supports agent files, copy only the agent you want from the owning department.

Examples:

```bash
cp sales/agents/sales-prospecting.md /path/to/your/agents/
cp engineering/agents/principal-engineer.md /path/to/your/agents/
cp business-ops/agents/executive.md /path/to/your/agents/
```

The agent files reference skills by logical name, so the corresponding department skills should also be available in that runtime.

### 9. Install only individual commands

If your runtime supports command markdown files, copy only the files you need from the owning department.

Examples:

```bash
cp business-ops/commands/investor-messaging.md /path/to/your/commands/
cp marketing/commands/slides.md /path/to/your/commands/
cp engineering/commands/repo-review.md /path/to/your/commands/
```

Command support is runtime-specific. In some environments, commands are ignored while skills still work.

### 10. Sparse checkout for partial clone

Use sparse checkout if you want only one part of the repo without pulling everything.

#### One skill

```bash
git clone --filter=blob:none --no-checkout https://github.com/alvarovillalbaa/plugins.git
cd plugins
git sparse-checkout init --cone
git sparse-checkout set marketing/skills/seo-and-geo
git checkout main
```

#### Only agents and commands

```bash
git clone --filter=blob:none --no-checkout https://github.com/alvarovillalbaa/plugins.git
cd plugins
git sparse-checkout init --cone
git sparse-checkout set sales/agents engineering/agents marketing/commands business-ops/commands
git checkout main
```

### 11. Other compatible approaches

Depending on the runtime, these also work:

- Install from a local path after cloning the repo
- Use symlinks instead of copies for local development
- Fork the repo and install from your own GitHub namespace
- Vendor specific `<department>/skills/<name>` folders into another repo
- Use the repo as a template for your own internal company package

### 12. Cursor

Cursor should target a department directory because each department contains its own [`.cursor-plugin/plugin.json`](/Users/alvipe/Desktop/plugins/engineering/.cursor-plugin/plugin.json).
The Cursor plugin manifest is metadata; it does not implicitly activate hooks. Wire Cursor hooks through the runtime wrapper when a project opts into the completion gate.

Examples:

- `engineering/`
- `marketing/`
- `sales/`

## Structure

```text
agent-company/
├── .claude-plugin/marketplace.json
├── COMPANY.md
├── assets/
├── scripts/
├── references/
├── learning-system/
├── marketing/
├── sales/
├── engineering/
├── product/
└── business-ops/
```

Each department follows the same contract:

```text
department/
├── .claude-plugin/plugin.json
├── .codex-plugin/plugin.json
├── .cursor-plugin/plugin.json
├── TEAM.md
├── profile.yaml
├── skills/
├── agents/
├── commands/
├── hooks/
└── scripts/
```

## Department map

- `learning-system`: `auto-improve`, `memory-management`, `second-brain`
- `marketing`: content, SEO/GEO, social, slides, video, visual content
- `sales`: GTM, pipeline, prospect research, outreach
- `engineering`: implementation, QA, docs, security, cloud, AI engineering
- `product`: product development and product strategy support
- `business-ops`: finance, reporting, research, review, executive operating cadence

## Notes

- The repo root is no longer the Codex or Cursor plugin root.
- The repo root is the Claude marketplace root and the company package root.
- Legacy root-level manifests, hooks, agents, and commands were moved under [`references/legacy`](/Users/alvipe/Desktop/plugins/references/legacy).

## License

MIT. See [LICENSE](/Users/alvipe/Desktop/plugins/LICENSE).
