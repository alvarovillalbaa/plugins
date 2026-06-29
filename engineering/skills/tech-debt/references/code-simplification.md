# Code Simplification

External owner boundary:

- Use `deslop` for AI-code cleanup and local style slop.
- Use `thermo-nuclear-code-quality-review` for aggressive structural simplification and maintainability review.
- Use `codebase-design` for deep-module vocabulary.
- Use `improve-codebase-architecture` when the task is to discover architecture-deepening candidates.

This local reference only defines how to scope a simplification pass and keep behavior unchanged.

## Scope

Resolve scope in this order:

1. User-named file, directory, function, or diff.
2. Branch diff against the configured upstream or default branch.
3. Most recently modified files mentioned in the conversation.

If the scope is empty or ambiguous, stop and ask before editing.

## Local simplification rules

- Preserve behavior unless fixing a proven bug.
- Prefer deleting duplicate or unused code over adding abstraction.
- Prefer existing canonical helpers over near-duplicates.
- Keep commits and verification scoped to the simplification target.
- Record any skipped finding with the evidence that made it a false positive.

## External chain points

Use the external owner skill before making broad cleanup changes:

| Need | External skill |
| --- | --- |
| Remove obvious AI-code residue | `deslop` |
| Challenge structure, branching, file size, abstractions | `thermo-nuclear-code-quality-review` |
| Decide whether a module is shallow or deep | `codebase-design` |
| Produce candidate architecture refactors | `improve-codebase-architecture` |

Do not restate those skills' checklists here.

## Verification

After simplification:

1. Run typecheck and lint when available.
2. Run focused tests for changed paths.
3. Broaden tests if the changed module is shared.
4. If no verification command exists, say so explicitly.

Never relax assertions, weaken types, or skip tests to make a simplification pass.
