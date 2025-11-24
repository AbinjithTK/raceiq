# Upload RaceIQ to GitHub

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `raceiq` (or your preferred name)
3. Description: `AI-powered race engineer for motorsports telemetry analysis`
4. Choose: **Public** (for hackathon visibility) or **Private**
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

## Step 2: Initialize Git (if not already done)

```bash
# Check if git is initialized
git status

# If not initialized, run:
git init
```

## Step 3: Configure Git (First time only)

```bash
# Set your name and email
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Step 4: Add Files to Git

```bash
# Add all files (respects .gitignore)
git add .

# Check what will be committed
git status

# You should see:
# - Source code (src/, frontend/)
# - Documentation (docs/, README.md)
# - Configuration files
# - NOT see: .venv/, node_modules/, *.csv files
```

## Step 5: Create First Commit

```bash
git commit -m "Initial commit: RaceIQ - AI Race Engineer

- Real race data analysis from Toyota GR Cup
- 3D track visualization with heatmaps
- Race strategy engine (fuel, pace, pit predictions)
- Tire degradation tracking
- Multi-track support (7 circuits)
- Google Vertex AI integration for RAG chatbot
- React frontend with Three.js
- FastAPI backend with real data analytics"
```

## Step 6: Add Remote Repository

```bash
# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/raceiq.git

# Verify remote
git remote -v
```

## Step 7: Push to GitHub

```bash
# Push to main branch
git push -u origin main

# If you get an error about 'master' vs 'main':
git branch -M main
git push -u origin main
```

## Step 8: Verify Upload

1. Go to your GitHub repository URL
2. You should see all files uploaded
3. README.md should display automatically

## Important Notes

### Files That Will Be Uploaded ✅
- All source code (`src/`, `frontend/`)
- Documentation (`docs/`, `README.md`)
- Configuration files (`requirements.txt`, `package.json`)
- Scripts (`demo.py`, `test_*.py`)
- RAG dataset (`rag_dataset/`)

### Files That Will NOT Be Uploaded ❌ (Good!)
- Virtual environment (`.venv/`)
- Node modules (`node_modules/`)
- CSV data files (`*.csv`, `*.CSV`) - Too large
- PDF files (`*.pdf`)
- IDE settings (`.vscode/`, `.idea/`)
- Build outputs (`dist/`, `build/`)

### About CSV Data Files

The CSV files are **NOT uploaded** because:
- They're too large for GitHub (100+ MB)
- Protected by .gitignore
- Should be downloaded separately or stored in cloud

**For users to get data:**
Add to README.md that data files should be obtained from the hackathon organizers.

## Step 9: Add Repository Description and Topics

On GitHub repository page:
1. Click "⚙️ Settings" (or edit description)
2. Add description: `AI-powered race engineer analyzing real motorsports telemetry with Google Vertex AI`
3. Add topics: `ai`, `racing`, `motorsports`, `telemetry`, `vertex-ai`, `react`, `fastapi`, `python`, `three-js`

## Step 10: Create a Good README Badge (Optional)

Add to top of README.md:

```markdown
# RaceIQ - AI Race Engineer

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18-61dafb.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688.svg)](https://fastapi.tiangolo.com/)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Vertex%20AI-4285F4.svg)](https://cloud.google.com/vertex-ai)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
```

## Troubleshooting

### Error: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/raceiq.git
```

### Error: "failed to push some refs"
```bash
# Pull first, then push
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### Error: "large files detected"
```bash
# Check what's being added
git status

# If CSV files are showing, update .gitignore:
echo "*.csv" >> .gitignore
echo "*.CSV" >> .gitignore
git rm --cached *.csv *.CSV
git add .gitignore
git commit -m "Update gitignore to exclude CSV files"
```

### Want to upload data files anyway?
Use Git LFS (Large File Storage):
```bash
git lfs install
git lfs track "*.csv"
git add .gitattributes
git commit -m "Add Git LFS for CSV files"
git push
```

## Quick Command Summary

```bash
# One-time setup
git init
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# Add and commit
git add .
git commit -m "Initial commit: RaceIQ - AI Race Engineer"

# Connect to GitHub
git remote add origin https://github.com/YOUR_USERNAME/raceiq.git
git branch -M main
git push -u origin main
```

## After Upload

1. ✅ Verify all files are on GitHub
2. ✅ Check README displays correctly
3. ✅ Add repository description and topics
4. ✅ Share repository URL in hackathon submission
5. ✅ Consider adding a LICENSE file (MIT recommended)

## Future Updates

```bash
# Make changes to code
# Then:
git add .
git commit -m "Description of changes"
git push
```

## Repository URL Format

Your repository will be at:
```
https://github.com/YOUR_USERNAME/raceiq
```

Share this URL in your hackathon submission!
