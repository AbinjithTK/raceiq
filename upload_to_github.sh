#!/bin/bash

# RaceIQ GitHub Upload Script
# This script helps you upload the project to GitHub

echo "==================================="
echo "  RaceIQ - GitHub Upload Script"
echo "==================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    echo "   Download from: https://git-scm.com/downloads"
    exit 1
fi

echo "✅ Git is installed"
echo ""

# Check if already initialized
if [ -d ".git" ]; then
    echo "✅ Git repository already initialized"
else
    echo "📦 Initializing Git repository..."
    git init
    echo "✅ Git initialized"
fi

echo ""
echo "Please enter your GitHub repository URL:"
echo "Example: https://github.com/YOUR_USERNAME/raceiq.git"
read -p "Repository URL: " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "❌ No URL provided. Exiting."
    exit 1
fi

echo ""
echo "📝 Adding files to Git..."
git add .

echo ""
echo "💾 Creating commit..."
git commit -m "Initial commit: RaceIQ - AI Race Engineer

- Real race data analysis from Toyota GR Cup
- 3D track visualization with heatmaps
- Race strategy engine (fuel, pace, pit predictions)
- Tire degradation tracking
- Multi-track support (7 circuits)
- Google Vertex AI integration for RAG chatbot
- React frontend with Three.js
- FastAPI backend with real data analytics"

echo ""
echo "🔗 Adding remote repository..."
git remote remove origin 2>/dev/null
git remote add origin "$REPO_URL"

echo ""
echo "🌿 Setting branch to main..."
git branch -M main

echo ""
echo "🚀 Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "==================================="
    echo "  ✅ Successfully uploaded to GitHub!"
    echo "==================================="
    echo ""
    echo "Your repository is now at:"
    echo "$REPO_URL"
    echo ""
    echo "Next steps:"
    echo "1. Visit your repository on GitHub"
    echo "2. Add description and topics"
    echo "3. Share the URL in your hackathon submission"
else
    echo ""
    echo "❌ Upload failed. Please check the error messages above."
    echo ""
    echo "Common issues:"
    echo "- Make sure you created the repository on GitHub first"
    echo "- Check your GitHub credentials"
    echo "- Verify the repository URL is correct"
fi
