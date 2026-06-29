# Calibration Example: Fixing Over-Verbose Code Review Agent

**Problem**: The code review agent produces responses that are 3–5× longer than necessary, adding boilerplate commentary on obvious things and burying real issues.

**Symptom**: Reviews are consistently flagging things like "consider adding more comments" and "variable naming could be improved" on well-written code, while sometimes missing actual bugs.

---

## Step 1: Document the Observed Behavior

```yaml
agent: code-reviewer
symptom: over-verbose, low signal-to-noise
example_output:
  - "The variable `user_id` is clear, but could be more descriptive"
  - "Consider adding JSDoc comments to this function"
  - "Good use of async/await here"
  - [missed: off-by-one error in loop condition]
expected_output:
  - Only flag genuine issues (bugs, security problems, architectural problems)
  - Skip praise and style commentary unless explicitly asked
  - Prioritize by severity
```

---

## Step 2: Identify the Root Cause

In this case, the agent's SKILL.md contains:

```markdown
## Behavior
Review code for quality, style, correctness, and maintainability.
```

The word "style" and "quality" are too broad — they invite commentary on anything and everything.

---

## Step 3: Tighten the Skill Definition

**Before** (SKILL.md excerpt):
```
Review code for quality, style, correctness, and maintainability. 
Flag any issues that could improve the code.
```

**After**:
```
Review code for correctness, security issues, and architectural problems.
Do not comment on style, naming, or formatting unless a linter isn't configured.
Prioritize: bugs > security > architecture > performance > style.
Skip praise. Skip observations that don't require action.
```

---

## Step 4: Test the Calibration

Run the agent on a known sample:
1. A clean, well-written function (expected: minimal output, no false positives)
2. A function with a subtle off-by-one error (expected: flag the error)
3. A function with inconsistent naming but no bugs (expected: either skip or low-priority note)

---

## Step 5: Document the Change

Add a note to `.skillmeta.yml` or a calibration log:

```yaml
calibration_history:
  - date: 2026-06-15
    change: "Narrowed review scope to correctness/security/architecture. Removed style commentary."
    reason: "Agent was too verbose and burying real issues."
    outcome: "Signal-to-noise ratio improved significantly on test samples."
```

---

## General Calibration Principles

- **Change one thing at a time** — if you adjust both the scope and the output format, you won't know which change had the effect.
- **Test on representative samples** — use real examples from past runs, not toy examples.
- **Document before and after** — calibration without a record is just churn.
- **Set a quality gate** — decide upfront what "better" looks like before you start.
