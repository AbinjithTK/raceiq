"""
Track Configuration and Multi-Track Data Management
Handles all 7 tracks in the Toyota GR Cup dataset
"""

import os
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

@dataclass
class TrackInfo:
    """Track metadata and file paths"""
    name: str
    short_name: str
    base_path: str
    map_image: str
    race_folders: List[str]
    lap_time_pattern: str
    lap_start_pattern: str
    lap_end_pattern: str
    telemetry_pattern: str
    results_pattern: str
    analysis_pattern: str
    weather_pattern: str
    best_laps_pattern: str
    
    # Track characteristics
    length_km: float
    turns: int
    direction: str  # "clockwise" or "counterclockwise"
    
    # GPS bounds (for 3D visualization)
    lat_min: Optional[float] = None
    lat_max: Optional[float] = None
    lon_min: Optional[float] = None
    lon_max: Optional[float] = None


# Track Database
TRACKS: Dict[str, TrackInfo] = {
    "barber": TrackInfo(
        name="Barber Motorsports Park",
        short_name="barber",
        base_path="barber",
        map_image="barber/map/barbermap.jpg",
        race_folders=["barber"],  # Flat structure
        lap_time_pattern="R{race}_barber_lap_time.csv",
        lap_start_pattern="R{race}_barber_lap_start.csv",
        lap_end_pattern="R{race}_barber_lap_end.csv",
        telemetry_pattern="R{race}_barber_telemetry_data.csv",
        results_pattern="03_*Results*Race {race}*.CSV",
        analysis_pattern="23_*AnalysisEndurance*Race {race}*.CSV",
        weather_pattern="26_Weather_Race {race}*.CSV",
        best_laps_pattern="99_Best 10 Laps*Race {race}*.CSV",
        length_km=3.7,
        turns=17,
        direction="clockwise"
    ),
    
    "indianapolis": TrackInfo(
        name="Indianapolis Motor Speedway (Road Course)",
        short_name="indianapolis",
        base_path="indianapolis",
        map_image="indianapolis/map/indianapolismap-01.jpg",
        race_folders=["indianapolis"],
        lap_time_pattern="R{race}_indianapolis_motor_speedway_lap_time.csv",
        lap_start_pattern="R{race}_indianapolis_motor_speedway_lap_start.csv",
        lap_end_pattern="R{race}_indianapolis_motor_speedway_lap_end.csv",
        telemetry_pattern="R{race}_indianapolis_motor_speedway_telemetry.csv",
        results_pattern="03_*Results*Race {race}*.CSV",
        analysis_pattern="23_*AnalysisEndurance*Race {race}*.CSV",
        weather_pattern="26_Weather_Race {race}*.CSV",
        best_laps_pattern="99_Best 10 Laps*Race {race}*.CSV",
        length_km=4.0,
        turns=14,
        direction="clockwise"
    ),
    
    "cota": TrackInfo(
        name="Circuit of The Americas",
        short_name="cota",
        base_path="COTA",
        map_image="COTA/map/coamap-01.jpg",
        race_folders=["COTA/Race 1", "COTA/Race 2"],
        lap_time_pattern="COTA_lap_time_R{race}.csv",
        lap_start_pattern="COTA_lap_start_time_R{race}.csv",
        lap_end_pattern="COTA_lap_end_time_R{race}.csv",
        telemetry_pattern="R{race}_cota_telemetry_data.csv",
        results_pattern="03_*Results*Race {race}*.CSV",
        analysis_pattern="23_*AnalysisEndurance*Race {race}*.CSV",
        weather_pattern="26_Weather_Race {race}*.CSV",
        best_laps_pattern="99_Best 10 Laps*Race {race}*.CSV",
        length_km=5.5,
        turns=20,
        direction="counterclockwise"
    ),
    
    "sebring": TrackInfo(
        name="Sebring International Raceway",
        short_name="sebring",
        base_path="sebring",
        map_image="sebring/map/sebringmap-01.jpg",
        race_folders=["sebring/Sebring/Race 1", "sebring/Sebring/Race 2"],
        lap_time_pattern="sebring_lap_time_R{race}.csv",
        lap_start_pattern="sebring_lap_start_time_R{race}.csv",
        lap_end_pattern="sebring_lap_end_time_R{race}.csv",
        telemetry_pattern="sebring_telemetry_R{race}.csv",
        results_pattern="03_*Results*Race {race}*.CSV",
        analysis_pattern="23_*AnalysisEndurance*Race {race}*.CSV",
        weather_pattern="26_Weather_Race {race}*.CSV",
        best_laps_pattern="99_Best 10 Laps*Race {race}*.CSV",
        length_km=6.0,
        turns=17,
        direction="clockwise"
    ),
    
    "road_america": TrackInfo(
        name="Road America",
        short_name="road_america",
        base_path="road-america",
        map_image="road-america/map/road-americamap-01.jpg",
        race_folders=["road-america/Road America/Race 1", "road-america/Road America/Race 2"],
        lap_time_pattern="road_america_lap_time_R{race}.csv",
        lap_start_pattern="road_america_lap_start_R{race}.csv",
        lap_end_pattern="road_america_lap_end_R{race}.csv",
        telemetry_pattern="R{race}_road_america_telemetry_data.csv",
        results_pattern="03_*Results*Race {race}*.CSV",
        analysis_pattern="23_*AnalysisEndurance*Race {race}*.CSV",
        weather_pattern="26_Weather_Race {race}*.CSV",
        best_laps_pattern="99_Best 10 Laps*Race {race}*.CSV",
        length_km=6.5,
        turns=14,
        direction="clockwise"
    ),
    
    "sonoma": TrackInfo(
        name="Sonoma Raceway",
        short_name="sonoma",
        base_path="Sonoma",
        map_image="Sonoma/map/sonomamap.png",
        race_folders=["Sonoma/Race 1", "Sonoma/Race 2"],
        lap_time_pattern="sonoma_lap_time_R{race}.csv",
        lap_start_pattern="sonoma_lap_start_time_R{race}.csv",
        lap_end_pattern="sonoma_lap_end_time_R{race}.csv",
        telemetry_pattern="sonoma_telemetry_R{race}.csv",
        results_pattern="03_*Results*Race {race}*.CSV",
        analysis_pattern="23_*AnalysisEndurance*Race {race}*.CSV",
        weather_pattern="26_Weather_Race {race}*.CSV",
        best_laps_pattern="99_Best 10 Laps*Race {race}*.CSV",
        length_km=4.0,
        turns=12,
        direction="clockwise"
    ),
    
    "vir": TrackInfo(
        name="Virginia International Raceway",
        short_name="vir",
        base_path="virginia-international-raceway",
        map_image="virginia-international-raceway/map/virginia-international-raceway.png",
        race_folders=["virginia-international-raceway/VIR/Race 1", "virginia-international-raceway/VIR/Race 2"],
        lap_time_pattern="vir_lap_time_R{race}.csv",
        lap_start_pattern="vir_lap_start_R{race}.csv",
        lap_end_pattern="vir_lap_end_R{race}.csv",
        telemetry_pattern="R{race}_vir_telemetry_data.csv",
        results_pattern="03_*Results*Race {race}*.CSV",
        analysis_pattern="23_*AnalysisEndurance*Race {race}*.CSV",
        weather_pattern="26_Weather_Race {race}*.CSV",
        best_laps_pattern="99_Best 10 Laps*Race {race}*.CSV",
        length_km=5.3,
        turns=18,
        direction="clockwise"
    )
}


def get_track_info(track_name: str) -> TrackInfo:
    """Get track configuration by name"""
    track_name = track_name.lower().replace(" ", "_").replace("-", "_")
    
    if track_name not in TRACKS:
        raise ValueError(f"Unknown track: {track_name}. Available: {list(TRACKS.keys())}")
    
    return TRACKS[track_name]


def list_available_tracks() -> List[str]:
    """Get list of all available tracks"""
    return list(TRACKS.keys())


def get_track_file_path(track_name: str, race_num: int, file_type: str) -> str:
    """
    Get the full path to a specific data file
    
    Args:
        track_name: Track identifier (e.g., 'barber', 'cota')
        race_num: Race number (1 or 2)
        file_type: Type of file ('lap_time', 'telemetry', 'results', etc.)
    
    Returns:
        Full file path
    """
    track = get_track_info(track_name)
    
    # Get the appropriate folder for this race
    if len(track.race_folders) == 1:
        folder = track.race_folders[0]
    else:
        folder = track.race_folders[race_num - 1]
    
    # Get the pattern for this file type
    pattern_map = {
        'lap_time': track.lap_time_pattern,
        'lap_start': track.lap_start_pattern,
        'lap_end': track.lap_end_pattern,
        'telemetry': track.telemetry_pattern,
        'results': track.results_pattern,
        'analysis': track.analysis_pattern,
        'weather': track.weather_pattern,
        'best_laps': track.best_laps_pattern
    }
    
    if file_type not in pattern_map:
        raise ValueError(f"Unknown file type: {file_type}")
    
    pattern = pattern_map[file_type].format(race=race_num)
    
    # For glob patterns, return the pattern
    if '*' in pattern:
        return os.path.join(folder, pattern)
    
    return os.path.join(folder, pattern)


def get_all_tracks_summary() -> Dict:
    """Get summary of all tracks and their data"""
    summary = {}
    
    for track_key, track in TRACKS.items():
        summary[track_key] = {
            'name': track.name,
            'length_km': track.length_km,
            'turns': track.turns,
            'direction': track.direction,
            'map_image': track.map_image,
            'races': len(track.race_folders)
        }
    
    return summary


if __name__ == "__main__":
    # Test the configuration
    print("Available Tracks:")
    print("=" * 60)
    
    for track_key in list_available_tracks():
        track = get_track_info(track_key)
        print(f"\n{track.name}")
        print(f"  Length: {track.length_km} km")
        print(f"  Turns: {track.turns}")
        print(f"  Direction: {track.direction}")
        print(f"  Map: {track.map_image}")
        print(f"  Races: {len(track.race_folders)}")
