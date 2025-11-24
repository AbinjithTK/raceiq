"""
Multi-Track Data Loader
Unified interface for loading data from all 7 tracks
"""

import pandas as pd
import glob
import os
from typing import Dict, List, Optional, Tuple
from src.track_config import get_track_info, get_track_file_path, list_available_tracks


class MultiTrackLoader:
    """Load and process data from multiple tracks"""
    
    def __init__(self, base_path: str = "."):
        self.base_path = base_path
        self.tracks = list_available_tracks()
    
    def load_lap_times(self, track_name: str, race_num: int) -> pd.DataFrame:
        """Load lap time data for a specific track and race"""
        track_info = get_track_info(track_name)
        filename = track_info.lap_time_pattern.format(race=race_num)
        
        # Try multiple base paths
        possible_paths = [
            os.path.join(self.base_path, track_info.base_path, filename),
            os.path.join(track_info.base_path, filename),
            filename
        ]
        
        full_path = None
        for path in possible_paths:
            if os.path.exists(path):
                full_path = path
                break
        
        if not full_path:
            raise FileNotFoundError(f"Lap time file not found: {filename}")
        
        try:
            # Try comma delimiter first (telemetry format)
            df = pd.read_csv(full_path, delimiter=',')
        except:
            # Fall back to semicolon (results format)
            df = pd.read_csv(full_path, delimiter=';')
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Add track metadata
        df['track_name'] = track_info.name
        df['track_short'] = track_name
        df['race_number'] = race_num
        
        return df
    
    def load_telemetry(self, track_name: str, race_num: int, 
                       sample_rate: Optional[int] = None) -> pd.DataFrame:
        """
        Load telemetry data for a specific track and race
        
        Args:
            track_name: Track identifier
            race_num: Race number
            sample_rate: If provided, sample every Nth row to reduce memory
        """
        file_path = get_track_file_path(track_name, race_num, 'telemetry')
        full_path = os.path.join(self.base_path, file_path)
        
        # Telemetry files are always comma-delimited
        if sample_rate:
            # Read with sampling for large files
            df = pd.read_csv(full_path, delimiter=',', 
                           skiprows=lambda i: i % sample_rate != 0 and i != 0)
        else:
            df = pd.read_csv(full_path, delimiter=',')
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Add track metadata
        track_info = get_track_info(track_name)
        df['track_name'] = track_info.name
        df['track_short'] = track_name
        df['race_number'] = race_num
        
        return df
    
    def load_results(self, track_name: str, race_num: int) -> pd.DataFrame:
        """Load race results"""
        pattern = get_track_file_path(track_name, race_num, 'results')
        full_pattern = os.path.join(self.base_path, pattern)
        
        files = glob.glob(full_pattern)
        if not files:
            raise FileNotFoundError(f"No results file found: {full_pattern}")
        
        # Use the first matching file (usually the official results)
        df = pd.read_csv(files[0], delimiter=';')
        df.columns = df.columns.str.strip()
        
        track_info = get_track_info(track_name)
        df['track_name'] = track_info.name
        df['track_short'] = track_name
        df['race_number'] = race_num
        
        return df
    
    def load_analysis(self, track_name: str, race_num: int) -> pd.DataFrame:
        """Load sector analysis data"""
        pattern = get_track_file_path(track_name, race_num, 'analysis')
        full_pattern = os.path.join(self.base_path, pattern)
        
        files = glob.glob(full_pattern)
        if not files:
            raise FileNotFoundError(f"No analysis file found: {full_pattern}")
        
        df = pd.read_csv(files[0], delimiter=';')
        df.columns = df.columns.str.strip()
        
        track_info = get_track_info(track_name)
        df['track_name'] = track_info.name
        df['track_short'] = track_name
        df['race_number'] = race_num
        
        return df
    
    def load_best_laps(self, track_name: str, race_num: int) -> pd.DataFrame:
        """Load best lap times by driver"""
        pattern = get_track_file_path(track_name, race_num, 'best_laps')
        full_pattern = os.path.join(self.base_path, pattern)
        
        files = glob.glob(full_pattern)
        if not files:
            raise FileNotFoundError(f"No best laps file found: {full_pattern}")
        
        df = pd.read_csv(files[0], delimiter=';')
        df.columns = df.columns.str.strip()
        
        track_info = get_track_info(track_name)
        df['track_name'] = track_info.name
        df['track_short'] = track_name
        df['race_number'] = race_num
        
        return df
    
    def load_all_tracks_lap_times(self, race_num: int = 1) -> pd.DataFrame:
        """Load lap times from all tracks for comparison"""
        all_data = []
        
        for track_name in self.tracks:
            try:
                df = self.load_lap_times(track_name, race_num)
                all_data.append(df)
                print(f"✓ Loaded {track_name}: {len(df)} laps")
            except Exception as e:
                print(f"✗ Failed to load {track_name}: {e}")
        
        if not all_data:
            raise ValueError("No data loaded from any track")
        
        return pd.concat(all_data, ignore_index=True)
    
    def load_all_tracks_results(self, race_num: int = 1) -> pd.DataFrame:
        """Load results from all tracks"""
        all_data = []
        
        for track_name in self.tracks:
            try:
                df = self.load_results(track_name, race_num)
                all_data.append(df)
                print(f"✓ Loaded {track_name} results: {len(df)} entries")
            except Exception as e:
                print(f"✗ Failed to load {track_name}: {e}")
        
        if not all_data:
            raise ValueError("No results loaded from any track")
        
        return pd.concat(all_data, ignore_index=True)
    
    def get_track_statistics(self) -> pd.DataFrame:
        """Get statistics about all tracks"""
        from track_config import TRACKS
        
        stats = []
        for track_key, track in TRACKS.items():
            stats.append({
                'track': track.name,
                'short_name': track_key,
                'length_km': track.length_km,
                'turns': track.turns,
                'direction': track.direction,
                'races_available': len(track.race_folders)
            })
        
        return pd.DataFrame(stats)
    
    def get_telemetry_file(self, track_name: str, race_num: int) -> Optional[str]:
        """Get the path to telemetry file for a track/race"""
        try:
            track_info = get_track_info(track_name)
            filename = track_info.telemetry_pattern.format(race=race_num)
            
            # Try multiple base paths
            possible_paths = [
                os.path.join(self.base_path, track_info.base_path, filename),
                os.path.join(track_info.base_path, filename),
                filename
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    return path
                
                # Try glob pattern
                files = glob.glob(path)
                if files:
                    return files[0]
            
            return None
        except Exception as e:
            print(f"Error finding telemetry file: {e}")
            return None
    
    def compare_vehicle_across_tracks(self, vehicle_id: str, race_num: int = 1) -> pd.DataFrame:
        """Compare a vehicle's performance across all tracks"""
        results = []
        
        for track_name in self.tracks:
            try:
                # Load lap times
                lap_times = self.load_lap_times(track_name, race_num)
                
                # Filter for this vehicle
                vehicle_laps = lap_times[lap_times['vehicle_id'].str.contains(vehicle_id, na=False)]
                
                if len(vehicle_laps) > 0:
                    track_info = get_track_info(track_name)
                    
                    # Calculate statistics
                    if 'value' in vehicle_laps.columns:
                        # Lap time in milliseconds
                        lap_times_ms = vehicle_laps['value'].dropna()
                        if len(lap_times_ms) > 0:
                            results.append({
                                'track': track_info.name,
                                'track_short': track_name,
                                'laps_completed': len(lap_times_ms),
                                'best_lap_ms': lap_times_ms.min(),
                                'best_lap_sec': lap_times_ms.min() / 1000,
                                'avg_lap_ms': lap_times_ms.mean(),
                                'avg_lap_sec': lap_times_ms.mean() / 1000,
                                'track_length_km': track_info.length_km
                            })
            except Exception as e:
                print(f"Could not load {track_name}: {e}")
        
        if not results:
            return pd.DataFrame()
        
        df = pd.DataFrame(results)
        
        # Calculate average speed
        if 'best_lap_sec' in df.columns and 'track_length_km' in df.columns:
            df['avg_speed_kmh'] = (df['track_length_km'] / df['best_lap_sec']) * 3600
        
        return df.sort_values('best_lap_sec')


def analyze_all_tracks():
    """Quick analysis of all available track data"""
    loader = MultiTrackLoader()
    
    print("\n" + "="*70)
    print("TOYOTA GR CUP - MULTI-TRACK ANALYSIS")
    print("="*70)
    
    # Track statistics
    print("\nTrack Statistics:")
    print("-" * 70)
    stats = loader.get_track_statistics()
    print(stats.to_string(index=False))
    
    # Try to load data from each track
    print("\n\nData Availability Check (Race 1):")
    print("-" * 70)
    
    for track in list_available_tracks():
        print(f"\n{track.upper()}:")
        try:
            lap_times = loader.load_lap_times(track, 1)
            print(f"  ✓ Lap Times: {len(lap_times)} records")
            
            results = loader.load_results(track, 1)
            print(f"  ✓ Results: {len(results)} entries")
            
            analysis = loader.load_analysis(track, 1)
            print(f"  ✓ Analysis: {len(analysis)} records")
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    analyze_all_tracks()
