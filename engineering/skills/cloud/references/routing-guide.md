# Cloud — Routing Guide

Router for cloud infrastructure work. Routes to cloud provider or domain specialist skills.

## Child Skills

| Child | Owns |
|-------|------|
| `aws-ops` | AWS services, IAM, ECS, RDS, S3, CloudWatch |
| `azure-ops` | Azure services, Entra, Container Apps, Cosmos DB |
| `gcp-ops` | GCP services, Cloud Run, BigQuery, Pub/Sub |
| `cloud-architecture` | Cloud design patterns, provider selection, IaC |
| `cloud-incidents` | Runbooks, incident response, postmortems |
| `cloud-container-pentest` | Container and Kubernetes security testing |
| `cicd` | Deployment pipelines that push to cloud |

## Routing Decision Tree

```
Is this AWS-specific work?
  → aws-ops

Is this Azure-specific work?
  → azure-ops

Is this GCP-specific work?
  → gcp-ops

Is this about designing cloud architecture or choosing services?
  → cloud-architecture

Is this an active incident or writing a runbook?
  → cloud-incidents

Is this a container or Kubernetes security audit?
  → cloud-container-pentest

Is this about deployment pipelines?
  → cicd
```

## Cloud Operating Standards

- **Least privilege**: No role gets more permissions than the minimum required.
- **Infrastructure as code**: All cloud resources managed via Terraform or equivalent — no console-only changes.
- **Cost tagging**: All resources must be tagged with department, environment, and owner.
- **Change freeze**: Communicate change windows 24 hours in advance for production.
- **Backup verification**: Backup restore is tested quarterly, not just backup creation.
