# RaceIQ Demo Script (Under 3 Minutes)

## Setup
- **Total Time**: 2:45
- **Format**: Screen recording with voiceover
- **Pace**: Quick, energetic, focused on value

---

## Script

### Opening (0:00 - 0:15)
**[Show RaceIQ dashboard loading]**

> "Meet RaceIQ - your AI-powered race engineer that turns raw telemetry into winning strategies. Let's see it in action with real Toyota GR Cup data from Barber Motorsports Park."

---

### Section 1: Live Telemetry (0:15 - 0:45)
**[Navigate to Track Map view, show live telemetry]**

> "Here's live telemetry visualization. Watch as we track speed, braking pressure, and G-forces around every corner."

**[Highlight 3D track view with car position]**

> "The 3D track map shows exactly where you are, with real-time coaching tips appearing at critical points - brake earlier here, carry more speed through turn 5."

**[Show real-time tips appearing]**

---

### Section 2: AI Coaching Insights (0:45 - 1:20)
**[Switch to Coaching Insights panel]**

> "The AI analyzes your driving against the fastest laps in the dataset. It identifies exactly where you're losing time."

**[Show sector comparison]**

> "Sector 2 - you're losing 0.8 seconds. The AI suggests: 'Trail brake deeper into turn 7, maintain higher minimum speed.'"

**[Show lap potential meter]**

> "Your lap potential shows you're capable of a 1:42.3 - that's 1.2 seconds faster than your current best."

---

### Section 3: Race Strategy (1:20 - 1:55)
**[Navigate to Race Strategy view]**

> "Now for race strategy. The system predicts tire degradation based on your driving style and track conditions."

**[Show tire degradation graph]**

> "Your fronts will drop off after lap 18. The AI recommends pitting on lap 19 during the yellow flag window."

**[Show pit stop prediction]**

> "Pit prediction accounts for traffic, fuel load, and tire wear - giving you the optimal strategy to gain positions."

---

### Section 4: Cross-Track Analysis (1:55 - 2:25)
**[Switch to Cross-Track Comparison]**

> "Here's where it gets powerful. Compare your performance across multiple tracks."

**[Show Barber, Sebring, Road America comparison]**

> "You're strong in high-speed corners but losing time in technical sections. The AI identifies this pattern across all circuits and suggests specific drills to improve."

**[Highlight pattern recognition]**

---

### Closing (2:25 - 2:45)
**[Return to dashboard overview]**

> "RaceIQ combines real telemetry, AI analysis, and predictive strategy - all in one platform. From club racers to professional teams, get the insights you need to win."

**[Show key features list on screen]**
- ✓ Real-time telemetry & coaching
- ✓ AI-powered lap analysis
- ✓ Predictive race strategy
- ✓ Multi-track performance insights

> "Ready to race smarter? Visit RaceIQ dot AI to get started."

**[Fade to logo and URL]**

---

## Visual Notes

### Key Screens to Capture
1. **Track Map** - 3D visualization with live car position
2. **Telemetry Live** - Speed/brake/throttle graphs
3. **Coaching Insights** - Sector comparison with AI tips
4. **Lap Potential** - Visual meter showing improvement opportunity
5. **Tire Degradation** - Graph with prediction curve
6. **Pit Strategy** - Timeline with optimal pit window
7. **Cross-Track Comparison** - Multi-circuit heatmap

### Transitions
- Quick cuts (0.5s max between sections)
- Highlight important data with subtle zoom or glow
- Use cursor movements to guide viewer attention

### Audio
- Upbeat background music (low volume)
- Clear, confident voiceover
- Sound effects for key moments (data loading, insights appearing)

---

## Technical Setup

### Before Recording
```bash
# Start backend
python src/api/main.py

# Start frontend (separate terminal)
cd frontend
npm run dev
```

### Demo Data
- Use **Barber R1** data (cleanest dataset)
- Pre-load vehicle **GR86-004-78** (consistent performer)
- Cache telemetry for smooth playback

### Browser Setup
- Full screen mode (F11)
- Hide bookmarks bar
- Clear console
- Zoom to 100%

---

## Backup Script (If Running Long)

### Cuts to Make
1. Reduce opening to 10 seconds
2. Combine Sections 1 & 2 (telemetry + coaching in 45s)
3. Shorten cross-track to 20 seconds
4. Tighten closing to 15 seconds

**New Total**: 2:30

---

## Post-Production Checklist

- [ ] Add text overlays for key metrics
- [ ] Highlight cursor for important clicks
- [ ] Add subtle zoom on data insights
- [ ] Include captions for accessibility
- [ ] Export at 1080p 60fps
- [ ] Add end card with CTA (5 seconds)
