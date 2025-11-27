# Complete Google Cloud Deployment Guide for RaceIQ

## Why Google Cloud?
✅ Already using Vertex AI for RAG  
✅ Better Python/FastAPI support  
✅ Simpler deployment  
✅ Lower cost (~$10-20/month vs AWS $30-60)

## Architecture

- **Frontend**: Firebase Hosting (static React app)
- **Backend**: Cloud Run (serverless FastAPI container)
- **Storage**: Cloud Storage (CSV data files)
- **AI**: Vertex AI (already integrated ✅)
- **CDN**: Firebase CDN (automatic)

## Prerequisites

1. Google Cloud account
2. `gcloud` CLI installed
3. Firebase CLI installed
4. Docker installed (optional - Cloud Run can build for you)

## Part 1: Setup Google Cloud Project

### Step 1.1: Install gcloud CLI

**Windows:**
Download from: https://cloud.google.com/sdk/docs/install

**Mac:**
```bash
brew install google-cloud-sdk
```

**Linux:**
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

### Step 1.2: Initialize gcloud

```bash
# Login to Google Cloud
gcloud auth login

# Create new project (or use existing)
gcloud projects create raceiq-prod --name="RaceIQ"

# Set as active project
gcloud config set project raceiq-prod

# Enable billing (required)
# Go to: https://console.cloud.google.com/billing
# Link billing account to raceiq-prod

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable aiplatform.googleapis.com
```

## Part 2: Deploy Backend to Cloud Run

### Step 2.1: Create Dockerfile

Create `Dockerfile` in project root:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY barber/ ./barber/
COPY COTA/ ./COTA/
COPY indianapolis/ ./indianapolis/
COPY road-america/ ./road-america/
COPY sebring/ ./sebring/
COPY Sonoma/ ./Sonoma/
COPY virginia-international-raceway/ ./virginia-international-raceway/
COPY rag_dataset/ ./rag_dataset/

# Expose port 8080 (Cloud Run requirement)
EXPOSE 8080

# Run FastAPI
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### Step 2.2: Create .dockerignore

Create `.dockerignore`:

```
.venv/
.vscode/
.kiro/
frontend/
docs/
*.md
*.pyc
__pycache__/
.git/
.gitignore
node_modules/
```

### Step 2.3: Deploy to Cloud Run (Easiest Method)

```bash
# Deploy directly from source (Cloud Run builds for you)
gcloud run deploy raceiq-backend \
  --source . \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --max-instances 10 \
  --min-instances 0

# This will:
# 1. Build Docker image using Cloud Build
# 2. Push to Container Registry
# 3. Deploy to Cloud Run
# 4. Give you a URL
```

**Your backend URL:**
```
https://raceiq-backend-xxxxx-uc.a.run.app
```

### Alternative: Build Docker Locally

```bash
# Build image
docker build -t gcr.io/raceiq-prod/raceiq-backend .

# Push to Google Container Registry
docker push gcr.io/raceiq-prod/raceiq-backend

# Deploy
gcloud run deploy raceiq-backend \
  --image gcr.io/raceiq-prod/raceiq-backend \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated
```

## Part 3: Deploy Frontend to Firebase Hosting

### Step 3.1: Install Firebase CLI

```bash
npm install -g firebase-tools
```

### Step 3.2: Login to Firebase

```bash
firebase login
```

### Step 3.3: Initialize Firebase

```bash
# In project root
firebase init hosting

# Answer prompts:
# ? What do you want to use as your public directory? frontend/dist
# ? Configure as a single-page app? Yes
# ? Set up automatic builds with GitHub? No
# ? File frontend/dist/index.html already exists. Overwrite? No
```

This creates `firebase.json`:

```json
{
  "hosting": {
    "public": "frontend/dist",
    "ignore": [
      "firebase.json",
      "**/.*",
      "**/node_modules/**"
    ],
    "rewrites": [
      {
        "source": "**",
        "destination": "/index.html"
      }
    ]
  }
}
```

### Step 3.4: Update Frontend API URL

Edit `frontend/src/api.js`:

```javascript
// Replace with your Cloud Run URL
const API_BASE_URL = 'https://raceiq-backend-xxxxx-uc.a.run.app'

export const fetchVehicles = async () => {
  const response = await fetch(`${API_BASE_URL}/vehicles`)
  return response.json()
}
// ... rest of the file
```

### Step 3.5: Build and Deploy Frontend

```bash
# Build React app
cd frontend
npm install
npm run build

# Deploy to Firebase
cd ..
firebase deploy --only hosting
```

**Your frontend URL:**
```
https://raceiq-prod.web.app
or
https://raceiq-prod.firebaseapp.com
```

## Part 4: Upload Data to Cloud Storage (Optional)

If you want to store CSV files in Cloud Storage instead of container:

### Step 4.1: Create Storage Bucket

```bash
# Create bucket
gsutil mb -l us-central1 gs://raceiq-data

# Upload track data
gsutil -m cp -r barber/ gs://raceiq-data/
gsutil -m cp -r COTA/ gs://raceiq-data/
gsutil -m cp -r indianapolis/ gs://raceiq-data/
gsutil -m cp -r road-america/ gs://raceiq-data/
gsutil -m cp -r sebring/ gs://raceiq-data/
gsutil -m cp -r Sonoma/ gs://raceiq-data/
gsutil -m cp -r virginia-international-raceway/ gs://raceiq-data/
gsutil -m cp -r rag_dataset/ gs://raceiq-data/
```

### Step 4.2: Make Bucket Accessible

```bash
# Get Cloud Run service account
gcloud run services describe raceiq-backend --region us-central1 --format 'value(spec.template.spec.serviceAccountName)'

# Grant access
gsutil iam ch serviceAccount:YOUR-PROJECT-NUMBER-compute@developer.gserviceaccount.com:objectViewer gs://raceiq-data
```

### Step 4.3: Update Backend to Read from Cloud Storage

Install google-cloud-storage:
```bash
pip install google-cloud-storage
```

Update `src/data_loader.py`:
```python
from google.cloud import storage
import pandas as pd
from io import StringIO

storage_client = storage.Client()
BUCKET_NAME = 'raceiq-data'

def load_from_gcs(file_path):
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(file_path)
    content = blob.download_as_text()
    return pd.read_csv(StringIO(content))
```

## Part 5: Configure Vertex AI

### Step 5.1: Enable Vertex AI API

```bash
gcloud services enable aiplatform.googleapis.com
```

### Step 5.2: Grant Permissions

```bash
# Get project number
PROJECT_NUMBER=$(gcloud projects describe raceiq-prod --format='value(projectNumber)')

# Grant Vertex AI access to Cloud Run
gcloud projects add-iam-policy-binding raceiq-prod \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role="roles/aiplatform.user"
```

### Step 5.3: Set Environment Variables

```bash
gcloud run services update raceiq-backend \
  --region us-central1 \
  --set-env-vars="VERTEX_AI_PROJECT=raceiq-prod,VERTEX_AI_LOCATION=us-central1"
```

## Part 6: Setup Custom Domain (Optional)

### Step 6.1: Add Domain to Firebase

```bash
# Add custom domain
firebase hosting:channel:deploy production --domain raceiq.com
```

Follow instructions to:
1. Verify domain ownership
2. Add DNS records

### Step 6.2: Add Domain to Cloud Run

```bash
# Map domain to Cloud Run
gcloud run domain-mappings create \
  --service raceiq-backend \
  --domain api.raceiq.com \
  --region us-central1
```

Add DNS record:
```
Type: CNAME
Name: api
Value: ghs.googlehosted.com
```

## Part 7: CI/CD with Cloud Build (Optional)

### Step 7.1: Create cloudbuild.yaml

Create `cloudbuild.yaml` in project root:

```yaml
steps:
  # Build backend container
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/raceiq-backend', '.']
  
  # Push to Container Registry
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/raceiq-backend']
  
  # Deploy to Cloud Run
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: gcloud
    args:
      - 'run'
      - 'deploy'
      - 'raceiq-backend'
      - '--image'
      - 'gcr.io/$PROJECT_ID/raceiq-backend'
      - '--region'
      - 'us-central1'
      - '--platform'
      - 'managed'
      - '--allow-unauthenticated'
      - '--memory'
      - '2Gi'

images:
  - 'gcr.io/$PROJECT_ID/raceiq-backend'
```

### Step 7.2: Connect to GitHub

```bash
# Create trigger
gcloud builds triggers create github \
  --repo-name=raceiq \
  --repo-owner=AbinjithTK \
  --branch-pattern="^main$" \
  --build-config=cloudbuild.yaml
```

Now every push to `main` branch auto-deploys! 🚀

## Quick Deploy Script

Create `deploy-gcloud.sh`:

```bash
#!/bin/bash

echo "==================================="
echo "  RaceIQ - Google Cloud Deployment"
echo "==================================="

# Set project
gcloud config set project raceiq-prod

# Deploy backend
echo "📦 Deploying backend to Cloud Run..."
gcloud run deploy raceiq-backend \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi

# Get backend URL
BACKEND_URL=$(gcloud run services describe raceiq-backend --region us-central1 --format 'value(status.url)')
echo "✅ Backend deployed: $BACKEND_URL"

# Update frontend API URL
echo "📝 Updating frontend API URL..."
sed -i "s|const API_BASE_URL = .*|const API_BASE_URL = '$BACKEND_URL'|" frontend/src/api.js

# Build frontend
echo "🔨 Building frontend..."
cd frontend
npm install
npm run build
cd ..

# Deploy frontend
echo "🚀 Deploying frontend to Firebase..."
firebase deploy --only hosting

echo ""
echo "==================================="
echo "  ✅ Deployment Complete!"
echo "==================================="
echo ""
echo "Backend:  $BACKEND_URL"
echo "Frontend: https://raceiq-prod.web.app"
echo ""
```

Make executable and run:
```bash
chmod +x deploy-gcloud.sh
./deploy-gcloud.sh
```

## Cost Estimate

### Monthly Costs (Low-Medium Traffic)

- **Cloud Run**: $5-15 (pay per request, scales to zero)
- **Firebase Hosting**: Free (10GB storage, 360MB/day transfer)
- **Cloud Storage**: $1-3 (depends on data size)
- **Cloud Build**: Free (120 build-minutes/day)
- **Vertex AI**: $0.50-5 (pay per request)

**Total**: ~$10-25/month

Much cheaper than AWS! 💰

## Monitoring

### View Logs

```bash
# Cloud Run logs
gcloud run services logs read raceiq-backend --region us-central1 --limit 50

# Follow logs in real-time
gcloud run services logs tail raceiq-backend --region us-central1
```

### View Metrics

```bash
# Get service details
gcloud run services describe raceiq-backend --region us-central1

# View in console
# https://console.cloud.google.com/run
```

## Troubleshooting

### Backend not starting

```bash
# Check logs
gcloud run services logs read raceiq-backend --region us-central1 --limit 100

# Common issues:
# - Port must be 8080
# - Check Dockerfile CMD
# - Verify requirements.txt
```

### Frontend can't reach backend

```bash
# Check CORS in src/api/main.py
# Verify API_BASE_URL in frontend/src/api.js
# Test backend directly:
curl https://raceiq-backend-xxxxx-uc.a.run.app
```

### Build fails

```bash
# Test Docker build locally
docker build -t raceiq-backend .
docker run -p 8080:8080 raceiq-backend

# Test locally
curl http://localhost:8080
```

### Vertex AI errors

```bash
# Check if API is enabled
gcloud services list --enabled | grep aiplatform

# Check permissions
gcloud projects get-iam-policy raceiq-prod
```

## Final Checklist

- [ ] gcloud CLI installed and configured
- [ ] Project created with billing enabled
- [ ] Backend deployed to Cloud Run
- [ ] Frontend deployed to Firebase
- [ ] API URL updated in frontend
- [ ] Vertex AI permissions configured
- [ ] CORS enabled in backend
- [ ] Custom domain configured (optional)
- [ ] CI/CD setup (optional)
- [ ] Monitoring enabled

## Your Deployed URLs

After deployment:

- **Frontend**: `https://raceiq-prod.web.app`
- **Backend**: `https://raceiq-backend-xxxxx-uc.a.run.app`
- **API Docs**: `https://raceiq-backend-xxxxx-uc.a.run.app/docs`

## Next Steps

1. Test the deployed application
2. Share URLs in hackathon submission
3. Monitor usage and costs
4. Setup custom domain
5. Enable CI/CD for auto-deployment

🎉 Your RaceIQ is now live on Google Cloud!
