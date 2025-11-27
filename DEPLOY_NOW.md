# Deploy RaceIQ to Google Cloud - Quick Start

## ✅ Files Created

All deployment files are ready:
- `Dockerfile` - Container configuration
- `cloudbuild.yaml` - CI/CD configuration
- `firebase.json` - Firebase hosting config
- `.firebaserc` - Firebase project config
- `.dockerignore` - Files to exclude from container
- `deploy-gcloud.bat` - Windows deployment script
- `deploy-gcloud.sh` - Mac/Linux deployment script

## 🚀 Deploy in 3 Steps

### Step 1: Install Required Tools

**Install gcloud CLI:**
- Windows: https://cloud.google.com/sdk/docs/install
- Mac: `brew install google-cloud-sdk`
- Linux: `curl https://sdk.cloud.google.com | bash`

**Install Firebase CLI:**
```bash
npm install -g firebase-tools
```

### Step 2: Login and Setup

```bash
# Login to Google Cloud
gcloud auth login

# Login to Firebase
firebase login

# Set your project ID (or create new project)
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable aiplatform.googleapis.com
```

### Step 3: Deploy!

**Windows:**
```bash
deploy-gcloud.bat
```

**Mac/Linux:**
```bash
chmod +x deploy-gcloud.sh
./deploy-gcloud.sh
```

That's it! The script will:
1. ✅ Deploy backend to Cloud Run (~3-5 minutes)
2. ✅ Update frontend API URL automatically
3. ✅ Build React frontend
4. ✅ Deploy frontend to Firebase
5. ✅ Give you live URLs

## 📋 What You'll Get

After deployment:

- **Backend API**: `https://raceiq-backend-xxxxx-uc.a.run.app`
- **Frontend App**: `https://YOUR-PROJECT.web.app`
- **API Docs**: `https://raceiq-backend-xxxxx-uc.a.run.app/docs`

## 💰 Cost

- Cloud Run: $5-15/month (scales to zero)
- Firebase: FREE
- Total: ~$10-20/month

## 🔧 Manual Deployment (Alternative)

If you prefer manual control:

### Deploy Backend:
```bash
gcloud run deploy raceiq-backend \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi
```

### Deploy Frontend:
```bash
# Update API URL in frontend/src/api.js first
cd frontend
npm install
npm run build
cd ..
firebase deploy --only hosting
```

## 🆘 Troubleshooting

**"gcloud: command not found"**
- Install gcloud CLI from link above
- Restart terminal after installation

**"firebase: command not found"**
```bash
npm install -g firebase-tools
```

**"Project not found"**
```bash
# Create new project
gcloud projects create raceiq-prod --name="RaceIQ"
gcloud config set project raceiq-prod

# Enable billing at: https://console.cloud.google.com/billing
```

**"Permission denied"**
```bash
# Make script executable (Mac/Linux)
chmod +x deploy-gcloud.sh
```

**Backend deployment fails**
- Check Dockerfile exists
- Verify requirements.txt is present
- Check logs: `gcloud run services logs read raceiq-backend --region us-central1`

**Frontend deployment fails**
- Run `firebase login` first
- Check firebase.json exists
- Verify frontend/dist folder exists after build

## 📊 Monitor Your Deployment

**View logs:**
```bash
gcloud run services logs tail raceiq-backend --region us-central1
```

**View metrics:**
```bash
gcloud run services describe raceiq-backend --region us-central1
```

**Or use Console:**
- Cloud Run: https://console.cloud.google.com/run
- Firebase: https://console.firebase.google.com

## 🔄 Update Deployment

After making changes:

```bash
# Just run the deploy script again
deploy-gcloud.bat  # Windows
./deploy-gcloud.sh # Mac/Linux
```

Or manually:
```bash
# Update backend
gcloud run deploy raceiq-backend --source . --region us-central1

# Update frontend
cd frontend && npm run build && cd ..
firebase deploy --only hosting
```

## ✨ You're Ready!

Just run:
```bash
deploy-gcloud.bat
```

And your RaceIQ will be live in ~5 minutes! 🚀
