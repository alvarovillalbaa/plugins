---
type: loop-config
loop_id: [domain/name]
loop_type: [improvement|evaluation|memory|experimentation]
---

# Loop Config: [Loop Name]

## Identity

| Field | Value |
|-------|-------|
| Loop ID | `[domain/name]` |
| Branch | `autoresearch/[domain]/[name]` |
| State dir | `.autoresearch/[domain]/[name]/` |
| Type | [improvement / evaluation / memory / experimentation] |

---

## Hypothesis

[What are you trying to learn or improve? State it as a testable hypothesis.]

**Hypothesis**: "[If we do X, then Y will change by Z.]"

---

## Initial State (`state.json`)

```json
{
  "loop_id": "[domain/name]",
  "iteration": 0,
  "status": "running",
  "hypothesis": "[Your hypothesis]",
  "target_metric": "[metric to optimize or measure]",
  "min_iterations": 3,
  "max_iterations": 10,
  "convergence_threshold": 0.05,
  "variants": []
}
```

---

## Per-Iteration Plan

What the loop does on each iteration:

1. **Read state**: Load `state.json`, check current iteration count.
2. **Generate**: Produce next variant/action based on hypothesis and prior results.
3. **Evaluate**: Run configured evaluation (metric check, LLM judge, A/B test, etc.).
4. **Update state**: Write outcome to `variants[]` in state.json.
5. **Decide**: Continue / converge / abort based on threshold or max iterations.

---

## Convergence Criteria

Stop the loop when:
- [ ] Metric delta < `convergence_threshold` for 2+ consecutive iterations
- [ ] `max_iterations` reached
- [ ] Winner identified with high confidence

---

## Failure / Abort Criteria

Abort and discard branch when:
- [ ] All variants underperform control
- [ ] Loop diverges (oscillating results)
- [ ] Evaluation tool returns errors for 2+ iterations

---

## Merge Plan (on convergence)

```bash
git checkout main
git merge autoresearch/[domain]/[name] --squash
git commit -m "Apply [loop-id] winner: [summary of outcome]"
```

---

## Discard Plan (on abort)

```bash
git checkout main
git branch -D autoresearch/[domain]/[name]
rm -rf .autoresearch/[domain]/[name]
```
