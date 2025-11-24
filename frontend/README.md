# RaceIQ Frontend Dashboard

**React-based web interface for RaceIQ**

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- RaceIQ API server running on port 8000

### Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The dashboard will be available at **http://localhost:3000**

## 📊 Features

### Real-Time Dashboard
- **Vehicle Selector** - Choose any vehicle from the race
- **Pit Window Prediction** - ML-powered pit strategy recommendations
- **Lap Time Potential** - Theoretical best lap calculator
- **Tire Degradation Analysis** - Visual lap-by-lap performance tracking
- **Coaching Insights** - Sector-specific driver feedback

### Live Updates
- Updates when vehicle or lap changes
- Color-coded alerts (green/yellow/red)
- Confidence scoring for predictions
- Interactive charts with Recharts

## 🎨 Design

### Color Scheme
- **Primary:** #3498db (Blue) - Information
- **Success:** #2ecc71 (Green) - Good performance
- **Warning:** #f39c12 (Orange) - Attention needed
- **Critical:** #e74c3c (Red) - Immediate action
- **Background:** Dark gradient (#1a1a2e → #16213e)

### Components
- `Header` - Branding and status indicator
- `VehicleSelector` - Vehicle selection dropdown
- `PitPrediction` - Pit window card
- `LapPotential` - Lap time potential card
- `TireDegradation` - Degradation chart card
- `CoachingInsights` - Coaching opportunities card

## 🛠️ Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **Recharts** - Chart library
- **Axios** - HTTP client
- **CSS3** - Styling with gradients and animations

## 📁 Project Structure

```
frontend/
├── index.html              # HTML entry point
├── package.json            # Dependencies
├── vite.config.js          # Vite configuration
├── src/
│   ├── main.jsx           # React entry point
│   ├── App.jsx            # Main app component
│   ├── App.css            # App styles
│   ├── index.css          # Global styles
│   ├── api.js             # API client
│   └── components/
│       ├── Header.jsx
│       ├── Header.css
│       ├── VehicleSelector.jsx
│       ├── VehicleSelector.css
│       ├── PitPrediction.jsx
│       ├── LapPotential.jsx
│       ├── TireDegradation.jsx
│       ├── CoachingInsights.jsx
│       └── Card.css       # Shared card styles
```

## 🔌 API Integration

The frontend connects to the FastAPI backend via proxy:

```javascript
// Vite proxy configuration
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true,
    rewrite: (path) => path.replace(/^\/api/, '')
  }
}
```

### API Endpoints Used
- `GET /vehicles` - List all vehicles
- `POST /pit-prediction` - Get pit window prediction
- `GET /tire-degradation/:id` - Get tire degradation data
- `POST /coaching` - Get coaching insights
- `GET /lap-potential/:id` - Get lap time potential

## 🎯 Usage

1. **Start API Server**
   ```bash
   python src/api/main.py
   ```

2. **Start Frontend**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Open Browser**
   Navigate to http://localhost:3000

4. **Select Vehicle**
   Choose a vehicle from the dropdown

5. **Adjust Current Lap**
   Use the lap control to simulate different race scenarios

6. **View Insights**
   - Check pit prediction
   - Review coaching opportunities
   - Analyze tire degradation
   - See lap time potential

## 🚀 Production Build

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

The build output will be in the `dist/` directory.

## 🎨 Customization

### Colors
Edit `src/index.css` and `src/components/Card.css` to change the color scheme.

### Layout
Modify `src/App.css` to adjust the dashboard grid layout.

### Components
Add new components in `src/components/` and import them in `App.jsx`.

## 🐛 Troubleshooting

### API Connection Error
**Problem:** "Failed to load vehicles"
**Solution:** Ensure API server is running on port 8000

```bash
python src/api/main.py
```

### Port Already in Use
**Problem:** Port 3000 is already in use
**Solution:** Change port in `vite.config.js`

```javascript
server: {
  port: 3001  // Use different port
}
```

### Dependencies Not Installing
**Problem:** npm install fails
**Solution:** Clear cache and retry

```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

## 📊 Performance

- **Initial Load:** <2s
- **API Response:** <50ms
- **Chart Rendering:** <100ms
- **Update Frequency:** On demand (vehicle/lap change)

## 🔮 Future Enhancements

- [ ] WebSocket for real-time updates
- [ ] Historical race playback
- [ ] Multi-vehicle comparison
- [ ] Export data to CSV/PDF
- [ ] Mobile responsive improvements
- [ ] Dark/light theme toggle
- [ ] Keyboard shortcuts
- [ ] Fullscreen mode

## 📝 License

Part of RaceIQ - Hack the Track 2024 submission

---

**Built with ❤️ for Toyota Racing Development**
