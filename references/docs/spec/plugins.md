## What are “plugins” in Claude Code?

A **Claude Code plugin** is a **shareable package** (a folder/repo) that **extends Claude Code** with one or more of:

* **Skills** (Agent Skills: `skills/<skill-name>/SKILL.md`)
* **Agents** (subagents)
* **Slash commands**
* **Hooks**
* **MCP servers** (tool connectors)
  …and it’s meant to be **reused across projects/teams** with **versioned releases**. ([Claude Code][1])

### How Claude Code knows it’s a plugin

A plugin is identified by a required manifest file:

* `/.claude-plugin/plugin.json` (required)
  Everything else (commands/, agents/, skills/, hooks/, `.mcp.json`, scripts/, etc.) lives at the **plugin root**, **not** inside `.claude-plugin/`. ([Claude Code][2])

Repo rule: this package is stricter than the general Claude plugin shape.
Department plugin roots do not contain `hooks/` or `scripts/`; hooks and helper
scripts live inside the owning skill folder, while shared repo tooling lives in
the company-root `scripts/` directory.

### Why plugins exist (vs `.claude/` per-project config)

Claude Code explicitly frames it like this:

* `.claude/` = personal or project-specific customization (short commands like `/hello`)
* **Plugins** = sharing with teammates/community, namespaced commands, versioning, reuse ([Claude Code][1])

---

## Do other AI-native coding tools support “plugins”?

Yes, but the word “plugin” means different things depending on the tool.

### VS Code + GitHub Copilot

* VS Code has a mature **extensions** ecosystem, and Copilot lives inside that environment. ([Visual Studio Code][3])
* VS Code also supports **MCP servers** as a way to add external tools to chat (alongside built-in + extension-contributed tools). MCP support is stated as generally available starting in **VS Code 1.102**. ([Visual Studio Code][4])
* Microsoft explicitly describes extending Copilot via **VS Code extensions** (and, for cross-surface chat participants, GitHub Apps via a partner program). ([Visual Studio Code][5])

### Cursor

* Cursor supports **VS Code extensions** (so its “plugin system” is effectively the VS Code extension ecosystem). ([Cursor][6])
* Cursor also supports **MCP** to connect agents to external tools/data. ([Cursor][7])

### Windsurf (Codeium)

* Windsurf provides **plugins for multiple IDEs** (JetBrains, VS Code, Visual Studio, Vim/NeoVim, etc.). ([docs.windsurf.com][8])
* They recommend their native editor or JetBrains plugin for “advanced agentic AI capabilities,” and say other plugins are under maintenance mode. ([docs.windsurf.com][8])

### Continue (VS Code / JetBrains extension)

* Continue extends via its own configuration and supports **MCP servers** to add custom tools. ([docs.continue.dev][9])

---

## Practical takeaway for Clous

If you want maximum distribution:

* **Claude Code**: publish a **plugin repo** (so teams can install once and get multiple HR skills + commands + optional MCP connectors). ([Claude Code][1])
* **VS Code/Cursor**: you’ll reach most dev teams either via **VS Code extensions** or via **MCP server configs** (tooling layer). ([Visual Studio Code][4])
* **Security**: treat plugins/MCP servers like executable supply chain—both Anthropic plugin directories and VS Code warn about trust/risk when installing tool packages/servers. ([GitHub][10])

**Reflection question:** do you want Clous’s “distribution unit” to be (1) a Claude Code plugin pack, (2) an MCP server that exposes HR workflows as tools, or (3) both?

[1]: https://code.claude.com/docs/en/plugins "Create plugins - Claude Code Docs"
[2]: https://code.claude.com/docs/en/plugins-reference "Plugins reference - Claude Code Docs"
[3]: https://code.visualstudio.com/docs/copilot/overview?utm_source=chatgpt.com "GitHub Copilot in VS Code"
[4]: https://code.visualstudio.com/docs/copilot/customization/mcp-servers "Use MCP servers in VS Code"
[5]: https://code.visualstudio.com/blogs/2024/06/24/extensions-are-all-you-need?utm_source=chatgpt.com "GitHub Copilot Extensions are all you need"
[6]: https://cursor.com/docs/configuration/extensions?utm_source=chatgpt.com "Extensions | Cursor Docs"
[7]: https://cursor.com/docs/context/mcp?utm_source=chatgpt.com "Model Context Protocol (MCP) | Cursor Docs"
[8]: https://docs.windsurf.com/plugins/getting-started "Welcome to Windsurf Plugins - Windsurf Docs"
[9]: https://docs.continue.dev/customize/mcp-tools?utm_source=chatgpt.com "MCP servers"
[10]: https://github.com/anthropics/claude-plugins-official?utm_source=chatgpt.com "Claude Code Plugins Directory"
