import React, { useState, useEffect } from 'react';
import { GradientButton } from './ui/gradient-button';
import { fetchTracks as fetchTracksAPI } from '../api';
import './TrackSelector.css';

const TrackSelector = ({ onTrackChange, currentTrack }) => {
  const [tracks, setTracks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showDropdown, setShowDropdown] = useState(false);

  useEffect(() => {
    loadTracks();
  }, []);

  const loadTracks = async () => {
    try {
      const data = await fetchTracksAPI();
      setTracks(data.tracks || []);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch tracks:', error);
      setLoading(false);
    }
  };

  const trackDisplayNames = {
    barber: 'Barber Motorsports Park',
    indianapolis: 'Indianapolis Motor Speedway',
    cota: 'Circuit of The Americas',
    sebring: 'Sebring International Raceway',
    road_america: 'Road America',
    sonoma: 'Sonoma Raceway',
    vir: 'Virginia International Raceway'
  };

  const trackIcons = {
    barber: '🏁',
    indianapolis: '🏎️',
    cota: '🌟',
    sebring: '⚡',
    road_america: '🌲',
    sonoma: '🍷',
    vir: '🏔️'
  };

  const handleTrackSelect = (track) => {
    onTrackChange(track);
    setShowDropdown(false);
  };

  if (loading) {
    return <div className="track-selector loading">Loading tracks...</div>;
  }

  return (
    <div className="track-selector">
      <GradientButton
        className="track-selector-button w-full justify-between"
        onClick={() => setShowDropdown(!showDropdown)}
      >
        <span className="flex items-center gap-3">
          <span className="track-icon">{trackIcons[currentTrack] || '🏁'}</span>
          <span className="track-name">{trackDisplayNames[currentTrack] || 'Select Track'}</span>
        </span>
        <span className="dropdown-arrow ml-4">{showDropdown ? '▲' : '▼'}</span>
      </GradientButton>

      {showDropdown && (
        <div className="track-dropdown">
          {tracks.map(track => (
            <button
              key={track}
              className={`track-option ${track === currentTrack ? 'active' : ''}`}
              onClick={() => handleTrackSelect(track)}
            >
              <span className="track-icon">{trackIcons[track] || '🏁'}</span>
              <span className="track-name">{trackDisplayNames[track] || track}</span>
              {track === currentTrack && <span className="check-mark">✓</span>}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export default TrackSelector;
