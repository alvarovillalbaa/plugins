# Runbook: <Operation Name>

> AWS operational runbook. Fill every section. A runbook nobody can follow at
> 3am is not a runbook.

## Metadata

- **Service / resource:** <e.g. orders-api on ECS Fargate>
- **AWS account(s):** <name + id>
- **Region(s):** <e.g. eu-west-1>
- **Owner:** <team / on-call rotation>
- **Last validated:** <YYYY-MM-DD by whom>

## When to use this runbook

<Trigger conditions: alarm name, symptom, scheduled maintenance, etc.>

## Pre-flight

- [ ] Confirm the target account and profile: `aws sts get-caller-identity --profile <p>`
- [ ] Confirm the region: `echo "$AWS_REGION"`
- [ ] Announce in <channel> if this is customer-impacting.
- [ ] Snapshot / backup taken if the operation is destructive: <how>

## Procedure

```bash
# Step 1 — <what and why>
aws <command> --profile <p> --region <r>

# Step 2 — <what and why>
aws <command> --profile <p> --region <r>
```

Each step should state: the command, the expected output, and how to tell it
worked.

## Verification

- [ ] <health check / metric / endpoint that proves success>
- [ ] CloudWatch alarm <name> back to OK
- [ ] No new errors in <log group>

## Rollback

```bash
# How to undo each step above, in reverse order.
```

If rollback is impossible, say so explicitly and describe the recovery path.

## Escalation

- Primary: <on-call>
- Secondary: <team lead>
- Vendor / AWS Support case severity: <level>

## References

- Related runbooks:
- Dashboards:
- Relevant ADRs:
