import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import './App.css'
import Header from './components/Header'
import VehicleSelector from './components/VehicleSelector'
import TrackSelector from './components/TrackSelector'
import TireDegradation from './components/TireDegradation'
import PitPrediction from './components/PitPrediction'
import CoachingInsights from './components/CoachingInsights'
import LapPotential from './components/LapPotential'
import TrackMap from './components/TrackMap'
import Track3DEnhanced from './components/Track3DEnhanced'
import TelemetryLive from './components/TelemetryLive'
import RealtimeTips from './components/RealtimeTips'
import CrossTrackComparison from './components/CrossTrackComparison'
import StrategyChart from './components/StrategyChart'
import AIEngineer from './components/AIEngineer'
import RaceStrategy from './components/RaceStrategy'
import { fetchVehicles } from './api'
import { TRACKS } from './data/tracks'

function App() {
  const [vehicles, setVehicles] = useState([])
  const [selectedVehicle, setSelectedVehicle] = useState(null)
  const [selectedTrack, setSelectedTrack] = useState('barber')
  const [currentLap, setCurrentLap] = useState(15)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [isPlaying, setIsPlaying] = useState(false)
  const [lapProgress, setLapProgress] = useState(0)
  const [currentSpeed, setCurrentSpeed] = useState(0)
  const [currentSector, setCurrentSector] = useState(1)

  useEffect(() => {
    loadVehicles()
  }, [])

  const loadVehicles = async () => {
    try {
      setLoading(true)
      const data = await fetchVehicles()
      setVehicles(data.vehicles)
      if (data.vehicles.length > 0) {
        // Default to race winner (position 1)
        const winner = data.vehicles.find(v => v.position === 1)
        setSelectedVehicle(winner || data.vehicles[0])
      }
      setError(null)
    } catch (err) {
      setError('Failed to load vehicles. Make sure the API server is running.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="app">
        <Header />
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading RaceIQ Dashboard...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="app">
        <Header />
        <div className="error-container">
          <div className="error-message">
            <h2>⚠️ Connection Error</h2>
            <p>{error}</p>
            <p className="error-hint">
              Start the API server: <code>python src/api/main.py</code>
            </p>
            <button onClick={loadVehicles} className="retry-button">
              Retry Connection
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="app">
      <Header />

      <div className="controls">
        <TrackSelector
          currentTrack={selectedTrack}
          onTrackChange={setSelectedTrack}
        />

        <VehicleSelector
          vehicles={vehicles}
          selectedVehicle={selectedVehicle}
          onSelectVehicle={setSelectedVehicle}
        />

        <div className="lap-control">
          <label>Current Lap:</label>
          <input
            type="number"
            min="1"
            max="27"
            value={currentLap}
            onChange={(e) => setCurrentLap(parseInt(e.target.value))}
          />
          <span className="lap-total">/ 27</span>
        </div>

        <button 
          className="play-pause-button"
          onClick={() => setIsPlaying(!isPlaying)}
        >
          {isPlaying ? '⏸️ Pause' : '▶️ Play'} Simulation
        </button>
      </div>

      {selectedVehicle && (
        <AnimatePresence mode="wait">
          <motion.div
            key={selectedTrack}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.5 }}
            className="dashboard"
          >
            {/* 3D Track with Heatmaps - Top Left (spans 2 rows) */}
            <div className="dashboard-3d">
              <Track3DEnhanced
                trackData={TRACKS[selectedTrack] || TRACKS['barber']}
                currentLap={currentLap}
                isPlaying={isPlaying}
                trackName={selectedTrack}
                onRaceUpdate={(data) => {
                  setCurrentSpeed(data.speed)
                  setLapProgress(data.progress / 100)
                  setCurrentSector(data.sector)
                }}
              />
            </div>

            {/* Tips and Telemetry - Top Right */}
            <div className="dashboard-tips-telemetry">
              <RealtimeTips
                lapProgress={lapProgress}
                sector={currentSector}
                isPlaying={isPlaying}
              />
              <TelemetryLive
                isPlaying={isPlaying}
                onSpeedUpdate={setCurrentSpeed}
                onProgressUpdate={setLapProgress}
                trackName={selectedTrack}
                vehicleNumber={selectedVehicle?.number || 78}
                currentLap={currentLap}
              />
            </div>

            {/* Strategy Cards - Middle Right */}
            <div className="dashboard-strategy">
              <StrategyChart
                currentLap={currentLap}
                totalLaps={27}
              />
              <PitPrediction
                vehicleNumber={selectedVehicle.number}
                currentLap={currentLap}
                totalLaps={27}
              />
            </div>

            {/* Real Race Strategy - Full Width */}
            <div className="dashboard-race-strategy">
              <RaceStrategy
                vehicleNumber={selectedVehicle.number}
                currentLap={currentLap}
                totalLaps={27}
                trackName={selectedTrack}
                raceNum={1}
              />
            </div>

            {/* Performance - Bottom (full width) */}
            <div className="dashboard-performance">
              <TireDegradation vehicleNumber={selectedVehicle.number} />
              <CoachingInsights
                vehicleNumber={selectedVehicle.number}
                currentLap={currentLap}
              />
            </div>

            {/* Cross-Track Comparison - Bottom */}
            <div className="dashboard-cross-track">
              <CrossTrackComparison vehicleId={selectedVehicle.number} />
            </div>
          </motion.div>
        </AnimatePresence>
      )}

      <footer className="footer">
        <p>RaceIQ - AI-Powered Race Engineer Assistant | Hack the Track 2024</p>
      </footer>

      <AIEngineer
        raceData={{
          speed: currentSpeed,
          lap: currentLap,
          sector: currentSector,
          tireLife: 95 - (currentLap * 2),
          track: selectedTrack,
          vehicle: selectedVehicle?.number
        }}
      />
    </div>
  )
}

export default App
