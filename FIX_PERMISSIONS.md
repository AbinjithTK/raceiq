# Fix Google Cloud Permissions

If you get permission errors during deployment, run these commands:

## Grant Required Permissions

```bash
# Set your project
gcloud config set project hackthetrack-479019

# Grant Cloud Build permissions
gcloud projects add-iam-policy-binding hackthetrack-479019 \
  --member="serviceAccount:1091035104912-compute@developer.gserviceaccount.com" \
  --role="roles/cloudbuild.builds.builder"

# Grant Storage permissions
gcloud projects add-iam-policy-binding hackthetrack-479019 \
  --member="serviceAccount:1091035104912-compute@developer.gserviceaccount.com" \
  --role="roles/storage.admin"

# Grant Cloud Run permissions
gcloud projects add-iam-policy-binding hackthetrack-479019 \
  --member="serviceAccount:1091035104912-compute@developer.gserviceaccount.com" \
  --role="roles/run.admin"
```

## Then Retry Deployment

```bash
gcloud run deploy raceiq-backend \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --project hackthetrack-479019
```

## Alternative: Use Console

1. Go to: https://console.cloud.google.com/iam-admin/iam?project=hackthetrack-479019
2. Find service account: `1091035104912-compute@developer.gserviceaccount.com`
3. Click "Edit" (pencil icon)
4. Add roles:
   - Cloud Build Service Account
   - Storage Admin
   - Cloud Run Admin
5. Save and retry deployment

## Check Permissions

```bash
gcloud projects get-iam-policy hackthetrack-479019 \
  --flatten="bindings[].members" \
  --filter="bindings.members:1091035104912-compute@developer.gserviceaccount.com"
```
