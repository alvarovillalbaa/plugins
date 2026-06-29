# ICP Definition Reference

Reference for capturing, refining, and applying Ideal Customer Profile (ICP) signals for research, positioning, sales, and marketing. The ICP is the single source of truth for "who we sell to best" — it should be evidence-based and continuously refined, not a one-time guess. Persist ICP facts to repo-local docs so every department pulls the same definition.

## ICP vs. related concepts

- **ICP (Ideal Customer Profile)** — the *type of company/account* that gets the most value and is best to sell to (B2B account-level).
- **Buyer persona / ICA (Ideal Customer Avatar)** — the *individual people* within an ICP account (roles in the buying group).
- **TAM/SAM/SOM** — market sizing; the ICP narrows the market you actually pursue.
- **Segment** — a slice of the market; the ICP is your best segment.

The ICP defines accounts; personas define people inside them. You need both.

## ICP signal categories

### Firmographic (company attributes)
- Industry / vertical
- Company size (headcount, revenue)
- Growth stage (startup, scale-up, enterprise)
- Geography / region
- Business model (B2B/B2C, SaaS, services)
- Funding stage / financial health

### Technographic (tech & tooling)
- Current tech stack and platforms
- Tools they use (complementary or competitive)
- Technical maturity / sophistication
- Integration ecosystem

### Behavioral / operational
- How they work (processes, team structure)
- Maturity in the problem area you solve
- Buying behavior (self-serve vs. sales-led, procurement complexity)

### Need / pain signals
- The specific pain your product solves, felt acutely
- A trigger that makes it urgent (the "why now")
- Current (bad) solution they're using

### Value-fit signals
- They get strong, fast outcomes from your product
- High retention / expansion potential
- Referenceable, low cost-to-serve

## Defining the ICP from evidence

Don't invent the ICP — derive it from your best existing customers:
1. **Look at who actually wins** — fastest to value, highest retention, biggest expansion, lowest churn, strongest advocacy.
2. **Find the common attributes** across those winners (firmographic + technographic + behavioral).
3. **Contrast with churned / bad-fit customers** — what attributes predict failure? The ICP is as much about *exclusion* as inclusion.
4. **Synthesize** into a profile: "Companies that are [firmographics], using [tech], experiencing [pain], triggered by [signal], who value [outcome]."
5. **Negative ICP** — explicitly state who is *not* a fit (saves wasted GTM effort).

## Scoring accounts against the ICP

Turn the profile into a rubric so it's applied consistently:
- Assign weights to the most predictive signals (not all signals matter equally).
- Score each prospect: strong-fit / moderate-fit / poor-fit, with the contributing factors.
- Layer **timing signals** (funding, hiring, leadership change) on top of fit — fit says *whether*, timing says *when*.
- Use the score to prioritize: pursue strong-fit + timing first.

This rubric is what `prospect` and `sales` apply when qualifying. Keep it authoritative and current.

## Applying the ICP across departments

| Department | Uses ICP to… |
| --- | --- |
| **Research** (`prospect`, market research) | Qualify accounts, score fit, build target lists |
| **Sales** | Prioritize pipeline, tailor messaging, set the wedge |
| **Marketing** | Target content/campaigns, choose channels, shape positioning |
| **Product** | Prioritize features for the best-fit segment, guide discovery |
| **Finances** | Model deal economics by segment (CAC/LTV by fit) |

A shared ICP keeps these aligned — everyone targets the same "best customer."

## Refining the ICP (it's a loop)

The ICP is a living hypothesis. Refine as evidence accumulates:
- **New wins** → which attributes did the best new customers share? Tighten or expand.
- **Churn analysis** → what fit-signals predicted the losses? Add to the negative ICP.
- **Expansion data** → which accounts grew? Those traits matter more.
- **Market shifts** → the ideal customer changes as product and market mature.

Run refinement on a cadence (and feed it from `customer-growth` churn data and `first-customers` win patterns). Version the ICP so changes are traceable.

## Quality gates

- **Evidence-based** — derive from real customer data, not aspiration. Flag when the ICP is still a hypothesis vs. validated.
- **Specific and exclusionary** — "everyone who needs X" is not an ICP. Name who's *out*.
- **Single source of truth** — persist to repo-local docs; don't let departments drift to private definitions.
- **Current** — re-verify before relying on it; a stale ICP misdirects the whole GTM motion.
- **Confidential** — customer analysis underlying the ICP is sensitive.

## Handoffs

- Account scoring/research application → `prospect` (productivity), `sales`.
- Win/churn signal inputs → `first-customers`, `customer-growth` (sales).
- Positioning derived from ICP → `positioning` (system), `product-marketing` (product).
- Persistence → `memory`, `knowledge-base`.
