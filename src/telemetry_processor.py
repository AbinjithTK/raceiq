"""
Optimized Telemetry Data Processor
Handles large telemetry files (1.5GB+) efficiently
Normalizes and cleans data for frontend consumption
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import os
from datetime import datetime


class TelemetryProcessor:
    """Process and optimize large telemetry files"""
    
    # Key telemetry parameters we care about (case-sensitive as in CSV)
    KEY_PARAMETERS = [
        'speed',           # Vehicle speed (km/h)
        'aps',             # Accelerator pedal position (0-100%)
        'ath',             # Throttle blade position (0-100%)
        'pbrake_f',        # Front brake pressure (bar)
        'pbrake_r',        # Rear brake pressure (bar)
        'gear',            # Current gear
        'nmot',            # Engine RPM
        'Steering_Angle',  # Steering wheel angle (degrees)
        'accx_can',        # Forward/backward acceleration (G's)
        'accy_can',        # Lateral acceleration (G's)
        'VBOX_Long_Minutes',  # GPS longitude
        'VBOX_Lat_Min',       # GPS latitude
        'Laptrigger_lapdist_dls'  # Distance from start/finish
    ]
    
    def __init__(self, cache_dir: str = "output/telemetry_cache"):
        """Initialize processor with cache directory"""
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def get_cache_path(self, track: str, race: int, lap: int) -> str:
        """Get cache file path for processed telemetry"""
        return os.path.join(self.cache_dir, f"{track}_R{race}_lap{lap}.csv")
    
    def is_cached(self, track: str, race: int, lap: int) -> bool:
        """Check if processed telemetry is cached"""
        return os.path.exists(self.get_cache_path(track, race, lap))
    
    def load_from_cache(self, track: str, race: int, lap: int) -> Optional[pd.DataFrame]:
        """Load processed telemetry from cache"""
        cache_path = self.get_cache_path(track, race, lap)
        if os.path.exists(cache_path):
            return pd.read_csv(cache_path)
        return None
    
    def save_to_cache(self, df: pd.DataFrame, track: str, race: int, lap: int):
        """Save processed telemetry to cache"""
        cache_path = self.get_cache_path(track, race, lap)
        df.to_csv(cache_path, index=False)
    
    def normalize_lap_number(self, lap: int) -> int:
        """Normalize lap number (handle error value 32768)"""
        if lap == 32768 or lap < 0 or lap > 100:
            return -1  # Invalid lap
        return lap
    
    def parse_vehicle_id(self, vehicle_id: str) -> Dict[str, str]:
        """Parse vehicle ID into chassis and car number"""
        # Format: GR86-004-78 (chassis: 004, car: 78)
        try:
            parts = str(vehicle_id).split('-')
            if len(parts) >= 3:
                return {
                    'chassis': parts[1],
                    'car_number': parts[2] if parts[2] != '000' else 'unassigned'
                }
        except:
            pass
        return {'chassis': 'unknown', 'car_number': 'unknown'}
    
    def clean_telemetry_value(self, value, param_name: str) -> float:
        """Clean and normalize telemetry value"""
        try:
            val = float(value)
            
            # Handle NaN and infinite values
            if pd.isna(val) or np.isinf(val):
                return self.get_default_value(param_name)
            
            # Normalize specific parameters
            if param_name in ['aps', 'ath']:
                # Throttle/pedal position: 0-100%
                return max(0, min(100, val))
            elif param_name in ['pbrake_f', 'pbrake_r']:
                # Brake pressure: 0-100 bar (normalize to 0-100)
                return max(0, min(100, val))
            elif param_name in ['Speed', 'speed']:
                # Speed: 0-250 km/h (reasonable range)
                return max(0, min(250, val))
            elif param_name in ['Gear', 'gear']:
                # Gear: 0-6
                return max(0, min(6, int(val)))
            elif param_name in ['nmotor', 'nmot']:
                # RPM: 0-8500
                return max(0, min(8500, val))
            elif param_name == 'Steering_Angle':
                # Steering: -540 to 540 degrees
                return max(-540, min(540, val))
            elif param_name in ['accx_can', 'accy_can']:
                # G-forces: -3 to 3 G (reasonable range)
                return max(-3, min(3, val))
            
            return val
        except:
            return self.get_default_value(param_name)
    
    def get_default_value(self, param_name: str) -> float:
        """Get default value for parameter"""
        defaults = {
            'Speed': 0,
            'speed': 0,
            'aps': 0,
            'ath': 0,
            'pbrake_f': 0,
            'pbrake_r': 0,
            'Gear': 4,
            'gear': 4,
            'nmotor': 5000,
            'nmot': 5000,
            'Steering_Angle': 0,
            'accx_can': 0,
            'accy_can': 0,
            'VBOX_Long_Minutes': 0,
            'VBOX_Lat_Min': 0,
            'Laptrigger_lapdist_dls': 0
        }
        return defaults.get(param_name, 0)
    
    def process_lap_telemetry(
        self, 
        telemetry_file: str, 
        lap: int,
        track: str,
        race: int,
        sample_rate: int = 50
    ) -> pd.DataFrame:
        """
        Process telemetry for a specific lap with optimization
        
        Args:
            telemetry_file: Path to telemetry CSV
            lap: Lap number to extract
            track: Track name for caching
            race: Race number for caching
            sample_rate: Take every Nth row (default: 50 = ~20Hz from 1000Hz)
        
        Returns:
            DataFrame with normalized telemetry
        """
        # Check cache first
        cached = self.load_from_cache(track, race, lap)
        if cached is not None:
            print(f"✅ Loaded lap {lap} from cache")
            return cached
        
        print(f"🔄 Processing lap {lap} from {telemetry_file}...")
        
        # Read file in chunks, filter for lap, and sample
        chunk_size = 500000
        lap_data_chunks = []
        rows_processed = 0
        
        for chunk in pd.read_csv(telemetry_file, chunksize=chunk_size):
            rows_processed += len(chunk)
            
            # Normalize lap numbers
            chunk['lap_normalized'] = chunk['lap'].apply(self.normalize_lap_number)
            
            # Filter for target lap
            lap_chunk = chunk[chunk['lap_normalized'] == lap].copy()
            
            if not lap_chunk.empty:
                # Sample to reduce data
                lap_chunk = lap_chunk.iloc[::sample_rate]
                lap_data_chunks.append(lap_chunk)
                print(f"   Found {len(lap_chunk)} points (processed {rows_processed:,} rows)")
            
            # Stop if we have enough data (assume lap data is contiguous)
            if len(lap_data_chunks) > 0 and rows_processed > chunk_size * 3:
                break
        
        if not lap_data_chunks:
            print(f"   ⚠️  No data found for lap {lap}")
            return pd.DataFrame()
        
        # Combine chunks
        lap_data = pd.concat(lap_data_chunks, ignore_index=True)
        print(f"   Combined {len(lap_data)} data points")
        
        # Pivot from long to wide format
        print(f"   Pivoting data...")
        pivoted = lap_data.pivot_table(
            index=['meta_time', 'timestamp', 'vehicle_id'],
            columns='telemetry_name',
            values='telemetry_value',
            aggfunc='first'
        ).reset_index()
        
        # Keep only key parameters
        available_params = [p for p in self.KEY_PARAMETERS if p in pivoted.columns]
        keep_cols = ['meta_time', 'timestamp', 'vehicle_id'] + available_params
        pivoted = pivoted[keep_cols]
        
        # Clean and normalize values
        print(f"   Normalizing {len(available_params)} parameters...")
        for param in available_params:
            pivoted[param] = pivoted[param].apply(
                lambda x: self.clean_telemetry_value(x, param)
            )
        
        # Parse vehicle info
        pivoted['chassis'] = pivoted['vehicle_id'].apply(
            lambda x: self.parse_vehicle_id(x)['chassis']
        )
        pivoted['car_number'] = pivoted['vehicle_id'].apply(
            lambda x: self.parse_vehicle_id(x)['car_number']
        )
        
        # Add computed fields
        if 'pbrake_f' in pivoted.columns and 'pbrake_r' in pivoted.columns:
            pivoted['brake_total'] = (pivoted['pbrake_f'] + pivoted['pbrake_r']) / 2
        
        if 'aps' in pivoted.columns:
            pivoted['throttle'] = pivoted['aps']  # Alias for clarity
        
        # Sort by time
        pivoted = pivoted.sort_values('meta_time').reset_index(drop=True)
        
        # Add progress through lap (0-1)
        pivoted['lap_progress'] = np.linspace(0, 1, len(pivoted))
        
        print(f"   ✅ Processed {len(pivoted)} points for lap {lap}")
        
        # Cache the result
        self.save_to_cache(pivoted, track, race, lap)
        
        return pivoted
    
    def get_optimal_lap_telemetry(
        self,
        telemetry_file: str,
        analysis_data: pd.DataFrame,
        track: str,
        race: int,
        sample_rate: int = 50
    ) -> Tuple[pd.DataFrame, int]:
        """
        Get telemetry for the fastest lap
        
        Returns:
            (telemetry_df, fastest_lap_number)
        """
        # Find fastest lap from analysis data
        def parse_lap_time(time_str):
            try:
                parts = str(time_str).split(':')
                if len(parts) == 2:
                    return float(parts[0]) * 60 + float(parts[1])
                return float(time_str)
            except:
                return 999999
        
        analysis_data['lap_time_seconds'] = analysis_data['LAP_TIME'].apply(parse_lap_time)
        valid_laps = analysis_data[analysis_data['lap_time_seconds'] < 180]
        
        if valid_laps.empty:
            return pd.DataFrame(), -1
        
        fastest_lap = valid_laps.loc[valid_laps['lap_time_seconds'].idxmin()]
        fastest_lap_num = int(fastest_lap['LAP_NUMBER'])
        
        print(f"🏆 Fastest lap: {fastest_lap_num} ({fastest_lap['lap_time_seconds']:.3f}s)")
        
        # Get telemetry for that lap
        telemetry = self.process_lap_telemetry(
            telemetry_file, 
            fastest_lap_num,
            track,
            race,
            sample_rate
        )
        
        return telemetry, fastest_lap_num
    
    def calculate_optimal_metrics(self, telemetry: pd.DataFrame) -> Dict:
        """Calculate average metrics from optimal lap telemetry"""
        if telemetry.empty:
            return {
                'avg_speed': 150.0,
                'max_speed': 180.0,
                'avg_throttle': 75.0,
                'avg_brake': 20.0,
                'avg_rpm': 6000.0
            }
        
        metrics = {}
        
        # Speed - filter out zeros and invalid values
        if 'speed' in telemetry.columns:
            valid_speed = telemetry['speed'][telemetry['speed'] > 0]
            if len(valid_speed) > 0:
                metrics['avg_speed'] = float(valid_speed.mean())
                metrics['max_speed'] = float(valid_speed.max())
            else:
                metrics['avg_speed'] = 140.0
                metrics['max_speed'] = 180.0
        elif 'Speed' in telemetry.columns:
            valid_speed = telemetry['Speed'][telemetry['Speed'] > 0]
            if len(valid_speed) > 0:
                metrics['avg_speed'] = float(valid_speed.mean())
                metrics['max_speed'] = float(valid_speed.max())
            else:
                metrics['avg_speed'] = 140.0
                metrics['max_speed'] = 180.0
        else:
            metrics['avg_speed'] = 140.0
            metrics['max_speed'] = 180.0
        
        # Throttle
        if 'throttle' in telemetry.columns:
            metrics['avg_throttle'] = float(telemetry['throttle'].mean())
        elif 'aps' in telemetry.columns:
            metrics['avg_throttle'] = float(telemetry['aps'].mean())
        else:
            metrics['avg_throttle'] = 75.0
        
        # Brake
        if 'brake_total' in telemetry.columns:
            metrics['avg_brake'] = float(telemetry['brake_total'].mean())
        elif 'pbrake_f' in telemetry.columns:
            metrics['avg_brake'] = float(telemetry['pbrake_f'].mean())
        else:
            metrics['avg_brake'] = 20.0
        
        # RPM
        if 'nmot' in telemetry.columns:
            valid_rpm = telemetry['nmot'][telemetry['nmot'] > 0]
            if len(valid_rpm) > 0:
                metrics['avg_rpm'] = float(valid_rpm.mean())
            else:
                metrics['avg_rpm'] = 6000.0
        elif 'nmotor' in telemetry.columns:
            valid_rpm = telemetry['nmotor'][telemetry['nmotor'] > 0]
            if len(valid_rpm) > 0:
                metrics['avg_rpm'] = float(valid_rpm.mean())
            else:
                metrics['avg_rpm'] = 6000.0
        else:
            metrics['avg_rpm'] = 6000.0
        
        return metrics
    
    def export_for_frontend(self, telemetry: pd.DataFrame) -> List[Dict]:
        """Export telemetry in frontend-friendly format"""
        if telemetry.empty:
            return []
        
        records = []
        for _, row in telemetry.iterrows():
            record = {
                'timestamp': str(row.get('meta_time', '')),
                'progress': float(row.get('lap_progress', 0)),
                'speed': float(row.get('speed', row.get('Speed', 0))),
                'throttle': float(row.get('throttle', row.get('aps', 0))),
                'brake': float(row.get('brake_total', row.get('pbrake_f', 0))),
                'gear': int(row.get('gear', row.get('Gear', 4))),
                'rpm': float(row.get('nmot', row.get('nmotor', 5000))),
                'steering': float(row.get('Steering_Angle', 0)),
                'accel_x': float(row.get('accx_can', 0)),
                'accel_y': float(row.get('accy_can', 0)),
            }
            records.append(record)
        
        return records


# Singleton instance
_processor = None

def get_telemetry_processor() -> TelemetryProcessor:
    """Get singleton telemetry processor instance"""
    global _processor
    if _processor is None:
        _processor = TelemetryProcessor()
    return _processor
