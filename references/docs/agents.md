# Agent Design and Coverage

Agents are reusable orchestrators for multi-step work. Skills remain the atomic capability owners; an agent selects and coordinates those skills without copying their instructions.

## Coverage contract

- Every skill listed in a plugin's `profile.yaml` must appear under `## Primary skills` in at least one agent from the same plugin.
- Every agent file must be listed in that plugin's `profile.yaml`.
- Agent names use concise role or workflow language and remain unique across the repository.
- A plugin may use one broad orchestrator when its capabilities form one coherent workflow family; headcount alone is not a reason to duplicate an agent.

## Conflict contract

- A `Scope` declaration states the workflow family the agent owns.
- `## Routing boundaries` states where that ownership ends and names the adjacent agent used for handoff.
- Agents with substantial skill overlap must name each other in mutual routing boundaries.
- Exact duplicate primary-skill sets are rejected because they provide no reliable routing signal.
- Strategy, orchestration, execution, and review may share supporting skills when their decision rights and output contracts are distinct.

## Portability contract

- Supply organization, product, user, paths, accounts, and preferences at runtime.
- Do not embed named organizations, maintainer identities, personal email addresses, or absolute home-directory paths.
- Keep plugin-relative paths only when the agent executes a workflow shipped by that plugin.
- Use reusable context labels such as organization, customer, account, project, and workspace.

## Verification

```bash
python3 scripts/audit_agents.py .
```

The audit enforces profile parity, complete same-plugin skill coverage, resolvable skills, required scope and boundary sections, duplicate/high-overlap checks, bounded agent size, and portability rules.

See [`agents-review.md`](agents-review.md) for the current portfolio decisions and plugin-by-plugin coverage evidence.
