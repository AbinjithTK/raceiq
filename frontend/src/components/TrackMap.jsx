import React, { useState, useEffect, useRef } from 'react'
import './TrackMap.css'
import { TRACKS } from '../data/tracks'

function TrackMap({ vehicleNumber, currentLap, totalLaps, isPlaying, onPlayPause, trackName = 'barber', onRaceUpdate }) {
  const [carPosition, setCarPosition] = useState(0)
  const [speed, setSpeed] = useState(0)
  const [sector, setSector] = useState(1)
  const [lapProgress, setLapProgress] = useState(0)
  const animationRef = useRef(null)
  const startTimeRef = useRef(null)

  const trackPath = TRACKS[trackName] || TRACKS['barber']

  const [ghostPosition, setGhostPosition] = useState(0)

  useEffect(() => {
    if (isPlaying) {
      startTimeRef.current = Date.now() - (lapProgress / 100 * 98000) // Resume from current progress
      animate()
    } else {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current)
      }
    }

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current)
      }
    }
  }, [isPlaying, trackName]) // Reset when track changes

  // Reset progress when track changes
  useEffect(() => {
    setLapProgress(0)
    setCarPosition(0)
    setGhostPosition(0)
    setSector(1)
    if (isPlaying) {
      startTimeRef.current = Date.now()
    }
  }, [trackName])

  const animate = () => {
    const elapsed = Date.now() - startTimeRef.current
    const lapDuration = 98000 // ~98 seconds per lap (1:38 lap time)
    const ghostLapDuration = 95000 // Ghost is slightly faster (1:35 lap time)

    const progress = (elapsed % lapDuration) / lapDuration
    const ghostProgress = (elapsed % ghostLapDuration) / ghostLapDuration

    const currentProgress = progress * 100
    setLapProgress(currentProgress)

    // Calculate position on track
    const positionIndex = Math.floor(progress * trackPath.length)
    setCarPosition(positionIndex % trackPath.length)

    const ghostIndex = Math.floor(ghostProgress * trackPath.length)
    setGhostPosition(ghostIndex % trackPath.length)

    // Update sector
    const currentPoint = trackPath[positionIndex % trackPath.length]
    let currentSector = 1
    if (currentPoint) {
      currentSector = currentPoint.sector
      setSector(currentSector)
    }

    // Simulate speed variation (120-180 km/h)
    const speedVariation = Math.sin(progress * Math.PI * 8) * 30
    const currentSpeed = Math.round(150 + speedVariation)
    setSpeed(currentSpeed)

    if (onRaceUpdate) {
      onRaceUpdate({
        speed: currentSpeed,
        progress: currentProgress,
        sector: currentSector
      })
    }

    animationRef.current = requestAnimationFrame(animate)
  }

  const currentPoint = trackPath[carPosition] || trackPath[0]
  const nextPoint = trackPath[(carPosition + 1) % trackPath.length] || trackPath[1]

  const ghostPoint = trackPath[ghostPosition] || trackPath[0]

  // Calculate car rotation
  const angle = Math.atan2(
    nextPoint.y - currentPoint.y,
    nextPoint.x - currentPoint.x
  ) * (180 / Math.PI)

  return (
    <div className="track-map-container">
      <div className="track-map-header">
        <h2 className="card-title">🗺️ Live Track Position - {trackName.replace('_', ' ').toUpperCase()}</h2>
        <div className="track-controls">
          <button
            className={`play-button ${isPlaying ? 'playing' : ''}`}
            onClick={onPlayPause}
          >
            {isPlaying ? '⏸️ Pause' : '▶️ Play'}
          </button>
        </div>
      </div>

      <div className="track-info">
        <div className="info-item">
          <span className="info-label">Lap</span>
          <span className="info-value">{currentLap} / {totalLaps}</span>
        </div>
        <div className="info-item">
          <span className="info-label">Sector</span>
          <span className={`info-value sector-${sector}`}>S{sector}</span>
        </div>
        <div className="info-item">
          <span className="info-label">Speed</span>
          <span className="info-value">{speed} km/h</span>
        </div>
        <div className="info-item">
          <span className="info-label">Progress</span>
          <span className="info-value">{lapProgress.toFixed(1)}%</span>
        </div>
      </div>

      <div className="track-canvas">
        <svg viewBox="0 0 100 100" className="track-svg">
          {/* Track background */}
          <defs>
            <linearGradient id="trackGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#2c3e50" />
              <stop offset="100%" stopColor="#34495e" />
            </linearGradient>

            <filter id="glow">
              <feGaussianBlur stdDeviation="0.5" result="coloredBlur" />
              <feMerge>
                <feMergeNode in="coloredBlur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>

          {/* Draw track */}
          <path
            d={`M ${trackPath.map(p => `${p.x},${p.y}`).join(' L ')} Z`}
            fill="none"
            stroke="url(#trackGradient)"
            strokeWidth="4"
            strokeLinecap="round"
            strokeLinejoin="round"
          />

          {/* Sector markers */}
          {trackPath.map((point, index) => {
            const prevSector = index > 0 ? trackPath[index - 1].sector : trackPath[trackPath.length - 1].sector
            if (point.sector !== prevSector) {
              return (
                <g key={`sector-${index}`}>
                  <circle
                    cx={point.x}
                    cy={point.y}
                    r="1.5"
                    fill={point.sector === 1 ? '#e74c3c' : point.sector === 2 ? '#f39c12' : '#2ecc71'}
                    opacity="0.8"
                  />
                  <text
                    x={point.x}
                    y={point.y - 3}
                    fontSize="3"
                    fill="white"
                    textAnchor="middle"
                    fontWeight="bold"
                  >
                    S{point.sector}
                  </text>
                </g>
              )
            }
            return null
          })}

          {/* Start/Finish line */}
          <line
            x1={trackPath[0].x - 2}
            y1={trackPath[0].y}
            x2={trackPath[0].x + 2}
            y2={trackPath[0].y}
            stroke="white"
            strokeWidth="0.5"
            strokeDasharray="1,1"
          />
          <text
            x={trackPath[0].x}
            y={trackPath[0].y + 5}
            fontSize="3"
            fill="white"
            textAnchor="middle"
            fontWeight="bold"
          >
            START/FINISH
          </text>

          {/* Ghost Car */}
          <circle
            cx={ghostPoint.x}
            cy={ghostPoint.y}
            r="2"
            fill="none"
            stroke="#bd00ff"
            strokeWidth="0.5"
            opacity="0.6"
            className="ghost-car"
          />

          {/* Car */}
          <g
            transform={`translate(${currentPoint.x}, ${currentPoint.y}) rotate(${angle})`}
            filter="url(#glow)"
          >
            {/* Car body */}
            <rect
              x="-2"
              y="-1"
              width="4"
              height="2"
              fill="#3498db"
              rx="0.5"
            />
            {/* Car number */}
            <text
              x="0"
              y="0.5"
              fontSize="1.5"
              fill="white"
              textAnchor="middle"
              fontWeight="bold"
            >
              {vehicleNumber}
            </text>
            {/* Speed indicator (trail) */}
            <circle
              cx="-3"
              cy="0"
              r="0.5"
              fill="#3498db"
              opacity="0.5"
            />
          </g>

          {/* Lap progress indicator */}
          <path
            d={`M ${trackPath.slice(0, Math.floor(carPosition) + 1).map(p => `${p.x},${p.y}`).join(' L ')}`}
            fill="none"
            stroke="#3498db"
            strokeWidth="1"
            opacity="0.6"
            strokeLinecap="round"
          />
        </svg>
      </div>

      <div className="track-legend">
        <div className="legend-item">
          <span className="legend-color sector-1"></span>
          <span>Sector 1</span>
        </div>
        <div className="legend-item">
          <span className="legend-color sector-2"></span>
          <span>Sector 2</span>
        </div>
        <div className="legend-item">
          <span className="legend-color sector-3"></span>
          <span>Sector 3</span>
        </div>
        <div className="legend-item">
          <span className="legend-color car"></span>
          <span>Car #{vehicleNumber}</span>
        </div>
        <div className="legend-item">
          <span className="legend-color ghost" style={{ background: 'none', border: '1px solid #bd00ff' }}></span>
          <span>Ghost (Optimal)</span>
        </div>
      </div>
    </div>
  )
}

export default TrackMap
