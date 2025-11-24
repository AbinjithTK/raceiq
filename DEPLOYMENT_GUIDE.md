# RaceIQ Deployment Guide

## Option 1: Google Cloud (Recommended - Already using Vertex AI)

### Quick Deploy

**Backend (Cloud Run):**
1. Create `Dockerfile` in root
2. Deploy: `gcloud run deploy raceiq-backend --source .`
3. Get URL: Your API will be at `https://raceiq-xxxxx.run.app`

**Frontend (Firebase Hosting):**
1. Install: `npm install -g firebase-tools`
2. Init: `firebase init hosting`
3. Build: `cd frontend && npm run build`
4. Deploy: `firebase deploy`

### Detailed Steps

**1. Setup Google Cloud**
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud services enable run.googleapis.com storage.googleapis.com
```

**2. Create Dockerfile**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ ./src/
COPY barber/ ./barber/
COPY rag_dataset/ ./rag_dataset/
EXPOSE 8080
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

**3. Deploy Backend**
```bash
gcloud run deploy raceiq-backend \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi
```

**4. Deploy Frontend**
```bash
# Update API URL in frontend/src/api.js with your Cloud Run URL
cd frontend
npm install
npm run build
firebase deploy
```

**Cost**: ~$10-20/month

---

## Option 2: AWS Amplify

### Quick Deploy

**Frontend (Amplify Hosting):**
1. Push code to GitHub
2. Go to AWS Amplify Console
3. Connect repository
4. Amplify auto-detects Vite/React
5. Deploy

**Backend (AWS App Runner or Lambda):**
1. Containerize with Docker
2. Push to ECR
3. Deploy to App Runner

### Detailed Steps

**1. Deploy Frontend to Amplify**

```bash
# Push to GitHub first
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/raceiq.git
git push -u origin main
```

Then in AWS Console:
1. Go to AWS Amplify
2. Click "New app" → "Host web app"
3. Connect GitHub repository
4. Configure build settings:
   - Build command: `cd frontend && npm install && npm run build`
   - Output directory: `frontend/dist`
5. Click "Save and deploy"

**2. Deploy Backend to App Runner**

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ ./src/
COPY barber/ ./barber/
EXPOSE 8080
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

Deploy:
```bash
# Install AWS CLI
aws configure

# Create ECR repository
aws ecr create-repository --repository-name raceiq-backend

# Build and push
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com
docker build -t raceiq-backend .
docker tag raceiq-backend:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/raceiq-backend:latest
docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/raceiq-backend:latest

# Create App Runner service in AWS Console
# Point to ECR image
```

**3. Update Frontend API URL**

In Amplify Console:
1. Go to "Environment variables"
2. Add: `VITE_API_URL` = `https://your-app-runner-url.amazonaws.com`

Update `frontend/src/api.js`:
```javascript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001'
```

**Cost**: ~$15-30/month

---

## Option 3: Simple Static Hosting (Frontend Only)

If you just want to demo the frontend without backend:

### Netlify (Easiest)
```bash
cd frontend
npm install
npm run build
npx netlify-cli deploy --prod --dir=dist
```

### Vercel
```bash
cd frontend
npm install
npm run build
npx vercel --prod
```

### GitHub Pages
```bash
cd frontend
npm install
npm run build
# Push dist/ folder to gh-pages branch
```

**Note**: These only host the frontend. Backend needs separate hosting.

---

## Comparison

| Feature | Google Cloud | AWS Amplify | Static Only |
|---------|-------------|-------------|-------------|
| Frontend | Firebase | Amplify | Netlify/Vercel |
| Backend | Cloud Run | App Runner | None |
| Database | Cloud Storage | S3 | None |
| AI | Vertex AI ✅ | Bedrock | None |
| Cost/month | $10-20 | $15-30 | Free-$5 |
| Setup Time | 30 min | 45 min | 5 min |
| Best For | Production | AWS users | Demo only |

## Recommendation

**Use Google Cloud** because:
- Already using Vertex AI
- Simpler integration
- Better for Python backend
- Lower cost
- Faster deployment

## Quick Start Commands

**Google Cloud:**
```bash
# Backend
gcloud run deploy raceiq-backend --source . --region us-central1 --allow-unauthenticated

# Frontend
cd frontend && npm run build && firebase deploy
```

**AWS Amplify:**
```bash
# Just push to GitHub, Amplify auto-deploys
git push origin main
```

**Static Demo:**
```bash
cd frontend && npm run build && npx netlify-cli deploy --prod --dir=dist
```
