# Growth Engine

Load this file when the task involves marketing experiments, A/B or multivariate testing, experiment scoring, weekly scorecards, playbook updates, or pacing alerts across growth channels.

This reference embeds the operating model from the external `growth-engine` skill and now has a local automation bundle in `skills/go-to-market/scripts/`.

Use these local commands when the user wants the operating model turned into a runnable system:

- `python3 skills/go-to-market/scripts/experiment-engine.py create ...`
- `python3 skills/go-to-market/scripts/experiment-engine.py log ...`
- `python3 skills/go-to-market/scripts/experiment-engine.py score ...`
- `python3 skills/go-to-market/scripts/experiment-engine.py list --agent <name>`
- `python3 skills/go-to-market/scripts/experiment-engine.py playbook --agent <name>`
- `python3 skills/go-to-market/scripts/experiment-engine.py suggest --agent <name>`
- `python3 skills/go-to-market/scripts/autogrowth-weekly-scorecard.py`
- `python3 skills/go-to-market/scripts/pacing-alert.py`

Configuration lives in `skills/go-to-market/.env.example`. The default data directory is `skills/go-to-market/data/experiments`, so the scripts work locally without extra setup.

## Role in GTM

Growth experimentation turns GTM iteration into a repeatable system.

Use it to answer questions such as:

- what should we test next
- did a variant actually win
- what proven rules should the team reuse before creating new content or campaigns
- where are campaigns or channel targets off pace
- how should weekly learning be summarized across channels

Do not treat experimentation as random content variation. The point is to produce reusable evidence and then operationalize it.

## Operating stance

Bias toward the same loop the source skill enforces:

1. Check the current playbook before creating new content or campaigns.
2. Create a clearly-scoped experiment.
3. Log what shipped and the resulting metrics.
4. Score the experiment against explicit thresholds.
5. Promote winners into the living playbook.
6. Suggest the next test and review weekly pacing.

Use one loop when the request is narrow. Use the whole sequence when the user wants an operating system for growth learning.

Track experiment lifecycle states explicitly:

- `running`: collecting data, not yet ready for judgment
- `trending`: early positive evidence, but not enough to promote
- `keep`: strong enough to reuse as a winner
- `discard`: weak, negative, or non-generalizable result

## 1. Design the experiment

Use this when the user wants to set up a test for content, email, paid, outbound, landing pages, or another GTM channel.

### Minimum experiment definition

- experiment ID or name
- channel or agent: `content`, `email`, `linkedin`, `seo`, `blog`, `paid`, `outbound`, or user-defined
- hypothesis: what should happen and why
- variable: the one thing being changed
- variants: two or more versions to compare
- primary metric: the decision metric
- guardrail metrics: metrics that protect quality or downstream outcomes
- cycle length or review cadence
- owner
- launch date or cohort window

### Design rules

- Change one main variable at a time when you need causal clarity.
- Batch or multivariate mode is useful when the user explicitly wants to compare several variants; use roughly `3-10` variants as the outer bound and keep the set small enough to interpret.
- Separate high-volume channels from low-volume channels because sample expectations differ.
- Always define what would count as a keep, trend, or discard outcome before data comes in.
- Capture where the metrics will come from before launch; an experiment with no trustworthy measurement path is not ready.

### Sample heuristics

Use the source skill's defaults as heuristics unless the user has a better evidence model:

- high-volume agents such as `content` and `email`: start with roughly `10` samples per variant
- lower-volume agents such as `seo`, `linkedin`, and `blog`: start with roughly `30` samples per variant
- batch mode: cap at `10` variants unless there is a strong reason to increase complexity

Treat these as working defaults, not scientific constants.

## 2. Log and evaluate the data

Use this when the user is recording results or judging whether a test has enough evidence.

### Logging schema

For each data point or review snapshot, capture:

- experiment ID
- variant
- timestamp or cohort window
- primary metric value
- guardrail metric values
- sample count
- data source or system of record
- notes on anomalies, launch changes, or tracking problems

### Evidence standard

Use explicit decision thresholds. Default heuristics from the source skill are:

- `keep`: p-value below `0.05` and at least `15%` lift
- `trending`: p-value below `0.10` but not yet strong enough to promote
- `discard`: no credible lift or underperforming result

Treat these as defaults, not universal laws. The user may need different thresholds.

### Scoring posture

- Prefer non-parametric reasoning when samples are small or distributions are messy.
- The source skill uses bootstrap confidence intervals plus Mann-Whitney U testing; use that exact framing when the user wants a concrete scoring method, or say "equivalent non-parametric significance plus uncertainty checks" when tooling differs.
- Report lift, uncertainty, and sample size together.
- Do not call a winner from a noisy sample just because the metric looks higher.
- If data quality is weak, say the result is inconclusive.

### Output expectation

Include:

- experiment ID or name
- tested variable and leading variant
- metric result and lift
- confidence or significance note
- decision: `running`, `trending`, `keep`, or `discard`
- recommended next action

## 3. Promote winners into the playbook

Use this when the user wants to preserve what worked.

The playbook should capture:

- channel or agent
- proven winning pattern
- source experiment
- promoted date or review date
- metric and lift summary
- usage note or constraint
- what conditions made the result likely to work

Good playbooks prevent the team from relearning the same lesson.

Do not promote winners if:

- the evidence is too weak
- the test changed too many things at once
- the winning condition would not generalize
- the lift came with guardrail damage the team would not accept

## 4. Suggest the next experiment

Use this when the user wants a next-test queue rather than just a readout.

The next suggestion should state:

- the next variable to test
- why it is a better next bet than alternative ideas
- whether the idea is meant to confirm a winner, probe a trend, or attack a bottleneck
- what previous playbook rule or experiment result informed the recommendation

Completed experiments should either update the playbook or sharpen the next queue. If neither happens, the system is not learning.

## 5. Weekly scorecards and pacing

Use this when the user wants a recurring operating review rather than one experiment readout.

### Weekly scorecard structure

Bias toward:

- active experiments
- new experiments launched
- experiments completed
- winners kept and losers discarded
- trends worth watching
- total data collected or signal volume
- next experiments to queue
- pipeline, acquisition, or revenue implications from the week's learning

Good weekly scorecards explain what was learned, not just what ran.

### Pacing alerts

Use pacing logic when the task involves campaign health, lead flow, pipeline targets, or recruiting-style throughput.

At minimum, compare:

- actual vs target pace
- whether the gap is temporary or structural
- likely bottleneck: traffic, response, conversion, stage progression, or volume
- action owner
- action needed this week

Exit conditions should be simple:

- `on pace`
- `watch`
- `alert`

## Configuration mapping

If the user wants to operationalize this as a real system, use the local scripts first, then mirror the same configuration model in whatever broader tooling they use:

- data directory or system table for experiment records
- allowed agent or channel list, with defaults like `content,email,linkedin,seo,blog`
- separate thresholds for winner vs trend decisions
- minimum lift needed for promotion
- bootstrap iteration count or equivalent uncertainty setting
- batch-mode variant cap
- campaign IDs, API endpoints, or target volumes needed for pacing alerts

Useful defaults from the source skill:

- winner p-value threshold: `0.05`
- trend p-value threshold: `0.10`
- winner lift threshold: `15%`
- bootstrap iterations: `1000`
- batch mode max variants: `10`

## Decision rules

- Always check the current playbook before designing a new test.
- Every completed experiment should either update the playbook or inform the next queue.
- Weekly reviews should connect experiment results to pipeline, acquisition, or revenue implications.
- Pacing alerts should trigger an action owner, not just a warning.
- If the user only has one-off results, give them a test design and scoring framework instead of pretending they have a full experimentation program.

## Failure modes

- testing multiple variables without acknowledging the ambiguity
- choosing vanity metrics that do not connect to business outcomes
- promoting winners without enough evidence
- running experiments without a next-test queue
- failing to log which variant actually shipped
- weekly scorecards that summarize activity but not learning
- pacing alerts with no thresholds or no owner
