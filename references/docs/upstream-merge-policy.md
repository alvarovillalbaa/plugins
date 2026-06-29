# Upstream Merge Policy

Auto-improvement proposes changes. It does not push directly to `main`.

## Classifications

| Class | Goes upstream? | Examples |
| --- | --- | --- |
| Upstream-safe | Yes | generic SKILL.md guidance, scripts, references, evals |
| Personalization-template | Yes | placeholders, schemas, example values |
| Local/private | No | company data, local paths, customer context, credentials |
| Generated/runtime | No | rendered output, logs, caches, runtime installs |

Only upstream-safe and personalization-template changes can be proposed upstream.

## Flow

1. Locate nearest `.skillmeta.yml`.
2. Trace target path to source owner.
3. Classify changed files.
4. Fail closed if forbidden paths or likely private data appear.
5. Generate a patch bundle by default.
6. Open a PR only when the user has authenticated GitHub tooling and explicitly
   selects PR mode.

```bash
python3 scripts/skillctl.py trace-origin system/skills/auto-improve
python3 scripts/skillctl.py diff-classify --base origin/main --head HEAD --fail-on-private
python3 scripts/skillctl.py propose-upstream --mode patch --title "Improve auto-improve skill"
```

## Branches

Use branch names like:

```text
auto-improve/<skill-name>/<short-topic>
```

Use git worktrees for long-running or risky improvements so the main checkout
stays reviewable.
