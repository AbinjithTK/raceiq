import React from 'react'
import './Header.css'

function Header() {
  return (
    <header className="header">
      <div className="header-content">
        <div className="logo">
          <span className="logo-icon">🏁</span>
          <h1>RaceIQ</h1>
        </div>
        <p className="tagline">AI-Powered Race Engineer Assistant</p>
      </div>
      <div className="header-status">
        <span className="status-indicator live"></span>
        <span>Live Dashboard</span>
      </div>
    </header>
  )
}

export default Header
