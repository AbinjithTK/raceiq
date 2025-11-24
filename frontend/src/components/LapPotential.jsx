import React, { useState, useEffect } from 'react'
import { fetchLapPotential } from '../api'
import './Card.css'

function LapPotential({ vehicleNumber }) {
  const [potential, setPotential] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadPotential()
  }, [vehicleNumber])

  const loadPotential = async () => {
    try {
      setLoading(true)
      const data = await fetchLapPotential(vehicleNumber)
      setPotential(data)
    } catch (error) {
      console.error('Failed to load lap potential:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="card">
        <h2 className="card-title">⚡ Lap Time Potential</h2>
        <div className="card-loading">Loading...</div>
      </div>
    )
  }

  if (!potential) return null

  const improvementPercent = (potential.improvement_potential / potential.actual_best * 100).toFixed(2)

  return (
    <div className="card">
      <h2 className="card-title">⚡ Lap Time Potential</h2>
      
      <div className="lap-potential-content">
        <div className="lap-times">
          <div className="lap-time-item">
            <span className="lap-time-label">Actual Best</span>
            <span className="lap-time-value">{potential.actual_best?.toFixed(3)}s</span>
          </div>
          
          <div className="lap-time-item theoretical">
            <span className="lap-time-label">Theoretical Best</span>
            <span className="lap-time-value">{potential.theoretical_best?.toFixed(3)}s</span>
          </div>
          
          <div className="lap-time-item improvement">
            <span className="lap-time-label">Improvement Available</span>
            <span className="lap-time-value highlight">
              {potential.improvement_potential?.toFixed(3)}s
              <span className="improvement-percent">({improvementPercent}%)</span>
            </span>
          </div>
        </div>

        <div className="sector-times">
          <h3>Best Sectors</h3>
          <div className="sectors">
            <div className="sector">
              <span className="sector-label">S1</span>
              <span className="sector-value">{potential.best_s1?.toFixed(3)}s</span>
            </div>
            <div className="sector">
              <span className="sector-label">S2</span>
              <span className="sector-value">{potential.best_s2?.toFixed(3)}s</span>
            </div>
            <div className="sector">
              <span className="sector-label">S3</span>
              <span className="sector-value">{potential.best_s3?.toFixed(3)}s</span>
            </div>
          </div>
        </div>

        {potential.improvement_potential < 0.1 ? (
          <div className="perfect-lap-message">
            ✅ Near-perfect execution! Driver is maximizing the car.
          </div>
        ) : (
          <div className="improvement-message">
            💡 {potential.improvement_potential?.toFixed(3)}s available through perfect sector execution
          </div>
        )}
      </div>
    </div>
  )
}

export default LapPotential
