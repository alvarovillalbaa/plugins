# External Skills Hook

This hook checks whether live external skills from `references/external-skills.yaml`
are installed for the selected runtime.

It is intentionally report-only by default. Set
`AGENT_COMPANY_AUTO_INSTALL_EXTERNAL_SKILLS=1` only when the runtime is allowed
to install missing external skills during hook execution.

Example:

```bash
hooks/external-skills/check.sh --agent codex --offline
```

Runtime integration is explicit. Do not assume Claude, Cursor, Codex, or any
other harness activates this hook automatically.
