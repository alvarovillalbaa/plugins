---
name: prospect
description: Turn heterogeneous inputs (LinkedIn, company site, job boards, research) into a decision-ready GTM brief with Account, Persona, and Next best motion. Use when the user has prospect/account URLs or content and needs a full positioning and outreach brief. Apply provided scorecards (ICP, ICA, signals) as authoritative rubrics.
version: 1.0.0
license: MIT
compatibility: Instruction-only. Optional scorecards and file inputs.
---

# Prospect Research (GTM Brief) Skill

Convert heterogeneous inputs (LinkedIn profile & posts, company site, personal site/portfolio, job boards, competitor case studies, web research, notes) into a **decision-ready brief** for GTM from first touch to close.

## Product context (positioning boundaries)

Respect the user’s product context only. Do not invent features. If a capability is not listed or explicitly provided, don’t claim it.

## Inputs you may receive

- Raw person/account URLs and content.
- Web findings (e.g. Perplexity summaries, job boards, case studies).
- **Scorecards provided at runtime:** Prospecting Signal Scorecard, Problem Signal Scorecard, ICP (Persona) Scorecard, ICA (Account) Scorecard. Treat scorecards as **authoritative rubrics**; apply them, do not restate or alter them.

## Research rules

- Prefer **recent (≤12 months)**, **quantified**, **attributable** facts. Flag older data `(older than 12m)`.
- **Cite inline** every non-obvious fact: `[SourceName|YYYY-MM-DD]` (e.g. `[LinkedIn|2025-07-20]`). Cite underlying sources, not only aggregator tools.
- Conflicting data: show variants with dates; choose most recent/authoritative and state why in one line.
- Inferences: mark `(inferred)` and give one-line rationale.

## Skills chaining

- Use `../../../productivity/skills/research/SKILL.md` for shared source policy, confidence rules, and general research methodology.
- Stay in `prospect` for account/persona GTM briefs, ICP/ICA scoring, next-best motion, and outreach-ready evidence.
- Chain to `outreach/follow-up` only after the research brief is evidence-backed and the next message is a follow-up.

## Output format (strict)

Markdown with **headings and information-rich bullet points**. Bold labels for list items; bullets concrete (numbers, names, dates, quotes). Include only web info that is quantified or material to the sections below.

### 1) Account
- **Executive summary:** What they do; why now (1–3 time-sensitive facts with citations); buying posture (Active/Latent/Disengaged) + one-line why.
- **Problem signals** (map to provided Problem Signal Scorecard): bullet per signal → evidence → scorecard tag → one-line implication.
- **ICA fit** (apply provided ICA scorecard): gate check (pass/fail per gate); dimension notes; overall fit (High/Medium/Low) + rationale; top 2 drivers, top 1 blocker.
- **Red flags** with mitigation idea in one line.

### 2) Persona
- **Executive summary:** Role scope, decision power; mutuals (with source/date); motivations (2–3 bullets).
- **Killer insight:** Single sharp observation; traceable to citation or `(inferred)` with one-line logic.
- **Prospecting signals** (map to Prospecting Signal Scorecard): evidence → scorecard tag → why it matters now (≤12 words).
- **Engagement cues:** Tone & topics; channel cadence; 2–3 hook angles (no feature claims).
- **Uncommon shared experiences** (if user context provided).
- **ICP fit** (apply provided ICP scorecard): tier (A/B/C); economic power; influence map (economic buyer/champion/influencer).

### 3) Next best motion
- **Objective** (e.g. secure discovery, test pilot, multi-thread intro).
- **Multi-threading targets:** 2–3 names/titles with reason (cite or infer).

## Style & quality

- Specificity > generality. Numbers, names, dates, quotes.
- Zero feature invention beyond stated product context.
- Short sentences; one idea per bullet. Use “Unknown” rather than guessing.

## Failure modes to avoid

- Restating or inventing scorecard math; scorecards are inputs.
- Generic claims; use observed proof.
- Over-indexing on summaries without source/date.
- Pitching beyond stated context.

## When to use

- User has prospect/account URLs or content and wants a full GTM brief.
- User provides ICP/ICA or signal scorecards to apply.
- User needs next best motion and multi-threading targets.

## External Skill Chains

Use live external skills when they are installed. If one is missing, report the fallback command instead of copying its guidance inline. Local skill rules, repo-specific facts, safety gates, product/channel constraints, and explicit local exceptions win over external guidance when they conflict.

- `last30days`: Use recent-30-days research guidance when freshness is part of the task. Install: `python scripts/install-external-skills.py --skill last30days --agent codex`.
- `browserbase-company-research`: Use browser-backed company research workflows for account and market context. Install: `python scripts/install-external-skills.py --skill browserbase-company-research --agent codex`.
- `browserbase-event-prospecting`: Use browser-backed event prospecting workflows for GTM research. Install: `python scripts/install-external-skills.py --skill browserbase-event-prospecting --agent codex`.
- `browserbase-search`: Use Browserbase search guidance for web discovery tasks. Install: `python scripts/install-external-skills.py --skill browserbase-search --agent codex`.
- `browserbase-fetch`: Use Browserbase fetch guidance for web retrieval tasks. Install: `python scripts/install-external-skills.py --skill browserbase-fetch --agent codex`.

Registry: [`../../../references/external-skills.yaml`](../../../references/external-skills.yaml).
Reference-only sources: [`../../../references/external-sources.yaml`](../../../references/external-sources.yaml).
