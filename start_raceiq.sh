#!/bin/bash

# RaceIQ Startup Script
# Starts both backend API and frontend dashboard

echo "🏁 Starting RaceIQ..."
echo ""

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.11+"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 18+"
    exit 1
fi

# Start API server in background
echo "🚀 Starting API server..."
python src/api/main.py &
API_PID=$!
echo "✓ API server started (PID: $API_PID)"
echo "  http://localhost:8000"
echo ""

# Wait for API to be ready
echo "⏳ Waiting for API to be ready..."
sleep 3

# Start frontend
echo "🎨 Starting frontend dashboard..."
cd frontend
npm run dev &
FRONTEND_PID=$!
echo "✓ Frontend started (PID: $FRONTEND_PID)"
echo "  http://localhost:3000"
echo ""

echo "✅ RaceIQ is running!"
echo ""
echo "📊 Dashboard: http://localhost:3000"
echo "📖 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for Ctrl+C
trap "echo ''; echo '🛑 Stopping RaceIQ...'; kill $API_PID $FRONTEND_PID; exit" INT
wait
