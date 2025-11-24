import React, { useState, useEffect } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Area, AreaChart } from 'recharts'
import './Card.css'
import './TelemetryLive.css'

function TelemetryLive({ isPlaying, onSpeedUpdate, onProgressUpdate, trackName = 'barber', vehicleNumber = 78, currentLap = 1 }) {
  const [telemetryData, setTelemetryData] = useState([])
  const [currentSpeed, setCurrentSpeed] = useState(0)
  const [currentThrottle, setCurrentThrottle] = useState(0)
  const [currentBrake, setCurrentBrake] = useState(0)
  const [currentGear, setCurrentGear] = useState(4)
  const [currentRPM, setCurrentRPM] = useState(5000)

  // Optimal telemetry values (ghost parameters)
  const [optimalSpeed, setOptimalSpeed] = useState(0)
  const [optimalThrottle, setOptimalThrottle] = useState(0)
  const [optimalBrake, setOptimalBrake] = useState(0)

  // Real telemetry data
  const [realTelemetry, setRealTelemetry] = useState([])
  const [optimalData, setOptimalData] = useState(null)
  const [telemetryIndex, setTelemetryIndex] = useState(0)

  // Load real telemetry data
  useEffect(() => {
    const loadTelemetryData = async () => {
      try {
        // Load optimal telemetry
        const optimalResponse = await fetch(`/api/telemetry/optimal/${trackName}/1`)
        if (optimalResponse.ok) {
          const optimal = await optimalResponse.json()
          setOptimalData(optimal)
          setOptimalSpeed(Math.round(optimal.avg_speed || 140))
          setOptimalThrottle(Math.round(optimal.avg_throttle || 75))
          setOptimalBrake(Math.round(optimal.avg_brake || 20))
        }

        // Load current vehicle telemetry
        const telemetryResponse = await fetch(`/api/telemetry/live/${trackName}/1/${vehicleNumber}?lap=${currentLap}`)
        if (telemetryResponse.ok) {
          const data = await telemetryResponse.json()
          if (data.points && data.points.length > 0) {
            setRealTelemetry(data.points)
            setTelemetryIndex(0)
          }
        }
      } catch (error) {
        console.error('Error loading telemetry:', error)
        // Fall back to simulated data
        setRealTelemetry([])
      }
    }

    loadTelemetryData()
  }, [trackName, vehicleNumber, currentLap])

  useEffect(() => {
    if (isPlaying) {
      const interval = setInterval(() => {
        if (realTelemetry.length > 0) {
          // Use real telemetry data
          const currentIndex = telemetryIndex % realTelemetry.length
          const point = realTelemetry[currentIndex]

          // Validate and extract data with fallbacks
          const speed = Math.max(0, point.speed || 0)
          const throttle = Math.max(0, Math.min(100, point.throttle || 0))
          const brakeFront = Math.max(0, Math.min(100, point.brake_front || 0))
          const brakeRear = Math.max(0, Math.min(100, point.brake_rear || 0))
          const brake = (brakeFront + brakeRear) / 2
          const gear = Math.max(1, Math.min(6, point.gear || 4))
          const rpm = Math.max(0, Math.min(8000, point.rpm || 5000))

          setCurrentSpeed(Math.round(speed))
          setCurrentThrottle(Math.round(throttle))
          setCurrentBrake(Math.round(brake))
          setCurrentGear(gear)
          setCurrentRPM(Math.round(rpm))

          // Calculate lap progress
          const lapProgress = currentIndex / realTelemetry.length

          // Update parent components
          if (onSpeedUpdate) onSpeedUpdate(Math.round(speed))
          if (onProgressUpdate) onProgressUpdate(lapProgress)

          // Add to chart data (keep last 50 points)
          setTelemetryData(prev => {
            const newData = [
              ...prev,
              {
                time: lapProgress.toFixed(2),
                speed: Math.round(speed),
                throttle: Math.round(throttle),
                brake: Math.round(brake),
                optimalSpeed: optimalSpeed,
                optimalThrottle: optimalThrottle,
                optimalBrake: optimalBrake,
              }
            ]
            return newData.slice(-50)
          })

          setTelemetryIndex(prev => (prev + 1) % realTelemetry.length)
        } else {
          // Fallback to simulated data
          const time = Date.now() / 1000
          const lapProgress = (time % 98) / 98

          const speed = 150 + Math.sin(lapProgress * Math.PI * 8) * 30
          const throttle = Math.max(0, 70 + Math.sin(lapProgress * Math.PI * 12) * 30)
          const brake = throttle < 50 ? Math.max(0, 50 - throttle) : 0
          const gear = Math.floor(2 + (speed / 180) * 4)
          const rpm = 4000 + (speed / 180) * 4000

          setCurrentSpeed(Math.round(speed))
          setCurrentThrottle(Math.round(throttle))
          setCurrentBrake(Math.round(brake))
          setCurrentGear(gear)
          setCurrentRPM(Math.round(rpm))

          if (onSpeedUpdate) onSpeedUpdate(Math.round(speed))
          if (onProgressUpdate) onProgressUpdate(lapProgress)

          setTelemetryData(prev => {
            const newData = [
              ...prev,
              {
                time: lapProgress.toFixed(2),
                speed: Math.round(speed),
                throttle: Math.round(throttle),
                brake: Math.round(brake),
                optimalSpeed: optimalSpeed,
                optimalThrottle: optimalThrottle,
                optimalBrake: optimalBrake,
              }
            ]
            return newData.slice(-50)
          })
        }
      }, 100)

      return () => clearInterval(interval)
    }
  }, [isPlaying, realTelemetry.length, optimalSpeed, optimalThrottle, optimalBrake, onSpeedUpdate, onProgressUpdate])

  return (
    <div className="card wide telemetry-live">
      <div className="telemetry-header">
        <h2 className="card-title">📊 Live Telemetry</h2>
        <div className="telemetry-legend">
          <span className="legend-item">
            <span className="legend-dot current"></span> Current
          </span>
          <span className="legend-item">
            <span className="legend-dot optimal"></span> ⚡ Optimal
          </span>
        </div>
      </div>

      <div className="telemetry-gauges">
        <div className="gauge-item">
          <div className="gauge-label">Speed</div>
          <div className="gauge-value-container">
            <div className="gauge-value speed">{currentSpeed}</div>
            <div className="gauge-optimal">⚡ {optimalSpeed}</div>
          </div>
          <div className="gauge-unit">km/h</div>
          <div className="gauge-bar">
            <div
              className="gauge-fill-ghost speed-ghost"
              style={{ width: `${(optimalSpeed / 200) * 100}%` }}
            ></div>
            <div
              className="gauge-fill speed-fill"
              style={{ width: `${(currentSpeed / 200) * 100}%` }}
            ></div>
          </div>
          <div className="gauge-delta" style={{ color: currentSpeed >= optimalSpeed ? '#2ecc71' : '#e74c3c' }}>
            {currentSpeed >= optimalSpeed ? '▲' : '▼'} {Math.abs(currentSpeed - optimalSpeed)} km/h
          </div>
        </div>

        <div className="gauge-item">
          <div className="gauge-label">Throttle</div>
          <div className="gauge-value-container">
            <div className="gauge-value throttle">{currentThrottle}</div>
            <div className="gauge-optimal">⚡ {optimalThrottle}</div>
          </div>
          <div className="gauge-unit">%</div>
          <div className="gauge-bar">
            <div
              className="gauge-fill-ghost throttle-ghost"
              style={{ width: `${optimalThrottle}%` }}
            ></div>
            <div
              className="gauge-fill throttle-fill"
              style={{ width: `${currentThrottle}%` }}
            ></div>
          </div>
          <div className="gauge-delta" style={{ color: Math.abs(currentThrottle - optimalThrottle) < 10 ? '#2ecc71' : '#f39c12' }}>
            Δ {Math.abs(currentThrottle - optimalThrottle)}%
          </div>
        </div>

        <div className="gauge-item">
          <div className="gauge-label">Brake</div>
          <div className="gauge-value-container">
            <div className="gauge-value brake">{currentBrake}</div>
            <div className="gauge-optimal">⚡ {optimalBrake}</div>
          </div>
          <div className="gauge-unit">%</div>
          <div className="gauge-bar">
            <div
              className="gauge-fill-ghost brake-ghost"
              style={{ width: `${optimalBrake}%` }}
            ></div>
            <div
              className="gauge-fill brake-fill"
              style={{ width: `${currentBrake}%` }}
            ></div>
          </div>
          <div className="gauge-delta" style={{ color: Math.abs(currentBrake - optimalBrake) < 10 ? '#2ecc71' : '#f39c12' }}>
            Δ {Math.abs(currentBrake - optimalBrake)}%
          </div>
        </div>

        <div className="gauge-item">
          <div className="gauge-label">Gear</div>
          <div className="gauge-value gear">{currentGear}</div>
          <div className="gauge-unit">gear</div>
        </div>

        <div className="gauge-item">
          <div className="gauge-label">RPM</div>
          <div className="gauge-value rpm">{currentRPM}</div>
          <div className="gauge-unit">rpm</div>
          <div className="gauge-bar">
            <div
              className="gauge-fill rpm-fill"
              style={{ width: `${(currentRPM / 8000) * 100}%` }}
            ></div>
          </div>
        </div>
      </div>

      {telemetryData.length > 0 && (
        <div className="telemetry-chart">
          <ResponsiveContainer width="100%" height={200}>
            <AreaChart data={telemetryData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis
                dataKey="time"
                stroke="rgba(255,255,255,0.6)"
                label={{ value: 'Lap Progress', position: 'insideBottom', offset: -5 }}
              />
              <YAxis
                stroke="rgba(255,255,255,0.6)"
                label={{ value: 'Value', angle: -90, position: 'insideLeft' }}
              />
              <Tooltip
                contentStyle={{
                  background: 'rgba(0,0,0,0.8)',
                  border: '1px solid rgba(255,255,255,0.2)',
                  borderRadius: '8px'
                }}
              />
              <Legend />
              <Area
                type="monotone"
                dataKey="optimalSpeed"
                stroke="#3498db"
                fill="rgba(52, 152, 219, 0.1)"
                strokeWidth={1}
                strokeDasharray="5 5"
                name="Optimal Speed"
              />
              <Area
                type="monotone"
                dataKey="speed"
                stroke="#3498db"
                fill="rgba(52, 152, 219, 0.3)"
                strokeWidth={2}
                name="Speed (km/h)"
              />
              <Area
                type="monotone"
                dataKey="optimalThrottle"
                stroke="#2ecc71"
                fill="rgba(46, 204, 113, 0.1)"
                strokeWidth={1}
                strokeDasharray="5 5"
                name="Optimal Throttle"
              />
              <Area
                type="monotone"
                dataKey="throttle"
                stroke="#2ecc71"
                fill="rgba(46, 204, 113, 0.3)"
                strokeWidth={2}
                name="Throttle (%)"
              />
              <Area
                type="monotone"
                dataKey="optimalBrake"
                stroke="#e74c3c"
                fill="rgba(231, 76, 60, 0.1)"
                strokeWidth={1}
                strokeDasharray="5 5"
                name="Optimal Brake"
              />
              <Area
                type="monotone"
                dataKey="brake"
                stroke="#e74c3c"
                fill="rgba(231, 76, 60, 0.3)"
                strokeWidth={2}
                name="Brake (%)"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      )}

      {isPlaying && (
        <div className="performance-indicator">
          {currentSpeed >= optimalSpeed - 5 && currentThrottle >= optimalThrottle - 10 ? (
            <div className="indicator-good">
              <span className="indicator-icon">✓</span>
              <span>Matching Optimal Performance</span>
            </div>
          ) : (
            <div className="indicator-improve">
              <span className="indicator-icon">⚠</span>
              <span>Room for Improvement</span>
            </div>
          )}
        </div>
      )}

      {!isPlaying && (
        <div className="telemetry-paused">
          <p>▶️ Press Play to start live telemetry simulation</p>
        </div>
      )}
    </div>
  )
}

export default TelemetryLive
