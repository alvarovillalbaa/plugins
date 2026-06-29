# Example: Deploying a Containerized App to Azure Container Apps

Worked example of shipping a containerized API to Azure Container Apps (ACA)
with image storage in Azure Container Registry (ACR), secrets from Key Vault,
and revision-based rollout. Adjust names, subscription, and region.

## Assumptions

- App listens on port 8080 and exposes `GET /health`.
- Logged in (`az login`) with the target subscription active.
- Region `westeurope`; resource group `orders-rg`.

## 0. One-time setup

```bash
az account set --subscription "<sub-id>"
az group create -n orders-rg -l westeurope

# Container Apps needs the extension + providers registered once.
az extension add --name containerapp --upgrade
az provider register --namespace Microsoft.App
az provider register --namespace Microsoft.OperationalInsights
```

## 1. Create the registry and build the image

```bash
az acr create -g orders-rg -n ordersacr --sku Basic
TAG=$(git rev-parse --short HEAD)

# ACR Tasks builds remotely — no local Docker / platform mismatch.
az acr build -r ordersacr -t orders-api:$TAG .
```

## 2. Create the Container Apps environment

```bash
az containerapp env create \
  -g orders-rg -n orders-env \
  --location westeurope
```

The environment provisions a Log Analytics workspace and is the shared
networking/observability boundary for the apps inside it.

## 3. Deploy the app with a managed identity and Key Vault secret

```bash
ACR_LOGIN=$(az acr show -n ordersacr --query loginServer -o tsv)

az containerapp create \
  -g orders-rg -n orders-api \
  --environment orders-env \
  --image "$ACR_LOGIN/orders-api:$TAG" \
  --target-port 8080 \
  --ingress external \
  --system-assigned \
  --registry-server "$ACR_LOGIN" \
  --registry-identity system \
  --min-replicas 1 --max-replicas 5 \
  --cpu 0.5 --memory 1.0Gi
```

Wire a Key Vault secret reference instead of a plaintext env var:

```bash
PRINCIPAL_ID=$(az containerapp show -g orders-rg -n orders-api \
  --query identity.principalId -o tsv)

az keyvault set-policy -n orders-kv \
  --object-id "$PRINCIPAL_ID" --secret-permissions get

az containerapp secret set -g orders-rg -n orders-api \
  --secrets "db-url=keyvaultref:https://orders-kv.vault.azure.net/secrets/DATABASE-URL,identityref:system"

az containerapp update -g orders-rg -n orders-api \
  --set-env-vars "DATABASE_URL=secretref:db-url"
```

## 4. Roll out a new revision

Each `update` that changes the image or config creates a new revision. With the
default single-revision mode, traffic shifts to it once it is healthy.

```bash
TAG=$(git rev-parse --short HEAD)
az acr build -r ordersacr -t orders-api:$TAG .
az containerapp update -g orders-rg -n orders-api \
  --image "$ACR_LOGIN/orders-api:$TAG"
```

For a canary, switch to multiple-revision mode and split traffic:

```bash
az containerapp revision set-mode -g orders-rg -n orders-api --mode multiple
az containerapp ingress traffic set -g orders-rg -n orders-api \
  --revision-weight <new-rev>=20 <old-rev>=80
```

## 5. Verify

```bash
FQDN=$(az containerapp show -g orders-rg -n orders-api \
  --query properties.configuration.ingress.fqdn -o tsv)
curl -fsS "https://$FQDN/health"

# Stream logs
az containerapp logs show -g orders-rg -n orders-api --follow
```

## 6. Rollback

```bash
az containerapp revision list -g orders-rg -n orders-api -o table
az containerapp ingress traffic set -g orders-rg -n orders-api \
  --revision-weight <previous-rev>=100
```

## Gotchas

- **Providers not registered** → `create` fails; run the `az provider register`
  steps once per subscription.
- **Scale-to-zero** (`--min-replicas 0`) adds cold-start latency; keep at least
  one replica for latency-sensitive APIs.
- **Registry auth**: prefer managed identity (`--registry-identity system`)
  over admin username/password.
- Watch cost: ACA bills per vCPU-second and request. Use
  `../scripts/estimate_azure_costs.py` to track month-to-date spend.
