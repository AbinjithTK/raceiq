@echo off
echo ========================================
echo Redeploying RaceIQ Backend to Google Cloud
echo ========================================

echo.
echo Building and deploying...
gcloud run deploy raceiq-backend --source . --region us-central1 --allow-unauthenticated --port 8080 --timeout 300

echo.
echo ========================================
echo Deployment Complete!
echo Backend URL: https://raceiq-backend-1091035104912.us-central1.run.app
echo ========================================
pause
