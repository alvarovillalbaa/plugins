# Documentation Drift Patterns Reference

Reference for detecting and fixing documentation that has fallen out of sync with code, product, or agent instructions. Drift is silent: docs don't error when they go stale, but they mislead readers and agents. Scope here includes agent instruction files (CLAUDE.md, AGENTS.md), READMEs, runbooks, and API/reference docs.

## What "drift" means

Documentation drift = a gap between what a doc *says* and what is *true now*. It accumulates whenever code/product changes ship without the corresponding doc update. For agent instruction files, drift is especially costly: an agent follows stale instructions confidently and produces wrong work.

## Common drift patterns

| Pattern | Looks like | Why it happens |
| --- | --- | --- |
| **Stale command/script** | Docs reference a script, flag, or command that was renamed/removed | Tooling changed; docs didn't |
| **Dead path/file reference** | Doc points to a file/dir that moved or no longer exists | Refactor without doc sweep |
| **Outdated API signature** | Documented params/response don't match code | API evolved |
| **Phantom feature** | Docs describe behavior that was removed or never shipped | Feature cut after docs written |
| **Missing feature** | New capability undocumented | Doc step skipped at ship time |
| **Wrong config/env** | Setup steps reference old env vars, versions, ports | Config drift |
| **Stale screenshots/examples** | UI/output examples no longer match | Visual changes |
| **Contradiction** | Two docs (or doc vs. code comment) disagree | No single source of truth |
| **Outdated ownership** | "Ask X" / "owned by team Y" no longer true | Org changes |
| **Version skew** | Docs assume an old version's behavior | Dependency upgrades |

## Detection methods

### For agent instruction files (CLAUDE.md / AGENTS.md)
- **Verify every named entity** — each command, script, path, file, function, or flag mentioned should still exist. Grep the repo for it.
- **Check setup/build/test commands actually run** — the fastest drift check is executing them.
- **Cross-check claims against code** — "we use X for Y" → confirm X is still in the dependency list / codebase.
- **Look for instructions describing removed workflows** — directories that no longer exist, steps for deprecated tools.
- **Confirm conventions still hold** — "always do X" should match what the current code actually does.

### For code/API docs
- **Compare signatures** in docs vs. source (params, types, return shapes, error codes).
- **Run documented examples** — do the code samples compile/execute and produce the stated output?
- **Diff against recent changes** — `git log` since the doc's last edit reveals what changed underneath it.
- **Check links** — internal links resolve, external links live.

### Signals that something drifted
- Doc's last-modified date much older than the code it describes.
- A referenced symbol returns zero grep hits.
- A command in the docs errors or 404s.
- Two sources state different things.
- "TODO," "coming soon," or version numbers that are now old.

## Fix workflow

1. **Confirm the drift** — verify against current reality (run it, grep it, read the code). Don't "fix" a doc that was actually right.
2. **Find the source of truth** — code is authoritative over prose; the running product is authoritative over both. Match the doc to reality, not the reverse (unless the *code* is the bug — then flag for engineering, don't paper over it).
3. **Make the smallest correct edit** — update the stale fact; don't rewrite the whole doc unless it's pervasively wrong.
4. **Check for siblings** — the same stale fact often appears in multiple docs; fix all instances.
5. **Note ownership** — if a doc has an owner, route the fix or flag them rather than silently editing critical instructions.
6. **Resolve contradictions** by establishing one canonical location and pointing others to it.

## What to flag vs. fix

- **Fix directly**: clear factual drift with an unambiguous correct value (renamed command, moved path, wrong version).
- **Flag for owner**: ambiguous cases, where the *code* might be the bug, deprecations needing a product decision, or critical instruction files where a wrong edit is risky.
- **Never** invent the "correct" content — if you can't verify the current truth, surface the gap rather than guessing.

## Report format

For each drift finding:
> **Doc** (path) · **Claim** (what it says) · **Reality** (what's true now, with evidence) · **Severity** (misleading agents/users? blocking?) · **Fix** (the correction or who should make it).

Prioritize: instruction files agents rely on > setup/onboarding docs > API references > everything else. A stale CLAUDE.md misleads every future session — fix those first.

## Prevention notes (advisory)

- Docs that name volatile specifics (paths, commands, versions) drift fastest — prefer pointing to a single source over duplicating values.
- Tie doc updates to the change that caused them (mention in the PR description) so they ship together.
- A doc-drift sweep is worth running on each release or major refactor.
