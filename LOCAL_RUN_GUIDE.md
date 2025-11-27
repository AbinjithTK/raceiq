# 🏁 RaceIQ - Local Development Guide

Complete guide to running RaceIQ on your local machine for development and testing.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **npm** (comes with Node.js)
- **Git** - [Download](https://git-scm.com/downloads)

### Verify Installation

```bash
# Check Python version
python --version

# Check Node.js version
node --version

# Check npm version
npm --version

# Check Git version
git --version
```

## 🚀 Quick Start (Recommended)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd raceiq
```

### 2. Install Dependencies

**Python Backend:**
```bash
pip install -r requirements.txt
```

**Frontend Dashboard:**
```bash
cd frontend
npm install
cd ..
```

### 3. Run the Application

**Windows:**
```bash
start_raceiq.bat
```

**Mac/Linux:**
```bash
chmod +x start_raceiq.sh
./start_raceiq.sh
```

### 4. Access the Application

- 🎨 **Dashboard**: http://localhost:3000
- 🚀 **API**: http://localhost:8000
- 📖 **API Docs**: http://localhost:8000/docs

## 🔧 Manual Setup (Step-by-Step)

### Backend Setup

1. **Create Virtual Environment (Optional but Recommended)**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # Mac/Linux
   source .venv/bin/activate
   ```

2. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify Data Files**
   Ensure the following directories contain CSV data:
   - `barber/` - Barber Motorsports Park data
   - `indianapolis/` - Indianapolis Motor Speedway data
   - `COTA/` - Circuit of The Americas data
   - `sebring/` - Sebring International Raceway data
   - `road-america/` - Road America data
   - `Sonoma/` - Sonoma Raceway data
   - `virginia-international-raceway/` - VIR data

4. **Start Backend Server**
   ```bash
   python src/api/main.py
   ```
   
   The API will be available at:
   - Base URL: http://localhost:8000
   - Interactive Docs: http://localhost:8000/docs
   - OpenAPI Schema: http://localhost:8000/openapi.json

### Frontend Setup

1. **Navigate to Frontend Directory**
   ```bash
   cd frontend
   ```

2. **Install Dependencies**
   ```bash
   npm install
   ```

3. **Start Development Server**
   ```bash
   npm run dev
   ```
   
   The dashboard will be available at: http://localhost:3000

4. **Build for Production (Optional)**
   ```bash
   npm run build
   npm run preview
   ```

## 🧪 Testing Components

### Test Data Loading
```bash
python src/data_loader.py
```

### Test Tire Degradation Analysis
```bash
python src/analysis/tire_degradation.py
```

### Test Racing Line Analysis
```bash
python src/analysis/racing_line.py
```

### Run Quick Demo
```bash
python demo.py
```

### Generate Visualizations
```bash
python src/dashboard/visualize.py
# Check output/ directory for generated charts
```

## 📁 Project Structure

```
raceiq/
├── src/
│   ├── api/              # FastAPI backend
│   ├── analysis/         # Analysis modules
│   ├── data_loader.py    # Data loading utilities
│   └── dashboard/        # Visualization tools
├── frontend/
│   ├── src/              # React components
│   ├── public/           # Static assets
│   └── package.json      # Frontend dependencies
├── barber/               # Barber track data
├── indianapolis/         # Indianapolis track data
├── COTA/                 # COTA track data
├── sebring/              # Sebring track data
├── road-america/         # Road America track data
├── Sonoma/               # Sonoma track data
├── virginia-international-raceway/  # VIR track data
├── requirements.txt      # Python dependencies
├── start_raceiq.bat      # Windows startup script
└── start_raceiq.sh       # Mac/Linux startup script
```

## 🐛 Troubleshooting

### Port Already in Use

**Backend (Port 8000):**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:8000 | xargs kill -9
```

**Frontend (Port 3000):**
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:3000 | xargs kill -9
```

### Python Module Not Found

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Frontend Build Errors

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Data Files Missing

Ensure all track directories contain the required CSV files:
- Race results (`03_*Results*.CSV`)
- Timing data (`R#_*_lap_*.csv`)
- Telemetry data (`R#_*_telemetry_data.csv`)

### API Not Responding

1. Check if the backend is running
2. Verify no firewall is blocking port 8000
3. Check console for error messages
4. Ensure all Python dependencies are installed

### Frontend Not Loading

1. Check if Node.js version is 18+
2. Clear browser cache
3. Check browser console for errors
4. Verify backend API is running

## 🔑 Environment Variables (Optional)

Create a `.env` file in the root directory for custom configuration:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Frontend Configuration
VITE_API_URL=http://localhost:8000

# Data Paths
DATA_DIR=./
```

## 📊 API Endpoints

### Health Check
```bash
GET http://localhost:8000/health
```

### Get Tracks
```bash
GET http://localhost:8000/api/tracks
```

### Get Telemetry
```bash
GET http://localhost:8000/api/telemetry/{track_name}?vehicle_id={id}&lap={lap_number}
```

### Get Tire Analysis
```bash
GET http://localhost:8000/api/tire-analysis/{track_name}?vehicle_id={id}
```

### Get Racing Line
```bash
GET http://localhost:8000/api/racing-line/{track_name}?vehicle_id={id}&lap={lap_number}
```

## 🎯 Development Tips

### Hot Reload

Both backend and frontend support hot reload:
- **Backend**: Automatically reloads on Python file changes
- **Frontend**: Automatically reloads on React file changes

### Debug Mode

**Backend:**
```bash
# Enable debug logging
python src/api/main.py --log-level debug
```

**Frontend:**
```bash
# Open browser DevTools (F12)
# Check Console and Network tabs
```

### Code Formatting

**Python:**
```bash
pip install black
black src/
```

**Frontend:**
```bash
cd frontend
npm run format  # If configured
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Three.js Documentation](https://threejs.org/docs/)
- [Vite Documentation](https://vitejs.dev/)

## 🆘 Getting Help

If you encounter issues:

1. Check the troubleshooting section above
2. Review console/terminal error messages
3. Check API documentation at http://localhost:8000/docs
4. Verify all prerequisites are installed correctly

## 🎉 Success!

Once everything is running, you should see:
- ✅ Backend API responding at http://localhost:8000
- ✅ Frontend dashboard at http://localhost:3000
- ✅ Real-time telemetry visualization
- ✅ AI-powered race insights

Happy racing! 🏎️💨
