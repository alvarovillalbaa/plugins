---
name: growth-engine
description: Autonomous growth experimentation framework. Creates A/B and multivariate experiments with hypotheses, logs data points, runs statistical analysis (bootstrap CI + Mann-Whitney U), auto-promotes winners to a living playbook, and suggests next experiments. Use before creating content to apply proven playbook rules; use after publishing to log results.
---

# Growth Engine

Autonomous growth experimentation framework based on Karpathy's autoresearch pattern applied to marketing. Creates experiments with hypotheses, logs data points, runs statistical analysis (bootstrap CI + Mann-Whitney U), auto-promotes winners to a living playbook, and suggests next experiments. Supports batch mode (up to 10 variants simultaneously).

## When to Use

- Creating or managing A/B or multivariate experiments for any marketing channel
- Logging experiment data points after content is published or campaigns run
- Scoring experiments to determine statistical winners
- Checking the playbook for proven best practices **before** creating new content
- Generating weekly scorecards across all channels
- Monitoring campaign pacing and health

Do NOT use for:
- One-off content creation without an active experiment (use playbook output as input, but don't run the engine)
- Non-experiment analytics or reporting (chain to `reporting`)
- Campaign setup in external platforms (this tracks experiments, not campaign config)

## Workflow

1. **Before creating content** → `playbook` — apply proven rules from previous experiments
2. **When publishing** → `log` — record which variant was used and its metrics
3. **Periodically** → `score` — check if experiments have reached statistical significance
4. **Weekly** → `autogrowth-weekly-scorecard.py` — review all channels
5. **After completing experiments** → `suggest` — pick the next variable to test

## Commands

### Setup
```bash
pip install -r scripts/requirements.txt
cp scripts/.env.example .env
# Edit .env with your channel names and API tokens
```

### Create an experiment
```bash
python3 scripts/experiment-engine.py create \
  --agent <agent_name> \
  --hypothesis "What you expect to happen" \
  --variable "<variable_name>" \
  --variants '["variant_a", "variant_b"]' \
  --metric "<primary_metric>" \
  --cycle-hours 24
```

Add `--batch-mode` for 3–10 variant tests. Add `--min-samples N` to override auto-detection.

### Log a data point
```bash
python3 scripts/experiment-engine.py log \
  --agent <agent_name> \
  --experiment-id <EXP-ID> \
  --variant "<variant_name>" \
  --metrics '{"metric_name": value}'
```

### Score an experiment
```bash
python3 scripts/experiment-engine.py score \
  --agent <agent_name> \
  --experiment-id <EXP-ID>
```

Statuses: `running` → `trending` → `keep` (winner) or `discard` (loser)

Winners auto-promote to the playbook. Requires p < 0.05 AND ≥ 15% lift.

### List experiments
```bash
python3 scripts/experiment-engine.py list \
  --agent <agent_name> \
  [--status running|trending|keep|discard]
```

### Check the playbook
```bash
python3 scripts/experiment-engine.py playbook --agent <agent_name>
```

Always check the playbook before creating new content to apply proven best practices.

### Suggest next experiments
```bash
python3 scripts/experiment-engine.py suggest --agent <agent_name>
```

### Generate weekly scorecard
```bash
python3 scripts/autogrowth-weekly-scorecard.py [--weeks N] [--output file.md]
```

### Check campaign pacing
```bash
python3 scripts/pacing-alert.py [--json]
```

Exit code 0 = on pace, 1 = alerts present.

## Chain Rules

Chain to these skills when the task crosses this skill's boundary:

- `content`
- `social-media`
- `keywords`
- `reporting`

## Statistical Thresholds

| Parameter | Default | What It Controls |
|-----------|---------|-----------------|
| `P_WINNER` | 0.05 | p-value threshold for declaring a winner |
| `P_TREND` | 0.10 | p-value threshold for "trending" early signal |
| `LIFT_WIN` | 15.0% | Minimum lift required for "keep" decision |
| `BOOTSTRAP_ITERATIONS` | 1000 | Bootstrap resamples for confidence intervals |

See [`references/statistical-methods.md`](references/statistical-methods.md) for the full rationale.

## Configuration

All configuration via environment variables. See `scripts/.env.example` for the full list.

| Variable | Default | Description |
|----------|---------|-------------|
| `GROWTH_ENGINE_DATA_DIR` | `./data/experiments` | Where experiment data is stored |
| `GROWTH_ENGINE_AGENTS` | `content,email,linkedin,seo,blog` | Comma-separated agent names |
| `HIGH_VOLUME_AGENTS` | `content,email` | Agents needing only 10 samples/variant |
| `LOW_VOLUME_AGENTS` | `seo,linkedin,blog` | Agents needing 30 samples/variant |

## Shared Map

See [`../../../skills-chaining-map.md`](../../../skills-chaining-map.md) for the complete skills-chaining graph.
