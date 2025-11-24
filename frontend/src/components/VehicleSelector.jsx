import React from 'react'
import { GradientButton } from './ui/gradient-button'
import './VehicleSelector.css'

function VehicleSelector({ vehicles, selectedVehicle, onSelectVehicle }) {
  return (
    <div className="vehicle-selector">
      <label>Vehicle:</label>
      <div className="relative flex-1">
        <select
          value={selectedVehicle?.number || ''}
          onChange={(e) => {
            const vehicle = vehicles.find(v => v.number === parseInt(e.target.value))
            onSelectVehicle(vehicle)
          }}
          className="vehicle-select-input"
        >
          {vehicles.map((vehicle) => (
            <option key={vehicle.number} value={vehicle.number}>
              #{vehicle.number} - P{vehicle.position} ({vehicle.laps} laps)
            </option>
          ))}
        </select>
        <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-white">
          <svg className="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
            <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
          </svg>
        </div>
      </div>

      {selectedVehicle && (
        <div className="vehicle-info">
          <span className="position-badge">P{selectedVehicle.position}</span>
          <span className="vehicle-number">#{selectedVehicle.number}</span>
          <span className="vehicle-status">{selectedVehicle.status}</span>
        </div>
      )}
    </div>
  )
}

export default VehicleSelector
