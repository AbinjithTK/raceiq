"""
Generate accurate track maps from GPS telemetry data
Uses real GPS coordinates to create smooth, properly scaled track layouts
"""

import pandas as pd
import numpy as np
from scipy.interpolate import splprep, splev
from scipy.spatial.distance import euclidean
import json
import os
from typing import List, Dict, Tuple

class AccurateTrackMapGenerator:
    """Generate accurate track maps from GPS telemetry"""
    
    def __init__(self, base_path: str = "."):
        self.base_path = base_path
        
    def load_gps_data(self, track_folder: str, race_num: int = 1) -> pd.DataFrame:
        """Load GPS data from telemetry file"""
        telemetry_file = os.path.join(self.base_path, track_folder, f"R{race_num}_{track_folder}_telemetry_data.csv")
        
        print(f"📍 Loading GPS data from {telemetry_file}...")
        
        # Read telemetry data
        df = pd.read_csv(telemetry_file)
        
        # Filter for GPS coordinates
        gps_data = df[df['telemetry_name'].isin(['VBOX_Long_Minutes', 'VBOX_Lat_Min'])].copy()
        
        # Pivot to get lat/lon columns
        gps_pivot = gps_data.pivot_table(
            index=['meta_time', 'timestamp', 'lap'],
            columns='telemetry_name',
            values='telemetry_value',
            aggfunc='first'
        ).reset_index()
        
        # Clean data
        gps_pivot = gps_pivot.dropna(subset=['VBOX_Long_Minutes', 'VBOX_Lat_Min'])
        
        # Normalize lap numbers (handle error value 32768)
        gps_pivot['lap_normalized'] = gps_pivot['lap'].apply(
            lambda x: 1 if x > 1000 else max(1, int(x))
        )
        
        print(f"✅ Loaded {len(gps_pivot)} GPS points")
        return gps_pivot
    
    def extract_single_lap(self, gps_data: pd.DataFrame, lap_num: int = None, sample_rate: int = 100) -> pd.DataFrame:
        """Extract GPS points for a single clean lap with sampling"""
        
        if lap_num is None:
            # Find lap with most GPS points (usually the cleanest)
            lap_counts = gps_data.groupby('lap_normalized').size()
            lap_num = lap_counts.idxmax()
        
        lap_data = gps_data[gps_data['lap_normalized'] == lap_num].copy()
        lap_data = lap_data.sort_values('meta_time')
        
        # Sample to reduce points (take every Nth point)
        lap_data = lap_data.iloc[::sample_rate]
        
        print(f"🏁 Extracted lap {lap_num} with {len(lap_data)} GPS points (sampled)")
        return lap_data
    
    def convert_to_meters(self, lat: float, lon: float, ref_lat: float, ref_lon: float) -> Tuple[float, float]:
        """Convert GPS coordinates (decimal degrees) to meters from reference point"""
        # GPS data is already in decimal degrees
        # Earth radius in meters
        R = 6371000
        
        # Convert to radians
        lat_rad = np.radians(lat)
        lon_rad = np.radians(lon)
        ref_lat_rad = np.radians(ref_lat)
        ref_lon_rad = np.radians(ref_lon)
        
        # Calculate x, y in meters using equirectangular projection
        x = R * (lon_rad - ref_lon_rad) * np.cos((lat_rad + ref_lat_rad) / 2)
        y = R * (lat_rad - ref_lat_rad)
        
        return x, y
    
    def smooth_track(self, points: np.ndarray, smoothing_factor: float = 5.0, num_points: int = 200) -> np.ndarray:
        """Apply spline smoothing to track points"""
        
        # Ensure we have enough points but not too many
        if len(points) > 1000:
            # Further downsample if needed
            step = len(points) // 500
            points = points[::step]
        
        # Close the loop
        points_closed = np.vstack([points, points[0]])
        
        try:
            # Fit spline (periodic for closed loop)
            tck, u = splprep([points_closed[:, 0], points_closed[:, 1]], 
                             s=smoothing_factor * len(points),  # Scale smoothing by number of points
                             per=True,
                             k=3)  # Cubic spline
            
            # Evaluate spline at evenly spaced points
            u_new = np.linspace(0, 1, num_points)
            smooth_x, smooth_y = splev(u_new, tck)
            
            return np.column_stack([smooth_x, smooth_y])
        except Exception as e:
            print(f"⚠️  Spline smoothing failed: {e}, using simple interpolation")
            # Fallback: simple linear interpolation
            indices = np.linspace(0, len(points)-1, num_points, dtype=int)
            return points[indices]
    
    def calculate_track_length(self, points: np.ndarray) -> float:
        """Calculate total track length in meters"""
        distances = [euclidean(points[i], points[i+1]) for i in range(len(points)-1)]
        # Add distance from last point back to first
        distances.append(euclidean(points[-1], points[0]))
        return sum(distances)
    
    def assign_sectors(self, points: np.ndarray, num_sectors: int = 3) -> np.ndarray:
        """Assign sector numbers to track points"""
        sectors = np.zeros(len(points), dtype=int)
        points_per_sector = len(points) // num_sectors
        
        for i in range(len(points)):
            sectors[i] = min((i // points_per_sector) + 1, num_sectors)
        
        return sectors
    
    def normalize_to_canvas(self, points: np.ndarray, canvas_size: int = 100, padding: int = 5) -> np.ndarray:
        """Normalize points to fit in canvas (0-100 range)"""
        
        # Find bounds
        min_x, min_y = points.min(axis=0)
        max_x, max_y = points.max(axis=0)
        
        # Calculate scale to fit in canvas with padding
        width = max_x - min_x
        height = max_y - min_y
        scale = (canvas_size - 2 * padding) / max(width, height)
        
        # Scale and center
        scaled = (points - [min_x, min_y]) * scale
        
        # Center in canvas
        scaled_width = (max_x - min_x) * scale
        scaled_height = (max_y - min_y) * scale
        offset_x = (canvas_size - scaled_width) / 2
        offset_y = (canvas_size - scaled_height) / 2
        
        normalized = scaled + [offset_x, offset_y]
        
        return normalized
    
    def generate_track_map(self, track_folder: str, race_num: int = 1, 
                          num_points: int = 200, smoothing: float = 0.5) -> Dict:
        """Generate complete track map from GPS data"""
        
        print(f"\n{'='*70}")
        print(f"🏎️  GENERATING ACCURATE TRACK MAP: {track_folder.upper()}")
        print(f"{'='*70}\n")
        
        # Load GPS data
        gps_data = self.load_gps_data(track_folder, race_num)
        
        # Extract single clean lap
        lap_data = self.extract_single_lap(gps_data)
        
        # Convert to meters
        ref_lat = lap_data['VBOX_Lat_Min'].iloc[0]
        ref_lon = lap_data['VBOX_Long_Minutes'].iloc[0]
        
        points_meters = []
        for _, row in lap_data.iterrows():
            x, y = self.convert_to_meters(
                row['VBOX_Lat_Min'],
                row['VBOX_Long_Minutes'],
                ref_lat,
                ref_lon
            )
            points_meters.append([x, y])
        
        points_meters = np.array(points_meters)
        
        # Calculate actual track length
        track_length_m = self.calculate_track_length(points_meters)
        track_length_km = track_length_m / 1000
        
        print(f"📏 Track length: {track_length_km:.3f} km ({track_length_m:.1f} m)")
        
        # Smooth the track
        print(f"🎨 Smoothing track with {num_points} points...")
        smooth_points = self.smooth_track(points_meters, smoothing, num_points)
        
        # Normalize to canvas coordinates
        normalized_points = self.normalize_to_canvas(smooth_points)
        
        # Assign sectors
        sectors = self.assign_sectors(normalized_points)
        
        # Create track data structure
        track_data = []
        for i, (point, sector) in enumerate(zip(normalized_points, sectors)):
            track_data.append({
                'x': float(point[0]),
                'y': float(point[1]),
                'sector': int(sector),
                'index': i,
                'progress': i / len(normalized_points)
            })
        
        # Calculate smooth track length
        smooth_length_m = self.calculate_track_length(smooth_points)
        smooth_length_km = smooth_length_m / 1000
        
        result = {
            'track_name': track_folder,
            'points': track_data,
            'metadata': {
                'total_points': len(track_data),
                'track_length_km': round(track_length_km, 3),
                'track_length_m': round(track_length_m, 1),
                'smooth_length_km': round(smooth_length_km, 3),
                'num_sectors': 3,
                'smoothing_factor': smoothing,
                'source': 'GPS telemetry',
                'race_number': race_num
            }
        }
        
        print(f"✅ Generated {len(track_data)} smooth track points")
        print(f"📊 Smoothed length: {smooth_length_km:.3f} km")
        
        return result
    
    def save_track_map(self, track_data: Dict, output_file: str):
        """Save track map to JSON file"""
        os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(track_data, f, indent=2)
        
        print(f"💾 Saved track map to {output_file}")


def generate_all_tracks():
    """Generate accurate maps for all available tracks"""
    
    generator = AccurateTrackMapGenerator()
    
    # List of available tracks (only barber for now)
    tracks = [
        'barber'
    ]
    
    output_dir = 'frontend/src/data/accurate_tracks'
    os.makedirs(output_dir, exist_ok=True)
    
    results = {}
    
    for track in tracks:
        try:
            # Generate track map
            track_data = generator.generate_track_map(
                track,
                race_num=1,
                num_points=200,  # Smooth curve with 200 points
                smoothing=0.5    # Moderate smoothing
            )
            
            # Save to file
            output_file = os.path.join(output_dir, f'{track}_accurate.json')
            generator.save_track_map(track_data, output_file)
            
            results[track] = {
                'success': True,
                'length_km': track_data['metadata']['track_length_km'],
                'points': track_data['metadata']['total_points']
            }
            
        except Exception as e:
            print(f"❌ Failed to generate {track}: {e}")
            results[track] = {
                'success': False,
                'error': str(e)
            }
    
    # Print summary
    print(f"\n{'='*70}")
    print("📊 TRACK GENERATION SUMMARY")
    print(f"{'='*70}\n")
    
    for track, result in results.items():
        if result['success']:
            print(f"✅ {track:30s} {result['length_km']:.3f} km ({result['points']} points)")
        else:
            print(f"❌ {track:30s} FAILED: {result['error']}")
    
    print(f"\n{'='*70}")
    print(f"✅ Generated {sum(1 for r in results.values() if r['success'])}/{len(tracks)} tracks")
    print(f"{'='*70}\n")


if __name__ == '__main__':
    generate_all_tracks()
