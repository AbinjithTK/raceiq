import React, { useRef, useMemo, useEffect, useState } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls, Line, Text, PerspectiveCamera } from '@react-three/drei'
import * as THREE from 'three'

// Determine sector from progress (simplified)
function getSectorFromProgress(progress) {
  if (progress < 0.33) return 1
  if (progress < 0.66) return 2
  return 3
}

function Car({ position, rotation, vehicleNumber, speed }) {
  const carRef = useRef()

  useFrame(() => {
    if (carRef.current) {
      // Smooth interpolation could be added here
      carRef.current.position.copy(position)
      carRef.current.rotation.y = rotation
    }
  })

  return (
    <group ref={carRef}>
      {/* Car body */}
      <mesh castShadow position={[0, 0.5, 0]}>
        <boxGeometry args={[3, 1, 5]} />
        <meshStandardMaterial color="#3498db" metalness={0.8} roughness={0.2} />
      </mesh>

      {/* Car number */}
      <Text
        position={[0, 1.5, 0]}
        fontSize={2}
        color="white"
        anchorX="center"
        anchorY="middle"
        rotation={[-Math.PI / 2, 0, 0]}
      >
        #{vehicleNumber}
      </Text>

      {/* Speed indicator */}
      <Text
        position={[0, 1.5, -6]}
        fontSize={1.5}
        color="#2ecc71"
        anchorX="center"
        anchorY="middle"
        rotation={[-Math.PI / 2, 0, 0]}
      >
        {speed} km/h
      </Text>

      {/* Direction indicator */}
      <mesh position={[0, 1.2, 3]} rotation={[0, 0, 0]}>
        <coneGeometry args={[1, 2, 3]} />
        <meshStandardMaterial color="#ff3b30" emissive="#ff3b30" emissiveIntensity={0.5} />
      </mesh>

      {/* Glow effect */}
      <pointLight position={[0, 5, 0]} intensity={3} distance={15} color="#3498db" />
    </group>
  )
}

function Track({ trackPoints, carProgress, onSectorChange }) {
  // Update sector
  useEffect(() => {
    const sector = getSectorFromProgress(carProgress)
    onSectorChange(sector)
  }, [carProgress, onSectorChange])

  if (!trackPoints || trackPoints.length === 0) return null

  // Convert simple objects to Vector3 if needed
  const points = useMemo(() => {
    return trackPoints.map(p => new THREE.Vector3(p.x, p.y, p.z))
  }, [trackPoints])

  return (
    <>
      {/* Main Track Line */}
      <Line
        points={points}
        color="#ffffff"
        lineWidth={3}
        transparent
        opacity={0.8}
      />

      {/* Track Surface (Wider line underneath) */}
      <Line
        points={points}
        color="#333333"
        lineWidth={12}
        transparent
        opacity={0.6}
        position={[0, -0.1, 0]}
      />

      {/* Start/Finish line */}
      {points.length > 0 && (
        <>
          <mesh position={[points[0].x, 0.2, points[0].z]} rotation={[-Math.PI / 2, 0, 0]}>
            <planeGeometry args={[15, 3]} />
            <meshStandardMaterial color="white" transparent opacity={0.9} />
          </mesh>

          <Text
            position={[points[0].x, 1, points[0].z - 12]}
            fontSize={3}
            color="white"
            anchorX="center"
            anchorY="middle"
            rotation={[-Math.PI / 2, 0, 0]}
          >
            START/FINISH
          </Text>
        </>
      )}
    </>
  )
}

function Scene({ carProgress, vehicleNumber, speed, onSectorChange, trackName }) {
  const [trackPoints, setTrackPoints] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchGeometry() {
      setLoading(true)
      try {
        const response = await fetch(`/api/tracks/${trackName}/geometry`)
        if (response.ok) {
          const data = await response.json()
          setTrackPoints(data.points)
        } else {
          console.error("Failed to load track geometry")
        }
      } catch (e) {
        console.error("Error fetching geometry:", e)
      } finally {
        setLoading(false)
      }
    }
    fetchGeometry()
  }, [trackName])

  const carPosition = useMemo(() => {
    if (!trackPoints || trackPoints.length === 0) return new THREE.Vector3(0, 0, 0)
    const index = Math.floor(carProgress * (trackPoints.length - 1))
    const p = trackPoints[index] || trackPoints[0]
    return new THREE.Vector3(p.x, p.y, p.z)
  }, [carProgress, trackPoints])

  const carRotation = useMemo(() => {
    if (!trackPoints || trackPoints.length === 0) return 0
    const index = Math.floor(carProgress * (trackPoints.length - 1))
    const nextIndex = Math.min(index + 1, trackPoints.length - 1)
    const current = trackPoints[index]
    const next = trackPoints[nextIndex]

    if (current && next) {
      return Math.atan2(next.x - current.x, next.z - current.z)
    }
    return 0
  }, [carProgress, trackPoints])

  return (
    <>
      <PerspectiveCamera makeDefault position={[0, 200, 0]} fov={45} rotation={[-Math.PI / 2, 0, 0]} />
      <OrbitControls
        enablePan={true}
        enableZoom={true}
        enableRotate={true}
        minDistance={50}
        maxDistance={500}
        target={[0, 0, 0]}
      />

      <ambientLight intensity={0.8} />
      <directionalLight position={[50, 100, 50]} intensity={1} castShadow />

      {/* Ground */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -2, 0]} receiveShadow>
        <planeGeometry args={[1000, 1000]} />
        <meshStandardMaterial color="#0a0a0f" />
      </mesh>

      {/* Grid helper */}
      <gridHelper args={[1000, 50, '#2c3e50', '#1a1a2e']} position={[0, -1.9, 0]} />

      {loading ? (
        <Text position={[0, 10, 0]} fontSize={5} color="white">
          Loading Track Geometry...
        </Text>
      ) : (
        <>
          <Track
            trackPoints={trackPoints}
            carProgress={carProgress}
            onSectorChange={onSectorChange}
          />

          <Car
            position={carPosition}
            rotation={carRotation}
            vehicleNumber={vehicleNumber}
            speed={speed}
          />
        </>
      )}
    </>
  )
}

export default function Track3D({ carProgress, vehicleNumber, speed, onSectorChange, trackName = 'barber' }) {
  return (
    <div style={{ width: '100%', height: '600px', borderRadius: '12px', overflow: 'hidden', background: '#0a0a0f' }}>
      <Canvas key={trackName} shadows>
        <Scene
          carProgress={carProgress}
          vehicleNumber={vehicleNumber}
          speed={speed}
          onSectorChange={onSectorChange}
          trackName={trackName}
        />
      </Canvas>
    </div>
  )
}
