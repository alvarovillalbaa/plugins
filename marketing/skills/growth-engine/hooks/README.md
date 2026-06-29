# Hooks

Place post-publish hooks here that auto-log experiment data points. For example, a hook that runs after a social post is published can call:

```bash
python3 scripts/experiment-engine.py log \
  --agent content \
  --experiment-id $EXPERIMENT_ID \
  --variant $VARIANT_USED \
  --metrics "{\"impressions\": $IMPRESSIONS, \"clicks\": $CLICKS}"
```
