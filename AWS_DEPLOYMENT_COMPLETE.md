# Complete AWS Deployment Guide for RaceIQ

## Architecture Overview

- **Frontend**: AWS Amplify (React app)
- **Backend**: AWS App Runner or ECS (FastAPI container)
- **Storage**: S3 (CSV data files)
- **Database**: DynamoDB (optional, for user data)
- **CDN**: CloudFront (fast global delivery)

## Prerequisites

1. AWS Account with billing enabled
2. AWS CLI installed
3. Docker installed
4. GitHub repository (already done ✅)

## Part 1: Deploy Frontend to AWS Amplify

### Step 1.1: Connect GitHub to Amplify

1. Go to AWS Console → AWS Amplify
2. Click "New app" → "Host web app"
3. Choose "GitHub"
4. Authorize AWS Amplify to access your GitHub
5. Select repository: `AbinjithTK/raceiq`
6. Select branch: `main`

### Step 1.2: Configure Build Settings

Amplify should auto-detect Vite. If not, use this configuration:

```yaml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - cd frontend
        - npm install
    build:
      commands:
        - npm run build
  artifacts:
    baseDirectory: frontend/dist
    files:
      - '**/*'
  cache:
    paths:
      - frontend/node_modules/**/*
```

### Step 1.3: Add Environment Variables

In Amplify Console → Environment variables:
- `VITE_API_URL` = (will add after backend deployment)

### Step 1.4: Deploy

Click "Save and deploy"

Your frontend will be at: `https://main.xxxxx.amplifyapp.com`

## Part 2: Deploy Backend to AWS

### Option A: AWS App Runner (Easiest)

#### Step 2A.1: Create Dockerfile

Already exists, but verify it's correct:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY barber/ ./barber/
COPY COTA/ ./COTA/
COPY indianapolis/ ./indianapolis/
COPY road-america/ ./road-america/
COPY sebring/ ./sebring/
COPY Sonoma/ ./Sonoma/
COPY virginia-international-raceway/ ./virginia-international-raceway/
COPY rag_dataset/ ./rag_dataset/

EXPOSE 8080

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

#### Step 2A.2: Push to Amazon ECR

```bash
# Install AWS CLI
# Download from: https://aws.amazon.com/cli/

# Configure AWS
aws configure
# Enter: Access Key ID, Secret Access Key, Region (us-east-1), Output format (json)

# Create ECR repository
aws ecr create-repository --repository-name raceiq-backend --region us-east-1

# Get login command
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Build Docker image
docker build -t raceiq-backend .

# Tag image
docker tag raceiq-backend:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/raceiq-backend:latest

# Push to ECR
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/raceiq-backend:latest
```

#### Step 2A.3: Create App Runner Service

1. Go to AWS Console → App Runner
2. Click "Create service"
3. Source: Container registry → Amazon ECR
4. Select your image: `raceiq-backend:latest`
5. Deployment: Automatic
6. Service name: `raceiq-backend`
7. Port: `8080`
8. CPU: 1 vCPU, Memory: 2 GB
9. Environment variables:
   - `PYTHONUNBUFFERED` = `1`
10. Click "Create & deploy"

Your backend will be at: `https://xxxxx.us-east-1.awsapprunner.com`

### Option B: AWS ECS Fargate (More Control)

#### Step 2B.1: Create ECS Cluster

```bash
aws ecs create-cluster --cluster-name raceiq-cluster --region us-east-1
```

#### Step 2B.2: Create Task Definition

Create `task-definition.json`:

```json
{
  "family": "raceiq-backend",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "containerDefinitions": [
    {
      "name": "raceiq-backend",
      "image": "YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/raceiq-backend:latest",
      "portMappings": [
        {
          "containerPort": 8080,
          "protocol": "tcp"
        }
      ],
      "essential": true,
      "environment": [
        {
          "name": "PYTHONUNBUFFERED",
          "value": "1"
        }
      ]
    }
  ]
}
```

Register task:
```bash
aws ecs register-task-definition --cli-input-json file://task-definition.json
```

#### Step 2B.3: Create Service

```bash
aws ecs create-service \
  --cluster raceiq-cluster \
  --service-name raceiq-backend \
  --task-definition raceiq-backend \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxxxx],securityGroups=[sg-xxxxx],assignPublicIp=ENABLED}"
```

## Part 3: Upload Data to S3 (Optional)

### Step 3.1: Create S3 Bucket

```bash
aws s3 mb s3://raceiq-data --region us-east-1
```

### Step 3.2: Upload CSV Files

```bash
# Upload all track data
aws s3 sync barber/ s3://raceiq-data/barber/
aws s3 sync COTA/ s3://raceiq-data/COTA/
aws s3 sync indianapolis/ s3://raceiq-data/indianapolis/
aws s3 sync road-america/ s3://raceiq-data/road-america/
aws s3 sync sebring/ s3://raceiq-data/sebring/
aws s3 sync Sonoma/ s3://raceiq-data/Sonoma/
aws s3 sync virginia-international-raceway/ s3://raceiq-data/virginia-international-raceway/
```

### Step 3.3: Update Backend to Read from S3

Install boto3:
```bash
pip install boto3
```

Update `src/data_loader.py`:
```python
import boto3
import pandas as pd
from io import StringIO

s3 = boto3.client('s3')
BUCKET_NAME = 'raceiq-data'

def load_from_s3(file_path):
    obj = s3.get_object(Bucket=BUCKET_NAME, Key=file_path)
    return pd.read_csv(StringIO(obj['Body'].read().decode('utf-8')))
```

## Part 4: Connect Frontend to Backend

### Step 4.1: Update Frontend API URL

In Amplify Console:
1. Go to Environment variables
2. Update `VITE_API_URL` = `https://your-apprunner-url.amazonaws.com`

### Step 4.2: Redeploy Frontend

Amplify will auto-redeploy when you update environment variables.

Or manually:
1. Go to Amplify Console
2. Click "Redeploy this version"

## Part 5: Setup Custom Domain (Optional)

### Step 5.1: Add Domain to Amplify

1. Amplify Console → Domain management
2. Add domain: `raceiq.com`
3. Follow DNS configuration steps

### Step 5.2: Add Domain to App Runner

1. App Runner Console → Custom domains
2. Add domain: `api.raceiq.com`
3. Update DNS with provided CNAME

## Part 6: Enable HTTPS and CORS

### Step 6.1: CORS Configuration

Already configured in `src/api/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update to specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

For production, update to:
```python
allow_origins=["https://main.xxxxx.amplifyapp.com", "https://raceiq.com"]
```

### Step 6.2: HTTPS

Both Amplify and App Runner provide HTTPS automatically ✅

## Part 7: Monitoring and Logging

### Step 7.1: CloudWatch Logs

```bash
# View App Runner logs
aws logs tail /aws/apprunner/raceiq-backend/application --follow

# View Amplify logs
# Available in Amplify Console → Logs
```

### Step 7.2: Setup Alarms

```bash
# Create CPU alarm
aws cloudwatch put-metric-alarm \
  --alarm-name raceiq-high-cpu \
  --alarm-description "Alert when CPU exceeds 80%" \
  --metric-name CPUUtilization \
  --namespace AWS/AppRunner \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold
```

## Cost Estimate

### Monthly Costs (Low Traffic)

- **Amplify Hosting**: $0-5 (free tier: 1000 build minutes, 15GB storage)
- **App Runner**: $25-40 (1 vCPU, 2GB RAM, always on)
- **ECR**: $1 (storage for Docker images)
- **S3**: $1-5 (depends on data size)
- **Data Transfer**: $5-10 (depends on traffic)

**Total**: ~$30-60/month

### Cost Optimization

1. Use App Runner with auto-scaling (scale to zero when idle)
2. Use S3 Intelligent-Tiering for data
3. Enable CloudFront caching
4. Use Reserved Instances for predictable workloads

## Quick Deploy Script

Create `deploy-aws.sh`:

```bash
#!/bin/bash

echo "=== RaceIQ AWS Deployment ==="

# Variables
AWS_REGION="us-east-1"
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_REPO="raceiq-backend"
IMAGE_TAG="latest"

# Build and push Docker image
echo "Building Docker image..."
docker build -t $ECR_REPO .

echo "Tagging image..."
docker tag $ECR_REPO:$IMAGE_TAG $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:$IMAGE_TAG

echo "Logging into ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

echo "Pushing to ECR..."
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:$IMAGE_TAG

echo "✅ Backend deployed to ECR"
echo "Next: Create App Runner service in AWS Console"
echo "Image: $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:$IMAGE_TAG"
```

Make executable and run:
```bash
chmod +x deploy-aws.sh
./deploy-aws.sh
```

## Troubleshooting

### Backend not starting
```bash
# Check App Runner logs
aws apprunner list-operations --service-arn YOUR_SERVICE_ARN

# Check container logs
aws logs tail /aws/apprunner/raceiq-backend/application --follow
```

### Frontend can't reach backend
- Check CORS settings in backend
- Verify VITE_API_URL environment variable
- Check App Runner security settings

### Docker build fails
```bash
# Test locally first
docker build -t raceiq-backend .
docker run -p 8080:8080 raceiq-backend

# Test API
curl http://localhost:8080
```

## Final Checklist

- [ ] Frontend deployed to Amplify
- [ ] Backend deployed to App Runner/ECS
- [ ] Data uploaded to S3 (optional)
- [ ] Environment variables configured
- [ ] CORS enabled
- [ ] HTTPS working
- [ ] Custom domain configured (optional)
- [ ] Monitoring enabled
- [ ] Costs reviewed

## Your Deployed URLs

After deployment, you'll have:

- **Frontend**: `https://main.xxxxx.amplifyapp.com`
- **Backend**: `https://xxxxx.us-east-1.awsapprunner.com`
- **Custom Domain** (optional): `https://raceiq.com`

Share these URLs in your hackathon submission! 🚀
