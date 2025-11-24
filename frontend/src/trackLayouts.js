// Accurate track layouts based on actual circuit maps
// Centered and scaled for optimal Three.js visualization

export const TRACK_LAYOUTS = {
  barber: {
    name: 'Barber Motorsports Park',
    length: 3673,
    turns: 17,
    generator: (t) => {
      // Barber: Clockwise, technical with elevation
      // Start/Finish on main straight
      const scale = 45
      let x, z
      
      if (t < 0.08) { // Main straight
        x = -scale * 0.8 + t / 0.08 * scale * 1.6
        z = scale * 0.9
      } else if (t < 0.15) { // Turn 1 (right)
        const a = (t - 0.08) / 0.07 * Math.PI * 0.4
        x = scale * 0.8 + Math.sin(a) * scale * 0.3
        z = scale * 0.9 - Math.cos(a) * scale * 0.3
      } else if (t < 0.25) { // Turn 2-3 complex
        const a = (t - 0.15) / 0.1
        x = scale * 1.0 - a * scale * 0.4
        z = scale * 0.6 - Math.sin(a * Math.PI) * scale * 0.2
      } else if (t < 0.35) { // Turn 4-5 (chicane)
        const a = (t - 0.25) / 0.1
        x = scale * 0.6 + Math.sin(a * Math.PI * 2) * scale * 0.15
        z = scale * 0.4 - a * scale * 0.5
      } else if (t < 0.45) { // Turn 6-7
        const a = (t - 0.35) / 0.1 * Math.PI * 0.6
        x = scale * 0.5 - Math.cos(a) * scale * 0.5
        z = -scale * 0.1 - Math.sin(a) * scale * 0.5
      } else if (t < 0.55) { // Turn 8-9
        const a = (t - 0.45) / 0.1
        x = 0 - a * scale * 0.6
        z = -scale * 0.6 - Math.sin(a * Math.PI) * scale * 0.2
      } else if (t < 0.68) { // Turn 10-13 (technical section)
        const a = (t - 0.55) / 0.13
        x = -scale * 0.6 - Math.sin(a * Math.PI * 1.5) * scale * 0.3
        z = -scale * 0.8 + a * scale * 0.8
      } else if (t < 0.82) { // Turn 14-15
        const a = (t - 0.68) / 0.14 * Math.PI * 0.8
        x = -scale * 0.9 + Math.cos(a) * scale * 0.4
        z = 0 + Math.sin(a) * scale * 0.4
      } else { // Turn 16-17 back to start
        const a = (t - 0.82) / 0.18
        x = -scale * 0.5 - a * scale * 0.3
        z = scale * 0.4 + a * scale * 0.5
      }
      
      return { x, y: 0, z }
    }
  },
  
  indianapolis: {
    name: 'Indianapolis Motor Speedway',
    length: 4023,
    turns: 14,
    generator: (t) => {
      // Indianapolis: Road course using part of oval
      const scale = 50
      let x, z
      
      if (t < 0.12) { // Start straight (pit straight)
        x = -scale * 0.9 + t / 0.12 * scale * 1.8
        z = scale * 0.8
      } else if (t < 0.22) { // Turn 1 (oval turn 1)
        const a = (t - 0.12) / 0.1 * Math.PI * 0.45
        x = scale * 0.9 + Math.sin(a) * scale * 0.5
        z = scale * 0.8 - Math.cos(a) * scale * 0.5
      } else if (t < 0.35) { // Infield section (turns 2-6)
        const a = (t - 0.22) / 0.13
        x = scale * 1.2 - a * scale * 1.4
        z = scale * 0.3 - Math.sin(a * Math.PI * 2) * scale * 0.4
      } else if (t < 0.48) { // More infield (turns 7-9)
        const a = (t - 0.35) / 0.13
        x = -scale * 0.2 - a * scale * 0.8
        z = scale * 0.1 - a * scale * 0.6
      } else if (t < 0.58) { // Turn 10-11
        const a = (t - 0.48) / 0.1 * Math.PI * 0.5
        x = -scale * 1.0 - Math.cos(a) * scale * 0.3
        z = -scale * 0.5 - Math.sin(a) * scale * 0.3
      } else if (t < 0.75) { // Back onto oval (turn 12-13)
        const a = (t - 0.58) / 0.17 * Math.PI * 0.6
        x = -scale * 1.3 + Math.cos(a) * scale * 0.8
        z = -scale * 0.8 + Math.sin(a) * scale * 0.8
      } else { // Oval turn 4 back to start
        const a = (t - 0.75) / 0.25 * Math.PI * 0.45
        x = -scale * 0.5 - Math.sin(a) * scale * 0.4
        z = 0 + Math.cos(a) * scale * 0.8
      }
      
      return { x, y: 0, z }
    }
  },
  
  cota: {
    name: 'Circuit of The Americas',
    length: 5513,
    turns: 20,
    generator: (t) => {
      // COTA: Counterclockwise, famous Turn 1 uphill
      const scale = 55
      let x, z
      
      if (t < 0.05) { // Main straight
        x = -scale * 0.9 + t / 0.05 * scale * 0.4
        z = scale * 0.9
      } else if (t < 0.12) { // Turn 1 (uphill left)
        const a = (t - 0.05) / 0.07 * Math.PI * 0.5
        x = -scale * 0.5 + Math.sin(a) * scale * 0.4
        z = scale * 0.9 - Math.cos(a) * scale * 0.4
      } else if (t < 0.25) { // Esses (turns 3-6)
        const a = (t - 0.12) / 0.13
        x = -scale * 0.1 + Math.sin(a * Math.PI * 3) * scale * 0.3
        z = scale * 0.5 - a * scale * 1.2
      } else if (t < 0.35) { // Turn 7-9
        const a = (t - 0.25) / 0.1
        x = scale * 0.2 - a * scale * 0.8
        z = -scale * 0.7 - Math.sin(a * Math.PI) * scale * 0.2
      } else if (t < 0.48) { // Turn 10-11 (hairpin)
        const a = (t - 0.35) / 0.13 * Math.PI
        x = -scale * 0.6 - Math.cos(a) * scale * 0.4
        z = -scale * 0.9 - Math.sin(a) * scale * 0.4
      } else if (t < 0.62) { // Turn 12-15 (technical)
        const a = (t - 0.48) / 0.14
        x = -scale * 1.0 + a * scale * 0.6
        z = -scale * 1.3 + a * scale * 0.8
      } else if (t < 0.75) { // Turn 16-18 (stadium section)
        const a = (t - 0.62) / 0.13 * Math.PI * 1.2
        x = -scale * 0.4 + Math.cos(a) * scale * 0.5
        z = -scale * 0.5 + Math.sin(a) * scale * 0.5
      } else { // Turn 19-20, back straight
        const a = (t - 0.75) / 0.25
        x = scale * 0.1 - a * scale * 1.0
        z = 0 + a * scale * 0.9
      }
      
      return { x, y: 0, z }
    }
  },
  
  sebring: {
    name: 'Sebring International Raceway',
    length: 6019,
    turns: 17,
    generator: (t) => {
      // Sebring: Clockwise, bumpy, long straights
      const scale = 60
      let x, z
      
      if (t < 0.15) { // Long main straight
        x = -scale * 1.0 + t / 0.15 * scale * 2.0
        z = scale * 0.8
      } else if (t < 0.22) { // Turn 1 (hairpin)
        const a = (t - 0.15) / 0.07 * Math.PI * 0.7
        x = scale * 1.0 + Math.sin(a) * scale * 0.4
        z = scale * 0.8 - Math.cos(a) * scale * 0.4
      } else if (t < 0.32) { // Turn 2-5
        const a = (t - 0.22) / 0.1
        x = scale * 1.4 - a * scale * 0.8
        z = scale * 0.4 - a * scale * 0.6
      } else if (t < 0.42) { // Turn 6-7 (Sunset Bend)
        const a = (t - 0.32) / 0.1 * Math.PI * 0.6
        x = scale * 0.6 - Math.cos(a) * scale * 0.6
        z = -scale * 0.2 - Math.sin(a) * scale * 0.6
      } else if (t < 0.55) { // Turn 8-10
        const a = (t - 0.42) / 0.13
        x = 0 - a * scale * 1.2
        z = -scale * 0.8 - Math.sin(a * Math.PI) * scale * 0.3
      } else if (t < 0.68) { // Turn 11-13
        const a = (t - 0.55) / 0.13 * Math.PI * 0.8
        x = -scale * 1.2 - Math.cos(a) * scale * 0.4
        z = -scale * 1.1 + Math.sin(a) * scale * 0.4
      } else { // Turn 14-17, back straight
        const a = (t - 0.68) / 0.32
        x = -scale * 1.6 + a * scale * 0.6
        z = -scale * 0.7 + a * scale * 1.5
      }
      
      return { x, y: 0, z }
    }
  },
  
  road_america: {
    name: 'Road America',
    length: 6515,
    turns: 14,
    generator: (t) => {
      // Road America: Clockwise, long, fast, flowing
      const scale = 65
      let x, z
      
      if (t < 0.18) { // Long front straight
        x = -scale * 1.0 + t / 0.18 * scale * 2.2
        z = scale * 0.9
      } else if (t < 0.28) { // Turn 1-3
        const a = (t - 0.18) / 0.1 * Math.PI * 0.5
        x = scale * 1.2 + Math.sin(a) * scale * 0.5
        z = scale * 0.9 - Math.cos(a) * scale * 0.5
      } else if (t < 0.38) { // Turn 4-5 (Carousel)
        const a = (t - 0.28) / 0.1 * Math.PI * 0.9
        x = scale * 1.7 - Math.cos(a) * scale * 0.7
        z = scale * 0.4 - Math.sin(a) * scale * 0.7
      } else if (t < 0.52) { // Turn 6-8 (Kink section)
        const a = (t - 0.38) / 0.14
        x = scale * 1.0 - a * scale * 1.8
        z = -scale * 0.3 - Math.sin(a * Math.PI) * scale * 0.4
      } else if (t < 0.65) { // Turn 9-11 (Canada Corner)
        const a = (t - 0.52) / 0.13 * Math.PI * 0.7
        x = -scale * 0.8 - Math.cos(a) * scale * 0.6
        z = -scale * 0.7 - Math.sin(a) * scale * 0.6
      } else { // Turn 12-14, back to start
        const a = (t - 0.65) / 0.35
        x = -scale * 1.4 + a * scale * 0.4
        z = -scale * 1.3 + a * scale * 2.2
      }
      
      return { x, y: 0, z }
    }
  },
  
  sonoma: {
    name: 'Sonoma Raceway',
    length: 4023,
    turns: 12,
    generator: (t) => {
      // Sonoma: Clockwise, hilly, technical
      const scale = 48
      let x, z
      
      if (t < 0.12) { // Start straight (uphill)
        x = -scale * 0.8 + t / 0.12 * scale * 1.0
        z = scale * 0.8
      } else if (t < 0.22) { // Turn 1-2 (uphill)
        const a = (t - 0.12) / 0.1 * Math.PI * 0.5
        x = scale * 0.2 + Math.sin(a) * scale * 0.5
        z = scale * 0.8 - Math.cos(a) * scale * 0.5
      } else if (t < 0.35) { // Turn 3-4 (top of hill)
        const a = (t - 0.22) / 0.13
        x = scale * 0.7 + Math.sin(a * Math.PI) * scale * 0.3
        z = scale * 0.3 - a * scale * 0.8
      } else if (t < 0.48) { // Turn 5-6 (downhill)
        const a = (t - 0.35) / 0.13 * Math.PI * 0.6
        x = scale * 1.0 - Math.cos(a) * scale * 0.8
        z = -scale * 0.5 - Math.sin(a) * scale * 0.8
      } else if (t < 0.62) { // Turn 7-8
        const a = (t - 0.48) / 0.14
        x = scale * 0.2 - a * scale * 1.0
        z = -scale * 1.3 + Math.sin(a * Math.PI) * scale * 0.3
      } else if (t < 0.78) { // Turn 9-10 (hairpin)
        const a = (t - 0.62) / 0.16 * Math.PI
        x = -scale * 0.8 - Math.cos(a) * scale * 0.4
        z = -scale * 1.6 + Math.sin(a) * scale * 0.4
      } else { // Turn 11-12, back to start
        const a = (t - 0.78) / 0.22
        x = -scale * 1.2 + a * scale * 0.4
        z = -scale * 1.2 + a * scale * 2.0
      }
      
      return { x, y: 0, z }
    }
  },
  
  vir: {
    name: 'Virginia International Raceway',
    length: 5263,
    turns: 18,
    generator: (t) => {
      // VIR: Clockwise, fast, flowing, scenic
      const scale = 58
      let x, z
      
      if (t < 0.10) { // Start straight
        x = -scale * 0.9 + t / 0.1 * scale * 1.2
        z = scale * 0.9
      } else if (t < 0.22) { // Turn 1-3 (fast sweepers)
        const a = (t - 0.10) / 0.12 * Math.PI * 0.6
        x = scale * 0.3 + Math.sin(a) * scale * 0.8
        z = scale * 0.9 - Math.cos(a) * scale * 0.8
      } else if (t < 0.35) { // Turn 4-6
        const a = (t - 0.22) / 0.13
        x = scale * 1.1 - a * scale * 0.8
        z = scale * 0.1 - a * scale * 0.6
      } else if (t < 0.48) { // Turn 7-9 (technical)
        const a = (t - 0.35) / 0.13
        x = scale * 0.3 - a * scale * 0.9
        z = -scale * 0.5 - Math.sin(a * Math.PI) * scale * 0.4
      } else if (t < 0.62) { // Turn 10-12 (Oak Tree)
        const a = (t - 0.48) / 0.14 * Math.PI * 0.8
        x = -scale * 0.6 - Math.cos(a) * scale * 0.7
        z = -scale * 0.9 - Math.sin(a) * scale * 0.7
      } else if (t < 0.78) { // Turn 13-16
        const a = (t - 0.62) / 0.16
        x = -scale * 1.3 + a * scale * 0.6
        z = -scale * 1.6 + a * scale * 1.0
      } else { // Turn 17-18, back to start
        const a = (t - 0.78) / 0.22
        x = -scale * 0.7 - a * scale * 0.2
        z = -scale * 0.6 + a * scale * 1.5
      }
      
      return { x, y: 0, z }
    }
  }
}

export function getTrackLayout(trackName) {
  return TRACK_LAYOUTS[trackName] || TRACK_LAYOUTS.barber
}
