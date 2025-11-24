import React, { useState, useEffect, useRef } from 'react'
import './RealtimeTips.css'

const TIPS_BY_SECTOR = {
  1: [
    { trigger: 0.02, message: "🏁 Accelerate hard out of start/finish!", type: "throttle" },
    { trigger: 0.05, message: "⚠️ Turn 1 approaching - brake early!", type: "brake" },
    { trigger: 0.08, message: "🎯 Apex Turn 1 - smooth steering input", type: "steering" },
    { trigger: 0.10, message: "⚡ Back on throttle - exit Turn 2", type: "throttle" },
    { trigger: 0.13, message: "💨 Building speed through Turn 3", type: "speed" },
  ],
  2: [
    { trigger: 0.18, message: "⚠️ Chicane ahead - brake hard!", type: "brake" },
    { trigger: 0.22, message: "🎯 Turn 4 apex - late apex line", type: "steering" },
    { trigger: 0.26, message: "⚡ Quick transition Turn 5", type: "steering" },
    { trigger: 0.30, message: "💨 Accelerate through Turn 6", type: "throttle" },
    { trigger: 0.33, message: "🎯 Turn 7 - maintain momentum", type: "speed" },
  ],
  3: [
    { trigger: 0.58, message: "⚠️ Turn 9 - heavy braking zone!", type: "brake" },
    { trigger: 0.62, message: "🎯 Turn 10 apex - smooth input", type: "steering" },
    { trigger: 0.66, message: "⚡ Turn 11 - early throttle!", type: "throttle" },
    { trigger: 0.72, message: "💨 Back straight - full throttle!", type: "throttle" },
    { trigger: 0.95, message: "🏁 Prepare for start/finish!", type: "speed" },
  ]
}

const TIP_TYPES = {
  throttle: { color: '#2ecc71', icon: '⚡' },
  brake: { color: '#e74c3c', icon: '⚠️' },
  steering: { color: '#3498db', icon: '🎯' },
  speed: { color: '#f39c12', icon: '💨' },
}

function RealtimeTips({ lapProgress, sector, isPlaying }) {
  const [currentTip, setCurrentTip] = useState(null)
  const [tipHistory, setTipHistory] = useState([])
  const shownTipsRef = useRef(new Set())

  useEffect(() => {
    if (!isPlaying) {
      setCurrentTip(null)
      shownTipsRef.current.clear()
      return
    }

    // Reset shown tips when lap restarts
    if (lapProgress < 0.01) {
      shownTipsRef.current.clear()
    }

    // Check all sectors for tips
    const allTips = Object.values(TIPS_BY_SECTOR).flat()

    for (const tip of allTips) {
      const tipKey = `${tip.trigger}-${tip.message}`

      // Show tip if we're at or past the trigger point and haven't shown it yet
      if (lapProgress >= tip.trigger &&
        lapProgress < tip.trigger + 0.02 &&
        !shownTipsRef.current.has(tipKey)) {

        setCurrentTip(tip)
        shownTipsRef.current.add(tipKey)

        // Add to history
        setTipHistory(prev => [
          { ...tip, timestamp: Date.now() },
          ...prev.slice(0, 4) // Keep last 5
        ])

        // Clear current tip after 3 seconds
        setTimeout(() => {
          setCurrentTip(null)
        }, 3000)

        break
      }
    }
  }, [lapProgress, isPlaying])

  if (!isPlaying) {
    return (
      <div className="realtime-tips">
        <h3 className="tips-title">💡 Real-Time Coaching</h3>
        <div className="tips-paused">
          <p>▶️ Start simulation to see real-time coaching tips</p>
        </div>
      </div>
    )
  }

  return (
    <div className="realtime-tips">
      <h3 className="tips-title">💡 Real-Time Coaching</h3>

      {currentTip && (
        <div
          className={`current-tip ${currentTip.type}`}
          style={{ borderColor: TIP_TYPES[currentTip.type].color }}
        >
          <div className="tip-icon">{TIP_TYPES[currentTip.type].icon}</div>
          <div className="tip-content">
            <div className="tip-message">{currentTip.message}</div>
            <div className="tip-type">{currentTip.type.toUpperCase()}</div>
          </div>
        </div>
      )}

      {tipHistory.length > 0 && (
        <div className="tip-history">
          <div className="history-title">Recent Tips</div>
          {tipHistory.map((tip, index) => (
            <div
              key={index}
              className="history-item"
              style={{ opacity: 1 - (index * 0.2) }}
            >
              <span className="history-icon">{TIP_TYPES[tip.type].icon}</span>
              <span className="history-message">{tip.message}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default RealtimeTips
