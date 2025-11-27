# Deploy RaceIQ Backend to Render.com (FREE)

Render.com offers free hosting for web services - perfect for your hackathon!

## Quick Deploy Steps

### Option 1: Deploy from GitHub (Recommended)

1. **Push your code to GitHub** (if not already done)
   ```bash
   git add .
   git commit -m "Ready for Render deployment"
   git push origin main
   ```

2. **Go to Render.com**
   - Visit: https://render.com
   - Sign up/Login with GitHub

3. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select `raceiq` or your repo name

4. **Configure Service**
   - Name: `raceiq-backend`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`
   - Plan: **Free**

5. **Deploy!**
   - Click "Create Web Service"
   - Wait 5-10 minutes for deployment
   - Your API will be live at: `https://raceiq-backend.onrender.com`

### Option 2: Deploy with render.yaml

The `render.yaml` file is already configured. Just:

1. Push to GitHub
2. In Render dashboard, click "New +" → "Blueprint"
3. Connect your repo
4. Render will auto-detect `render.yaml` and deploy

## Update Frontend

Once deployed, update `frontend/src/api.js`:

```javascript
const API_BASE_URL = 'https://raceiq-backend.onrender.com'
```

Then redeploy frontend:
```bash
cd frontend
npm run build
npx netlify-cli deploy --prod --dir=dist
```

## Notes

- **Free tier**: 750 hours/month (plenty for hackathon)
- **Cold starts**: First request after inactivity takes ~30 seconds
- **Auto-deploy**: Pushes to GitHub trigger automatic redeployment
- **HTTPS**: Automatic SSL certificates

## Troubleshooting

If deployment fails:
1. Check build logs in Render dashboard
2. Ensure all dependencies are in `requirements.txt`
3. Verify Python version is 3.11

Your RaceIQ backend will be live and free! 🚀
