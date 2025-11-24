@echo off
REM RaceIQ Startup Script for Windows
REM Starts both backend API and frontend dashboard

echo.
echo 🏁 Starting RaceIQ...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.11+
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js not found. Please install Node.js 18+
    pause
    exit /b 1
)

REM Start API server in new window
echo 🚀 Starting API server...
start "RaceIQ API" cmd /k "python src/api/main.py"
echo ✓ API server started
echo   http://localhost:8000
echo.

REM Wait for API to be ready
echo ⏳ Waiting for API to be ready...
timeout /t 3 /nobreak >nul

REM Start frontend in new window
echo 🎨 Starting frontend dashboard...
cd frontend
start "RaceIQ Dashboard" cmd /k "npm run dev"
echo ✓ Frontend started
echo   http://localhost:3000
echo.

echo ✅ RaceIQ is running!
echo.
echo 📊 Dashboard: http://localhost:3000
echo 📖 API Docs: http://localhost:8000/docs
echo.
echo Close the terminal windows to stop services
echo.
pause
