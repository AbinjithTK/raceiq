@echo off
echo ========================================
echo Uploading Race Data to Google Cloud Storage
echo ========================================

echo.
echo Creating storage bucket...
gsutil mb -p hackthetrack-479019 -l us-central1 gs://raceiq-data-bucket 2>nul
if %errorlevel% neq 0 (
    echo Bucket already exists or error occurred, continuing...
)

echo.
echo Uploading data folders...
gsutil -m cp -r barber gs://raceiq-data-bucket/
gsutil -m cp -r COTA gs://raceiq-data-bucket/
gsutil -m cp -r indianapolis gs://raceiq-data-bucket/
gsutil -m cp -r road-america gs://raceiq-data-bucket/
gsutil -m cp -r sebring gs://raceiq-data-bucket/
gsutil -m cp -r Sonoma gs://raceiq-data-bucket/
gsutil -m cp -r virginia-international-raceway gs://raceiq-data-bucket/
gsutil -m cp -r rag_dataset gs://raceiq-data-bucket/

echo.
echo Making bucket publicly readable...
gsutil iam ch allUsers:objectViewer gs://raceiq-data-bucket

echo.
echo ========================================
echo Upload Complete!
echo Bucket: gs://raceiq-data-bucket
echo ========================================
pause
