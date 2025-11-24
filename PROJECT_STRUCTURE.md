# RaceIQ - Clean Project Structure

## Root Level (Keep These)

### Essential Files
- `README.md` - Main project documentation
- `requirements.txt` - Python dependencies
- `.gitignore` - Git ignore rules
- `start_raceiq.bat` / `start_raceiq.sh` - Quick start scripts

### Test Files
- `demo.py` - Demo script
- `test_real_strategy.py` - Strategy tests
- `test_working_features.py` - Feature tests
- `test_real_data_integration.py` - Integration tests
- `precache_telemetry.py` - Telemetry caching

### Utility Scripts
- `show_dataset_samples.py` - View dataset samples
- `inspect_*.py` - Data inspection scripts
- `find_channels.py` - Channel finder
- `debug_geometry.py` - Geometry debugger

## Organized Documentation

### `/docs/submission/` - Hackathon Submission
- `DEVPOST_SIMPLE.md` ⭐ - Simple submission (USE THIS)
- `DEVPOST_SUBMISSION_ACCURATE.md` - Detailed accurate version
- `HACKATHON_SUBMISSION_STORY.md` - Full story version
- `ELEVATOR_PITCH.md` - Elevator pitch
- `SUBMISSION_CHECKLIST.md` - Submission checklist
- `PRESENTATION_SCRIPT.md` - Presentation guide
- `HACKATHON_WINNING_STRATEGY.md` - Strategy notes
- `HACKATHON_CATEGORY_COVERAGE.md` - Category coverage

### `/docs/guides/` - User Guides
- `HOW_TO_TEST.md` ⭐ - Testing guide
- `INSTALLATION_GUIDE.md` ⭐ - Installation steps
- `QUICK_START_GUIDE.md` - Quick start
- `QUICK_REFERENCE.md` - Quick reference
- `TESTING_INSTRUCTIONS.md` - Testing instructions
- `VERTEX_AI_QUICK_START.md` - Vertex AI setup
- `VERTEX_AI_INTEGRATION_GUIDE.md` - Vertex AI integration

### `/docs/development/` - Development Docs
- `IMPLEMENTATION_COMPLETE_SUMMARY.txt` - Implementation summary
- `REAL_STRATEGY_IMPLEMENTATION.md` - Strategy implementation
- `PLACEHOLDER_TO_REAL_DATA_SUMMARY.md` - Real data migration
- `REAL_DATA_AUDIT.md` - Data audit
- `PROJECT_SUMMARY.md` - Project summary
- `TECHNICAL_DETAILS.md` - Technical details

### `/docs/archive/` - Historical/Status Files
- All `*_COMPLETE.md` files
- All `*_FIX*.md` files
- All `*_STATUS.md` files
- All `MULTI_TRACK_*.md` files
- All `RAG_DATASET_*.md` files
- All `FINAL_*.md` files

### `/docs/` - Core Documentation
- `README.md` - Docs index
- `INDEX.md` - Documentation index
- `VIBE_CODING_CONTEXT.md` - Context
- `CHAT_HISTORY.md` - Development history

## Source Code Structure

### `/src/` - Backend Python Code
- `__init__.py`
- `data_loader.py` ⭐ - Data loading
- `multi_track_loader.py` ⭐ - Multi-track support
- `track_config.py` ⭐ - Track configuration
- `telemetry_processor.py` ⭐ - Telemetry processing
- `rag_data_generator.py` - RAG dataset generator
- `generate_*.py` - Various generators

### `/src/analysis/` - Analytics Modules
- `race_strategy.py` ⭐ - Race strategy analyzer
- `tire_degradation.py` ⭐ - Tire degradation
- `racing_line.py` ⭐ - Racing line analysis
- `track_geometry.py` ⭐ - Track geometry
- `cross_track_analysis.py` ⭐ - Cross-track comparison

### `/src/api/` - API Server
- `main.py` ⭐ - FastAPI server

### `/src/dashboard/` - Dashboard
- `visualize.py` - Visualization

## Frontend Structure

### `/frontend/` - React Application
- `index.html` - Entry point
- `vite.config.js` - Vite config
- `package.json` - Dependencies
- `README.md` - Frontend docs

### `/frontend/src/` - React Source
- `App.jsx` ⭐ - Main app
- `App.css` ⭐ - Main styles
- `api.js` ⭐ - API client
- `trackLayouts.js` ⭐ - Track data

### `/frontend/src/components/` - React Components
**Essential:**
- `Track3DEnhanced.jsx` ⭐ - 3D visualization
- `RaceStrategy.jsx` ⭐ - Strategy panel
- `TelemetryLive.jsx` ⭐ - Live telemetry
- `CrossTrackComparison.jsx` ⭐ - Cross-track
- `TrackSelector.jsx` ⭐ - Track selector

**Supporting:**
- `TireDegradation.jsx` - Tire analysis
- `PitPrediction.jsx` - Pit predictions
- `CoachingInsights.jsx` - Coaching
- `LapPotential.jsx` - Lap potential
- `RealtimeTips.jsx` - Real-time tips
- `AIEngineer.jsx` - AI chatbot
- `Header.jsx` - Header
- `VehicleSelector.jsx` - Vehicle selector

## Data Structure

### Track Data Folders
- `/barber/` ⭐ - Barber Motorsports Park
- `/COTA/` - Circuit of the Americas
- `/indianapolis/` - Indianapolis Motor Speedway
- `/road-america/` - Road America
- `/sebring/` - Sebring International
- `/Sonoma/` - Sonoma Raceway
- `/virginia-international-raceway/` - VIR

### RAG Dataset
- `/rag_dataset/` - AI knowledge base
  - `race_engineer_enhanced.jsonl` ⭐
  - `README.md`
  - `QUICK_START.md`
  - `DATASET_SUMMARY.md`

### Output
- `/output/` - Generated outputs

## Configuration

### `.kiro/` - Kiro IDE Config
- `/steering/` - Steering rules
  - `product.md` - Product context
  - `structure.md` - Structure context
  - `tech.md` - Technical context

### `.vscode/` - VS Code Config
- Editor settings

### `.venv/` - Python Virtual Environment
- Python packages (don't commit)

## Files to Keep in Root

✅ Keep:
- README.md
- requirements.txt
- .gitignore
- start_raceiq.*
- demo.py
- test_*.py
- precache_telemetry.py
- Barber_Circuit_Map.pdf

❌ Can Archive (already in docs/):
- All other .md files (moved to docs/)
- All .txt status files (moved to docs/)

## Recommended Cleanup Actions

1. **Delete duplicate files** in root that are now in docs/
2. **Keep only essential** .md files in root (README.md)
3. **Archive old status files** you don't need
4. **Clean up test files** you're not using
5. **Remove generated files** in output/ if not needed

## Quick Access

**For Judges/Users:**
- Start here: `README.md`
- Installation: `docs/guides/INSTALLATION_GUIDE.md`
- Testing: `docs/guides/HOW_TO_TEST.md`
- Submission: `docs/submission/DEVPOST_SIMPLE.md`

**For Developers:**
- Architecture: `docs/development/TECHNICAL_DETAILS.md`
- Implementation: `docs/development/REAL_STRATEGY_IMPLEMENTATION.md`
- API: `src/api/main.py`
- Frontend: `frontend/src/App.jsx`
