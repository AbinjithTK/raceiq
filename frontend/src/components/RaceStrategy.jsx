import React, { useState, useEffect } from 'react'
import './Card.css'

function RaceStrategy({ vehicleNumber, currentLap, totalLaps, trackName, raceNum }) {
  const [fuelStrategy, setFuelStrategy] = useState(null)
  const [paceAnalysis, setPaceAnalysis] = useState(null)
  const [pitStrategy, setPitStrategy] = useState(null)
  const [finishPrediction, setFinishPrediction] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadStrategyData()
  }, [vehicleNumber, currentLap])

  const loadStrategyData = async () => {
    try {
      setLoading(true)
      
      // Load all strategy data in parallel
      const [fuel, pace, pit, finish] = await Promise.all([
        fetch(`http://localhost:8001/strategy/fuel/${vehicleNumber}?current_lap=${currentLap}&total_laps=${totalLaps}`)
          .then(r => r.json()),
        fetch(`http://localhost:8001/strategy/pace/${vehicleNumber}?current_lap=${currentLap}`)
          .then(r => r.json()),
        fetch(`http://localhost:8001/strategy/pit-optimal/${vehicleNumber}?current_lap=${currentLap}&total_laps=${totalLaps}`)
          .then(r => r.json()),
        fetch(`http://localhost:8001/strategy/finish-prediction/${vehicleNumber}?current_lap=${currentLap}&total_laps=${totalLaps}`)
          .then(r => r.json())
      ])
      
      setFuelStrategy(fuel)
      setPaceAnalysis(pace)
      setPitStrategy(pit)
      setFinishPrediction(finish)
    } catch (error) {
      console.error('Failed to load strategy data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="card wide">
        <h2 className="card-title">🎯 Race Strategy</h2>
        <div className="card-loading">Analyzing race data...</div>
      </div>
    )
  }

  const getPaceStatus = () => {
    if (!paceAnalysis) return 'neutral'
    if (paceAnalysis.is_improving) return 'success'
    if (paceAnalysis.is_degrading) return 'warning'
    return 'neutral'
  }

  return (
    <div className="card wide">
      <h2 className="card-title">🎯 Race Strategy - Real Data Analysis</h2>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px' }}>
        
        {/* Fuel Strategy */}
        {fuelStrategy && (
          <div className="strategy-section" style={{
            background: 'rgba(52, 152, 219, 0.1)',
            border: '1px solid rgba(52, 152, 219, 0.3)',
            borderRadius: '8px',
            padding: '16px'
          }}>
            <h3 style={{ margin: '0 0 12px 0', fontSize: '16px', color: '#3498db' }}>
              ⛽ Fuel Strategy
            </h3>
            <div style={{ fontSize: '14px', lineHeight: '1.6' }}>
              <div style={{ marginBottom: '8px' }}>
                <strong>Current Fuel:</strong> {fuelStrategy.current_fuel_liters}L
              </div>
              <div style={{ marginBottom: '8px' }}>
                <strong>Consumption:</strong> {fuelStrategy.consumption_per_lap}L/lap
              </div>
              <div style={{ marginBottom: '8px' }}>
                <strong>Laps Remaining:</strong> {fuelStrategy.laps_on_current_fuel} laps
              </div>
              {fuelStrategy.needs_pit && (
                <div style={{
                  marginTop: '12px',
                  padding: '8px',
                  background: 'rgba(231, 76, 60, 0.2)',
                  borderRadius: '4px',
                  color: '#e74c3c'
                }}>
                  <strong>⚠️ Pit Required</strong><br />
                  Lap {fuelStrategy.recommended_pit_lap}<br />
                  Add {fuelStrategy.fuel_to_add_liters}L
                </div>
              )}
              {!fuelStrategy.needs_pit && (
                <div style={{
                  marginTop: '12px',
                  padding: '8px',
                  background: 'rgba(46, 204, 113, 0.2)',
                  borderRadius: '4px',
                  color: '#2ecc71'
                }}>
                  ✅ Fuel sufficient to finish
                </div>
              )}
            </div>
          </div>
        )}

        {/* Pace Analysis */}
        {paceAnalysis && (
          <div className="strategy-section" style={{
            background: 'rgba(155, 89, 182, 0.1)',
            border: '1px solid rgba(155, 89, 182, 0.3)',
            borderRadius: '8px',
            padding: '16px'
          }}>
            <h3 style={{ margin: '0 0 12px 0', fontSize: '16px', color: '#9b59b6' }}>
              📊 Race Pace
            </h3>
            <div style={{ fontSize: '14px', lineHeight: '1.6' }}>
              <div style={{ marginBottom: '8px' }}>
                <strong>Current Pace:</strong> {paceAnalysis.current_pace}s
              </div>
              <div style={{ marginBottom: '8px' }}>
                <strong>Best Lap:</strong> {paceAnalysis.best_lap}s
              </div>
              <div style={{ marginBottom: '8px' }}>
                <strong>Delta:</strong> <span style={{ color: paceAnalysis.pace_delta > 0.5 ? '#e74c3c' : '#2ecc71' }}>
                  +{paceAnalysis.pace_delta}s
                </span>
              </div>
              <div style={{ marginBottom: '8px' }}>
                <strong>Position by Pace:</strong> {paceAnalysis.pace_position}/{paceAnalysis.total_competitors}
              </div>
              <div style={{
                marginTop: '12px',
                padding: '8px',
                background: paceAnalysis.is_improving ? 'rgba(46, 204, 113, 0.2)' : 
                           paceAnalysis.is_degrading ? 'rgba(231, 76, 60, 0.2)' : 
                           'rgba(149, 165, 166, 0.2)',
                borderRadius: '4px',
                color: paceAnalysis.is_improving ? '#2ecc71' : 
                       paceAnalysis.is_degrading ? '#e74c3c' : '#95a5a6'
              }}>
                {paceAnalysis.is_improving && '📈 Pace Improving'}
                {paceAnalysis.is_degrading && '📉 Pace Degrading'}
                {!paceAnalysis.is_improving && !paceAnalysis.is_degrading && '➡️ Pace Stable'}
              </div>
              {paceAnalysis.is_consistent && (
                <div style={{ marginTop: '8px', fontSize: '12px', color: '#2ecc71' }}>
                  ✓ Consistent (σ={paceAnalysis.consistency_std.toFixed(3)}s)
                </div>
              )}
            </div>
          </div>
        )}

        {/* Pit Strategy */}
        {pitStrategy && (
          <div className="strategy-section" style={{
            background: 'rgba(230, 126, 34, 0.1)',
            border: '1px solid rgba(230, 126, 34, 0.3)',
            borderRadius: '8px',
            padding: '16px'
          }}>
            <h3 style={{ margin: '0 0 12px 0', fontSize: '16px', color: '#e67e22' }}>
              🔧 Pit Strategy
            </h3>
            <div style={{ fontSize: '14px', lineHeight: '1.6' }}>
              <div style={{ marginBottom: '8px' }}>
                <strong>Recommendation:</strong> {pitStrategy.should_pit ? 'PIT' : 'STAY OUT'}
              </div>
              {pitStrategy.should_pit && (
                <>
                  <div style={{ marginBottom: '8px' }}>
                    <strong>Optimal Lap:</strong> {pitStrategy.optimal_pit_lap}
                  </div>
                  <div style={{ marginBottom: '8px' }}>
                    <strong>Laps Until Pit:</strong> {pitStrategy.laps_until_pit}
                  </div>
                  <div style={{ marginBottom: '8px' }}>
                    <strong>Time Saved:</strong> <span style={{ color: '#2ecc71' }}>
                      {pitStrategy.time_saved_seconds}s
                    </span>
                  </div>
                </>
              )}
              <div style={{ marginBottom: '8px' }}>
                <strong>Tire Deg Rate:</strong> {pitStrategy.degradation_rate}s/lap
              </div>
              <div style={{
                marginTop: '12px',
                padding: '8px',
                background: pitStrategy.should_pit ? 'rgba(230, 126, 34, 0.2)' : 'rgba(46, 204, 113, 0.2)',
                borderRadius: '4px',
                fontSize: '13px',
                color: pitStrategy.should_pit ? '#e67e22' : '#2ecc71'
              }}>
                {pitStrategy.message}
              </div>
            </div>
          </div>
        )}

        {/* Finish Prediction */}
        {finishPrediction && (
          <div className="strategy-section" style={{
            background: 'rgba(241, 196, 15, 0.1)',
            border: '1px solid rgba(241, 196, 15, 0.3)',
            borderRadius: '8px',
            padding: '16px'
          }}>
            <h3 style={{ margin: '0 0 12px 0', fontSize: '16px', color: '#f1c40f' }}>
              🏆 Finish Prediction
            </h3>
            <div style={{ fontSize: '14px', lineHeight: '1.6' }}>
              <div style={{ marginBottom: '8px' }}>
                <strong>Predicted Time:</strong><br />
                <span style={{ fontSize: '18px', color: '#f1c40f' }}>
                  {finishPrediction.predicted_finish_time}
                </span>
              </div>
              <div style={{ marginBottom: '8px' }}>
                <strong>Time Elapsed:</strong> {(finishPrediction.time_elapsed / 60).toFixed(1)} min
              </div>
              <div style={{ marginBottom: '8px' }}>
                <strong>Time Remaining:</strong> {(finishPrediction.time_remaining / 60).toFixed(1)} min
              </div>
              <div style={{ marginBottom: '8px' }}>
                <strong>Laps to Go:</strong> {finishPrediction.laps_remaining}
              </div>
              <div style={{ marginBottom: '8px' }}>
                <strong>Predicted Avg:</strong> {finishPrediction.predicted_avg_lap}s/lap
              </div>
            </div>
          </div>
        )}

      </div>

      <div style={{
        marginTop: '16px',
        padding: '12px',
        background: 'rgba(52, 73, 94, 0.3)',
        borderRadius: '8px',
        fontSize: '12px',
        color: '#95a5a6',
        textAlign: 'center'
      }}>
        📊 All calculations based on real race data from {trackName} Race {raceNum}
      </div>
    </div>
  )
}

export default RaceStrategy
