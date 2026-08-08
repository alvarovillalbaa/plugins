# Engineering — Operating Defaults & Routing Rules

Runtime-neutral policy for the engineering plugin. These rules apply to every engineering skill and agent. Platform safety requirements and the user's explicitly authorized scope take precedence; narrower skills may add compatible implementation detail but may not relax the authorization gates or contradict the ownership boundaries below.

## Department boundary

Engineering owns technical architecture, multi-agent execution, AI systems and evaluation, software delivery, code quality, testing, documentation, cloud operations, security engineering, and technical risk. It does not own product prioritization, positioning, pricing economics, customer messaging, or revenue decisions; route those decisions to the Product, Finances, Marketing, or Sales plugin and return to Engineering for implementation.

## Routing constraints

Pick the **narrowest** owning skill. When a request spans lanes, chain rather than overload one skill.

| Request shape | Route to |
| --- | --- |
| System design, service boundaries, tradeoff analysis | `architecture`, `cloud-architecture` |
| End-to-end technical delivery, harness setup, or technical-debt reduction | `agentic-development`, `agent-harness`, `tech-debt` |
| Multi-perspective expert deliberation and one evidence-led ruling | `council` through `multi-agent` |
| Bounded inspect-act-verify-adapt execution of one concrete task | `agentic-loops` through `multi-agent` |
| Dependency-shaped parallel execution, handoffs, and dynamic replanning | `agentic-graphs` through `multi-agent` |
| Explicit durable outcome pursued and resumed across turns | `agentic-goals` through `multi-agent` |
| Build/ship code in an app surface | `backend`, `apis`, `frontend`, `databases` |
| Frontend performance, accessibility, or onboarding UX | `performance`, `accessibility`, `onboarding-flows` through `frontend` |
| LLM/agent features, prompts, context, and RAG | `ai-engineering`, `agent-system-architecture`, `prompt-engineering`, `context-engineering` |
| AI governance, model risk, human oversight, and safety controls | `ai-governance-safety` |
| Data/ML pipelines or computer-vision systems | `data-ml-pipelines`, `computer-vision` |
| AI scenarios, datasets, graders, calibration, experiments, and release gates | `ai-evals` |
| Production AI traces, score monitoring, drift signals, and debugging telemetry | `ai-evals-observability` |
| Cloud resources, delivery pipelines, incidents, or provider operations | `resources`, `cicd`, `cloud-incidents`, `aws-ops`, `azure-ops`, `gcp-ops` through `cloud` |
| Authorized offensive testing | `pentest` and its children (`web-vuln-validation`, `api-pentest`); use `testing` for business-logic and race tests |
| Defensive security review and threat reduction | `security` through `quality-assurance` |
| Test strategy, backend suites, frontend E2E, coverage, and flakes | `testing`, `frontend-e2e`, `flake` through `quality-assurance` |
| Code simplification without behavior changes | `simplify` through `quality-assurance` |
| PR prep, merge, review, and release readiness | `prs`, `release-landing` |
| Docs that lag the code | `code-documentation` |

When two skills appear equally valid, prefer the one that owns the **artifact being changed** (e.g., editing a React component → `frontend`, even if the bug is a perf issue).

Use `system/loops` for repeatable improvement, evaluation, monitoring, memory, learning, and experimentation programs. Use `agentic-loops` for bounded dynamic execution of one concrete technical task. Do not route solely on the word “loop.”

## Operating defaults

- **Edit over create.** Extend existing files and patterns before adding new ones. Match the surrounding code style.
- **No speculative abstraction.** Build for the task in front of you, not hypothetical future needs.
- **Comments explain WHY, not WHAT.** Default to none.
- **Verify before claiming done.** Run the relevant tests/typecheck/build. For UI changes, exercise the feature in a browser. If you cannot verify, say so explicitly.
- **Read before edit.** Never modify a file you have not read in the current session.
- **Context is supplied, not embedded.** Pull organization-, project-, environment-, and preference-specific facts from user-provided or workspace-local sources; never hardcode them into reusable rules.

## Authorization gates

The request may authorize scoped local implementation. Obtain confirmation at the point of action for anything destructive, externally visible, shared-state, security-sensitive, or cost-bearing that the request did not already authorize exactly.

- **Destructive or hard-to-reverse operations**: confirm exact targets before deleting branches or files, force-pushing, dropping data, killing processes, or overwriting uncommitted work. Prefer recoverable operations.
- **Shared-state or externally visible actions**: confirm before pushing code, opening/closing/merging pull requests, posting comments, sending messages, deploying, or applying CI/CD, infrastructure, or permission changes. Editing local configuration within an authorized implementation is not itself an external action.
- **Cloud-costly actions**: surface the estimated cost and confirm before provisioning, scaling, or starting a recurring bill.
- **Security-sensitive work**: active offensive testing requires confirmed authorization and a bounded target/scope. Reconnaissance outside that scope is prohibited.
- **Secrets**: never commit, log, or echo credentials. Never weaken authentication, disable verification, or bypass safety checks as a shortcut.

## Quality bar

- Fix root causes, not symptoms. Do not silence errors or add fallbacks for conditions that cannot occur.
- Validate untrusted input at trust boundaries. Add internal invariant checks only where a realistic failure mode justifies them; do not duplicate framework guarantees mechanically.
- Keep diffs minimal and scoped to the request — no drive-by refactors bundled into a bug fix.
- Leave the test suite green. A partial or failing implementation is not "done."
