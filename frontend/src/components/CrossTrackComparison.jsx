import React, { useState, useEffect } from 'react';
import './CrossTrackComparison.css';

const CrossTrackComparison = ({ vehicleId }) => {
  const [comparison, setComparison] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (vehicleId) {
      fetchComparison();
    }
  }, [vehicleId]);

  const fetchComparison = async () => {
    try {
      setLoading(true);
      setError(null);

      // The vehicleId is actually the vehicle number (e.g., 78)
      // The backend expects a vehicle_id string that appears in the data (e.g., "78" or "GR86-XXX-78")
      // Try with just the number first
      const response = await fetch(`/api/vehicle/${vehicleId}/cross-track?race_num=1`);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setComparison(data);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch cross-track comparison:', error);
      setError(error.message);
      setComparison(null);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="cross-track-card">
        <h3>🌍 Cross-Track Performance</h3>
        <div className="loading-state">Analyzing performance across all tracks...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="cross-track-card">
        <h3>🌍 Cross-Track Performance</h3>
        <div className="error-state">
          <p>Unable to load cross-track data</p>
          <p className="error-detail">{error}</p>
        </div>
      </div>
    );
  }

  if (!comparison || !comparison.comparison || comparison.comparison.length === 0) {
    return (
      <div className="cross-track-card">
        <h3>🌍 Cross-Track Performance</h3>
        <div className="no-data">
          <p>No cross-track data available for vehicle #{vehicleId}</p>
          <p className="hint">This vehicle may not have competed at other tracks yet.</p>
        </div>
      </div>
    );
  }

  const tracks = comparison.comparison;
  const bestTrack = tracks.reduce((best, track) =>
    track.best_lap_sec < best.best_lap_sec ? track : best
  );

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = (seconds % 60).toFixed(3);
    return `${mins}:${secs.padStart(6, '0')}`;
  };

  return (
    <div className="cross-track-card">
      <div className="card-header">
        <h3>🌍 Cross-Track Performance</h3>
        <div className="tracks-count">{tracks.length} Tracks</div>
      </div>

      <div className="best-track-highlight">
        <div className="label">Best Performance</div>
        <div className="track-name">{bestTrack.track}</div>
        <div className="time">{formatTime(bestTrack.best_lap_sec)}</div>
        <div className="speed">{bestTrack.avg_speed_kmh.toFixed(1)} km/h avg</div>
      </div>

      <div className="tracks-list">
        {tracks.map((track, index) => {
          const isBest = track.track === bestTrack.track;
          const gapToBest = track.best_lap_sec - bestTrack.best_lap_sec;

          return (
            <div key={index} className={`track-item ${isBest ? 'best' : ''}`}>
              <div className="track-position">{index + 1}</div>
              <div className="track-info">
                <div className="track-name">{track.track}</div>
                <div className="track-stats">
                  <span className="stat">
                    <span className="stat-label">Best:</span>
                    <span className="stat-value">{formatTime(track.best_lap_sec)}</span>
                  </span>
                  <span className="stat">
                    <span className="stat-label">Speed:</span>
                    <span className="stat-value">{track.avg_speed_kmh.toFixed(1)} km/h</span>
                  </span>
                  <span className="stat">
                    <span className="stat-label">Laps:</span>
                    <span className="stat-value">{track.laps_completed}</span>
                  </span>
                </div>
                {!isBest && gapToBest > 0 && (
                  <div className="gap-to-best">+{gapToBest.toFixed(3)}s</div>
                )}
              </div>
              {isBest && <div className="best-badge">⭐ Best</div>}
            </div>
          );
        })}
      </div>

      <div className="summary-stats">
        <div className="summary-item">
          <div className="summary-label">Total Laps</div>
          <div className="summary-value">
            {tracks.reduce((sum, t) => sum + t.laps_completed, 0)}
          </div>
        </div>
        <div className="summary-item">
          <div className="summary-label">Avg Speed</div>
          <div className="summary-value">
            {(tracks.reduce((sum, t) => sum + t.avg_speed_kmh, 0) / tracks.length).toFixed(1)} km/h
          </div>
        </div>
        <div className="summary-item">
          <div className="summary-label">Tracks Raced</div>
          <div className="summary-value">{tracks.length}/7</div>
        </div>
      </div>
    </div>
  );
};

export default CrossTrackComparison;
