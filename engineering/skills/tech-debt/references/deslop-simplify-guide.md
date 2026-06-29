# Deslop and Simplify Guide

Two focused tools for raising code quality without changing behavior.

## Deslop — remove low-quality code

**Goal**: raise the quality bar. Remove code that is vague, noisy, brittle, or unnecessarily complex.

### What counts as slop

- **Vague names**: `data`, `stuff`, `temp`, `foo`, `handle_thing`. Names should reveal intent and domain.
- **Noise**: commented-out code, debug prints, TODOs without tickets, redundant comments that restate code.
- **Weak error handling**: swallowing exceptions, bare `except`, generic "something went wrong" messages.
- **Magic values**: literals that affect behavior without a named constant or explanation.
- **Unnecessary complexity**: over-abstraction, speculative generality, convoluted control flow.
- **Inconsistency**: mixed patterns in the same file (error handling styles, naming schemes).
- **Dead or redundant code**: unused branches, duplicate logic, unreachable code.

### Deslop checklist

**Naming and intent**
- [ ] Every name reveals purpose and domain. No `data`/`stuff`/`temp`/`thing`.
- [ ] Function names are verbs describing what the function does.
- [ ] Booleans read clearly: `is_valid`, `has_permission`, not `flag` or `check`.

**Error handling**
- [ ] No bare `except:` or silent catch-and-ignore without documented reason.
- [ ] User/API-facing errors have clear, actionable messages.
- [ ] Critical failures are logged; no logging noise for normal flow.

**Clarity and structure**
- [ ] No commented-out code.
- [ ] No debug prints.
- [ ] No magic numbers/strings — use named constants.
- [ ] Control flow uses guard clauses and early returns. No deep nesting without justification.

**Consistency**
- [ ] Matches project style (formatting, type hints, docstrings).
- [ ] Uses project patterns (services for logic, serializers for validation, unified access checks).
- [ ] No duplicate logic that already exists in shared code.

**Dead code**
- [ ] No unreachable code.
- [ ] No functions that only forward arguments with no logic.
- [ ] Unused imports and variables removed.

### What NOT to do with deslop

- Change behavior for style reasons.
- Over-engineer ("adding abstraction for quality").
- Rewrite everything at once — prefer targeted fixes.
- Skip running tests after cleanup.

## Simplify — same behavior, less code

**Goal**: achieve the same behavior with fewer lines, less duplication, simpler control flow.

### Simplification checklist

**Remove and consolidate**
- [ ] Remove unused imports, variables, functions, branches.
- [ ] Extract repeated logic into a single helper or loop.
- [ ] Replace redundant conditionals with guard clauses or early returns.
- [ ] Replace long hand-written blocks with existing utilities, list comprehensions, or library calls.

**Simplify control flow**
- [ ] Replace long if/elif chains with a dict lookup or `match`.
- [ ] Use `any`, `all`, `next`, and comprehensions where they clarify intent.

**Use what already exists**
- [ ] Check project helpers before adding new code.
- [ ] Use stdlib (`pathlib`, `dataclasses`, `functools`) over custom code.
- [ ] Use framework features (`get_or_create`, `update_or_create`, `select_related`) over hand-rolled loops.

**Shrink surface area**
- [ ] Prefer a single clear function over many wrappers that only forward arguments.
- [ ] Group related args into a small struct when there are many booleans or optional args.
- [ ] Remove indirection layers that add no value.

### What NOT to do with simplify

- Change behavior or contracts.
- Introduce a new base class or framework "for the future."
- Sacrifice readability for brevity — prefer explicit over clever.
- Break existing tests.

## Workflow

1. Scope the target: file, function, directory, or current diff.
2. Run the relevant checklist.
3. Implement targeted fixes — prefer small, reviewable changes.
4. Run `pytest -q` and `ruff check .` on the changed scope.
5. Report: slop list (file/line, severity), edits made, verification reminder.

## Output format

```
## Findings

### Correctness/Safety
- [file:line] Issue description

### Clarity
- [file:line] Issue description

### Dead code
- [file:line] Issue description

## Changes made
- [file]: [brief summary of edit]

## Verification
Run: pytest -q && ruff check .
```
