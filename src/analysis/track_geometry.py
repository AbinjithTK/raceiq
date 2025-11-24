"""
Track Geometry Generator
Extracts real GPS coordinates from telemetry data and generates 3D track geometry
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from multi_track_loader import MultiTrackLoader
from track_config import get_track_info


def lat_lon_to_meters(lat, lon, ref_lat, ref_lon):
    """
    Convert lat/lon to meters relative to reference point
    Uses simple equirectangular projection (good for small areas)
    """
    # Earth radius in meters
    R = 6371000
    
    # Convert to radians
    lat_rad = np.radians(lat)
    lon_rad = np.radians(lon)
    ref_lat_rad = np.radians(ref_lat)
    ref_lon_rad = np.radians(ref_lon)
    
    # Calculate x, y in meters
    x = R * (lon_rad - ref_lon_rad) * np.cos(ref_lat_rad)
    y = R * (lat_rad - ref_lat_rad)
    
    return x, y


def extract_track_geometry(track_name: str, race_num: int = 1, sample_rate: int = 100) -> Dict:
    """
    Extract track geometry from telemetry GPS data
    
    Args:
        track_name: Track identifier
        race_num: Race number
        sample_rate: Sample every Nth point to reduce data size
    
    Returns:
        Dictionary with track points and metadata
    """
    loader = MultiTrackLoader()
    track_info = get_track_info(track_name)
    
    try:
        # Load telemetry data with sampling
        telemetry = loader.load_telemetry(track_name, race_num, sample_rate=sample_rate)
        
        # Check if data is in long format (telemetry_name/telemetry_value)
        if 'telemetry_name' in telemetry.columns and 'telemetry_value' in telemetry.columns:
            # Pivot to wide format
            gps_lat = telemetry[telemetry['telemetry_name'] == 'VBOX_Lat_Min'].copy()
            gps_lon = telemetry[telemetry['telemetry_name'] == 'VBOX_Long_Minutes'].copy()
            
            if len(gps_lat) == 0 or len(gps_lon) == 0:
                print("No GPS telemetry found in data")
                return generate_fallback_geometry(track_info)
            
            # Merge lat/lon data
            gps_lat = gps_lat[['timestamp', 'vehicle_id', 'telemetry_value']].rename(columns={'telemetry_value': 'lat'})
            gps_lon = gps_lon[['timestamp', 'vehicle_id', 'telemetry_value']].rename(columns={'telemetry_value': 'lon'})
            
            gps_data = pd.merge(gps_lat, gps_lon, on=['timestamp', 'vehicle_id'], how='inner')
            gps_data['lat'] = pd.to_numeric(gps_data['lat'], errors='coerce')
            gps_data['lon'] = pd.to_numeric(gps_data['lon'], errors='coerce')
            gps_data = gps_data.dropna()
            
        else:
            # Check for GPS columns in wide format
            lat_col = None
            lon_col = None
            
            for col in telemetry.columns:
                col_lower = col.lower()
                if 'lat' in col_lower and 'vbox' in col_lower:
                    lat_col = col
                if 'lon' in col_lower and 'vbox' in col_lower:
                    lon_col = col
            
            if not lat_col or not lon_col:
                print(f"GPS columns not found. Available columns: {telemetry.columns.tolist()}")
                return generate_fallback_geometry(track_info)
            
            # Filter valid GPS data
            gps_data = telemetry[[lat_col, lon_col, 'vehicle_id']].copy()
            gps_data = gps_data.rename(columns={lat_col: 'lat', lon_col: 'lon'})
            gps_data = gps_data.dropna()
        
        if len(gps_data) == 0:
            print("No valid GPS data found")
            return generate_fallback_geometry(track_info)
        
        # Get one vehicle's complete lap for track outline
        # Use the vehicle with most GPS points
        vehicle_counts = gps_data['vehicle_id'].value_counts()
        if len(vehicle_counts) == 0:
            return generate_fallback_geometry(track_info)
        
        best_vehicle = vehicle_counts.index[0]
        vehicle_gps = gps_data[gps_data['vehicle_id'] == best_vehicle].copy()
        
        # Sort by timestamp to get proper order
        vehicle_gps = vehicle_gps.sort_values('timestamp')
        
        # Further sample to reduce points (target ~500 points for smooth track)
        target_points = 500
        if len(vehicle_gps) > target_points:
            step = len(vehicle_gps) // target_points
            vehicle_gps = vehicle_gps.iloc[::step]
        
        # Extract coordinates
        lats = vehicle_gps['lat'].values
        lons = vehicle_gps['lon'].values
        
        # Use center of track as reference point
        ref_lat = np.mean(lats)
        ref_lon = np.mean(lons)
        
        # Convert to meters
        points = []
        for lat, lon in zip(lats, lons):
            x, y = lat_lon_to_meters(lat, lon, ref_lat, ref_lon)
            points.append({'x': float(x), 'y': 0, 'z': float(y)})
        
        # Smooth the track line
        points = smooth_track_points(points, window=5)
        
        # Close the loop if needed
        if len(points) > 10:
            first = points[0]
            last = points[-1]
            dist = np.sqrt((first['x'] - last['x'])**2 + (first['z'] - last['z'])**2)
            if dist > 50:  # If not closed, interpolate
                points = close_track_loop(points)
        
        return {
            'points': points,
            'track_name': track_info.name,
            'length_km': track_info.length_km,
            'turns': track_info.turns,
            'point_count': len(points),
            'source': 'gps_telemetry'
        }
        
    except Exception as e:
        print(f"Error extracting GPS geometry for {track_name}: {e}")
        return generate_fallback_geometry(track_info)


def smooth_track_points(points: List[Dict], window: int = 5) -> List[Dict]:
    """Apply moving average smoothing to track points"""
    if len(points) < window:
        return points
    
    smoothed = []
    for i in range(len(points)):
        start = max(0, i - window // 2)
        end = min(len(points), i + window // 2 + 1)
        
        x_avg = np.mean([p['x'] for p in points[start:end]])
        z_avg = np.mean([p['z'] for p in points[start:end]])
        
        smoothed.append({'x': float(x_avg), 'y': 0, 'z': float(z_avg)})
    
    return smoothed


def close_track_loop(points: List[Dict], num_interpolate: int = 10) -> List[Dict]:
    """Interpolate points to close the track loop"""
    first = points[0]
    last = points[-1]
    
    for i in range(1, num_interpolate + 1):
        t = i / (num_interpolate + 1)
        x = last['x'] + t * (first['x'] - last['x'])
        z = last['z'] + t * (first['z'] - last['z'])
        points.append({'x': float(x), 'y': 0, 'z': float(z)})
    
    return points


def generate_simple_oval(t: float, radius: float) -> Dict:
    """Generate a simple oval track shape"""
    angle = t * 2 * np.pi
    x = np.cos(angle) * radius
    z = np.sin(angle) * radius * 0.6  # Oval shape
    y = 0
    return {'x': x, 'y': y, 'z': z}


def generate_fallback_geometry(track_info) -> Dict:
    """
    Generate stylized track geometry when GPS data is unavailable
    Uses track characteristics to create representative shape
    """
    # Import track layouts from frontend (fallback only)
    TRACK_LAYOUTS = {
        'barber': {'generator': lambda t: generate_simple_oval(t, 50)},
        'indianapolis': {'generator': lambda t: generate_simple_oval(t, 60)},
        'cota': {'generator': lambda t: generate_simple_oval(t, 70)},
        'sebring': {'generator': lambda t: generate_simple_oval(t, 75)},
        'road_america': {'generator': lambda t: generate_simple_oval(t, 80)},
        'sonoma': {'generator': lambda t: generate_simple_oval(t, 55)},
        'vir': {'generator': lambda t: generate_simple_oval(t, 65)}
    }
    
    track_key = track_info.short_name
    if track_key not in TRACK_LAYOUTS:
        track_key = 'barber'
    
    layout = TRACK_LAYOUTS[track_key]
    points = []
    num_points = 200
    
    for i in range(num_points + 1):
        t = i / num_points
        coord = layout['generator'](t)
        points.append({
            'x': float(coord['x']),
            'y': float(coord['y']),
            'z': float(coord['z'])
        })
    
    return {
        'points': points,
        'track_name': track_info.name,
        'length_km': track_info.length_km,
        'turns': track_info.turns,
        'point_count': len(points),
        'source': 'stylized'
    }


def get_track_bounds(points: List[Dict]) -> Dict:
    """Calculate bounding box for track"""
    if not points:
        return {'min_x': 0, 'max_x': 0, 'min_z': 0, 'max_z': 0}
    
    xs = [p['x'] for p in points]
    zs = [p['z'] for p in points]
    
    return {
        'min_x': min(xs),
        'max_x': max(xs),
        'min_z': min(zs),
        'max_z': max(zs),
        'width': max(xs) - min(xs),
        'height': max(zs) - min(zs)
    }


def normalize_track_geometry(points: List[Dict], target_size: float = 200) -> List[Dict]:
    """
    Normalize track to fit within target size while maintaining aspect ratio
    """
    bounds = get_track_bounds(points)
    
    # Calculate scale factor
    max_dimension = max(bounds['width'], bounds['height'])
    if max_dimension == 0:
        return points
    
    scale = target_size / max_dimension
    
    # Calculate center
    center_x = (bounds['min_x'] + bounds['max_x']) / 2
    center_z = (bounds['min_z'] + bounds['max_z']) / 2
    
    # Normalize points
    normalized = []
    for p in points:
        normalized.append({
            'x': float((p['x'] - center_x) * scale),
            'y': float(p['y']),
            'z': float((p['z'] - center_z) * scale)
        })
    
    return normalized


# Cache for track geometries
_geometry_cache = {}


def get_cached_track_geometry(track_name: str, race_num: int = 1) -> Dict:
    """Get track geometry with caching"""
    cache_key = f"{track_name}_{race_num}"
    
    if cache_key not in _geometry_cache:
        geometry = extract_track_geometry(track_name, race_num)
        # Normalize to consistent size
        geometry['points'] = normalize_track_geometry(geometry['points'])
        _geometry_cache[cache_key] = geometry
    
    return _geometry_cache[cache_key]


if __name__ == "__main__":
    # Test geometry extraction
    print("Testing Track Geometry Extraction\n")
    print("=" * 60)
    
    from track_config import list_available_tracks
    
    for track in list_available_tracks()[:3]:  # Test first 3 tracks
        print(f"\n{track.upper()}:")
        try:
            geometry = get_cached_track_geometry(track, race_num=1)
            print(f"  ✓ Points: {geometry['point_count']}")
            print(f"  ✓ Source: {geometry['source']}")
            print(f"  ✓ Track: {geometry['track_name']}")
            
            bounds = get_track_bounds(geometry['points'])
            print(f"  ✓ Bounds: {bounds['width']:.1f}m x {bounds['height']:.1f}m")
        except Exception as e:
            print(f"  ✗ Error: {e}")
