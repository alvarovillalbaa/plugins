# Skills Chaining Map

This map is the source of truth for the canonical skill taxonomy. Old slugs were hard-renamed; do not recreate old alias skills. Preserve capability by moving, merging, or routing content through the canonical owners below.

## Rules

- Parent skills remain compact routers.
- Child skills contain lane-specific assets and execution depth.
- `Children` means ownership. Route-only delegation belongs in `Chains To`.
- `parent/child` notation is valid only when the child is owned by that parent in this map.
- Every skill directory must contain `examples/`, `hooks/`, `references/`, `scripts/`, and `templates/`.
- Empty required folders use `README.md` placeholders.
- Local skill rules, repo facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.
- `alvarovillalbaa/plugins` is the canonical upstream source. Runtime installs, caches, rendered overlays, and local personalization files are not source owners.
- Engineering and product-spec work should chain to `quality-assurance` and `code-documentation` by default unless the task is explicitly read-only, trivial, or the user forbids tests/docs.
- Prefer hard cuts over compatibility residue: no backfills, compatibility shims, backward-compat aliases, facade layers, or routing files unless the user explicitly opts into a temporary production-migration path.
- Treat wrong data payload shapes as producer bugs. Do not hide them with frontend normalization or payload transformations; fix the canonical owner and reject invalid shapes at the boundary.
- Product specs are manually driven or externally driven product contracts. Keep them focused on user outcomes, scope, success criteria, and acceptance; include only small technical hints needed to prevent obvious implementation mistakes.
- For UI work, defer Fluid Functionalism details to the `fluid-functionalism` reference source; keep local skills focused on repo, product, and channel constraints.

## External Chains

External skills are installed from [`references/external-skills.yaml`](references/external-skills.yaml). Reference-only sources live in [`references/external-sources.yaml`](references/external-sources.yaml). Installable skills track their configured upstream ref, usually `main`.

| Internal skill | External skills |
| --- | --- |
| `agentic-development` | `codex-loop`, `claude-loop`, `ralph`, `no-mistakes`, `how-to-ralph-wiggum`, `ralph-playbook`, `clous-agent-runs`, `clous-platform-operation` |
| `agent-harness` | `codex-loop`, `claude-loop`, `ralph`, `no-mistakes`, `use-afs`, `clous-agent-runs` |
| `multi-agent` | `codex-loop`, `claude-loop`, `ralph`, `clous-agent-runs` |
| `release-landing` | `codex-loop`, `claude-loop`, `ralph`, `no-mistakes`, `clous-sdk-release` |
| `loops` | `codex-loop`, `claude-loop`, `ralph`, `no-mistakes` |
| `prds` | `codex-loop`, `claude-loop`, `ralph-prd`, `ralph-playbook` |
| `user-stories` | `codex-loop`, `claude-loop`, `ralph-prd`, `ralph-playbook` |
| `quality-assurance` | `deslop`, `thermo-nuclear-code-quality-review`, `no-mistakes`, `improve`, `browserbase-ui-test` |
| `code-review` | `deslop`, `thermo-nuclear-code-quality-review`, `no-mistakes`, `improve` |
| `prs` | `deslop`, `thermo-nuclear-code-quality-review`, `no-mistakes`, `improve` |
| `tech-debt` | `deslop`, `thermo-nuclear-code-quality-review`, `improve`, `codebase-design`, `improve-codebase-architecture`, `grill-with-docs`, `tdd` |
| `backend-testing` | `deslop`, `thermo-nuclear-code-quality-review`, `no-mistakes`, `improve`, `codebase-design`, `improve-codebase-architecture`, `grill-with-docs`, `tdd` |
| `flake` | `deslop`, `thermo-nuclear-code-quality-review`, `no-mistakes`, `improve` |
| `architecture` | `codebase-design`, `improve-codebase-architecture`, `grill-with-docs`, `tdd` |
| `test-strategy-coverage` | `codebase-design`, `improve-codebase-architecture`, `grill-with-docs`, `tdd` |
| `backend` | `clous-a2a-integration`, `clous-api-integration`, `clous-api-use`, `clous-oauth-integration`, `clous-webhook-integration`, `clous-webhook-operations`, `browserbase-browser-to-api` |
| `apis` | `clous-a2a-integration`, `clous-api-integration`, `clous-api-use`, `clous-oauth-integration`, `clous-webhook-integration`, `clous-webhook-operations`, `browserbase-browser-to-api` |
| `cloud` | `clous-remote-mcp-integration`, `clous-platform-operation`, `clous-mcp-use`, `browserbase-cli` |
| `cicd` | `clous-cli-integration`, `clous-cli-use`, `clous-sdk-release`, `browserbase-cli` |
| `prompt-tool-design` | `browserbase-webmcp-gen`, `browserbase-functions`, `clous-mcp-use` |
| `context-memory-rag` | `clous-knowledge-retrieval`, `use-afs` |
| `ai-engineering` | `browserbase-agent-experience`, `browserbase-webmcp-gen`, `browserbase-functions`, `clous-agent-runs` |
| `frontend` | `hallmark`, `taste-skill`, `impeccable`, `emil-design-eng`, `userinterface-wiki`, `transitions-dev`, `animate-text`, `browserbase-browser`, `browserbase-safe-browser`, `fluid-functionalism` |
| `frontend-e2e` | `browserbase-ui-test`, `browserbase-browser`, `browserbase-browser-trace`, `browserbase-autobrowse`, `browserbase-safe-browser`, `browserbase-browser-to-api`, `browserbase-cookie-sync`, `browserbase-browser-use-to-stagehand` |
| `accessibility` | `userinterface-wiki`, `browserbase-ui-test`, `hallmark` |
| `performance` | `userinterface-wiki`, `review-animations`, `transitions-dev`, `browserbase-browser-trace` |
| `onboarding-flows` | `hallmark`, `taste-skill`, `userinterface-wiki`, `browserbase-ui-test` |
| `design` | `hallmark`, `taste-skill`, `taste-skill-v1`, `gpt-tasteskill`, `impeccable`, `emil-design-eng`, `userinterface-wiki`, `fluid-functionalism` |
| `direction` | `hallmark`, `brandkit`, `taste-skill`, `impeccable`, `fluid-functionalism` |
| `critique` | `hallmark`, `review-animations`, `userinterface-wiki`, `impeccable` |
| `taste` | `hallmark`, `taste-skill`, `taste-skill-v1`, `gpt-tasteskill`, `brutalist-skill`, `minimalist-skill`, `soft-skill`, `output-skill`, `impeccable`, `fluid-functionalism` |
| `polish` | `hallmark`, `redesign-skill`, `impeccable`, `emil-design-eng`, `review-animations` |
| `design-systems` | `hallmark`, `brandkit`, `userinterface-wiki`, `impeccable`, `emil-design-eng` |
| `visualization` | `hallmark`, `visual-explainer`, `frontend-slides`, `userinterface-wiki` |
| `images` | `hallmark`, `visual-explainer`, `image-to-code-skill`, `imagegen-frontend-web`, `imagegen-frontend-mobile`, `stitch-skill` |
| `slides` | `hallmark`, `frontend-slides`, `visual-explainer` |
| `video` | `manim-video`, `animate-text`, `transitions-dev`, `review-animations` |
| `remotion` | `manim-video`, `animate-text`, `transitions-dev`, `review-animations` |
| `hyperframes` | `animate-text`, `transitions-dev`, `review-animations` |
| `content` | `unslop`, `stop-slop` |
| `humanizing` | `unslop`, `stop-slop` |
| `copywrite` | `unslop`, `stop-slop` |
| `geo` | `unslop`, `stop-slop` |
| `outreach` | `unslop`, `stop-slop` |
| `voice` | `unslop`, `stop-slop` |
| `x-posts` | `unslop`, `stop-slop` |
| `x-articles` | `unslop`, `stop-slop` |
| `linkedin-posts` | `unslop`, `stop-slop` |
| `linkedin-articles` | `unslop`, `stop-slop` |
| `communication-style` | `unslop`, `stop-slop` |
| `code-documentation` | `unslop`, `stop-slop`, `writing-great-skills`, `teach`, `grilling`, `grill-me`, `grill-with-docs`, `visual-explainer` |
| `auto-improve` | `writing-great-skills`, `teach`, `grilling`, `grill-me`, `grill-with-docs`, `codebase-design`, `improve-codebase-architecture`, `tdd`, `use-afs`, `codex-loop`, `no-mistakes` |
| `skills-management` | `writing-great-skills`, `teach`, `grilling`, `grill-me`, `grill-with-docs`, `use-afs` |
| `skill-eval-loop` | `writing-great-skills`, `teach`, `grilling`, `grill-me`, `grill-with-docs`, `use-afs` |
| `documentation-drift` | `writing-great-skills`, `teach`, `grilling`, `grill-me`, `grill-with-docs`, `use-afs` |
| `knowledge-base` | `writing-great-skills`, `teach`, `grilling`, `grill-me`, `grill-with-docs`, `use-afs`, `clous-knowledge-retrieval` |
| `brain` | `writing-great-skills`, `teach`, `grilling`, `grill-me`, `grill-with-docs`, `use-afs`, `clous-knowledge-retrieval` |
| `ingestion` | `writing-great-skills`, `teach`, `grilling`, `grill-me`, `grill-with-docs`, `use-afs`, `clous-knowledge-retrieval` |
| `memory` | `use-afs`, `writing-great-skills`, `teach` |
| `learning` | `teach`, `writing-great-skills` |
| `lessons` | `teach`, `writing-great-skills` |
| `research` | `last30days`, `browserbase-search`, `browserbase-fetch`, `browserbase-company-research`, `browserbase-competitor-analysis` |
| `market-competitor-research` | `last30days`, `browserbase-competitor-analysis`, `browserbase-search`, `browserbase-fetch` |
| `customer-qual-research` | `last30days`, `browserbase-company-research`, `browserbase-search`, `browserbase-fetch` |
| `prospect` | `last30days`, `browserbase-company-research`, `browserbase-event-prospecting`, `browserbase-search`, `browserbase-fetch` |
| `seo-competitor-gap` | `browserbase-search`, `browserbase-fetch`, `browserbase-competitor-analysis` |
| `diligence-vendor-research` | `last30days`, `browserbase-company-research`, `browserbase-search`, `browserbase-fetch` |
| `go-to-market` | `last30days`, `office-hours`, `browserbase-company-research`, `browserbase-competitor-analysis`, `browserbase-event-prospecting` |
| `first-customers` | `office-hours`, `browserbase-company-research`, `browserbase-event-prospecting` |
| `technical-sales` | `clous-api-use`, `clous-platform-operation`, `browserbase-company-research` |
| `sales-pipeline` | `clous-object-management`, `clous-platform-operation` |
| `commercial-docs` | `unslop`, `stop-slop` |
| `product-marketing` | `hallmark`, `browserbase-competitor-analysis`, `office-hours` |
| `cro` | `hallmark`, `browserbase-ui-test`, `userinterface-wiki` |
| `discoverability` | `browserbase-search`, `browserbase-fetch`, `browserbase-competitor-analysis` |
| `technical-seo` | `browserbase-search`, `browserbase-fetch` |
| `aeo` | `browserbase-search`, `browserbase-fetch`, `unslop`, `stop-slop` |
| `social-media` | `unslop`, `stop-slop`, `animate-text`, `visual-explainer` |

## Chains

### System

| Parent | Children | Chains To |
| --- | --- | --- |
| `auto-improve` | — | `skills-management/skill-eval-loop`, `memory`, `brain/ingestion`, `personalize`, `loops`, `agentic-development/agent-harness`, `code-documentation`, `quality-assurance` |
| `skills-management` | `skill-eval-loop` | `memory`, `knowledge-base`, `learning`, `loops`, `code-documentation` |
| `learning` | `lessons` | `knowledge-base`, `memory`, `brain`, `code-documentation` |
| `brain` | `ingestion` | `knowledge-base`, `memory`, `research`, `reporting` |
| `personalize` | `communication-style`, `voice`, `calibration`, `positioning`, `icp` | `outreach`, `content`, `product-marketing`, `research` |

### Marketing

| Parent | Children | Chains To |
| --- | --- | --- |
| `content` | `humanizing`, `repurposing`, `syndication`, `keywords`, `context-to-content`, `copywrite` | `discoverability`, `social-media`, `product-marketing` |
| `discoverability` | `seo-and-geo`, `aeo`, `geo` | `content`, `product-marketing/cro`, `frontend/performance`, `reporting` |
| `seo-and-geo` | `on-page-seo`, `technical-seo` | `geo`, `content`, `product-marketing/cro`, `frontend/performance`, `reporting` |
| `social-media` | `x-posts`, `linkedin-posts`, `x-articles`, `linkedin-articles` | `content/repurposing`, `personalize/positioning`, `launches/virality`, `images`, `video` |
| `video` | `hyperframes`, `remotion` | `content`, `social-media`, `images`, `slides` |
| `growth-engine` | — | `content`, `social-media`, `keywords`, `reporting` |

### Sales

| Parent | Children | Chains To |
| --- | --- | --- |
| `go-to-market` | `first-customers`, `technical-sales`, `revenue-intelligence` | `product-marketing`, `product-development`, `outreach`, `sales-pipeline`, `research` |
| `sales-pipeline` | `commercial-docs`, `collateral` | `go-to-market`, `outreach`, `growth` |
| `outreach` | `initial`, `sequence`, `follow-up`, `linkedin-dms`, `x-dms` | `prospect`, `go-to-market/first-customers`, `sales-pipeline`, `personalize` |
| `launches` | `virality` | `content`, `social-media`, `video`, `images`, `go-to-market` |
| `growth` | `revenue-ops`, `customer-growth` | `go-to-market`, `sales-pipeline`, `reporting` |

### Engineering

| Parent | Children | Chains To |
| --- | --- | --- |
| `agentic-development` | `architecture`, `multi-agent`, `release-landing`, `agent-harness`, `tech-debt` | `frontend`, `backend`, `quality-assurance`, `code-documentation`, `cloud`, `prs`, `skills-management` |
| `ai-engineering` | `agent-system-architecture`, `prompt-tool-design`, `context-memory-rag`, `ai-evals-observability`, `ai-governance-safety`, `data-ml-pipelines`, `computer-vision-systems` | `quality-assurance/ai-evals`, `quality-assurance/security`, `backend`, `cloud`, `skills-management`, `brain` |
| `backend` | `apis`, `databases` | `quality-assurance/backend-testing`, `quality-assurance/security`, `quality-assurance`, `code-documentation`, `cloud`, `ai-engineering` |
| `frontend` | `performance`, `accessibility`, `onboarding-flows` | `product-development`, `product-marketing`, `quality-assurance/frontend-e2e`, `quality-assurance`, `code-documentation`, `images`, `visualization`, `design` |
| `cloud` | `resources`, `cicd`, `cloud-incidents`, `aws-ops`, `azure-ops`, `gcp-ops`, `cloud-architecture` | `quality-assurance`, `agentic-development/release-landing`, `backend`, `ai-engineering`, `pentest/cloud-container-pentest` |
| `pentest` | `web-vuln-validation`, `api-pentest`, `cloud-container-pentest`, `business-logic-race-testing`, `pentest-report` | `quality-assurance/security`, `cloud`, `backend` |
| `quality-assurance` | `test-strategy-coverage`, `frontend-e2e`, `backend-testing`, `flake`, `security`, `ai-evals` | `pentest`, `ai-engineering/ai-evals-observability`, `frontend/performance`, `frontend`, `backend`, `prs`, `cloud` |

### Product

| Parent | Children | Chains To |
| --- | --- | --- |
| `product-development` | `strategy`, `discovery`, `prds`, `experiments`, `user-stories` | `product-marketing`, `frontend/onboarding-flows`, `quality-assurance/test-strategy-coverage`, `quality-assurance`, `code-documentation`, `reporting` |
| `product-marketing` | `cro`, `content-led`, `lead-magnets`, `buyer-psychology` | `content`, `discoverability`, `go-to-market`, `frontend`, `reporting` |
| `design` | `taste`, `direction`, `design-systems`, `polish`, `critique` | `frontend`, `product-development`, `product-marketing`, `quality-assurance/frontend-e2e`, `code-documentation`, `visualization` |

### Finances

| Parent | Children | Chains To |
| --- | --- | --- |
| `finances` | `expenses`, `reconciliation`, `planning`, `taxes`, `fundraising`, `fiscal-close`, `quantitative`, `fundamentals`, `macro` | `reporting`, `research`, `product-marketing` |

### Productivity

| Parent | Children | Chains To |
| --- | --- | --- |
| `reporting` | `content-audit` | `research`, `finances`, `product-development` |
| `research` | `market-competitor-research`, `diligence-vendor-research`, `customer-qual-research`, `seo-competitor-gap`, `prospect` | `reporting`, `go-to-market`, `product-development`, `outreach` |
| `review` | `code-review`, `design-review`, `grill`, `documentation-drift` | `quality-assurance`, `frontend`, `product-development`, `prs` |
