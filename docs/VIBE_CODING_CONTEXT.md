# RaceIQ - Vibe Coding Context

**Quick Reference for AI-Assisted Development**

---

## 🎯 Project Essence

**What:** AI-powered race engineer assistant for real-time strategy
**Why:** Transform telemetry into actionable race-day decisions
**How:** ML predictions + sector analysis + coaching insights

---

## 💡 Core Philosophy

### Design Principles
1. **Actionable over descriptive** - "Do this" not "you did that"
2. **Predictive over reactive** - Show future, not just past
3. **Production over prototype** - Ready to use today
4. **Impact over features** - Measurable results matter

### Development Approach
- **Validate early** - Test with real race winner data
- **Document thoroughly** - Code + API + presentation
- **Keep it simple** - Linear regression beats complex models
- **Focus on UX** - Engineers need clear, fast insights

---

## 🛠️ Technical Stack

### Core Technologies
```python
# Data Processing
pandas, numpy

# Machine Learning
scikit-learn (LinearRegression)

# API
FastAPI, uvicorn, pydantic

# Visualization
matplotlib, seaborn

# Analysis
scipy, geopy (future)
```

### Architecture Pattern
```
Data Layer → Analytics Engine → API Layer → User Interface
```

---

## 📊 Key Algorithms

### Tire Degradation Predictor
```python
# Core concept: Linear regression on recent laps
X = recent_laps['LAP_NUMBER']
y = recent_laps['delta_to_best']
model = LinearRegression().fit(X, y)

degradation_rate = model.coef_[0]
laps_until_pit = (threshold - current_delta) / degradation_rate
confidence = min(100, data_points * 20)
```

### Racing Line Coach
```python
# Core concept: Compare to personal best
for sector in ['S1', 'S2', 'S3']:
    delta = current_lap[sector] - best_lap[sector]
    if delta > 0.1:  # Significant loss
        generate_coaching(sector, delta)
```

---

## 🎨 Code Style

### Naming Conventions
- Classes: `TireDegradationAnalyzer`, `RacingLineAnalyzer`
- Methods: `predict_pit_window()`, `analyze_lap_degradation()`
- Variables: `vehicle_number`, `current_lap`, `degradation_rate`

### Documentation Style
```python
def predict_pit_window(analysis_df, vehicle_number, current_lap, total_laps):
    """
    Predict optimal pit window based on tire degradation
    
    Args:
        analysis_df: DataFrame with lap analysis data
        vehicle_number: Vehicle to analyze
        current_lap: Current lap number
        total_laps: Total race laps
        
    Returns:
        dict with pit_lap, confidence, laps_remaining, message
    """
```

### Error Handling
```python
if len(vehicle_laps) < 5:
    return {
        'pit_lap': None,
        'confidence': 0,
        'message': 'Insufficient data'
    }
```

---

## 📁 Project Structure

```
src/
├── data_loader.py           # CSV parsing, data cleaning
├── analysis/
│   ├── tire_degradation.py  # ML model for pit prediction
│   └── racing_line.py       # Coaching insights
├── api/
│   └── main.py              # FastAPI endpoints
└── dashboard/
    └── visualize.py         # Chart generation

docs/                        # Context for future development
output/                      # Generated visualizations
demo.py                      # Interactive demonstration
```

---

## 🔧 Common Patterns

### Data Loading
```python
# Handle multiple CSV formats
df = pd.read_csv(file, delimiter=';')  # Official results
df = pd.read_csv(file)  # Telemetry (comma)

# Clean column names
df.columns = df.columns.str.strip()

# Filter invalid data
df = df[df['lap'] != 32768]
```

### API Endpoints
```python
@app.post("/pit-prediction")
async def predict_pit_window(request: PitPredictionRequest):
    prediction = tire_analyzer.predict_pit_window(
        analysis_data,
        request.vehicle_number,
        request.current_lap,
        request.total_laps
    )
    return prediction
```

### Visualization
```python
fig, ax = plt.subplots(figsize=(14, 8))
ax.plot(data['x'], data['y'], 'o-', linewidth=2)
ax.set_xlabel('Label', fontsize=12, fontweight='bold')
plt.savefig(output_file, dpi=300, bbox_inches='tight')
```

---

## 🎯 Validation Approach

### Test with Race Winner
```python
# Vehicle #13 won the race
vehicle_num = 13

# Validate tire prediction
prediction = analyzer.predict_pit_window(analysis, 13, 15, 27)
# Expected: Can finish without pitting
# Actual: Won race without pitting ✅

# Validate coaching
opportunities = analyzer.find_coaching_opportunities(analysis, 13, lap_15)
# Expected: Sector-specific insights
# Actual: 0.753s available across sectors ✅
```

---

## 💬 Communication Style

### For Technical Audience
- Show algorithms and math
- Explain model choices
- Discuss performance metrics
- Reference validation results

### For Business Audience
- Focus on impact (2-5s per race)
- Emphasize cost savings ($500-1000)
- Highlight scalability
- Show ROI potential

### For Judges
- Balance technical depth with clarity
- Demonstrate production readiness
- Validate with real data
- Show immediate practical value

---

## 🚀 Development Workflow

### 1. Understand Data
```bash
python src/data_loader.py
# Check columns, formats, data quality
```

### 2. Build Algorithm
```python
# Start simple (linear regression)
# Validate with known outcomes
# Iterate based on results
```

### 3. Create API
```python
# FastAPI for auto-docs
# Pydantic for validation
# JSON responses
```

### 4. Generate Visualizations
```python
# matplotlib for charts
# 300 DPI for quality
# Professional styling
```

### 5. Document Everything
```markdown
# README for quick start
# Technical docs for depth
# Presentation for pitch
```

---

## 🎬 Demo Script Pattern

```python
print_header("Feature Name")
# Load data
# Run analysis
# Show results
# Explain significance
```

---

## 📊 Key Metrics to Track

### Technical
- API response time: <50ms
- Data processing: <1s
- Prediction confidence: 100% with 5+ laps
- Visualization quality: 300 DPI

### Business
- Time savings: 2-5s per race
- Cost savings: $500-1000 per race
- Development acceleration: 50% faster
- Market applicability: All racing series

---

## 🎯 Success Criteria

### Code Quality
✅ No syntax errors
✅ All tests pass
✅ Clean, documented code
✅ Production-ready

### Functionality
✅ Predictions accurate
✅ API responds correctly
✅ Visualizations generate
✅ Demo runs smoothly

### Documentation
✅ README complete
✅ API documented
✅ Algorithms explained
✅ Presentation ready

---

## 💡 Key Insights

### What Works
- **Simple models** - Linear regression is effective
- **Real validation** - Test with actual race data
- **Clear UX** - Engineers need fast, actionable insights
- **Production mindset** - Build for immediate use

### What to Avoid
- **Over-engineering** - Complex models without validation
- **Analysis paralysis** - Too much data, no action
- **Prototype thinking** - "Demo-ware" vs production code
- **Feature creep** - Focus on core value

---

## 🔮 Future Development

### Phase 2 Priorities
1. Full telemetry integration (GPS, brake, throttle)
2. Fuel consumption model
3. Weather integration
4. Competitor analysis

### Phase 3 Priorities
1. Mobile app for pit crew
2. Live timing integration
3. Neural network models
4. Voice commands

---

## 📚 Reference Commands

```bash
# Quick demo
python demo.py

# Generate visualizations
python src/dashboard/visualize.py

# Start API server
python src/api/main.py

# Test components
python src/data_loader.py
python src/analysis/tire_degradation.py
python src/analysis/racing_line.py
```

---

## 🏁 Remember

**"In racing, milliseconds matter. RaceIQ finds them."**

- Focus on actionable insights
- Validate with real data
- Build for production
- Document thoroughly
- Present confidently

---

**Use this context to maintain the project's vibe and direction in future development sessions.**
