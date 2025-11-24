import React, { useRef, useEffect, useState, useMemo } from 'react'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
import './Track3D.css'

function Track3DEnhanced({ trackData, currentLap, isPlaying, onRaceUpdate, trackName = 'barber' }) {
  const mountRef = useRef(null)
  const sceneRef = useRef(null)
  const cameraRef = useRef(null)
  const rendererRef = useRef(null)
  const controlsRef = useRef(null)
  const carRef = useRef(null)
  const animationRef = useRef(null)
  
  const [carPosition, setCarPosition] = useState(0)
  const [speed, setSpeed] = useState(0)
  const [currentSector, setCurrentSector] = useState(1)
  const [heatmapMode, setHeatmapMode] = useState('speed') // 'speed', 'braking', 'gforce'
  const [showGhost, setShowGhost] = useState(true)
  const [optimalTelemetry, setOptimalTelemetry] = useState(null)
  const [optimalLapTime, setOptimalLapTime] = useState(95)
  
  const startTimeRef = useRef(Date.now())
  
  // Load optimal telemetry data
  useEffect(() => {
    const loadOptimalTelemetry = async () => {
      try {
        const response = await fetch(`/api/telemetry/optimal/${trackName}/1`)
        if (response.ok) {
          const data = await response.json()
          setOptimalTelemetry(data)
          setOptimalLapTime(data.lap_time || 95)
          console.log('✅ Loaded optimal telemetry:', data)
        }
      } catch (error) {
        console.error('Failed to load optimal telemetry:', error)
      }
    }
    
    loadOptimalTelemetry()
  }, [trackName])

  // Process track data with telemetry for heatmaps and optimal line
  const processedTrackData = useMemo(() => {
    if (!trackData || trackData.length === 0) {
      console.log('No track data provided')
      return []
    }
    
    // Scale track coordinates to fit in 3D space
    const scaledData = trackData.map((point, index) => {
      const progress = index / trackData.length
      
      // Scale coordinates (original is 0-100, scale to -20 to 20)
      const scaledX = (point.x - 50) * 0.8
      const scaledY = (point.y - 50) * 0.8
      
      // Simulate speed variation (slower in corners, faster on straights)
      const speedVariation = Math.sin(progress * Math.PI * 12) * 40
      const simulatedSpeed = 140 + speedVariation
      
      // Simulate braking zones (before corners)
      const braking = Math.abs(Math.sin(progress * Math.PI * 12)) > 0.7 ? 80 : 0
      
      // Simulate G-forces (higher in corners)
      const gforce = Math.abs(Math.sin(progress * Math.PI * 12)) * 1.5
      
      // Calculate acceleration (change in speed)
      const nextProgress = (index + 1) / trackData.length
      const nextSpeedVar = Math.sin(nextProgress * Math.PI * 12) * 40
      const nextSpeed = 140 + nextSpeedVar
      const acceleration = nextSpeed - simulatedSpeed
      
      return {
        x: scaledX,
        y: scaledY,
        sector: point.sector || 1,
        speed: simulatedSpeed,
        braking: braking,
        gforce: gforce,
        acceleration: acceleration,
        throttle: acceleration > 0 ? 100 : 50
      }
    })
    
    // Calculate optimal racing line (ghost car path)
    // Ghost follows the fastest path based on speed analysis
    const avgSpeed = scaledData.reduce((sum, p) => sum + p.speed, 0) / scaledData.length
    
    const optimalData = scaledData.map((point, index) => {
      // Optimal line is where speed is consistently high
      const isOptimalSpeed = point.speed > avgSpeed * 1.05
      const prevPoint = scaledData[index - 1] || point
      const nextPoint = scaledData[index + 1] || point
      
      // Calculate racing line offset (optimal line is slightly different)
      const lineOffset = isOptimalSpeed ? 0 : 0.2
      
      // Calculate perpendicular offset for racing line
      const dx = nextPoint.x - prevPoint.x
      const dy = nextPoint.y - prevPoint.y
      const length = Math.sqrt(dx * dx + dy * dy) || 1
      const perpX = -dy / length * lineOffset
      const perpY = dx / length * lineOffset
      
      return {
        ...point,
        optimalX: point.x + perpX,
        optimalY: point.y + perpY,
        isOptimal: isOptimalSpeed,
        // Ghost car has better metrics
        optimalSpeed: point.speed * 1.05,
        optimalBraking: point.braking * 0.9,
        optimalAcceleration: point.acceleration * 1.1
      }
    })
    
    console.log(`Processed ${optimalData.length} track points with optimal line`)
    return optimalData
  }, [trackData])

  // Get color based on heatmap mode
  const getHeatmapColor = (point) => {
    let value = 0
    let max = 1
    
    switch (heatmapMode) {
      case 'speed':
        value = point.speed || 0
        max = 180
        break
      case 'braking':
        value = point.braking || 0
        max = 100
        break
      case 'gforce':
        value = point.gforce || 0
        max = 2.0
        break
      default:
        value = point.speed || 0
        max = 180
    }
    
    const normalized = Math.min(value / max, 1)
    
    // Color gradient: Blue (low) -> Green -> Yellow -> Red (high)
    if (normalized < 0.25) {
      // Blue to Cyan
      const t = normalized / 0.25
      return new THREE.Color(0, t, 1)
    } else if (normalized < 0.5) {
      // Cyan to Green
      const t = (normalized - 0.25) / 0.25
      return new THREE.Color(0, 1, 1 - t)
    } else if (normalized < 0.75) {
      // Green to Yellow
      const t = (normalized - 0.5) / 0.25
      return new THREE.Color(t, 1, 0)
    } else {
      // Yellow to Red
      const t = (normalized - 0.75) / 0.25
      return new THREE.Color(1, 1 - t, 0)
    }
  }

  useEffect(() => {
    if (!mountRef.current || !processedTrackData || processedTrackData.length === 0) {
      console.log('Cannot initialize 3D: missing mount or track data')
      return
    }
    
    console.log('Initializing 3D scene with', processedTrackData.length, 'points')

    // Scene setup
    const scene = new THREE.Scene()
    scene.background = new THREE.Color(0x0a0a0b)
    scene.fog = new THREE.Fog(0x0a0a0b, 50, 200)
    sceneRef.current = scene

    // Camera setup
    const camera = new THREE.PerspectiveCamera(
      60,
      mountRef.current.clientWidth / mountRef.current.clientHeight,
      0.1,
      1000
    )
    camera.position.set(0, 30, 40)
    cameraRef.current = camera

    // Renderer setup
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true })
    renderer.setSize(mountRef.current.clientWidth, mountRef.current.clientHeight)
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
    renderer.shadowMap.enabled = true
    renderer.shadowMap.type = THREE.PCFSoftShadowMap
    mountRef.current.appendChild(renderer.domElement)
    rendererRef.current = renderer

    // Controls
    const controls = new OrbitControls(camera, renderer.domElement)
    controls.enableDamping = true
    controls.dampingFactor = 0.05
    controls.minDistance = 10
    controls.maxDistance = 100
    controls.maxPolarAngle = Math.PI / 2.2
    controlsRef.current = controls

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6)
    scene.add(ambientLight)

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8)
    directionalLight.position.set(20, 40, 20)
    directionalLight.castShadow = true
    directionalLight.shadow.camera.left = -50
    directionalLight.shadow.camera.right = 50
    directionalLight.shadow.camera.top = 50
    directionalLight.shadow.camera.bottom = -50
    directionalLight.shadow.mapSize.width = 2048
    directionalLight.shadow.mapSize.height = 2048
    scene.add(directionalLight)

    // Ground plane
    const groundGeometry = new THREE.PlaneGeometry(200, 200)
    const groundMaterial = new THREE.MeshStandardMaterial({
      color: 0x1a1a1a,
      roughness: 0.8,
      metalness: 0.2
    })
    const ground = new THREE.Mesh(groundGeometry, groundMaterial)
    ground.rotation.x = -Math.PI / 2
    ground.receiveShadow = true
    scene.add(ground)

    // Grid helper
    const gridHelper = new THREE.GridHelper(200, 40, 0x333333, 0x222222)
    gridHelper.position.y = 0.01
    scene.add(gridHelper)

    // Create track with heatmap
    createTrackWithHeatmap(scene, processedTrackData)

    // Create car
    const car = createCar()
    scene.add(car)
    carRef.current = car

    // Create ghost car
    const ghostCar = createCar(true)
    scene.add(ghostCar)
    ghostCar.visible = showGhost

    // Animation loop
    const animate = () => {
      animationRef.current = requestAnimationFrame(animate)
      
      if (isPlaying && processedTrackData.length > 0) {
        const elapsed = Date.now() - startTimeRef.current
        const lapDuration = 98000 // 98 seconds (player lap time)
        const progress = (elapsed % lapDuration) / lapDuration
        
        const exactPosition = progress * processedTrackData.length
        const positionIndex = Math.floor(exactPosition)
        const interpolationFactor = exactPosition - positionIndex
        
        const currentPoint = processedTrackData[positionIndex]
        const nextPoint = processedTrackData[(positionIndex + 1) % processedTrackData.length]
        
        if (currentPoint && nextPoint && car) {
          // Smooth interpolation between points
          const interpX = currentPoint.x + (nextPoint.x - currentPoint.x) * interpolationFactor
          const interpY = currentPoint.y + (nextPoint.y - currentPoint.y) * interpolationFactor
          
          // Update car position with smooth interpolation
          car.position.set(interpX, 0.5, interpY)
          
          // Smooth car rotation
          const targetAngle = Math.atan2(
            nextPoint.y - currentPoint.y,
            nextPoint.x - currentPoint.x
          )
          const currentRotation = car.rotation.y
          const angleDiff = targetAngle - currentRotation
          const smoothAngle = currentRotation + angleDiff * 0.15
          car.rotation.y = -smoothAngle + Math.PI / 2
          
          // Interpolate speed for smooth display
          const interpSpeed = currentPoint.speed + (nextPoint.speed - currentPoint.speed) * interpolationFactor
          setSpeed(Math.round(interpSpeed))
          setCarPosition(positionIndex)
          setCurrentSector(currentPoint.sector || 1)
          
          // Ghost car follows optimal racing line (uses real optimal lap time)
          const ghostLapDuration = optimalLapTime * 1000 // Convert to milliseconds
          const ghostProgress = ((elapsed % ghostLapDuration) / ghostLapDuration)
          const ghostExactPos = ghostProgress * processedTrackData.length
          const ghostIndex = Math.floor(ghostExactPos)
          const ghostInterp = ghostExactPos - ghostIndex
          
          const ghostPoint = processedTrackData[ghostIndex]
          const ghostNextPoint = processedTrackData[(ghostIndex + 1) % processedTrackData.length]
          
          if (ghostPoint && ghostNextPoint && ghostCar) {
            // Ghost follows optimal line (slightly offset for visibility)
            const ghostX = ghostPoint.optimalX + (ghostNextPoint.optimalX - ghostPoint.optimalX) * ghostInterp
            const ghostY = ghostPoint.optimalY + (ghostNextPoint.optimalY - ghostPoint.optimalY) * ghostInterp
            
            ghostCar.position.set(ghostX, 0.5, ghostY)
            
            const ghostAngle = Math.atan2(
              ghostNextPoint.optimalY - ghostPoint.optimalY,
              ghostNextPoint.optimalX - ghostPoint.optimalX
            )
            ghostCar.rotation.y = -ghostAngle + Math.PI / 2
            
            // Make ghost semi-transparent to distinguish from player
            if (ghostCar.material) {
              ghostCar.material.opacity = 0.6
              ghostCar.material.transparent = true
            }
          }
          
          if (onRaceUpdate) {
            onRaceUpdate({
              speed: Math.round(interpSpeed),
              progress: progress * 100,
              sector: currentPoint.sector || 1,
              // Telemetry comparison with real optimal data
              playerBraking: currentPoint.braking,
              optimalBraking: optimalTelemetry ? optimalTelemetry.avg_brake : currentPoint.braking * 0.9,
              playerAcceleration: currentPoint.acceleration,
              optimalAcceleration: currentPoint.acceleration * 1.1,
              optimalSpeed: optimalTelemetry ? optimalTelemetry.avg_speed : interpSpeed * 1.05,
              optimalMaxSpeed: optimalTelemetry ? optimalTelemetry.max_speed : 180,
              delta: (lapDuration - ghostLapDuration) / 1000, // Time delta in seconds
              ghostLapTime: optimalLapTime
            })
          }
        }
      }
      
      controls.update()
      renderer.render(scene, camera)
    }
    
    animate()

    // Handle resize
    const handleResize = () => {
      if (!mountRef.current) return
      camera.aspect = mountRef.current.clientWidth / mountRef.current.clientHeight
      camera.updateProjectionMatrix()
      renderer.setSize(mountRef.current.clientWidth, mountRef.current.clientHeight)
    }
    window.addEventListener('resize', handleResize)

    // Cleanup
    return () => {
      window.removeEventListener('resize', handleResize)
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current)
      }
      if (mountRef.current && renderer.domElement) {
        mountRef.current.removeChild(renderer.domElement)
      }
      renderer.dispose()
    }
  }, [processedTrackData, isPlaying, heatmapMode, showGhost])

  // Create track with heatmap visualization
  const createTrackWithHeatmap = (scene, trackData) => {
    if (trackData.length < 2) return

    // Create track surface with heatmap colors
    const trackWidth = 1.5
    
    let lastSector = 0  // Initialize to 0 so first sector marker is created
    
    for (let i = 0; i < trackData.length - 1; i++) {
      const current = trackData[i]
      const next = trackData[i + 1]
      
      // Get heatmap color for this segment
      const color = getHeatmapColor(current)
      
      // Create track segment
      const segmentGeometry = new THREE.BoxGeometry(
        Math.hypot(next.x - current.x, next.y - current.y),
        0.1,
        trackWidth
      )
      
      const segmentMaterial = new THREE.MeshStandardMaterial({
        color: color,
        roughness: 0.7,
        metalness: 0.3,
        emissive: color,
        emissiveIntensity: 0.2
      })
      
      const segment = new THREE.Mesh(segmentGeometry, segmentMaterial)
      
      // Position and rotate segment
      segment.position.set(
        (current.x + next.x) / 2,
        0.05,
        (current.y + next.y) / 2
      )
      
      const angle = Math.atan2(next.y - current.y, next.x - current.x)
      segment.rotation.y = -angle
      
      segment.castShadow = true
      segment.receiveShadow = true
      scene.add(segment)
      
      // Add sector markers when sector changes
      if (current.sector !== lastSector) {
        // Create taller, more visible marker pillar
        const markerGeometry = new THREE.CylinderGeometry(0.4, 0.4, 2, 16)
        const markerMaterial = new THREE.MeshStandardMaterial({
          color: 0xffff00,
          emissive: 0xffff00,
          emissiveIntensity: 0.8,
          transparent: true,
          opacity: 0.9
        })
        const marker = new THREE.Mesh(markerGeometry, markerMaterial)
        marker.position.set(current.x, 1, current.y)
        marker.castShadow = true
        scene.add(marker)
        
        // Add glowing top cap
        const capGeometry = new THREE.CylinderGeometry(0.5, 0.4, 0.2, 16)
        const capMaterial = new THREE.MeshStandardMaterial({
          color: 0xffff00,
          emissive: 0xffff00,
          emissiveIntensity: 1.0
        })
        const cap = new THREE.Mesh(capGeometry, capMaterial)
        cap.position.set(current.x, 2.1, current.y)
        scene.add(cap)
        
        // Add point light for glow effect
        const sectorLight = new THREE.PointLight(0xffff00, 1, 5)
        sectorLight.position.set(current.x, 2, current.y)
        scene.add(sectorLight)
        
        // Add sector number label (using sprite)
        const canvas = document.createElement('canvas')
        canvas.width = 128
        canvas.height = 128
        const ctx = canvas.getContext('2d')
        
        // Draw background circle
        ctx.fillStyle = '#ffff00'
        ctx.beginPath()
        ctx.arc(64, 64, 60, 0, Math.PI * 2)
        ctx.fill()
        
        // Draw sector number
        ctx.fillStyle = '#000000'
        ctx.font = 'bold 80px Arial'
        ctx.textAlign = 'center'
        ctx.textBaseline = 'middle'
        ctx.fillText(`S${current.sector}`, 64, 64)
        
        const texture = new THREE.CanvasTexture(canvas)
        const spriteMaterial = new THREE.SpriteMaterial({ 
          map: texture,
          transparent: true
        })
        const sprite = new THREE.Sprite(spriteMaterial)
        sprite.position.set(current.x, 3, current.y)
        sprite.scale.set(1.5, 1.5, 1)
        scene.add(sprite)
        
        lastSector = current.sector
      }
    }
    
    // Add Start/Finish line at first point
    const startPoint = trackData[0]
    const startLineGeometry = new THREE.BoxGeometry(trackWidth + 0.5, 0.15, 0.5)
    const startLineMaterial = new THREE.MeshStandardMaterial({
      color: 0x00ff00,
      emissive: 0x00ff00,
      emissiveIntensity: 0.6
    })
    const startLine = new THREE.Mesh(startLineGeometry, startLineMaterial)
    startLine.position.set(startPoint.x, 0.1, startPoint.y)
    startLine.castShadow = true
    scene.add(startLine)
    
    // Add optimal racing line visualization (ghost path)
    const optimalLineGeometry = new THREE.BufferGeometry()
    const optimalLinePoints = []
    
    trackData.forEach(point => {
      optimalLinePoints.push(
        new THREE.Vector3(point.optimalX || point.x, 0.2, point.optimalY || point.y)
      )
    })
    // Close the loop
    optimalLinePoints.push(optimalLinePoints[0])
    
    optimalLineGeometry.setFromPoints(optimalLinePoints)
    const optimalLineMaterial = new THREE.LineBasicMaterial({
      color: 0x3b82f6,
      linewidth: 2,
      transparent: true,
      opacity: 0.6
    })
    const optimalLine = new THREE.Line(optimalLineGeometry, optimalLineMaterial)
    scene.add(optimalLine)
    
    // Add braking point markers (red cones)
    trackData.forEach((point, index) => {
      if (point.braking > 60) {
        const coneGeometry = new THREE.ConeGeometry(0.2, 0.6, 8)
        const coneMaterial = new THREE.MeshStandardMaterial({
          color: 0xff0000,
          emissive: 0xff0000,
          emissiveIntensity: 0.4
        })
        const cone = new THREE.Mesh(coneGeometry, coneMaterial)
        cone.position.set(point.x, 0.3, point.y)
        cone.castShadow = true
        scene.add(cone)
      }
    })
    
    // Add track borders
    const borderMaterial = new THREE.MeshStandardMaterial({
      color: 0xffffff,
      roughness: 0.9,
      metalness: 0.1
    })
    
    for (let i = 0; i < trackData.length - 1; i++) {
      const current = trackData[i]
      const next = trackData[i + 1]
      
      const angle = Math.atan2(next.y - current.y, next.x - current.x)
      const perpAngle = angle + Math.PI / 2
      
      // Left border
      const leftBorderGeom = new THREE.CylinderGeometry(0.05, 0.05, 
        Math.hypot(next.x - current.x, next.y - current.y), 8)
      const leftBorder = new THREE.Mesh(leftBorderGeom, borderMaterial)
      leftBorder.position.set(
        (current.x + next.x) / 2 + Math.cos(perpAngle) * (trackWidth / 2 + 0.1),
        0.15,
        (current.y + next.y) / 2 + Math.sin(perpAngle) * (trackWidth / 2 + 0.1)
      )
      leftBorder.rotation.z = Math.PI / 2
      leftBorder.rotation.y = -angle
      scene.add(leftBorder)
      
      // Right border
      const rightBorder = leftBorder.clone()
      rightBorder.position.set(
        (current.x + next.x) / 2 - Math.cos(perpAngle) * (trackWidth / 2 + 0.1),
        0.15,
        (current.y + next.y) / 2 - Math.sin(perpAngle) * (trackWidth / 2 + 0.1)
      )
      scene.add(rightBorder)
    }
  }

  // Create car model
  const createCar = (isGhost = false) => {
    const car = new THREE.Group()
    
    // Car body
    const bodyGeometry = new THREE.BoxGeometry(0.8, 0.4, 1.6)
    const bodyMaterial = new THREE.MeshStandardMaterial({
      color: isGhost ? 0x3b82f6 : 0xc96287,
      roughness: 0.3,
      metalness: 0.7,
      transparent: isGhost,
      opacity: isGhost ? 0.5 : 1
    })
    const body = new THREE.Mesh(bodyGeometry, bodyMaterial)
    body.position.y = 0.2
    body.castShadow = true
    car.add(body)
    
    // Cockpit
    const cockpitGeometry = new THREE.BoxGeometry(0.6, 0.3, 0.8)
    const cockpitMaterial = new THREE.MeshStandardMaterial({
      color: 0x111111,
      roughness: 0.2,
      metalness: 0.8,
      transparent: isGhost,
      opacity: isGhost ? 0.3 : 0.8
    })
    const cockpit = new THREE.Mesh(cockpitGeometry, cockpitMaterial)
    cockpit.position.set(0, 0.5, -0.2)
    cockpit.castShadow = true
    car.add(cockpit)
    
    // Wheels
    const wheelGeometry = new THREE.CylinderGeometry(0.15, 0.15, 0.1, 16)
    const wheelMaterial = new THREE.MeshStandardMaterial({
      color: 0x222222,
      roughness: 0.9,
      transparent: isGhost,
      opacity: isGhost ? 0.5 : 1
    })
    
    const wheelPositions = [
      [-0.4, 0, 0.6],
      [0.4, 0, 0.6],
      [-0.4, 0, -0.6],
      [0.4, 0, -0.6]
    ]
    
    wheelPositions.forEach(pos => {
      const wheel = new THREE.Mesh(wheelGeometry, wheelMaterial)
      wheel.rotation.z = Math.PI / 2
      wheel.position.set(...pos)
      wheel.castShadow = true
      car.add(wheel)
    })
    
    return car
  }

  return (
    <div className="track-3d-container">
      <div className="track-3d-controls">
        <div className="heatmap-selector">
          <button 
            className={heatmapMode === 'speed' ? 'active' : ''}
            onClick={() => setHeatmapMode('speed')}
          >
            🏎️ Speed
          </button>
          <button 
            className={heatmapMode === 'braking' ? 'active' : ''}
            onClick={() => setHeatmapMode('braking')}
          >
            🔴 Braking
          </button>
          <button 
            className={heatmapMode === 'gforce' ? 'active' : ''}
            onClick={() => setHeatmapMode('gforce')}
          >
            ⚡ G-Force
          </button>
        </div>
        <div className="view-options">
          <label>
            <input 
              type="checkbox" 
              checked={showGhost}
              onChange={(e) => setShowGhost(e.target.checked)}
            />
            Show Reference Car
          </label>
        </div>
      </div>
      
      <div className="track-3d-stats">
        <div className="stat-item">
          <span className="stat-label">Speed</span>
          <span className="stat-value">{speed} km/h</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Sector</span>
          <span className="stat-value">S{currentSector}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Position</span>
          <span className="stat-value">{carPosition}/{processedTrackData.length}</span>
        </div>
        {optimalTelemetry && showGhost && (
          <div className="stat-item ghost-stat">
            <span className="stat-label">⚡ Ghost Lap</span>
            <span className="stat-value">{optimalLapTime.toFixed(2)}s</span>
          </div>
        )}
      </div>
      
      <div className="telemetry-comparison">
        <div className="comparison-title">📊 Telemetry Comparison</div>
        <div className="comparison-grid">
          <div className="comparison-item">
            <div className="comparison-label">Braking</div>
            <div className="comparison-bars">
              <div className="bar-container">
                <div className="bar player" style={{width: `${(processedTrackData[carPosition]?.braking || 0)}%`}}>
                  <span className="bar-label">You</span>
                </div>
              </div>
              <div className="bar-container">
                <div className="bar optimal" style={{width: `${(processedTrackData[carPosition]?.braking || 0) * 0.9}%`}}>
                  <span className="bar-label">Optimal</span>
                </div>
              </div>
            </div>
          </div>
          
          <div className="comparison-item">
            <div className="comparison-label">Throttle</div>
            <div className="comparison-bars">
              <div className="bar-container">
                <div className="bar player" style={{width: `${processedTrackData[carPosition]?.throttle || 0}%`}}>
                  <span className="bar-label">You</span>
                </div>
              </div>
              <div className="bar-container">
                <div className="bar optimal" style={{width: `${Math.min((processedTrackData[carPosition]?.throttle || 0) * 1.05, 100)}%`}}>
                  <span className="bar-label">Optimal</span>
                </div>
              </div>
            </div>
          </div>
          
          <div className="comparison-item">
            <div className="comparison-label">G-Force</div>
            <div className="comparison-value">
              <span className="value-player">{(processedTrackData[carPosition]?.gforce || 0).toFixed(2)}G</span>
              <span className="value-separator">vs</span>
              <span className="value-optimal">{((processedTrackData[carPosition]?.gforce || 0) * 1.05).toFixed(2)}G</span>
            </div>
          </div>
        </div>
        <div className="delta-display">
          <span className="delta-label">Time Delta:</span>
          <span className="delta-value">-3.0s</span>
          <span className="delta-hint">behind optimal</span>
        </div>
      </div>
      
      <div ref={mountRef} className="track-3d-canvas" />
      
      <div className="heatmap-legend">
        <div className="legend-header">
          <div className="legend-title">{heatmapMode.toUpperCase()} HEATMAP</div>
          <div className="legend-description">
            {heatmapMode === 'speed' && 'Blue = Slow (corners) • Red = Fast (straights)'}
            {heatmapMode === 'braking' && 'Blue = No braking • Red = Heavy braking'}
            {heatmapMode === 'gforce' && 'Blue = Low G • Red = High G (corners)'}
          </div>
        </div>
        <div className="legend-gradient">
          <span className="legend-label">Low</span>
          <div className="gradient-bar">
            <div className="gradient-marker" style={{left: '0%'}}>
              <span className="marker-label">0</span>
            </div>
            <div className="gradient-marker" style={{left: '25%'}}>
              <span className="marker-label">25%</span>
            </div>
            <div className="gradient-marker" style={{left: '50%'}}>
              <span className="marker-label">50%</span>
            </div>
            <div className="gradient-marker" style={{left: '75%'}}>
              <span className="marker-label">75%</span>
            </div>
            <div className="gradient-marker" style={{left: '100%'}}>
              <span className="marker-label">100%</span>
            </div>
          </div>
          <span className="legend-label">High</span>
        </div>
        <div className="legend-indicators">
          <div className="indicator">
            <div className="indicator-icon" style={{background: '#00ff00'}}>🏁</div>
            <span>Start/Finish</span>
          </div>
          <div className="indicator">
            <div className="indicator-icon" style={{background: '#ffff00'}}>S</div>
            <span>Sector Marker</span>
          </div>
          <div className="indicator">
            <div className="indicator-icon" style={{background: '#c96287'}}>🏎️</div>
            <span>Your Car</span>
          </div>
          <div className="indicator">
            <div className="indicator-icon" style={{background: '#3b82f6', opacity: 0.6}}>👻</div>
            <span>Reference</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Track3DEnhanced
