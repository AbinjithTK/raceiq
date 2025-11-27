# 🎉 RaceIQ Deployment - SUCCESS!

## ✅ Your Live URLs

### Backend API
```
https://raceiq-backend-1091035104912.us-central1.run.app
```

**Test it:**
- API Root: https://raceiq-backend-1091035104912.us-central1.run.app
- API Docs: https://raceiq-backend-1091035104912.us-central1.run.app/docs
- Vehicles: https://raceiq-backend-1091035104912.us-central1.run.app/vehicles

### Frontend App
```
https://raceiq781.web.app
or
https://raceiq781.firebaseapp.com
```

## 📊 Deployment Details

**Project ID:** `hackthetrack-479019`
**Region:** `us-central1`
**Backend:** Cloud Run (Serverless)
**Frontend:** Firebase Hosting
**Status:** ✅ LIVE

## 🔗 Share These URLs

Use these URLs in your hackathon submission:

**Live Demo:** https://raceiq781.web.app
**API Endpoint:** https://raceiq-backend-1091035104912.us-central1.run.app
**GitHub Repo:** https://github.com/AbinjithTK/raceiq

## 📈 Monitor Your Deployment

**Cloud Run Console:**
https://console.cloud.google.com/run?project=hackthetrack-479019

**Firebase Console:**
https://console.firebase.google.com/project/hackthetrack-479019

**View Logs:**
```bash
gcloud run services logs read raceiq-backend --region us-central1 --project hackthetrack-479019
```

## 💰 Cost Estimate

- Cloud Run: $5-15/month (scales to zero)
- Firebase Hosting: FREE
- **Total: ~$5-15/month**

## 🔄 Update Deployment

To update your deployment after making changes:

```bash
# Update backend
gcloud run deploy raceiq-backend --source . --region us-central1 --project hackthetrack-479019

# Update frontend
cd frontend
npm run build
cd ..
firebase deploy --only hosting --project hackthetrack-479019
```

## ✨ Your RaceIQ is LIVE!

Congratulations! Your AI-powered race engineer is now deployed on Google Cloud and accessible worldwide! 🚀

Share your demo URL in the hackathon submission and show off your amazing project!
