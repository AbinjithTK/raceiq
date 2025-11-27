#!/bin/bash

echo "==================================="
echo "  RaceIQ - Google Cloud Deployment"
echo "==================================="
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI is not installed"
    echo "   Download from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

echo "✅ gcloud CLI found"
echo ""

# Get current project
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)

if [ -z "$PROJECT_ID" ]; then
    echo "⚠️  No project set. Please enter your Google Cloud project ID:"
    read -p "Project ID: " PROJECT_ID
    gcloud config set project $PROJECT_ID
fi

echo "📦 Using project: $PROJECT_ID"
echo ""

# Deploy backend to Cloud Run
echo "🚀 Deploying backend to Cloud Run..."
echo "   This may take 3-5 minutes..."
echo ""

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

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Backend deployment failed"
    exit 1
fi

# Get backend URL
BACKEND_URL=$(gcloud run services describe raceiq-backend --region us-central1 --format 'value(status.url)')

echo ""
echo "✅ Backend deployed successfully!"
echo "   URL: $BACKEND_URL"
echo ""

# Update frontend API URL
echo "📝 Updating frontend API URL..."
sed -i.bak "s|const API_BASE_URL = .*|const API_BASE_URL = '$BACKEND_URL'|" frontend/src/api.js
rm -f frontend/src/api.js.bak

echo "✅ Frontend API URL updated"
echo ""

# Build frontend
echo "🔨 Building frontend..."
cd frontend
npm install
npm run build

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Frontend build failed"
    exit 1
fi

cd ..
echo "✅ Frontend built successfully"
echo ""

# Check if firebase is installed
if ! command -v firebase &> /dev/null; then
    echo "⚠️  Firebase CLI not found. Installing..."
    npm install -g firebase-tools
fi

# Deploy to Firebase
echo "🚀 Deploying frontend to Firebase..."
firebase deploy --only hosting

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Frontend deployment failed"
    echo "   Run 'firebase login' first if not authenticated"
    exit 1
fi

# Get Firebase URL
FIREBASE_URL="https://${PROJECT_ID}.web.app"

echo ""
echo "==================================="
echo "  ✅ Deployment Complete!"
echo "==================================="
echo ""
echo "🎉 Your RaceIQ is now live!"
echo ""
echo "Backend API:  $BACKEND_URL"
echo "Frontend App: $FIREBASE_URL"
echo "API Docs:     $BACKEND_URL/docs"
echo ""
echo "Next steps:"
echo "1. Visit $FIREBASE_URL to test your app"
echo "2. Share these URLs in your hackathon submission"
echo "3. Monitor usage at: https://console.cloud.google.com"
echo ""
