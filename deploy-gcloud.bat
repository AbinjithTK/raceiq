@echo off
REM RaceIQ Google Cloud Deployment Script for Windows

echo ===================================
echo   RaceIQ - Google Cloud Deployment
echo ===================================
echo.

REM Check if gcloud is installed
gcloud --version >nul 2>&1
if errorlevel 1 (
    echo X gcloud CLI is not installed
    echo   Download from: https://cloud.google.com/sdk/docs/install
    pause
    exit /b 1
)

echo [OK] gcloud CLI found
echo.

REM Get current project
for /f "tokens=*" %%i in ('gcloud config get-value project 2^>nul') do set PROJECT_ID=%%i

if "%PROJECT_ID%"=="" (
    echo [!] No project set. Please enter your Google Cloud project ID:
    set /p PROJECT_ID="Project ID: "
    gcloud config set project %PROJECT_ID%
)

echo [*] Using project: %PROJECT_ID%
echo.

REM Deploy backend
echo [*] Deploying backend to Cloud Run...
echo    This may take 3-5 minutes...
echo.

gcloud run deploy raceiq-backend --source . --region us-central1 --platform managed --allow-unauthenticated --memory 2Gi --cpu 2 --timeout 300 --max-instances 10 --min-instances 0

if errorlevel 1 (
    echo.
    echo X Backend deployment failed
    pause
    exit /b 1
)

REM Get backend URL
for /f "tokens=*" %%i in ('gcloud run services describe raceiq-backend --region us-central1 --format "value(status.url)"') do set BACKEND_URL=%%i

echo.
echo [OK] Backend deployed successfully!
echo    URL: %BACKEND_URL%
echo.

REM Update frontend API URL
echo [*] Updating frontend API URL...
powershell -Command "(Get-Content frontend\src\api.js) -replace 'const API_BASE_URL = .*', 'const API_BASE_URL = ''%BACKEND_URL%''' | Set-Content frontend\src\api.js"

echo [OK] Frontend API URL updated
echo.

REM Build frontend
echo [*] Building frontend...
cd frontend
call npm install
call npm run build

if errorlevel 1 (
    echo.
    echo X Frontend build failed
    cd ..
    pause
    exit /b 1
)

cd ..
echo [OK] Frontend built successfully
echo.

REM Check if firebase is installed
firebase --version >nul 2>&1
if errorlevel 1 (
    echo [!] Firebase CLI not found. Installing...
    call npm install -g firebase-tools
)

REM Deploy to Firebase
echo [*] Deploying frontend to Firebase...
firebase deploy --only hosting

if errorlevel 1 (
    echo.
    echo X Frontend deployment failed
    echo   Run 'firebase login' first if not authenticated
    pause
    exit /b 1
)

REM Get Firebase URL
set FIREBASE_URL=https://%PROJECT_ID%.web.app

echo.
echo ===================================
echo   [OK] Deployment Complete!
echo ===================================
echo.
echo [*] Your RaceIQ is now live!
echo.
echo Backend API:  %BACKEND_URL%
echo Frontend App: %FIREBASE_URL%
echo API Docs:     %BACKEND_URL%/docs
echo.
echo Next steps:
echo 1. Visit %FIREBASE_URL% to test your app
echo 2. Share these URLs in your hackathon submission
echo 3. Monitor usage at: https://console.cloud.google.com
echo.
pause
