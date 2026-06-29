# Loop Example: Automated SEO Experiment Loop

**Loop type**: Improvement loop (iterative content experiments)  
**Domain**: marketing  
**Name**: seo-title-experiments  
**Branch**: `autoresearch/marketing/seo-title-experiments`

---

## Setup

```bash
# Create autoresearch state directory
mkdir -p .autoresearch/marketing/seo-title-experiments

# Initialize experiment state
cat > .autoresearch/marketing/seo-title-experiments/state.json << 'EOF'
{
  "loop_id": "seo-title-experiments",
  "iteration": 0,
  "status": "running",
  "hypothesis": "Adding a specific number in H1 titles increases click-through rate",
  "control_url": "/blog/how-to-reduce-pr-cycle-time",
  "variants": [],
  "target_metric": "organic_ctr",
  "min_iterations": 3,
  "convergence_threshold": 0.05
}
EOF
```

---

## Running an Iteration

```bash
python system/skills/loops/scripts/run_experiment.py \
  --domain marketing \
  --name seo-title-experiments \
  --iteration 1
```

**What the loop does per iteration**:
1. Reads current state from `.autoresearch/marketing/seo-title-experiments/state.json`
2. Generates a hypothesis-driven variant (e.g., new title with a number)
3. Writes the variant to `state.json` under `variants[]`
4. Runs any configured evaluation (CTR check, LLM judge, human review flag)
5. Updates state with outcome
6. Decides: continue (next iteration) or converge (stop)

---

## State After 3 Iterations

```json
{
  "loop_id": "seo-title-experiments",
  "iteration": 3,
  "status": "converged",
  "hypothesis": "Adding a specific number in H1 titles increases click-through rate",
  "variants": [
    {
      "iteration": 1,
      "variant": "How to Reduce PR Cycle Time by 60%",
      "metric_delta": "+12% CTR",
      "outcome": "winner"
    },
    {
      "iteration": 2,
      "variant": "Cut PR Cycle Time in Half: 5 Tactics That Work",
      "metric_delta": "+8% CTR",
      "outcome": "runner-up"
    },
    {
      "iteration": 3,
      "variant": "3 Ways to Get PR Cycle Time Under 12 Hours",
      "metric_delta": "+6% CTR",
      "outcome": "diminishing"
    }
  ],
  "conclusion": "Number-first titles outperform generic titles. Best variant: iteration 1.",
  "recommended_action": "Apply 'How to Reduce PR Cycle Time by 60%' as canonical title."
}
```

---

## Converging and Merging

When a loop converges:

```bash
# Apply the winner to the working tree
git checkout main
git merge autoresearch/marketing/seo-title-experiments --squash
git commit -m "Apply SEO title experiment winner: +12% CTR variant"

# Archive the experiment state
mv .autoresearch/marketing/seo-title-experiments .autoresearch/marketing/seo-title-experiments-archived-$(date +%Y%m%d)
```

---

## When to Discard (Not Merge)

If all iterations underperform the control, or the loop diverges without convergence:

```bash
# Discard failed experiment branch
git checkout main
git branch -D autoresearch/marketing/seo-title-experiments
rm -rf .autoresearch/marketing/seo-title-experiments
```

The state directory isolates all experiment artifacts, so discarding the branch leaves no trace on main.
