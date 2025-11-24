"""
RaceIQ API - Real-time race strategy assistant
FastAPI backend for serving race analytics
Multi-track support for all 7 Toyota GR Cup circuits
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List, Dict
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.data_loader import RaceDataLoader
from src.analysis.tire_degradation import TireDegradationAnalyzer
from src.analysis.racing_line import RacingLineAnalyzer
from src.analysis.race_strategy import RaceStrategyAnalyzer
from src.multi_track_loader import MultiTrackLoader
from src.track_config import list_available_tracks, get_track_info, get_all_tracks_summary
import json
import re

app = FastAPI(
    title="RaceIQ API", 
    version="2.0.0",
    description="AI Race Engineer for Toyota GR Cup - Multi-Track Analysis"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize data and analyzers
# Use absolute path to project root
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
barber_path = os.path.join(project_root, 'barber')
loader = RaceDataLoader(data_dir=barber_path)
multi_loader = MultiTrackLoader(base_path=project_root)
tire_analyzer = TireDegradationAnalyzer()
line_analyzer = RacingLineAnalyzer()
strategy_analyzer = RaceStrategyAnalyzer()

# Load data on startup
race_results = None
lap_times = None
analysis_data = None
rag_dataset = []

@app.on_event("startup")
async def startup_event():
    global race_results, lap_times, analysis_data, rag_dataset
    print("🏁 Loading race data...")
    try:
        race_results = loader.load_race_results(race_num=1)
        lap_times = loader.load_lap_times(race_num=1)
        analysis_data = loader.load_analysis_endurance(race_num=1)
        print("✅ Data loaded successfully!")
    except Exception as e:
        print(f"⚠️  Warning: Could not load data: {e}")
        print("API will run with limited functionality")
    
    # Load RAG dataset
    print("🤖 Loading AI knowledge base...")
    try:
        rag_path = os.path.join(os.path.dirname(__file__), '../../rag_dataset/race_engineer_enhanced.jsonl')
        with open(rag_path, 'r', encoding='utf-8') as f:
            rag_dataset = [json.loads(line) for line in f]
        print(f"✅ Loaded {len(rag_dataset)} knowledge entries!")
    except Exception as e:
        print(f"⚠️  Warning: Could not load RAG dataset: {e}")


class PitPredictionRequest(BaseModel):
    vehicle_number: int
    current_lap: int
    total_laps: int = 27


class CoachingRequest(BaseModel):
    vehicle_number: int
    lap_number: int


class AIQueryRequest(BaseModel):
    query: str
    context: Optional[Dict] = None


@app.get("/")
async def root():
    return {
        "message": "RaceIQ API - AI-Powered Race Engineer Assistant",
        "version": "2.0.0",
        "endpoints": {
            "vehicles": "/vehicles",
            "pit_prediction": "/pit-prediction",
            "tire_degradation": "/tire-degradation/{vehicle_number}",
            "coaching": "/coaching",
            "lap_potential": "/lap-potential/{vehicle_number}",
            "fuel_strategy": "/strategy/fuel/{vehicle_number}",
            "race_pace": "/strategy/pace/{vehicle_number}",
            "optimal_pit": "/strategy/pit-optimal/{vehicle_number}",
            "sector_performance": "/strategy/sectors/{vehicle_number}",
            "finish_prediction": "/strategy/finish-prediction/{vehicle_number}"
        }
    }


@app.get("/vehicles")
async def get_vehicles():
    """Get list of all vehicles in the race"""
    if race_results is None:
        raise HTTPException(status_code=503, detail="Data not loaded")
    
    vehicles = []
    for _, row in race_results.iterrows():
        vehicles.append({
            "number": int(row['NUMBER']),
            "position": int(row['POSITION']),
            "laps": int(row['LAPS']),
            "status": row['STATUS'],
            "fastest_lap": row['FL_TIME'] if 'FL_TIME' in row else None
        })
    
    return {"vehicles": vehicles}


@app.post("/pit-prediction")
async def predict_pit_window(request: PitPredictionRequest):
    """Predict optimal pit window based on tire degradation"""
    if analysis_data is None:
        raise HTTPException(status_code=503, detail="Data not loaded")
    
    prediction = tire_analyzer.predict_pit_window(
        analysis_data,
        request.vehicle_number,
        request.current_lap,
        request.total_laps
    )
    
    return prediction


@app.get("/tire-degradation/{vehicle_number}")
async def get_tire_degradation(vehicle_number: int):
    """Get detailed tire degradation analysis"""
    if analysis_data is None:
        raise HTTPException(status_code=503, detail="Data not loaded")
    
    degradation = tire_analyzer.analyze_lap_degradation(analysis_data, vehicle_number)
    
    if len(degradation) == 0:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    # Convert to JSON-serializable format
    result = {
        "vehicle_number": vehicle_number,
        "total_laps": len(degradation),
        "best_lap_time": float(degradation['lap_time_seconds'].min()),
        "worst_lap_time": float(degradation['lap_time_seconds'].max()),
        "avg_degradation": float(degradation['delta_to_best'].mean()),
        "laps": degradation[['LAP_NUMBER', 'lap_time_seconds', 'delta_to_best', 'estimated_tire_life']].to_dict('records')
    }
    
    return result


@app.post("/coaching")
async def get_coaching_insights(request: CoachingRequest):
    """Get coaching insights for a specific lap"""
    if analysis_data is None:
        raise HTTPException(status_code=503, detail="Data not loaded")
    
    vehicle_laps = analysis_data[analysis_data['NUMBER'] == request.vehicle_number]
    
    if len(vehicle_laps) == 0:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    lap_data = vehicle_laps[vehicle_laps['LAP_NUMBER'] == request.lap_number]
    
    if len(lap_data) == 0:
        raise HTTPException(status_code=404, detail="Lap not found")
    
    opportunities = line_analyzer.find_coaching_opportunities(
        analysis_data,
        request.vehicle_number,
        lap_data.iloc[0]
    )
    
    return {"opportunities": opportunities}


@app.get("/lap-potential/{vehicle_number}")
async def get_lap_potential(vehicle_number: int):
    """Calculate theoretical best lap time"""
    if analysis_data is None:
        raise HTTPException(status_code=503, detail="Data not loaded")
    
    potential = line_analyzer.calculate_potential_lap_time(analysis_data, vehicle_number)
    
    if not potential:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    return potential


@app.get("/sector-degradation/{vehicle_number}")
async def get_sector_degradation(vehicle_number: int):
    """Get sector-by-sector degradation analysis"""
    if analysis_data is None:
        raise HTTPException(status_code=503, detail="Data not loaded")
    
    degradation = tire_analyzer.analyze_sector_degradation(analysis_data, vehicle_number)
    
    if not degradation:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    return {"sector_degradation": degradation}


# ============================================================================
# REAL RACE STRATEGY ENDPOINTS
# ============================================================================

@app.get("/strategy/fuel/{vehicle_number}")
async def get_fuel_strategy(
    vehicle_number: int,
    current_lap: int,
    total_laps: int = 27,
    current_fuel: Optional[float] = None
):
    """Calculate fuel strategy using real race data"""
    if analysis_data is None:
        raise HTTPException(status_code=503, detail="Data not loaded")
    
    strategy = strategy_analyzer.calculate_fuel_strategy(
        analysis_data,
        vehicle_number,
        current_lap,
        total_laps,
        current_fuel
    )
    
    if 'error' in strategy:
        raise HTTPException(status_code=404, detail=strategy['error'])
    
    return strategy


@app.get("/strategy/pace/{vehicle_number}")
async def get_race_pace(vehicle_number: int, current_lap: int):
    """Analyze race pace using real lap time data"""
    if analysis_data is None:
        raise HTTPException(status_code=503, detail="Data not loaded")
    
    pace = strategy_analyzer.analyze_race_pace(
        analysis_data,
        vehicle_number,
        current_lap
    )
    
    if 'error' in pace:
        raise HTTPException(status_code=404, detail=pace['error'])
    
    return pace


@app.get("/strategy/pit-optimal/{vehicle_number}")
async def get_optimal_pit_strategy(
    vehicle_number: int,
    current_lap: int,
    total_laps: int = 27
):
    """Calculate optimal pit strategy considering tires and fuel"""
    if analysis_data is None:
        raise HTTPException(status_code=503, detail="Data not loaded")
    
    strategy = strategy_analyzer.calculate_optimal_pit_strategy(
        analysis_data,
        vehicle_number,
        current_lap,
        total_laps
    )
    
    if 'error' in strategy:
        raise HTTPException(status_code=404, detail=strategy['error'])
    
    return strategy


@app.get("/strategy/sectors/{vehicle_number}")
async def get_sector_performance(vehicle_number: int, current_lap: int):
    """Analyze sector performance using real timing data"""
    if analysis_data is None:
        raise HTTPException(status_code=503, detail="Data not loaded")
    
    sectors = strategy_analyzer.analyze_sector_performance(
        analysis_data,
        vehicle_number,
        current_lap
    )
    
    if 'error' in sectors:
        raise HTTPException(status_code=404, detail=sectors['error'])
    
    return sectors


@app.get("/strategy/finish-prediction/{vehicle_number}")
async def predict_finish(
    vehicle_number: int,
    current_lap: int,
    total_laps: int = 27
):
    """Predict race finish time based on current pace"""
    if analysis_data is None:
        raise HTTPException(status_code=503, detail="Data not loaded")
    
    prediction = strategy_analyzer.predict_finish_time(
        analysis_data,
        vehicle_number,
        current_lap,
        total_laps
    )
    
    if 'error' in prediction:
        raise HTTPException(status_code=404, detail=prediction['error'])
    
    return prediction


# ============================================================================
# AI RACE ENGINEER CHATBOT
# ============================================================================

def find_relevant_knowledge(query: str, context: Optional[Dict] = None, top_k: int = 3):
    """Find most relevant knowledge from RAG dataset using simple keyword matching"""
    query_lower = query.lower()
    
    # Extract keywords
    keywords = re.findall(r'\b\w+\b', query_lower)
    
    # Score each entry
    scored_entries = []
    for entry in rag_dataset:
        score = 0
        question_lower = entry['question'].lower()
        answer_lower = entry['answer'].lower()
        
        # Keyword matching
        for keyword in keywords:
            if keyword in question_lower:
                score += 3
            if keyword in answer_lower:
                score += 1
        
        # Context matching
        if context:
            if 'track' in context and entry['context'].get('track') == context['track']:
                score += 5
            if 'category' in context and entry['context'].get('category') == context.get('category'):
                score += 3
        
        if score > 0:
            scored_entries.append((score, entry))
    
    # Sort by score and return top_k
    scored_entries.sort(reverse=True, key=lambda x: x[0])
    return [entry for score, entry in scored_entries[:top_k]]


def generate_ai_response(query: str, relevant_knowledge: List[Dict], context: Optional[Dict] = None):
    """Generate AI response based on query and relevant knowledge"""
    query_lower = query.lower()
    
    # If we have relevant knowledge, use it
    if relevant_knowledge:
        # Combine answers from top matches
        answers = [entry['answer'] for entry in relevant_knowledge[:2]]
        
        # Create contextual response
        if 'tire' in query_lower or 'wear' in query_lower:
            return {
                "text": f"{answers[0]} Monitor your tire temperatures and adjust driving style accordingly.",
                "type": "warning",
                "confidence": 0.85,
                "sources": [entry['id'] for entry in relevant_knowledge[:2]]
            }
        elif 'strategy' in query_lower or 'pit' in query_lower:
            return {
                "text": answers[0],
                "type": "info",
                "confidence": 0.90,
                "sources": [entry['id'] for entry in relevant_knowledge[:2]]
            }
        elif 'track' in query_lower:
            return {
                "text": answers[0],
                "type": "info",
                "confidence": 0.95,
                "sources": [entry['id'] for entry in relevant_knowledge[:2]]
            }
        elif 'time' in query_lower or 'lap' in query_lower or 'fast' in query_lower:
            return {
                "text": answers[0],
                "type": "success",
                "confidence": 0.88,
                "sources": [entry['id'] for entry in relevant_knowledge[:2]]
            }
        else:
            return {
                "text": answers[0],
                "type": "neutral",
                "confidence": 0.75,
                "sources": [entry['id'] for entry in relevant_knowledge[:2]]
            }
    
    # Fallback responses for common queries
    if 'losing time' in query_lower or 'slow' in query_lower:
        return {
            "text": "Based on telemetry analysis, focus on your braking points and throttle application. The data shows opportunities in corner exit speed. I recommend reviewing your sector times to identify specific areas for improvement.",
            "type": "warning",
            "confidence": 0.70,
            "sources": []
        }
    elif 'gap' in query_lower or 'position' in query_lower:
        return {
            "text": "Current gap analysis shows you're competitive in Sector 2. Maintain your pace and focus on consistency. Track position is crucial at this circuit.",
            "type": "success",
            "confidence": 0.65,
            "sources": []
        }
    elif 'fuel' in query_lower:
        return {
            "text": "Fuel consumption is nominal. You have sufficient fuel to complete the race distance. No concerns at this time.",
            "type": "info",
            "confidence": 0.80,
            "sources": []
        }
    
    return {
        "text": "I'm analyzing that data. Could you be more specific? I can help with strategy, tire management, lap times, track information, and performance analysis.",
        "type": "neutral",
        "confidence": 0.50,
        "sources": []
    }


@app.post("/ai/query")
async def ai_race_engineer(request: AIQueryRequest):
    """AI Race Engineer - Answer questions using RAG dataset"""
    try:
        # Find relevant knowledge
        relevant = find_relevant_knowledge(request.query, request.context, top_k=5)
        
        # Generate response
        response = generate_ai_response(request.query, relevant, request.context)
        
        return {
            "query": request.query,
            "response": response['text'],
            "type": response['type'],
            "confidence": response['confidence'],
            "sources": response['sources'],
            "relevant_entries": len(relevant)
        }
    except Exception as e:
        return {
            "query": request.query,
            "response": f"I encountered an issue processing your question. Please try rephrasing it.",
            "type": "error",
            "confidence": 0.0,
            "sources": [],
            "error": str(e)
        }


# ============================================================================
# MULTI-TRACK ENDPOINTS
# ============================================================================

@app.get("/tracks")
async def get_tracks():
    """Get list of all available tracks"""
    return {
        "tracks": list_available_tracks(),
        "summary": get_all_tracks_summary()
    }

@app.get("/tracks/{track_name}")
async def get_track_info_endpoint(track_name: str):
    """Get detailed information about a specific track"""
    try:
        track = get_track_info(track_name)
        return {
            "name": track.name,
            "short_name": track.short_name,
            "length_km": track.length_km,
            "turns": track.turns,
            "direction": track.direction,
            "map_image": track.map_image,
            "races_available": len(track.race_folders)
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/tracks/{track_name}/race/{race_num}/results")
async def get_track_results(track_name: str, race_num: int):
    """Get race results for a specific track and race"""
    try:
        loader = MultiTrackLoader()
        results = loader.load_results(track_name, race_num)
        
        return {
            "track": track_name,
            "race": race_num,
            "total_entries": len(results),
            "results": results.to_dict(orient='records')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tracks/{track_name}/race/{race_num}/lap-times")
async def get_track_lap_times(
    track_name: str, 
    race_num: int,
    vehicle_id: Optional[str] = None
):
    """Get lap times for a specific track and race"""
    try:
        loader = MultiTrackLoader()
        lap_times = loader.load_lap_times(track_name, race_num)
        
        if vehicle_id:
            lap_times = lap_times[lap_times['vehicle_id'].str.contains(vehicle_id, na=False)]
        
        return {
            "track": track_name,
            "race": race_num,
            "total_laps": len(lap_times),
            "lap_times": lap_times.to_dict(orient='records')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tracks/{track_name}/race/{race_num}/analysis")
async def get_track_analysis(track_name: str, race_num: int):
    """Get sector analysis for a specific track and race"""
    try:
        loader = MultiTrackLoader()
        analysis = loader.load_analysis(track_name, race_num)
        
        return {
            "track": track_name,
            "race": race_num,
            "total_records": len(analysis),
            "analysis": analysis.to_dict(orient='records')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/vehicle/{vehicle_id}/cross-track")
async def compare_vehicle_across_tracks(vehicle_id: str, race_num: int = 1):
    """Compare a vehicle's performance across all tracks"""
    try:
        loader = MultiTrackLoader()
        comparison = loader.compare_vehicle_across_tracks(vehicle_id, race_num)
        
        if comparison.empty:
            raise HTTPException(
                status_code=404, 
                detail=f"No data found for vehicle {vehicle_id}"
            )
        
        return {
            "vehicle_id": vehicle_id,
            "race_num": race_num,
            "tracks_competed": len(comparison),
            "comparison": comparison.to_dict(orient='records')
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/championship/standings")
async def get_championship_standings():
    """Get championship standings across all tracks"""
    try:
        loader = MultiTrackLoader()
        
        # Load results from all tracks
        all_results = []
        for track in list_available_tracks():
            try:
                for race_num in [1, 2]:
                    results = loader.load_results(track, race_num)
                    all_results.append(results)
            except:
                continue
        
        if not all_results:
            raise HTTPException(status_code=404, detail="No results data available")
        
        import pandas as pd
        combined = pd.concat(all_results, ignore_index=True)
        
        # Group by vehicle and calculate points (simplified)
        if 'POS' in combined.columns:
            standings = combined.groupby('NO').agg({
                'POS': 'count',  # Races participated
                'track_name': lambda x: list(x.unique())
            }).reset_index()
            standings.columns = ['vehicle_number', 'races_completed', 'tracks']
            
            return {
                "total_vehicles": len(standings),
                "standings": standings.to_dict(orient='records')
            }
        
        return {"message": "Championship data processing in progress"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tracks/{track_name}/map")
async def get_track_map(track_name: str):
    """Get track map image"""
    try:
        track = get_track_info(track_name)
        map_path = track.map_image
        
        if not os.path.exists(map_path):
            raise HTTPException(status_code=404, detail="Map image not found")
        
        return FileResponse(map_path)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/tracks/{track_name}/geometry")
async def get_track_geometry(track_name: str, race_num: int = 1):
    """Get 3D track geometry from GPS telemetry data"""
    try:
        from src.analysis.track_geometry import get_cached_track_geometry
        
        geometry = get_cached_track_geometry(track_name, race_num)
        
        return {
            "points": geometry['points'],
            "track_name": geometry['track_name'],
            "length_km": geometry['length_km'],
            "turns": geometry['turns'],
            "point_count": geometry['point_count'],
            "source": geometry['source']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating geometry: {str(e)}")


@app.get("/api/telemetry/live/{track_name}/{race_num}/{vehicle_number}")
async def get_live_telemetry(track_name: str, race_num: int, vehicle_number: int, lap: int = 1):
    """Get real telemetry data for a specific vehicle and lap - OPTIMIZED"""
    try:
        # Lazy import to avoid startup delay
        from src.telemetry_processor import get_telemetry_processor
        
        # Get telemetry file
        telemetry_file = multi_loader.get_telemetry_file(track_name, race_num)
        if not telemetry_file:
            raise HTTPException(status_code=404, detail="Telemetry data not found")
        
        # Use optimized processor
        processor = get_telemetry_processor()
        telemetry_df = processor.process_lap_telemetry(
            telemetry_file,
            lap,
            track_name,
            race_num,
            sample_rate=50  # Sample every 50th point (~20Hz from 1000Hz)
        )
        
        if telemetry_df.empty:
            raise HTTPException(status_code=404, detail=f"No telemetry data for lap {lap}")
        
        # Export for frontend
        telemetry_points = processor.export_for_frontend(telemetry_df)
        
        return {
            "track": track_name,
            "race": race_num,
            "vehicle": vehicle_number,
            "lap": lap,
            "points": telemetry_points,
            "total_points": len(telemetry_points),
            "cached": processor.is_cached(track_name, race_num, lap)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading telemetry: {str(e)}")


@app.get("/api/telemetry/optimal/{track_name}/{race_num}")
async def get_optimal_telemetry(track_name: str, race_num: int, lap: Optional[int] = None):
    """Get optimal telemetry (fastest lap) for comparison - OPTIMIZED"""
    try:
        # Lazy import to avoid startup delay
        from src.telemetry_processor import get_telemetry_processor
        
        # Load analysis data
        analysis_data = multi_loader.load_analysis(track_name, race_num)
        if analysis_data.empty:
            raise HTTPException(status_code=404, detail="No analysis data found")
        
        # Get telemetry file
        telemetry_file = multi_loader.get_telemetry_file(track_name, race_num)
        if not telemetry_file:
            raise HTTPException(status_code=404, detail="Telemetry data not found")
        
        # Use optimized processor
        processor = get_telemetry_processor()
        optimal_telemetry, fastest_lap_num = processor.get_optimal_lap_telemetry(
            telemetry_file,
            analysis_data,
            track_name,
            race_num,
            sample_rate=50
        )
        
        if optimal_telemetry.empty:
            raise HTTPException(status_code=404, detail="No optimal telemetry found")
        
        # Calculate metrics
        metrics = processor.calculate_optimal_metrics(optimal_telemetry)
        metrics['lap_number'] = fastest_lap_num
        
        # Get lap time from analysis
        def parse_lap_time(time_str):
            try:
                parts = str(time_str).split(':')
                if len(parts) == 2:
                    return float(parts[0]) * 60 + float(parts[1])
                return float(time_str)
            except:
                return 0
        
        analysis_data['lap_time_seconds'] = analysis_data['LAP_TIME'].apply(parse_lap_time)
        fastest_lap_data = analysis_data[analysis_data['LAP_NUMBER'] == fastest_lap_num]
        if not fastest_lap_data.empty:
            metrics['lap_time'] = float(fastest_lap_data.iloc[0]['lap_time_seconds'])
        
        return metrics
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading optimal telemetry: {str(e)}")


@app.get("/api/telemetry/comparison/{track_name}/{race_num}/{vehicle_number}")
async def get_telemetry_comparison(track_name: str, race_num: int, vehicle_number: int, lap: int):
    """Compare vehicle telemetry against optimal"""
    try:
        # Get current vehicle telemetry
        current = await get_live_telemetry(track_name, race_num, vehicle_number, lap)
        
        # Get optimal telemetry
        optimal = await get_optimal_telemetry(track_name, race_num)
        
        # Calculate current averages
        if current['points']:
            current_avg_speed = sum(p['speed'] for p in current['points']) / len(current['points'])
            current_avg_throttle = sum(p['throttle'] for p in current['points']) / len(current['points'])
            current_avg_brake = sum((p['brake_front'] + p['brake_rear'])/2 for p in current['points']) / len(current['points'])
        else:
            current_avg_speed = 0
            current_avg_throttle = 0
            current_avg_brake = 0
        
        # Calculate deltas
        speed_delta = current_avg_speed - optimal['avg_speed']
        throttle_delta = current_avg_throttle - optimal['avg_throttle']
        brake_delta = current_avg_brake - optimal['avg_brake']
        
        return {
            "current": {
                "speed": current_avg_speed,
                "throttle": current_avg_throttle,
                "brake": current_avg_brake
            },
            "optimal": {
                "speed": optimal['avg_speed'],
                "throttle": optimal['avg_throttle'],
                "brake": optimal['avg_brake']
            },
            "delta": {
                "speed": speed_delta,
                "throttle": throttle_delta,
                "brake": brake_delta
            },
            "performance_score": calculate_performance_score(speed_delta, throttle_delta, brake_delta)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error comparing telemetry: {str(e)}")


def calculate_performance_score(speed_delta: float, throttle_delta: float, brake_delta: float) -> float:
    """Calculate performance score (0-100) based on deltas"""
    # Closer to optimal = higher score
    speed_score = max(0, 100 - abs(speed_delta) * 2)
    throttle_score = max(0, 100 - abs(throttle_delta))
    brake_score = max(0, 100 - abs(brake_delta))
    
    return (speed_score + throttle_score + brake_score) / 3


if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting RaceIQ API server...")
    print("📊 Dashboard will be available at http://localhost:8001")
    print("📖 API docs at http://localhost:8001/docs")
    uvicorn.run(app, host="0.0.0.0", port=8001)
