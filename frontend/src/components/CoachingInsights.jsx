import React, { useState, useEffect } from 'react'
import { fetchCoachingInsights } from '../api'
import './Card.css'

function CoachingInsights({ vehicleNumber, currentLap }) {
  const [insights, setInsights] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadInsights()
  }, [vehicleNumber, currentLap])

  const loadInsights = async () => {
    try {
      setLoading(true)
      const data = await fetchCoachingInsights(vehicleNumber, currentLap)
      setInsights(data)
    } catch (error) {
      console.error('Failed to load coaching insights:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="card wide">
        <h2 className="card-title">💡 Coaching Insights</h2>
        <div className="card-loading">Loading...</div>
      </div>
    )
  }

  if (!insights || !insights.opportunities) return null

  const totalTimeAvailable = insights.opportunities.reduce(
    (sum, opp) => sum + opp.time_loss, 0
  )

  return (
    <div className="card wide">
      <h2 className="card-title">💡 Coaching Insights - Lap {currentLap}</h2>

      <div className="coaching-content">
        {insights.opportunities.length === 0 ? (
          <div className="perfect-lap">
            <div className="perfect-icon">✅</div>
            <h3>Perfect Lap!</h3>
            <p>No improvements needed - driver is matching personal best in all sectors.</p>
          </div>
        ) : (
          <>
            <div className="total-opportunity">
              <span className="opportunity-label">Total Time Available</span>
              <span className="opportunity-value">{totalTimeAvailable.toFixed(3)}s</span>
            </div>

            <div className="opportunities-list">
              {insights.opportunities.map((opp, index) => (
                <div key={index} className="opportunity-item">
                  <div className="opportunity-header">
                    <span className="opportunity-sector">{opp.sector}</span>
                    <span className="opportunity-time">+{opp.time_loss.toFixed(3)}s</span>
                  </div>
                  <div className="opportunity-message">{opp.message}</div>
                  <div className="opportunity-suggestion">
                    <span className="suggestion-icon">💡</span>
                    {opp.suggestion}
                  </div>
                </div>
              ))}
            </div>

            <div className="coaching-summary">
              <p>
                Focus on the highlighted sectors to recover {totalTimeAvailable.toFixed(3)}s per lap.
                Over the remaining race, this could save significant time.
              </p>
            </div>
          </>
        )}
      </div>
    </div>
  )
}

export default CoachingInsights
