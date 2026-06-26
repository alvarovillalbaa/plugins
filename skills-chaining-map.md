# Skills Chaining Map

This map is the source of truth for the corrected strict fragmentation. Original skills remain installable parent routers or shared-methodology skills. Child skills contain lane-specific assets and execution depth.

## Rules

- Use only the children listed here; do not recreate research-suggested extras.
- Every skill directory must contain `examples/`, `hooks/`, `references/`, `scripts/`, and `templates/`.
- Empty required folders use `README.md` placeholders, not `.gitkeep`.
- `debug-investigation` is a `quality-assurance` parent reference/chain, not a child skill.
- `research` stays the shared methodology owner while specialized research skills reference it.
- External skills own duplicated general methodology, but local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

## External Chains

External skills are installed from [`references/external-skills.yaml`](references/external-skills.yaml). They track their configured upstream ref, usually `main`.

| Internal skill | External skills |
| --- | --- |
| `agentic-development` | `codex-loop`, `claude-loop`, `no-mistakes` |
| `agent-harness-improvement` | `codex-loop`, `claude-loop`, `no-mistakes` |
| `multi-agent-execution` | `codex-loop`, `claude-loop` |
| `release-landing` | `codex-loop`, `claude-loop`, `no-mistakes` |
| `prds` | `codex-loop`, `claude-loop` |
| `user-stories` | `codex-loop`, `claude-loop` |
| `quality-assurance` | `deslop`, `thermo-nuclear-code-quality-review`, `no-mistakes`, `improve` |
| `code-diff-review` | `deslop`, `thermo-nuclear-code-quality-review`, `no-mistakes`, `improve` |
| `pr-management` | `deslop`, `thermo-nuclear-code-quality-review`, `no-mistakes`, `improve` |
| `tech-debt-management` | `deslop`, `thermo-nuclear-code-quality-review`, `improve`, `codebase-design`, `improve-codebase-architecture`, `grill-with-docs`, `tdd` |
| `backend-test-engineering` | `deslop`, `thermo-nuclear-code-quality-review`, `no-mistakes`, `improve`, `codebase-design`, `improve-codebase-architecture`, `grill-with-docs`, `tdd` |
| `ci-flake-debugging` | `deslop`, `thermo-nuclear-code-quality-review`, `no-mistakes`, `improve` |
| `architecture-system-design` | `codebase-design`, `improve-codebase-architecture`, `grill-with-docs`, `tdd` |
| `test-strategy-coverage` | `codebase-design`, `improve-codebase-architecture`, `grill-with-docs`, `tdd` |
| `frontend-implementation` | `codebase-design`, `improve-codebase-architecture`, `grill-with-docs`, `tdd` |
| `frontend` | `hallmark` |
| `design-direction` | `hallmark` |
| `design-critique` | `hallmark` |
| `visual-taste-calibration` | `hallmark` |
| `ui-polish-review` | `hallmark` |
| `design-systems-components` | `hallmark` |
| `html-visual` | `hallmark` |
| `code-as-images` | `hallmark` |
| `code-slides` | `hallmark` |
| `content-writing` | `unslop`, `stop-slop` |
| `humanizing` | `unslop`, `stop-slop` |
| `copywriting` | `unslop`, `stop-slop` |
| `geo-ai-discoverability` | `unslop`, `stop-slop` |
| `message-outreach` | `unslop`, `stop-slop` |
| `sender-voice-calibration` | `unslop`, `stop-slop` |
| `x-engagement-posts` | `unslop`, `stop-slop` |
| `ux-copy-product` | `unslop`, `stop-slop` |
| `conversion-copywriting` | `unslop`, `stop-slop` |
| `code-documentation` | `unslop`, `stop-slop`, `writing-great-skills`, `teach`, `grilling`, `grill-me`, `grill-with-docs` |
| `auto-improve` | `writing-great-skills`, `teach`, `grilling`, `grill-me`, `grill-with-docs` |
| `skill-eval-loop` | `writing-great-skills`, `teach`, `grilling`, `grill-me`, `grill-with-docs` |
| `agent-doc-drift-review` | `writing-great-skills`, `teach`, `grilling`, `grill-me`, `grill-with-docs` |
| `knowledge-base-improve` | `writing-great-skills`, `teach`, `grilling`, `grill-me`, `grill-with-docs` |
| `second-brain` | `writing-great-skills`, `teach`, `grilling`, `grill-me`, `grill-with-docs` |
| `raw-ingestion` | `writing-great-skills`, `teach`, `grilling`, `grill-me`, `grill-with-docs` |

## External Owner Review

This review records why each external owner is chained and which local methodology should stay out of internal skills.

| External skill | Upstream owner scope | Internal skills | Local content superseded or reduced |
| --- | --- | --- | --- |
| `codex-loop` | Codex story/PRD execution loops with fresh agents, progress tracking, archives, and worktrees. | `agentic-development`, `agent-harness-improvement`, `multi-agent-execution`, `release-landing`, `prds`, `user-stories` | Local PRD-loop worker prompts, `prd.json` conventions, progress files, wave orchestration, and completion protocols. |
| `claude-loop` | Claude story/PRD execution loops with Task-based workers, progress tracking, archives, and worktrees. | `agentic-development`, `agent-harness-improvement`, `multi-agent-execution`, `release-landing`, `prds`, `user-stories` | Claude-specific loop and worker methodology duplicated in harness and multi-agent references. |
| `no-mistakes` | Ship/push/PR validation gates that prove intent before merge or release. | `agentic-development`, `agent-harness-improvement`, `release-landing`, `quality-assurance`, `code-diff-review`, `pr-management`, `backend-test-engineering`, `ci-flake-debugging` | Generic final-gate checklists where the external gate should be invoked for explicit ship, push, CI, or PR flows. |
| `deslop` | Branch-diff cleanup for AI-generated code slop, defensive clutter, unnecessary comments, and local style drift. | `quality-assurance`, `code-diff-review`, `pr-management`, `tech-debt-management`, `backend-test-engineering`, `ci-flake-debugging` | Local AI-code-slop review doctrine inside diff review, PR, and tech-debt references. |
| `thermo-nuclear-code-quality-review` | Severe maintainability review for wrong abstractions, spaghetti branching, shallow wrappers, and large-file pressure. | `quality-assurance`, `code-diff-review`, `pr-management`, `tech-debt-management`, `backend-test-engineering`, `ci-flake-debugging` | Duplicated harsh code-review rubrics and structural-maintainability smell lists. |
| `improve` | Read-only senior advisor audit that writes implementation plans for other agents. | `quality-assurance`, `code-diff-review`, `pr-management`, `tech-debt-management`, `backend-test-engineering`, `ci-flake-debugging` | Local architecture-audit planning flow where a non-mutating advisor plan is the better owner. |
| `codebase-design` | Deep-module vocabulary for modules, interfaces, seams, adapters, depth, leverage, and locality. | `architecture-system-design`, `tech-debt-management`, `test-strategy-coverage`, `backend-test-engineering`, `frontend-implementation` | Local deep-module and interface-design doctrine in architecture, refactor, and test strategy references. |
| `improve-codebase-architecture` | Architecture-improvement scan, report, and follow-up grilling loop. | `architecture-system-design`, `tech-debt-management`, `test-strategy-coverage`, `backend-test-engineering`, `frontend-implementation` | Duplicated architecture-improvement scan flow and refactor-candidate discovery process. |
| `grill-with-docs` | Decision interview that maintains ADRs, glossary, and domain docs. | `architecture-system-design`, `tech-debt-management`, `test-strategy-coverage`, `backend-test-engineering`, `frontend-implementation`, `code-documentation`, `auto-improve`, `skill-eval-loop`, `agent-doc-drift-review`, `knowledge-base-improve`, `second-brain`, `raw-ingestion` | Local interviewer patterns when the output must update maintained docs. |
| `tdd` | Public-interface TDD, vertical tracer bullets, one-test implementation cycles, and mocking discipline. | `architecture-system-design`, `tech-debt-management`, `test-strategy-coverage`, `backend-test-engineering`, `frontend-implementation` | Local red-green-refactor scripts, deep TDD workflow, and mocking doctrine outside backend/framework mechanics. |
| `hallmark` | Anti-AI-slop design, macrostructures, themes, typography, palettes, responsive gates, and design audits. | `frontend`, `design-direction`, `design-critique`, `visual-taste-calibration`, `ui-polish-review`, `design-systems-components`, `html-visual`, `code-as-images`, `code-slides` | Local visual taste catalogs, anti-slop UI rules, theme recipes, animation catalogs, and style presets. |
| `unslop` | Prose cleanup for AI-writing tells, filler, rhythm, jargon, passive voice, and sentence texture. | `content-writing`, `humanizing`, `copywriting`, `geo-ai-discoverability`, `message-outreach`, `sender-voice-calibration`, `x-engagement-posts`, `ux-copy-product`, `conversion-copywriting`, `code-documentation` | Generic anti-AI-writing checklists in marketing, sales, UX copy, social copy, and docs references. |
| `stop-slop` | Prose scoring and cleanup for formulaic AI writing, over-explaining, and filler patterns. | `content-writing`, `humanizing`, `copywriting`, `geo-ai-discoverability`, `message-outreach`, `sender-voice-calibration`, `x-engagement-posts`, `ux-copy-product`, `conversion-copywriting`, `code-documentation` | Local prose-polish rubrics where external prose scoring is the better owner. |
| `writing-great-skills` | Skill authoring, splitting, invocation descriptions, context-load control, and pruning. | `code-documentation`, `auto-improve`, `skill-eval-loop`, `agent-doc-drift-review`, `knowledge-base-improve`, `second-brain`, `raw-ingestion` | Local skill-writing templates, description rules, extraction checklists, and generic quality gates. |
| `teach` | Teaching workspaces, trusted resources, lessons, learning records, and learner-progress loops. | `code-documentation`, `auto-improve`, `skill-eval-loop`, `agent-doc-drift-review`, `knowledge-base-improve`, `second-brain`, `raw-ingestion` | Local lesson-construction methodology when the task is instructional rather than knowledge storage. |
| `grilling` | Structured interview loop for difficult decisions, one question at a time. | `code-documentation`, `auto-improve`, `skill-eval-loop`, `agent-doc-drift-review`, `knowledge-base-improve`, `second-brain`, `raw-ingestion` | Generic interview flow in learning and documentation skills. |
| `grill-me` | Quick challenge loop that probes assumptions before accepting an answer or plan. | `code-documentation`, `auto-improve`, `skill-eval-loop`, `agent-doc-drift-review`, `knowledge-base-improve`, `second-brain`, `raw-ingestion` | Lightweight local self-questioning checklists where the external prompt loop is sufficient. |

## Chains

### Engineering

| Parent | Children | Chains To |
| --- | --- | --- |
| `agentic-development` | `architecture-system-design`, `multi-agent-execution`, `release-landing`, `agent-harness-improvement`, `tech-debt-management` | `frontend`, `backend`, `quality-assurance`, `code-documentation`, `cloud-management`, `pr-management`, `auto-improve` |
| `ai-engineering` | `agent-system-architecture`, `prompt-tool-design`, `context-memory-rag`, `ai-evals-observability`, `ai-governance-safety`, `data-ml-pipelines`, `computer-vision-systems` | `quality-assurance/ai-evals-testing`, `quality-assurance/passive-security-review`, `backend`, `cloud-management`, `auto-improve`, `second-brain` |
| `quality-assurance` | `test-strategy-coverage`, `frontend-e2e-browser-qa`, `backend-test-engineering`, `ci-flake-debugging`, `performance-testing`, `passive-security-review`, `ai-evals-testing` | `pentest`, `ai-engineering/ai-evals-observability`, `frontend`, `backend`, `pr-management`, `cloud-management` |
| `pentest` | `web-vuln-validation`, `api-pentest`, `cloud-container-pentest`, `business-logic-race-testing`, `pentest-reporting-disclosure` | `quality-assurance/passive-security-review`, `cloud-management`, `backend` |
| `frontend` | `design-systems-components`, `frontend-performance-accessibility`, `onboarding-flows`, `ui-polish-review`, `frontend-implementation`, `visual-taste-calibration`, `design-critique`, `design-direction` | `product-development`, `product-marketing`, `quality-assurance/frontend-e2e-browser-qa`, `code-as-images`, `html-visual` |
| `cloud-management` | `cloud-resources-optimization`, `cloud-deployment-cicd`, `cloud-ops-cost-incidents`, `aws-platform-ops`, `azure-platform-ops`, `gcp-platform-ops`, `cloud-architecture-design` | `quality-assurance`, `agentic-development/release-landing`, `backend`, `ai-engineering`, `pentest/cloud-container-pentest` |
| `backend` | `api-service-design`, `database-persistence` | `quality-assurance/backend-test-engineering`, `quality-assurance/passive-security-review`, `cloud-management`, `ai-engineering` |

### Business Ops

| Parent | Children | Chains To |
| --- | --- | --- |
| `finances` | `expense-bill-ops`, `reconciliation`, `financial-planning`, `taxes`, `fundraising`, `month-end-close`, `quantitative-analysis`, `fundamentals-analysis`, `macro-analysis` | `reporting`, `research`, `product-marketing` |
| `research` | `market-competitor-research`, `diligence-vendor-research`, `customer-qual-research` | `reporting`, `go-to-market`, `product-development`, `message-outreach`, `prospect-research` |
| `review` | `code-diff-review`, `design-ux-review`, `grill` | `quality-assurance`, `frontend`, `product-development`, `pr-management` |

### Product

| Parent | Children | Chains To |
| --- | --- | --- |
| `product-development` | `product-strategy`, `discovery-prioritization`, `prds`, `product-experimentation`, `user-stories`, `ux-copy-product` | `product-marketing`, `frontend/onboarding-flows`, `quality-assurance/test-strategy-coverage`, `reporting` |
| `product-marketing` | `positioning-messaging`, `cro`, `conversion-copywriting`, `content-led-marketing`, `lead-magnets`, `buyer-psychology` | `content-writing`, `seo-and-geo`, `go-to-market`, `frontend`, `reporting` |

### Marketing

| Parent | Children | Chains To |
| --- | --- | --- |
| `content-writing` | `humanizing`, `repurposing-syndication`, `keywords`, `content-audit`, `support-to-content`, `copywriting` | `seo-and-geo/geo-ai-discoverability`, `seo-and-geo/on-page-seo-optimization`, `social-media-management`, `product-marketing` |
| `seo-and-geo` | `technical-seo-audits`, `on-page-seo-optimization`, `aeo-answer-optimization`, `geo-ai-discoverability`, `seo-competitor-gap-audit` | `content-writing`, `product-marketing/cro`, `frontend/frontend-performance-accessibility`, `reporting` |
| `social-media-management` | `x-engagement-posts`, `x-viral-launch`, `linkedin-engagement-dms` | `content-writing/repurposing-syndication`, `product-marketing/positioning-messaging`, `go-to-market/launch-gtm`, `code-as-images`, `video-generation` |
| `video-generation` | `hyperframes`, `remotion` | `content-writing`, `social-media-management`, `code-as-images`, `code-slides` |

### Sales

| Parent | Children | Chains To |
| --- | --- | --- |
| `go-to-market` | `first-customer-gtm`, `launch-gtm`, `growth-experimentation`, `technical-sales`, `revenue-intelligence`, `revenue-ops`, `customer-growth-retention`, `commercial-docs` | `product-marketing`, `product-development`, `message-outreach`, `sales-pipeline`, `prospect-research`, `research` |
| `message-outreach` | `sender-voice-calibration`, `follow-up-messaging` | `prospect-research`, `go-to-market/first-customer-gtm`, `sales-pipeline`, `auto-improve/writing-style-learning` |

### Learning System

| Parent | Children | Chains To |
| --- | --- | --- |
| `auto-improve` | `skill-eval-loop`, `memory-improve`, `knowledge-base-improve`, `writing-style-learning`, `agent-doc-drift-review` | `memory-management`, `second-brain`, `code-documentation`, `agentic-development/agent-harness-improvement`, `message-outreach/sender-voice-calibration` |
| `second-brain` | `raw-ingestion` | `auto-improve/knowledge-base-improve`, `code-documentation`, `research`, `reporting` |
