# Deploy Backend Only (No Firebase Required)

If you want to deploy just the backend first, here's how:

## Step 1: Install gcloud CLI

Download and install from: https://cloud.google.com/sdk/docs/install

## Step 2: Login to Google Cloud

```bash
gcloud auth login
```

## Step 3: Set Project

```bash
# Create new project (or use existing)
gcloud projects create raceiq-prod --name="RaceIQ"

# Set as active
gcloud config set project raceiq-prod

# Enable billing at: https://console.cloud.google.com/billing
```

## Step 4: Enable APIs

```bash
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

## Step 5: Deploy Backend

```bash
# Deploy to Cloud Run (this builds and deploys in one command)
gcloud run deploy raceiq-backend --source . --region us-central1 --allow-unauthenticated --memory 2Gi
```

This will:
1. Build your Docker container
2. Push to Google Container Registry
3. Deploy to Cloud Run
4. Give you a URL

## Step 6: Get Your Backend URL

```bash
gcloud run services describe raceiq-backend --region us-central1 --format 'value(status.url)'
```

Your backend will be at: `https://raceiq-backend-xxxxx-uc.a.run.app`

## Step 7: Test Backend

```bash
# Test the API
curl https://raceiq-backend-xxxxx-uc.a.run.app

# View API docs
# Open in browser: https://raceiq-backend-xxxxx-uc.a.run.app/docs
```

## Frontend Later

You can deploy the frontend later once Firebase CLI is installed:

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# Update API URL in frontend/src/api.js
# Then deploy
cd frontend
npm install
npm run build
cd ..
firebase deploy --only hosting
```

## Quick Commands Summary

```bash
# 1. Login
gcloud auth login

# 2. Set project
gcloud config set project YOUR_PROJECT_ID

# 3. Deploy backend
gcloud run deploy raceiq-backend --source . --region us-central1 --allow-unauthenticated

# Done! Backend is live.
```

## Cost

Backend only: ~$5-15/month (scales to zero when not used)
