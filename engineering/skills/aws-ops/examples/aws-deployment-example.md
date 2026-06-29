# Example: Deploying a Node.js App to ECS Fargate

End-to-end worked example of shipping a containerized Node.js API to Amazon ECS
on Fargate, fronted by an Application Load Balancer. Adjust names, account, and
region to your environment.

## Assumptions

- App listens on port 3000 and exposes `GET /health`.
- An ECR repo, ECS cluster, VPC with two public/private subnets, and an ALB
  target group already exist (or are created via IaC, not shown here).
- Profile `prod` resolves valid credentials; region `eu-west-1`.

## 1. Containerize

```dockerfile
# Dockerfile
FROM node:20-slim
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY . .
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s CMD node -e "fetch('http://localhost:3000/health').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"
CMD ["node", "server.js"]
```

## 2. Build and push to ECR

```bash
ACCOUNT=$(aws sts get-caller-identity --profile prod --query Account --output text)
REGION=eu-west-1
REPO="$ACCOUNT.dkr.ecr.$REGION.amazonaws.com/orders-api"
TAG=$(git rev-parse --short HEAD)

aws ecr get-login-password --profile prod --region $REGION \
  | docker login --username AWS --password-stdin "$ACCOUNT.dkr.ecr.$REGION.amazonaws.com"

docker build --platform linux/amd64 -t "$REPO:$TAG" .
docker push "$REPO:$TAG"
```

> Build for `linux/amd64` explicitly — Fargate runs amd64 by default, and an
> Apple Silicon laptop will otherwise produce an arm64 image that crash-loops.

## 3. Register a new task definition

`task-def.json` (key fields):

```json
{
  "family": "orders-api",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::ACCOUNT:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::ACCOUNT:role/orders-api-task",
  "containerDefinitions": [
    {
      "name": "orders-api",
      "image": "ACCOUNT.dkr.ecr.eu-west-1.amazonaws.com/orders-api:TAG",
      "portMappings": [{ "containerPort": 3000, "protocol": "tcp" }],
      "secrets": [
        { "name": "DATABASE_URL", "valueFrom": "arn:aws:ssm:eu-west-1:ACCOUNT:parameter/orders-api/DATABASE_URL" }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/orders-api",
          "awslogs-region": "eu-west-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

```bash
sed -e "s/ACCOUNT/$ACCOUNT/g" -e "s/TAG/$TAG/g" task-def.json > /tmp/task-def.json
TASK_DEF_ARN=$(aws ecs register-task-definition \
  --cli-input-json file:///tmp/task-def.json \
  --profile prod --region $REGION \
  --query 'taskDefinition.taskDefinitionArn' --output text)
echo "Registered: $TASK_DEF_ARN"
```

> Inject config as SSM/Secrets Manager `secrets`, never as plaintext env vars
> baked into the image.

## 4. Roll out the deployment

```bash
aws ecs update-service \
  --cluster prod \
  --service orders-api \
  --task-definition "$TASK_DEF_ARN" \
  --force-new-deployment \
  --profile prod --region $REGION
```

ECS performs a rolling replacement governed by the service's
`deploymentConfiguration` (default min 100% / max 200%), draining old tasks
from the ALB target group only after new ones pass health checks.

## 5. Watch the rollout

```bash
aws ecs wait services-stable \
  --cluster prod --services orders-api \
  --profile prod --region $REGION

aws ecs describe-services \
  --cluster prod --services orders-api \
  --profile prod --region $REGION \
  --query 'services[0].deployments'
```

Confirm target health:

```bash
aws elbv2 describe-target-health \
  --target-group-arn <tg-arn> \
  --profile prod --region $REGION \
  --query 'TargetHealthDescriptions[].TargetHealth.State'
```

## 6. Rollback

Roll back by pointing the service at the previous task definition revision:

```bash
aws ecs update-service \
  --cluster prod --service orders-api \
  --task-definition orders-api:<previous-revision> \
  --force-new-deployment \
  --profile prod --region $REGION
```

## Gotchas

- **Health check grace period** too low → ECS kills slow-starting tasks. Set
  `healthCheckGracePeriodSeconds` to cover cold start.
- **Execution role** missing `ssm:GetParameters` / `secretsmanager:GetSecretValue`
  → tasks fail before the container starts; check stopped-task `stoppedReason`.
- **Security group** on the service must allow the ALB SG on port 3000.
- Watch costs: idle Fargate tasks still bill. Right-size `cpu`/`memory` and use
  the cost script in `../scripts/list_running_costs.py`.
