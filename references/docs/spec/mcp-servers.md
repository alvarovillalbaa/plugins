In Claude Code **there’s no required `mcp/` folder**.

What matters is **one file at the plugin root**:

* `./.mcp.json` **or**
* an inline `"mcpServers": { ... }` block in `./.claude-plugin/plugin.json`

And then *you* choose where the actual server code/binary lives (docs commonly use `servers/`). ([Claude Code][1])

---

## Recommended plugin layout (with bundled MCP server)

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
├── .mcp.json
├── servers/
│   └── agent-company/
│       ├── dist/
│       │   └── server.js
│       ├── package.json
│       └── README.md
└── skills/
    └── hiring-intake/
        └── SKILL.md
```

Why `servers/`? It’s the convention shown in Claude Code’s plugin docs, and it keeps “executable stuff” clearly separated from skills/content. ([Claude Code][1])

---

## `.mcp.json` example (points to your bundled server)

This is the **standard** format Claude Code expects in plugins:

```json
{
  "mcpServers": {
    "agent-company": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/servers/agent-company/dist/server.js"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}",
      "env": {
        "AGENT_COMPANY_API_URL": "${AGENT_COMPANY_API_URL}",
        "AGENT_COMPANY_API_KEY": "${AGENT_COMPANY_API_KEY}"
      }
    }
  }
}
```

Key rules:

* Use `${CLAUDE_PLUGIN_ROOT}` for plugin-relative paths. ([Claude Code][1])
* Plugin MCP servers **start automatically when the plugin is enabled**. ([Claude Code][2])

---

## If you *insist* on an `mcp/` folder

You can do it—Claude Code doesn’t care about the folder name. Just point `.mcp.json` to it:

```
my-plugin/
├── .mcp.json
├── mcp/
│   └── agent-company-server.js
...
```

```json
{
  "mcpServers": {
    "agent-company": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/mcp/agent-company-server.js"]
    }
  }
}
```

But again: docs/examples lean toward `servers/`. ([Claude Code][1])

---

## Alternative: don’t bundle code, run a published server via `npx`

Useful if you ship the MCP server as an npm package:

```json
{
  "mcpServers": {
    "agent-company": {
      "command": "npx",
      "args": ["-y", "@agent-company/mcp", "--mode", "plugin"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}"
    }
  }
}
```

This pattern is also shown in the plugin docs. ([Claude Code][1])
Tradeoff: it depends on network + supply chain trust.

---

**Reflection question:** do you want your agent-company plugin to ship **real tools** through MCP, or stay **instruction-only** with skills that output portable artifacts?

[1]: https://code.claude.com/docs/en/plugins-reference "Plugins reference - Claude Code Docs"
[2]: https://code.claude.com/docs/en/mcp "Connect Claude Code to tools via MCP - Claude Code Docs"
