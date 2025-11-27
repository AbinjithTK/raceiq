import axios from 'axios'

const API_BASE_URL = 'https://raceiq-backend.onrender.com'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const fetchVehicles = async () => {
  const response = await api.get('/vehicles')
  return response.data
}

export const fetchPitPrediction = async (vehicleNumber, currentLap, totalLaps) => {
  const response = await api.post('/pit-prediction', {
    vehicle_number: vehicleNumber,
    current_lap: currentLap,
    total_laps: totalLaps,
  })
  return response.data
}

export const fetchTireDegradation = async (vehicleNumber) => {
  const response = await api.get(`/tire-degradation/${vehicleNumber}`)
  return response.data
}

export const fetchCoachingInsights = async (vehicleNumber, lapNumber) => {
  const response = await api.post('/coaching', {
    vehicle_number: vehicleNumber,
    lap_number: lapNumber,
  })
  return response.data
}

export const fetchLapPotential = async (vehicleNumber) => {
  const response = await api.get(`/lap-potential/${vehicleNumber}`)
  return response.data
}

export const fetchSectorDegradation = async (vehicleNumber) => {
  const response = await api.get(`/sector-degradation/${vehicleNumber}`)
  return response.data
}

export const fetchTracks = async () => {
  const response = await api.get('/tracks')
  return response.data
}

export const fetchTrackInfo = async (trackName) => {
  const response = await api.get(`/tracks/${trackName}`)
  return response.data
}
