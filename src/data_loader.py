"""
Data loading utilities for RaceIQ
Handles CSV parsing with proper delimiters and data cleaning
"""

import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional
import warnings

warnings.filterwarnings('ignore')


class RaceDataLoader:
    """Load and preprocess Toyota GR Cup race data"""
    
    def __init__(self, data_dir: str = "barber"):
        self.data_dir = Path(data_dir)
        
    def load_race_results(self, race_num: int = 1) -> pd.DataFrame:
        """Load official race results (semicolon delimited)"""
        pattern = f"03_*Race {race_num}*.CSV"
        files = list(self.data_dir.glob(pattern))
        
        if not files:
            raise FileNotFoundError(f"No results file found for race {race_num}")
            
        df = pd.read_csv(files[0], delimiter=';', encoding='utf-8')
        return df
    
    def load_lap_times(self, race_num: int = 1) -> pd.DataFrame:
        """Load lap timing data (comma delimited)"""
        file_path = self.data_dir / f"R{race_num}_barber_lap_time.csv"
        
        if not file_path.exists():
            raise FileNotFoundError(f"Lap time file not found: {file_path}")
        
        df = pd.read_csv(file_path)
        
        # Clean lap data - remove erroneous lap 32768
        df = df[df['lap'] != 32768].copy()
        
        # Parse timestamps
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['meta_time'] = pd.to_datetime(df['meta_time'])
        
        # Extract chassis and car number
        df['chassis_number'] = df['vehicle_id'].str.extract(r'GR86-(\d+)-')[0]
        df['car_number'] = df['vehicle_id'].str.extract(r'-(\d+)$')[0].astype(int)
        
        return df
    
    def load_telemetry(self, race_num: int = 1, sample_rate: Optional[int] = None) -> pd.DataFrame:
        """
        Load telemetry data (comma delimited)
        Warning: Large files! Use sample_rate to load every Nth row
        """
        file_path = self.data_dir / f"R{race_num}_barber_telemetry_data.csv"
        
        if not file_path.exists():
            raise FileNotFoundError(f"Telemetry file not found: {file_path}")
        
        # Sample data if requested (for faster loading)
        if sample_rate:
            df = pd.read_csv(file_path, skiprows=lambda i: i % sample_rate != 0)
        else:
            df = pd.read_csv(file_path)
        
        # Parse timestamps
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        if 'meta_time' in df.columns:
            df['meta_time'] = pd.to_datetime(df['meta_time'])
        
        return df
    
    def load_analysis_endurance(self, race_num: int = 1) -> pd.DataFrame:
        """Load detailed lap analysis with sector times (semicolon delimited)"""
        pattern = f"23_*Race {race_num}*.CSV"
        files = list(self.data_dir.glob(pattern))
        
        if not files:
            raise FileNotFoundError(f"No analysis file found for race {race_num}")
        
        df = pd.read_csv(files[0], delimiter=';', encoding='utf-8')
        
        # Clean column names (remove leading/trailing spaces)
        df.columns = df.columns.str.strip()
        
        # Convert time strings to seconds
        if 'LAP_TIME' in df.columns:
            df['lap_time_seconds'] = df['LAP_TIME'].apply(self._time_to_seconds)
        
        return df
    
    @staticmethod
    def _time_to_seconds(time_str: str) -> float:
        """Convert lap time string (M:SS.mmm) to seconds"""
        try:
            if pd.isna(time_str):
                return None
            parts = time_str.split(':')
            if len(parts) == 2:
                minutes = int(parts[0])
                seconds = float(parts[1])
                return minutes * 60 + seconds
            return float(time_str)
        except:
            return None
    
    def get_vehicle_laps(self, lap_times_df: pd.DataFrame, vehicle_number: int) -> pd.DataFrame:
        """Get all laps for a specific vehicle"""
        return lap_times_df[lap_times_df['vehicle_number'] == vehicle_number].copy()
    
    def get_fastest_lap(self, analysis_df: pd.DataFrame, vehicle_number: int) -> pd.Series:
        """Get fastest lap for a vehicle"""
        vehicle_laps = analysis_df[analysis_df['NUMBER'] == vehicle_number].copy()
        if len(vehicle_laps) == 0:
            return None
        return vehicle_laps.loc[vehicle_laps['lap_time_seconds'].idxmin()]


if __name__ == "__main__":
    # Test data loading
    loader = RaceDataLoader()
    
    print("Loading race results...")
    results = loader.load_race_results(race_num=1)
    print(f"✓ Loaded {len(results)} race results")
    print(f"  Columns: {list(results.columns[:5])}...")
    
    print("\nLoading lap times...")
    lap_times = loader.load_lap_times(race_num=1)
    print(f"✓ Loaded {len(lap_times)} lap records")
    print(f"  Vehicles: {lap_times['vehicle_number'].nunique()}")
    print(f"  Laps per vehicle: {lap_times.groupby('vehicle_number')['lap'].max().mean():.1f}")
    
    print("\nLoading analysis data...")
    analysis = loader.load_analysis_endurance(race_num=1)
    print(f"✓ Loaded {len(analysis)} lap analysis records")
    
    print("\n✅ All data loaded successfully!")
