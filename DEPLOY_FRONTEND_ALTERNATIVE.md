# Deploy Frontend - Alternative Methods

Firebase is having authentication issues. Here are simpler alternatives:

## Option 1: Use Cloud Storage + Load Balancer (Recommended)

### Step 1: Create Storage Bucket
```bash
gsutil mb -b on gs://raceiq-frontend
gsutil web set -m index.html -e index.html gs://raceiq-frontend
```

### Step 2: Upload Frontend
```bash
cd frontend/dist
gsutil -m cp -r * gs://raceiq-frontend/
gsutil iam ch allUsers:objectViewer gs://raceiq-frontend
```

### Step 3: Access
Your frontend will be at:
```
https://storage.googleapis.com/raceiq-frontend/index.html
```

## Option 2: Deploy to Netlify (Easiest)

```bash
cd frontend
npm install -g netlify-cli
netlify deploy --prod --dir=dist
```

Follow prompts and you'll get a URL like:
```
https://raceiq-xxxxx.netlify.app
```

## Option 3: Deploy to Vercel

```bash
cd frontend
npm install -g vercel
vercel --prod
```

You'll get:
```
https://raceiq-xxxxx.vercel.app
```

## Option 4: Fix Firebase Login

```bash
# Logout and login again
firebase logout
firebase login --reauth

# Then deploy
firebase deploy --only hosting --project hackthetrack-479019
```

## Current Status

✅ **Backend is LIVE:**
```
https://raceiq-backend-1091035104912.us-central1.run.app
```

⏳ **Frontend needs deployment** - Choose one option above

## Recommendation

Use **Netlify** (Option 2) - it's the fastest:
```bash
cd frontend
npx netlify-cli deploy --prod --dir=dist
```

Takes 30 seconds and gives you a live URL!
