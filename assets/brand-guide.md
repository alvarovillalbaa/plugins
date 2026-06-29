# Agent Company — Brand Guide

Shared brand assets and guidelines for use across all department plugins. Department-specific assets live inside the corresponding department plugin.

## Company Identity

**Name**: Agent Company  
**Tagline**: The agent-native operating system for modern teams.  
**Mission**: Run every department function — marketing, sales, engineering, product, finance, and operations — through AI agents that learn, improve, and compound over time.

## Voice & Tone

| Attribute | Description |
|-----------|-------------|
| **Direct** | No hedging. State the answer, then the rationale. |
| **Technical** | Comfortable with code, APIs, data, and systems. |
| **Confident** | Confident without being arrogant. Precise without being cold. |
| **Lean** | Short sentences. No filler. No corporate jargon. |

**Avoid**: "leverage", "synergy", "robust solution", "cutting-edge", "game-changing", "seamlessly".

## Writing Standards

- Use the active voice.
- Lead with the most important information.
- One idea per sentence.
- Use numbered lists for steps, bullet lists for options.
- Spell out acronyms on first use.

## Formatting Conventions

- **Headers**: Title Case for H1, sentence case for H2–H4.
- **Code**: Always use fenced code blocks with a language tag.
- **Links**: Descriptive link text — never "click here".
- **Dates**: ISO 8601 (`YYYY-MM-DD`) in technical docs; Month DD, YYYY in prose.

## Output Quality Gates

All agent-generated content must pass these gates before delivery:

1. **No slop**: Remove AI writing tells — "delve", "certainly", "I'd be happy to", "absolutely", "of course".
2. **Source-grounded**: Claims referencing data or competitors need a traceable source.
3. **Brand-consistent**: Matches voice, tone, and formatting standards above.
4. **Actionable**: Every output should close with a clear next step or decision.

## Department Assets

Department-specific logos, templates, and media live inside each department plugin:

```
engineering/    → technical diagrams, architecture templates
marketing/      → content templates, brand copy, visual specs
sales/          → pitch decks, battlecards, one-pagers
product/        → PRD templates, UX specs, user story formats
finances/       → financial model templates, report formats
productivity/   → report templates, research brief formats
system/         → skill templates, memory formats, loop configs
```

## Usage Policy

These assets are for internal agent use only. Do not include confidential company data in shared asset files. Sensitive assets (pricing, internal roadmaps, legal documents) belong in local overlay files (`*.local.yml`, `.company/`) that are excluded from upstream contribution.
