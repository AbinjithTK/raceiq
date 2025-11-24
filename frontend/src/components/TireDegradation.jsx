import React, { useState, useEffect } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { fetchTireDegradation } from '../api'
import './Card.css'

function TireDegradation({ vehicleNumber }) {
  const [degradation, setDegradation] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadDegradation()
  }, [vehicleNumber])

  const loadDegradation = async () => {
    try {
      setLoading(true)
      const data = await fetchTireDegradation(vehicleNumber)
      setDegradation(data)
    } catch (error) {
      console.error('Failed to load tire degradation:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="card wide">
        <h2 className="card-title">🔴 Tire Degradation Analysis</h2>
        <div className="card-loading">Loading...</div>
      </div>
    )
  }

  if (!degradation || !degradation.laps) return null

  return (
    <div className="card wide">
      <h2 className="card-title">🔴 Tire Degradation Analysis</h2>

      <div className="tire-degradation-content">
        <div className="degradation-summary">
          <div className="summary-item">
            <span className="summary-label">Best Lap</span>
            <span className="summary-value">{degradation.best_lap_time?.toFixed(3)}s</span>
          </div>
          <div className="summary-item">
            <span className="summary-label">Worst Lap</span>
            <span className="summary-value">{degradation.worst_lap_time?.toFixed(3)}s</span>
          </div>
          <div className="summary-item">
            <span className="summary-label">Avg Degradation</span>
            <span className="summary-value">+{degradation.avg_degradation?.toFixed(3)}s</span>
          </div>
          <div className="summary-item">
            <span className="summary-label">Total Laps</span>
            <span className="summary-value">{degradation.total_laps}</span>
          </div>
        </div>

        <div className="chart-container">
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={degradation.laps}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis
                dataKey="LAP_NUMBER"
                stroke="rgba(255,255,255,0.6)"
                label={{ value: 'Lap Number', position: 'insideBottom', offset: -5 }}
              />
              <YAxis
                stroke="rgba(255,255,255,0.6)"
                label={{ value: 'Lap Time (s)', angle: -90, position: 'insideLeft' }}
              />
              <Tooltip
                contentStyle={{
                  background: 'rgba(0,0,0,0.8)',
                  border: '1px solid rgba(255,255,255,0.2)',
                  borderRadius: '8px'
                }}
              />
              <Legend />
              <Line
                type="monotone"
                dataKey="lap_time_seconds"
                stroke="#e74c3c"
                strokeWidth={2}
                dot={{ r: 4 }}
                name="Lap Time"
              />
              <Line
                type="monotone"
                dataKey="delta_to_best"
                stroke="#3498db"
                strokeWidth={2}
                dot={{ r: 3 }}
                name="Delta to Best"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}

export default TireDegradation
