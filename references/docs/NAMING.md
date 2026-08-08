# Naming Conventions

These rules keep skills, agents, and commands consistent and discoverable.

## Skills

- Use short hyphen-case names.
- Keep one primary job per skill.
- Prefer durable domain nouns or verb-noun names.
- Avoid overlapping synonyms across skills.

Examples:

- `blog-articles`
- `prospect`
- `slides`
- `quality-assurance`

## Agents

- Use concise role or workflow names.
- Agents orchestrate multiple skills and commands; they do not replace skills.
- Keep each agent focused on one workflow family.
- Give every agent an explicit `Scope` declaration plus `Primary skills` and `Routing boundaries` sections.
- Cover every same-plugin skill through at least one agent while rejecting duplicate roles and documenting intentional high-overlap handoffs.
- Keep agents reusable: organization, user, account, and workspace specifics are runtime context, never embedded defaults.

See [`agents.md`](agents.md) for the complete coverage, conflict, and portability contract.

Examples:

- `principal-engineer`
- `pr-reviewer`
- `growth-lead`
- `financial-analyst`
- `memory-analyst`
- `product-manager`
- `designer`

## Commands

- Commands should represent a narrow end-to-end automation or a stable slice of a larger workflow.
- Prefer action-oriented names that describe the outcome.
- Avoid vague mega-commands when the real work splits into distinct outputs.
- Do not reuse the public name of a same-plugin skill; the skill owns that invocation and shadows the command.
- Register every command's unique capability, canonical skill owner, and exclusion boundary in `../command-capabilities.json`.

Examples:

- `blog-draft`
- `social-pack`
- `investor-messaging`
- `materials-audit`
- `pipeline-diagnostics`
- `repo-review`
