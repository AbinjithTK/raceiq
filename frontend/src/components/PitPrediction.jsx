import React, { useState, useEffect } from 'react'
import { fetchPitPrediction } from '../api'
import './Card.css'

function PitPrediction({ vehicleNumber, currentLap, totalLaps }) {
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadPrediction()
  }, [vehicleNumber, currentLap])

  const loadPrediction = async () => {
    try {
      setLoading(true)
      const data = await fetchPitPrediction(vehicleNumber, currentLap, totalLaps)
      setPrediction(data)
    } catch (error) {
      console.error('Failed to load pit prediction:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="card">
        <h2 className="card-title">🏁 Pit Window Prediction</h2>
        <div className="card-loading">Loading...</div>
      </div>
    )
  }

  if (!prediction) return null

  const getAlertLevel = () => {
    if (prediction.laps_remaining <= 2) return 'critical'
    if (prediction.laps_remaining <= 5) return 'warning'
    return 'normal'
  }

  const alertLevel = getAlertLevel()

  return (
    <div className={`card alert-${alertLevel}`}>
      <h2 className="card-title">🏁 Pit Window Prediction</h2>

      <div className="pit-prediction-content">
        <div className="prediction-main">
          <div className="prediction-value">
            <span className="label">Recommended Pit Lap</span>
            <span className="value large">{prediction.pit_lap}</span>
          </div>

          <div className="prediction-value">
            <span className="label">Laps Remaining</span>
            <span className="value">{prediction.laps_remaining}</span>
          </div>
        </div>

        <div className="prediction-metrics">
          <div className="metric">
            <span className="metric-label">Degradation Rate</span>
            <span className="metric-value">{prediction.degradation_rate?.toFixed(3)}s/lap</span>
          </div>

          <div className="metric">
            <span className="metric-label">Current Delta</span>
            <span className="metric-value">+{prediction.current_delta?.toFixed(3)}s</span>
          </div>

          <div className="metric">
            <span className="metric-label">Confidence</span>
            <div className="confidence-bar">
              <div
                className="confidence-fill"
                style={{ width: `${prediction.confidence}%` }}
              ></div>
              <span className="confidence-text">{prediction.confidence}%</span>
            </div>
          </div>
        </div>

        <div className={`prediction-message ${alertLevel}`}>
          {prediction.message}
        </div>
      </div>
    </div>
  )
}

export default PitPrediction
