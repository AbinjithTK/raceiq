@echo off
echo ========================================
echo Deploying RaceIQ Backend to AWS Lambda
echo ========================================

echo.
echo Installing Serverless Framework...
npm install -g serverless
npm install --save-dev serverless-python-requirements

echo.
echo Deploying to AWS...
serverless deploy --verbose

echo.
echo ========================================
echo Deployment Complete!
echo ========================================
echo.
echo Check the output above for your API Gateway URL
echo Update frontend/src/api.js with the new URL
echo.
pause
