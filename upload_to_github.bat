@echo off
REM RaceIQ GitHub Upload Script for Windows

echo ===================================
echo   RaceIQ - GitHub Upload Script
echo ===================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo X Git is not installed. Please install Git first.
    echo   Download from: https://git-scm.com/downloads
    pause
    exit /b 1
)

echo [OK] Git is installed
echo.

REM Check if already initialized
if exist ".git" (
    echo [OK] Git repository already initialized
) else (
    echo [*] Initializing Git repository...
    git init
    echo [OK] Git initialized
)

echo.
echo Please enter your GitHub repository URL:
echo Example: https://github.com/YOUR_USERNAME/raceiq.git
set /p REPO_URL="Repository URL: "

if "%REPO_URL%"=="" (
    echo X No URL provided. Exiting.
    pause
    exit /b 1
)

echo.
echo [*] Adding files to Git...
git add .

echo.
echo [*] Creating commit...
git commit -m "Initial commit: RaceIQ - AI Race Engineer" -m "- Real race data analysis from Toyota GR Cup" -m "- 3D track visualization with heatmaps" -m "- Race strategy engine (fuel, pace, pit predictions)" -m "- Tire degradation tracking" -m "- Multi-track support (7 circuits)" -m "- Google Vertex AI integration for RAG chatbot" -m "- React frontend with Three.js" -m "- FastAPI backend with real data analytics"

echo.
echo [*] Adding remote repository...
git remote remove origin 2>nul
git remote add origin %REPO_URL%

echo.
echo [*] Setting branch to main...
git branch -M main

echo.
echo [*] Pushing to GitHub...
git push -u origin main

if errorlevel 1 (
    echo.
    echo ===================================
    echo   X Upload failed
    echo ===================================
    echo.
    echo Common issues:
    echo - Make sure you created the repository on GitHub first
    echo - Check your GitHub credentials
    echo - Verify the repository URL is correct
    pause
    exit /b 1
)

echo.
echo ===================================
echo   [OK] Successfully uploaded to GitHub!
echo ===================================
echo.
echo Your repository is now at:
echo %REPO_URL%
echo.
echo Next steps:
echo 1. Visit your repository on GitHub
echo 2. Add description and topics
echo 3. Share the URL in your hackathon submission
echo.
pause
