# Hooks and Scripts

This repository distinguishes hooks by **when they run**, not by the language
used to implement them.

## Boundary

| Capability | Use | Location |
| --- | --- | --- |
| Automatic work tied to a supported runtime lifecycle event | Hook registration | Claude plugin `hooks/hooks.json` or supported skill frontmatter |
| Executable implementation called by a hook | Hook-handler script | The owning plugin or skill `scripts/` directory |
| Deterministic work selected by a user, skill, command, test, or maintainer | On-demand script | The owning skill `scripts/` directory, or repository-root `scripts/` for repository-wide tooling |
| A checklist, reminder, decision rule, or review gate performed by the agent | Instruction/reference | `SKILL.md` or `references/`; never `hooks/` |

A file is not a hook merely because it is named `pre-tool.sh`, `post-run.md`, or
`session-end.sh`. It becomes hook behavior only when a supported runtime
registration points to it.

## When to develop a hook

Create a hook only when all of these are true:

1. The behavior must happen automatically at a specific lifecycle event.
2. Deterministic execution is materially safer or more reliable than an
   instruction.
3. The handler is narrowly matched, non-interactive, bounded, and fast.
4. Repeated execution will not create noisy output, duplicate writes, or hidden
   network/cost side effects.
5. The registration and handler can be tested together.

Do not create a hook for advice, routing reminders, missing-input prompts,
format preferences, or a check already enforced by the invoked script. Put
those rules in the skill and make the script fail clearly when its own input is
invalid.

## When to develop a script

Create a script when repeatable code materially improves correctness, speed, or
verification. Typical cases are parsing, validation, transformation, report
generation, scaffolding, and a stable integration boundary. Keep a workflow in
`SKILL.md` when it is primarily judgment, tool selection, or prose guidance.

Each runnable script must:

- own one clear capability and live with that owner;
- avoid hard-coded people, companies, home directories, credentials, tenant
  IDs, campaign IDs, or private endpoints;
- accept inputs through arguments, stdin, configuration, or documented
  environment variables;
- provide `--help` or a usage message when it is a user-facing CLI;
- fail loudly on invalid input and avoid destructive defaults;
- keep output/state in caller-selected or documented portable locations.

Support modules, test files, dependency manifests, and `.env.example` files may
live beside runnable scripts, but they are not counted as standalone commands.

## Runtime contract

Claude plugin-wide hooks are registered in `<plugin>/hooks/hooks.json`.
Skill-scoped Claude hooks are registered in `SKILL.md` frontmatter. A skill
distributed inside a plugin should use exec form plus `${CLAUDE_PLUGIN_ROOT}`
for its owned handler path, so installation paths and spaces do not affect
execution. Hook handlers receive the runtime event as JSON on stdin and
communicate through the event's documented exit/output contract.

The Codex and Cursor manifests in this repository do not declare equivalent
hook wiring. Therefore, a safety or data-integrity invariant must also be
enforced by the command that performs the action. Never rely on Claude-only
hook activation as the sole implementation of a cross-runtime invariant.

## Ownership and conflicts

- One canonical skill owns each executable capability.
- Two skill-local scripts may not use the same filename for overlapping
  behavior. Rename genuinely different tools and consolidate copies.
- Exact duplicate implementations are not allowed.
- Hook registrations must use the narrowest event and matcher that satisfies
  the requirement.
- Multiple hooks may observe the same event only when their effects are
  independent and their ordering is irrelevant.
- Plugin installs must not reference handlers outside the plugin root.

## Review and validation

Run the repository-wide audit after changing a hook, script, skill, or plugin:

```bash
python3 scripts/audit_hooks_scripts.py .
```

The audit inventories every department and skill, resolves every hook handler,
checks ownership conflicts and exact duplicates, rejects placeholder resource
folders and unregistered hook-like files, scans executable code for portability
violations, and can render the current coverage matrix with `--report`.

## Addition checklist

Before adding a hook or script:

1. Name the owning plugin/skill and the capability it exclusively owns.
2. Confirm an existing script or skill instruction cannot cover it.
3. Choose hook registration, hook-handler script, on-demand script, or
   instruction/reference using the table above.
4. Add direct tests for parsing, failure behavior, and side effects.
5. Document invocation in the owning skill when the script is user-facing.
6. Run the hook/script audit and the normal plugin validation suite.
