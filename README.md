# RaceIQ - AI-Powered Race Engineer Assistant

**Hack the Track 2024 - Real-Time Analytics Category**

## 🏁 The Problem

Race engineers need to make split-second decisions during a race:
- When to pit for tires?
- Where is the driver losing time?
- Can we make it to the finish on fuel?

Currently, they rely on gut feel and basic timing data. **RaceIQ changes that.**

## 💡 The Solution

An AI-powered assistant that analyzes real-time telemetry to provide actionable insights:

1. **Tire Degradation Predictor** - Know exactly when to pit
2. **Racing Line Coach** - Show drivers where they're losing time
3. **Multi-Track Performance Analysis** - Compare performance across all 7 circuits
4. **Real-Time 3D Visualization** - Live track simulation with coaching tips
5. **Championship Strategy** - Optimize points across the full season

## 🎯 Key Features

### Real-Time Analysis
- **Live tire life estimation** using brake pressure, G-forces, and speed degradation
- **GPS-based racing line analysis** comparing actual vs optimal paths
- **Sector-by-sector coaching** with specific time gains available
- **Interactive 3D track visualization** with real-time car position

### Multi-Track Intelligence
- **7 Track Support**: Barber, Indianapolis, COTA, Sebring, Road America, Sonoma, VIR
- **Cross-track comparison**: Identify driver strengths by track type
- **Track difficulty ranking**: Understand which circuits are most challenging
- **Championship simulation**: Calculate standings across the full season
- **Performance insights**: Technical vs flowing, short vs long track analysis

### Professional Dashboard
- **Real-time telemetry display** with 5 live metrics
- **Context-aware coaching tips** triggered by lap progress
- **Pit strategy prediction** with confidence scoring
- **Responsive design** optimized for all screen sizes

## 🛠️ Tech Stack

- **Backend**: Python, pandas, scikit-learn, FastAPI
- **Frontend**: React, Three.js, Recharts
- **3D Visualization**: React Three Fiber, Three.js
- **Data**: Toyota GR Cup telemetry, timing, and GPS data from 7 tracks

## 📊 Dataset Coverage

### Tracks (7 Total)
- **Barber Motorsports Park** (3.7 km, 17 turns)
- **Indianapolis Motor Speedway** (4.0 km, 14 turns)
- **Circuit of The Americas** (5.5 km, 20 turns)
- **Sebring International Raceway** (6.0 km, 17 turns)
- **Road America** (6.5 km, 14 turns)
- **Sonoma Raceway** (4.0 km, 12 turns)
- **Virginia International Raceway** (5.3 km, 18 turns)

### Data Types
- Race results and classifications (14 races)
- Lap timing with sector splits (4,152+ laps)
- High-frequency telemetry (speed, throttle, brake, G-forces, GPS)
- Weather conditions
- Track maps and GPS coordinates

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+ and npm
- pip package manager

### Installation

```bash
# 1. Clone the repository
git clone <repository-url>
cd barber-motorsports-park

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install frontend dependencies
cd frontend
npm install
cd ..

# 4. Verify data is in place
# Ensure barber/ directory contains CSV files
```

### Run Full Application (Recommended)

**Windows:**
```bash
# Double-click or run:
start_raceiq.bat
```

**Mac/Linux:**
```bash
# Make executable and run:
chmod +x start_raceiq.sh
./start_raceiq.sh
```

This will start:
- 🚀 API Server at http://localhost:8000
- 🎨 Dashboard at http://localhost:3000

### Run Components Separately

**Backend API:**
```bash
python src/api/main.py
# API available at: http://localhost:8000
# Interactive docs: http://localhost:8000/docs
```

**Frontend Dashboard:**
```bash
cd frontend
npm run dev
# Dashboard at: http://localhost:3000
```

**Quick Demo (CLI):**
```bash
python demo.py
```

**Generate Visualizations:**
```bash
python src/dashboard/visualize.py
# View outputs in output/ directory
```

### Test Individual Components

```bash
# Test data loading
python src/data_loader.py

# Test tire degradation analysis
python src/analysis/tire_degradation.py

# Test racing line analysis
python src/analysis/racing_line.py
```

## 📈 Impact

- **For Teams**: Optimize pit strategy, reduce tire costs
- **For Drivers**: Learn faster with data-driven coaching
- **For Fans**: Understand the strategy behind the race
- **Beyond GR Cup**: Applicable to any racing series, track days, sim racing

## 🏆 Hackathon Category

**Real-Time Analytics** with elements of **Driver Training & Insights**

---

Built with ❤️ for Toyota Racing Development
