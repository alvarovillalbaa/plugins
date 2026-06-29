If you want other teams to install your agent skills with `npx skills add`, treat your repo as a **skills package**: a set of **small, atomic, installable folders**, each with a `SKILL.md` that follows the Agent Skills spec (YAML frontmatter + instructions). ([Agent Skills][1]) This repo (`alvarovillalbaa/plugins`) is an example of a multi-skill, multi-agent package with department plugins, commands, and skill-owned hooks.

## 1) The simplest open-source shape (works with `npx skills add`)

**One repo = many skills.** This matches how the ecosystem is evolving (e.g., Vercel’s skill collections). ([GitHub][2])

Recommended layout (canonical per-skill structure used in this repo):

```
skills/<skill-name>/
├── SKILL.md              # Main instructions (see SKILL.md template below)
├── references.md         # Short index: "Use references/ for …"
├── references/           # Optional: legal, domain, methodology
├── examples/             # Optional: example inputs/outputs
├── templates/            # Optional: JSON schemas, doc templates
└── scripts/              # Optional: validation/helper scripts
```

Legacy/minimal layout (also valid):

```
clousai/hr-agent-skills/
  README.md
  skills/
    engineering-hiring-intake/
      SKILL.md
      references/
      assets/
      templates/
    ...
```

**SKILL.md content template (comprehensive):** Frontmatter: `name`, `description`, `version`, `license`, `compatibility`. Sections: Overview → When to Use → Inputs Required → Outputs Produced (with schema/template path) → Tooling rule → Core Process (numbered steps) → Using Supporting Resources (Templates, References, Scripts) → Example Workflow → Next Steps After [skill] → Validation checklist → Legal/caveats (if relevant).

Why this works:

* A “skill” is literally a folder with `SKILL.md` (+ optional resources/scripts). ([OpenAI Developers][3])
* Installers/agents discover skills by reading the frontmatter `name` + `description` to decide when to load the full content. ([Agent Skills][4])
* `npx skills add <org>/<repo>` installs the repo as a skill collection; many examples also support picking a specific one via `--skill`. ([Skills][5])

## 2) What your `SKILL.md` should look like for HR (developer-friendly)

Agent Skills spec requires:

* `name` (lowercase, hyphens, must match folder name)
* `description` (should include *what it does* + *when to use it* + keywords) ([Agent Skills][4])

A **good HR skill** also includes:

* **Inputs** (explicit fields the developer should provide)
* **Output contract** (JSON schema or strict markdown sections)
* **Guardrails** (bias/discrimination, privacy, “not legal advice”)
* **Examples** (2–3 realistic calls)
* **Validation checklist** (so the agent self-checks)

Example skeleton:

```md
---
name: engineering-hiring-intake
description: Turns a messy hiring request into a structured intake brief for engineering roles. Use when a user asks to open a role, define requirements, align stakeholders, or create a kickoff doc for hiring managers.
license: MIT
compatibility: Works as instruction-only. No tools required.
---

# Engineering Hiring Intake

## Inputs required
- Company stage + team
- Role title + level
- Location/remote + timezone constraints
- Tech stack
- Must-have vs nice-to-have
- Interview loop constraints
- Compensation philosophy (if known)

## Output format (strict JSON)
Return ONLY:
{ ... clearly defined fields ... }

## Process
1) Ask up to 5 clarifying questions if inputs missing
2) Produce the intake brief
3) Run validation checklist

## Validation checklist
- No protected-class language
- Requirements are measurable
- Must-haves <= 6
...
```

(You can validate frontmatter + naming conventions with `skills-ref validate`. ([Agent Skills][4]))

## 3) Make it easy to adopt: “HR skills that compile into product”

Your constraint is key: *not code*, but used by engineers. So design skills that output **machine-consumable artifacts** engineers can drop into their systems:

**Patterns that work well**

* “Return strict JSON” skills (intake brief, scorecard rubric, leveling matrix)
* “Generate templates” skills (JD template, interview plan template, onboarding plan)
* “Audit/critique” skills (job post bias audit, interview loop anti-pattern audit)
* “Decision support” skills (calibration summary, offer risk memo)

This makes your repo valuable even to teams that **aren’t** using Clous—because it produces artifacts that fit any ATS/HRIS/analytics stack.

## 4) Distribution + install instructions (README must be crystal clear)

In your README, include:

* Install whole pack:

  * `npx skills add clousai/hr-agent-skills` ([Skills][5])
* Install one skill (if supported by the installer they use):

  * `npx skills add clousai/hr-agent-skills --skill "engineering-hiring-intake"` ([Skills][6])
* Manual install locations for popular tools (optional, but helpful)

Also mention the adjacent installer `add-skill` used in the ecosystem (some users will use it instead of `skills`). ([GitHub][7])

## 5) Versioning: don’t ship a “moving target”

Big trap: people install once and expect stability.

Minimum viable approach:

* Use **Git tags/releases** (`v0.1.0`, `v0.2.0`)
* Add `metadata.version` in frontmatter if you want it machine-readable (spec supports metadata fields). ([Agent Skills][4])
* Maintain a CHANGELOG at repo root

Optional (but likely worth it): add a Claude Code marketplace manifest per skill (`.claude-plugin/plugin.json`) so the same repo can be installed as a plugin marketplace entry without breaking SKILL.md consumers. ([GitHub][8])

## 6) Security + trust: HR skills are *high-stakes*

Even “instruction-only” skills can be a prompt-injection surface; if you ever add scripts, the risk increases. Two practical rules:

* Start **instruction-only** (no scripts) until you’ve proven adoption
* If you add scripts later, use least-privilege and consider `allowed-tools` (experimental in the spec). ([Agent Skills][4])


---

**Reflection question:** what’s the *one artifact* you want external teams to generate first (intake brief, scorecard, leveling matrix, calibration summary), and what exact fields must it contain so it plugs into their workflow?

[1]: https://agentskills.io/what-are-skills?utm_source=chatgpt.com "What are skills? - Agent Skills"
[2]: https://github.com/vercel-labs/agent-skills?utm_source=chatgpt.com "vercel-labs/agent-skills"
[3]: https://developers.openai.com/codex/skills/?utm_source=chatgpt.com "Agent Skills"
[4]: https://agentskills.io/specification?utm_source=chatgpt.com "Specification - Agent Skills"
[5]: https://skills.sh/docs/cli "CLI | Skills Documentation"
[6]: https://skills.sh/anthropics/skills/skill-creator?utm_source=chatgpt.com "skill-creator by anthropics/skills"
[7]: https://github.com/vercel-labs/add-skill?utm_source=chatgpt.com "vercel-labs/add-skill"
[8]: https://github.com/vercel-labs/agent-skills/issues/20?utm_source=chatgpt.com "RFC: Claude Code Marketplace Compatibility"
