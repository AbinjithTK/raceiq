@echo off
echo ========================================
echo Deploying RaceIQ to AWS Elastic Beanstalk
echo ========================================

echo.
echo Step 1: Install EB CLI (if not installed)
pip install awsebcli --upgrade --quiet

echo.
echo Step 2: Initialize Elastic Beanstalk application
eb init -p python-3.11 raceiq-backend --region us-east-1

echo.
echo Step 3: Create environment and deploy
eb create raceiq-production --instance-type t3.small --single

echo.
echo Step 4: Open application
eb open

echo.
echo ========================================
echo Deployment Complete!
echo ========================================
echo.
echo To get your API URL, run: eb status
echo Then update frontend/src/api.js with the new URL
echo.
pause
