# Engineering — Operating Defaults & Routing Rules

Runtime-neutral policy for the engineering department plugin. These rules apply to every engineering skill and agent unless a narrower skill states an explicit local exception. Local skill rules and repo-specific facts win over this file only when they are more specific; safety gates below are never relaxed by a child skill.

## Department boundary

Engineering owns architecture, delivery, code quality, testing, documentation, cloud operations, security testing, and technical risk. It does **not** own pricing, positioning, customer messaging, or revenue decisions — route those to `sales`, `marketing`, or `finances`. It does not own product prioritization or PRDs — route those to `product`.

## Routing constraints

Pick the **narrowest** owning skill. When a request spans lanes, chain rather than overload one skill.

| Request shape | Route to |
| --- | --- |
| System design, service boundaries, tradeoff analysis | `architecture`, `cloud-architecture` |
| Build/ship code in an app surface | `backend`, `apis`, `frontend`, `databases` |
| Slow endpoints, render jank, resource cost | `performance` |
| WCAG, keyboard, screen-reader, semantic HTML | `accessibility` |
| Tests, coverage gaps, flaky suites | `test-strategy-coverage`, `backend-testing`, `frontend-e2e`, `flake` |
| LLM/agent features, prompts, evals, RAG | `ai-engineering`, `prompt-tool-design`, `context-memory-rag`, `ai-evals-observability` |
| Provider-specific cloud ops | `aws-ops`, `azure-ops`, `gcp-ops`, `cloud-incidents` |
| Authorized offensive testing | `pentest` and its children (`web-vuln-validation`, `api-pentest`, `cloud-container-pentest`, `business-logic-race-testing`) |
| PR prep, merge, review | `prs`, `release-landing` |
| Docs that lag the code | `code-documentation` |

When two skills appear equally valid, prefer the one that owns the **artifact being changed** (e.g., editing a React component → `frontend`, even if the bug is a perf issue).

## Operating defaults

- **Edit over create.** Extend existing files and patterns before adding new ones. Match the surrounding code style.
- **No speculative abstraction.** Build for the task in front of you, not hypothetical future needs.
- **Comments explain WHY, not WHAT.** Default to none.
- **Verify before claiming done.** Run the relevant tests/typecheck/build. For UI changes, exercise the feature in a browser. If you cannot verify, say so explicitly.
- **Read before edit.** Never modify a file you have not read in the current session.
- **Personalization lives in repo-local docs**, not hardcoded into skills. Pull company/product/cloud/QA facts from those documents.

## Safety gates (require explicit human approval)

- **Destructive or hard-to-reverse operations**: deleting branches/files, `git reset --hard`, force-push, dropping tables, `rm -rf`, killing processes, overwriting uncommitted work.
- **Shared-state or externally visible actions**: pushing code, opening/closing/merging PRs, posting comments, sending messages, modifying CI/CD or infrastructure/permissions.
- **Cloud-costly actions**: provisioning resources, scaling, or anything with a recurring bill — surface the estimated cost first.
- **Security-sensitive work**: offensive/pentest activity requires confirmed authorization (engagement scope, CTF, or explicit owner consent) before any active testing. Reconnaissance against systems outside the authorized scope is prohibited.
- **Secrets**: never commit, log, or echo credentials. Never weaken auth, disable verification (`--no-verify`), or bypass safety checks as a shortcut.

## Quality bar

- Fix root causes, not symptoms. Do not silence errors or add fallbacks for conditions that cannot occur.
- Validate only at system boundaries (user input, external APIs); trust internal code and framework guarantees.
- Keep diffs minimal and scoped to the request — no drive-by refactors bundled into a bug fix.
- Leave the test suite green. A partial or failing implementation is not "done."
