"""
Racing Line Analysis
Analyzes GPS telemetry to identify optimal racing lines and coaching opportunities
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from scipy.spatial.distance import euclidean


class RacingLineAnalyzer:
    """Analyze racing lines using GPS and telemetry data"""
    
    def __init__(self):
        self.track_segments = None
        
    def extract_racing_line(self, telemetry_df: pd.DataFrame, vehicle_id: str, lap_num: int) -> pd.DataFrame:
        """
        Extract GPS racing line for a specific lap
        Returns DataFrame with GPS coordinates and telemetry
        """
        lap_data = telemetry_df[
            (telemetry_df['vehicle_id'] == vehicle_id) & 
            (telemetry_df['lap'] == lap_num)
        ].copy()
        
        if len(lap_data) == 0:
            return pd.DataFrame()
        
        # Sort by distance from start/finish
        if 'Laptrigger_lapdist_dls' in lap_data.columns:
            lap_data = lap_data.sort_values('Laptrigger_lapdist_dls')
        
        return lap_data
    
    def compare_racing_lines(
        self, 
        telemetry_df: pd.DataFrame,
        vehicle_id: str,
        fast_lap: int,
        slow_lap: int
    ) -> Dict:
        """
        Compare two laps to identify where time is lost/gained
        """
        fast_line = self.extract_racing_line(telemetry_df, vehicle_id, fast_lap)
        slow_line = self.extract_racing_line(telemetry_df, vehicle_id, slow_lap)
        
        if len(fast_line) == 0 or len(slow_line) == 0:
            return {'error': 'Insufficient data for comparison'}
        
        # Calculate average speed difference
        speed_diff = slow_line['Speed'].mean() - fast_line['Speed'].mean()
        
        # Find sections with biggest speed differences
        # This would require more sophisticated track segmentation
        
        return {
            'fast_lap': fast_lap,
            'slow_lap': slow_lap,
            'avg_speed_diff': round(speed_diff, 2),
            'fast_lap_avg_speed': round(fast_line['Speed'].mean(), 2),
            'slow_lap_avg_speed': round(slow_line['Speed'].mean(), 2),
            'data_points_fast': len(fast_line),
            'data_points_slow': len(slow_line)
        }
    
    def analyze_braking_points(
        self, 
        telemetry_df: pd.DataFrame,
        vehicle_id: str,
        lap_num: int
    ) -> List[Dict]:
        """
        Identify braking zones and analyze braking performance
        """
        lap_data = self.extract_racing_line(telemetry_df, vehicle_id, lap_num)
        
        if len(lap_data) == 0 or 'pbrake_f' not in lap_data.columns:
            return []
        
        # Find braking zones (front brake pressure > 10 bar)
        braking_threshold = 10
        lap_data['is_braking'] = lap_data['pbrake_f'] > braking_threshold
        
        # Identify braking zone starts
        lap_data['braking_start'] = (
            (~lap_data['is_braking'].shift(1, fill_value=False)) & 
            lap_data['is_braking']
        )
        
        braking_zones = []
        
        for idx in lap_data[lap_data['braking_start']].index:
            # Get braking zone data
            zone_start = idx
            zone_data = lap_data.loc[idx:]
            zone_data = zone_data[zone_data['is_braking']]
            
            if len(zone_data) == 0:
                continue
            
            zone_end = zone_data.index[-1]
            
            braking_zones.append({
                'start_distance': lap_data.loc[zone_start, 'Laptrigger_lapdist_dls'] if 'Laptrigger_lapdist_dls' in lap_data.columns else None,
                'entry_speed': lap_data.loc[zone_start, 'Speed'],
                'exit_speed': lap_data.loc[zone_end, 'Speed'],
                'max_brake_pressure': zone_data['pbrake_f'].max(),
                'max_decel_g': zone_data['accx_can'].min() if 'accx_can' in zone_data.columns else None,
                'duration_points': len(zone_data)
            })
        
        return braking_zones
    
    def find_coaching_opportunities(
        self,
        analysis_df: pd.DataFrame,
        vehicle_number: int,
        current_lap_data: pd.Series
    ) -> List[Dict]:
        """
        Compare current lap to best lap and identify specific improvements
        """
        # Get best lap for this vehicle
        vehicle_laps = analysis_df[analysis_df['NUMBER'] == vehicle_number].copy()
        
        if len(vehicle_laps) == 0:
            return []
        
        best_lap = vehicle_laps.loc[vehicle_laps['lap_time_seconds'].idxmin()]
        
        opportunities = []
        
        # Sector 1 analysis
        if 'S1_SECONDS' in current_lap_data.index:
            s1_delta = current_lap_data['S1_SECONDS'] - best_lap['S1_SECONDS']
            if s1_delta > 0.1:  # Losing more than 0.1s
                opportunities.append({
                    'sector': 'S1',
                    'time_loss': round(s1_delta, 3),
                    'message': f'Sector 1: {s1_delta:.3f}s slower than your best',
                    'suggestion': 'Focus on entry speed and early apex in Turn 1-3'
                })
        
        # Sector 2 analysis
        if 'S2_SECONDS' in current_lap_data.index:
            s2_delta = current_lap_data['S2_SECONDS'] - best_lap['S2_SECONDS']
            if s2_delta > 0.1:
                opportunities.append({
                    'sector': 'S2',
                    'time_loss': round(s2_delta, 3),
                    'message': f'Sector 2: {s2_delta:.3f}s slower than your best',
                    'suggestion': 'Check mid-corner speed and throttle application'
                })
        
        # Sector 3 analysis
        if 'S3_SECONDS' in current_lap_data.index:
            s3_delta = current_lap_data['S3_SECONDS'] - best_lap['S3_SECONDS']
            if s3_delta > 0.1:
                opportunities.append({
                    'sector': 'S3',
                    'time_loss': round(s3_delta, 3),
                    'message': f'Sector 3: {s3_delta:.3f}s slower than your best',
                    'suggestion': 'Maximize exit speed for main straight'
                })
        
        # Sort by time loss (biggest opportunities first)
        opportunities.sort(key=lambda x: x['time_loss'], reverse=True)
        
        return opportunities
    
    def calculate_potential_lap_time(
        self,
        analysis_df: pd.DataFrame,
        vehicle_number: int
    ) -> Dict:
        """
        Calculate theoretical best lap time using best sectors
        """
        vehicle_laps = analysis_df[analysis_df['NUMBER'] == vehicle_number].copy()
        
        if len(vehicle_laps) == 0:
            return {}
        
        best_s1 = vehicle_laps['S1_SECONDS'].min()
        best_s2 = vehicle_laps['S2_SECONDS'].min()
        best_s3 = vehicle_laps['S3_SECONDS'].min()
        
        theoretical_best = best_s1 + best_s2 + best_s3
        actual_best = vehicle_laps['lap_time_seconds'].min()
        
        improvement_potential = actual_best - theoretical_best
        
        return {
            'theoretical_best': round(theoretical_best, 3),
            'actual_best': round(actual_best, 3),
            'improvement_potential': round(improvement_potential, 3),
            'best_s1': round(best_s1, 3),
            'best_s2': round(best_s2, 3),
            'best_s3': round(best_s3, 3)
        }


if __name__ == "__main__":
    # Test racing line analysis
    import sys
    sys.path.append('.')
    from src.data_loader import RaceDataLoader
    
    loader = RaceDataLoader()
    analysis = loader.load_analysis_endurance(race_num=1)
    
    analyzer = RacingLineAnalyzer()
    
    # Test with vehicle #13
    vehicle_num = 13
    print(f"\n🏁 Racing Line Analysis for vehicle #{vehicle_num}")
    
    # Calculate theoretical best lap
    potential = analyzer.calculate_potential_lap_time(analysis, vehicle_num)
    print(f"\n⚡ Lap Time Potential:")
    print(f"  Actual best lap: {potential['actual_best']}s")
    print(f"  Theoretical best: {potential['theoretical_best']}s")
    print(f"  Improvement potential: {potential['improvement_potential']}s")
    print(f"  Best sectors: S1={potential['best_s1']}s, S2={potential['best_s2']}s, S3={potential['best_s3']}s")
    
    # Find coaching opportunities for lap 15
    vehicle_laps = analysis[analysis['NUMBER'] == vehicle_num]
    lap_15 = vehicle_laps[vehicle_laps['LAP_NUMBER'] == 15].iloc[0]
    
    opportunities = analyzer.find_coaching_opportunities(analysis, vehicle_num, lap_15)
    print(f"\n💡 Coaching Opportunities (Lap 15):")
    for opp in opportunities:
        print(f"  • {opp['message']}")
        print(f"    → {opp['suggestion']}")
    
    print("\n✅ Racing line analysis complete!")
