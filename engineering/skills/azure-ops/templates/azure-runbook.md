# Runbook: <Operation Name>

> Azure operational runbook. Fill every section.

## Metadata

- **Service / resource:** <e.g. orders-api on Container Apps>
- **Subscription:** <name + id>
- **Resource group(s):** <rg-name>
- **Region(s):** <e.g. westeurope>
- **Owner:** <team / on-call rotation>
- **Last validated:** <YYYY-MM-DD by whom>

## When to use this runbook

<Trigger conditions: alert rule, symptom, scheduled maintenance, etc.>

## Pre-flight

- [ ] Confirm the active subscription: `az account show --query name -o tsv`
- [ ] Set it if needed: `az account set --subscription <id>`
- [ ] Confirm the resource group and region.
- [ ] Announce in <channel> if customer-impacting.
- [ ] Backup / snapshot taken if destructive: <how>

## Procedure

```bash
# Step 1 — <what and why>
az <group> <command> --resource-group <rg> --name <res>

# Step 2 — <what and why>
az <group> <command> --resource-group <rg> --name <res>
```

State the expected output and success signal for each step.

## Verification

- [ ] <health probe / metric / endpoint>
- [ ] Alert rule <name> resolved
- [ ] No new failures in Log Analytics: `az monitor log-analytics query ...`

## Rollback

```bash
# How to undo each step above, in reverse order.
# Container Apps: az containerapp revision activate --revision <previous>
```

## Escalation

- Primary: <on-call>
- Secondary: <team lead>
- Azure Support severity: <level>

## References

- Related runbooks:
- Workbooks / dashboards:
- Relevant ADRs:
