# AWS Incident Response — <Incident Title>

> Use during an active AWS incident. Capture facts as you go; this doubles as
> the post-incident timeline.

## Summary

- **Incident ID:** <INC-YYYY-NNNN>
- **Severity:** <SEV1 / SEV2 / SEV3>
- **Status:** <investigating | identified | mitigating | monitoring | resolved>
- **Commander:** <name>
- **Scribe:** <name>
- **Started:** <UTC timestamp>  **Detected:** <UTC>  **Resolved:** <UTC>

## Impact

- Affected services / regions:
- Customer-facing symptom:
- Estimated blast radius (tenants / % traffic):
- SLA / SLO breached: <yes/no — which>

## Detection

- How detected: <alarm | customer report | dashboard>
- First signal source: <CloudWatch alarm name / log group / metric>

## Timeline (UTC)

| Time | Event / action | By |
| --- | --- | --- |
| | Alarm fired | |
| | Incident declared | |
| | Hypothesis: | |
| | Mitigation applied: | |
| | Recovery confirmed | |

## Investigation aids

```bash
# Recent service events
aws ecs describe-services --cluster <c> --services <s> --profile <p> --region <r>

# Tail logs
aws logs tail <log-group> --since 30m --follow --profile <p> --region <r>

# Recent infra changes (CloudTrail)
aws cloudtrail lookup-events --max-results 25 --profile <p> --region <r>

# Health of dependencies (RDS / cache / queue depth)
aws cloudwatch get-metric-statistics ...
```

## Mitigation

- Action taken:
- Why it was safe:
- Was it a rollback, scale, failover, config change, or feature flag?

## Resolution

- Root cause (one sentence, no blame):
- Permanent fix and owner:
- Tracking issue:

## Follow-ups

| Action | Owner | Priority | Due |
| --- | --- | --- | --- |
| | | | |

## Lessons

- What worked:
- What slowed us down:
- Detection / runbook gaps to close:
