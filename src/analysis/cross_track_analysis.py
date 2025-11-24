"""
Cross-Track Performance Analysis
Compare driver/vehicle performance across all 7 tracks
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from multi_track_loader import MultiTrackLoader
from track_config import get_track_info, list_available_tracks


class CrossTrackAnalyzer:
    """Analyze performance patterns across multiple tracks"""
    
    def __init__(self):
        self.loader = MultiTrackLoader()
        self.tracks = list_available_tracks()
    
    def get_vehicle_performance_matrix(self, vehicle_id: str, race_num: int = 1) -> pd.DataFrame:
        """
        Create a performance matrix for a vehicle across all tracks
        
        Returns DataFrame with columns:
        - track, best_lap, avg_lap, consistency, track_length, avg_speed
        """
        comparison = self.loader.compare_vehicle_across_tracks(vehicle_id, race_num)
        
        if comparison.empty:
            return pd.DataFrame()
        
        # Calculate consistency (std dev of lap times)
        consistency_data = []
        for _, row in comparison.iterrows():
            try:
                lap_times = self.loader.load_lap_times(row['track_short'], race_num)
                vehicle_laps = lap_times[lap_times['vehicle_id'].str.contains(vehicle_id, na=False)]
                
                if 'value' in vehicle_laps.columns:
                    lap_values = vehicle_laps['value'].dropna()
                    if len(lap_values) > 1:
                        consistency = lap_values.std() / lap_values.mean() * 100  # CV%
                    else:
                        consistency = 0
                else:
                    consistency = 0
                
                consistency_data.append(consistency)
            except:
                consistency_data.append(None)
        
        comparison['consistency_cv'] = consistency_data
        
        return comparison
    
    def find_strongest_tracks(self, vehicle_id: str, race_num: int = 1, top_n: int = 3) -> List[Dict]:
        """
        Identify which tracks a vehicle performs best at
        Based on relative position to field average
        """
        performance = self.get_vehicle_performance_matrix(vehicle_id, race_num)
        
        if performance.empty:
            return []
        
        # Calculate performance relative to track characteristics
        performance['speed_per_km'] = performance['avg_speed_kmh'] / performance['track_length_km']
        
        # Sort by best lap time (lower is better)
        strongest = performance.nsmallest(top_n, 'best_lap_sec')
        
        return strongest[['track', 'best_lap_sec', 'avg_speed_kmh', 'laps_completed']].to_dict('records')
    
    def compare_vehicles_at_track(self, track_name: str, race_num: int = 1, 
                                  top_n: int = 10) -> pd.DataFrame:
        """
        Compare all vehicles at a specific track
        Returns leaderboard with best lap times
        """
        try:
            lap_times = self.loader.load_lap_times(track_name, race_num)
            
            if 'value' not in lap_times.columns:
                return pd.DataFrame()
            
            # Group by vehicle and get best lap
            leaderboard = lap_times.groupby('vehicle_id').agg({
                'value': ['min', 'mean', 'count']
            }).reset_index()
            
            leaderboard.columns = ['vehicle_id', 'best_lap_ms', 'avg_lap_ms', 'laps']
            leaderboard['best_lap_sec'] = leaderboard['best_lap_ms'] / 1000
            leaderboard['avg_lap_sec'] = leaderboard['avg_lap_ms'] / 1000
            
            # Calculate gap to leader
            leader_time = leaderboard['best_lap_ms'].min()
            leaderboard['gap_to_leader_ms'] = leaderboard['best_lap_ms'] - leader_time
            leaderboard['gap_to_leader_sec'] = leaderboard['gap_to_leader_ms'] / 1000
            
            # Sort by best lap
            leaderboard = leaderboard.sort_values('best_lap_ms')
            leaderboard['position'] = range(1, len(leaderboard) + 1)
            
            track_info = get_track_info(track_name)
            leaderboard['track'] = track_info.name
            
            return leaderboard.head(top_n)
            
        except Exception as e:
            print(f"Error comparing vehicles at {track_name}: {e}")
            return pd.DataFrame()
    
    def get_track_difficulty_ranking(self, race_num: int = 1) -> pd.DataFrame:
        """
        Rank tracks by difficulty based on:
        - Average lap time variance
        - Number of incidents/outliers
        - Lap time spread across field
        """
        difficulty_scores = []
        
        for track_name in self.tracks:
            try:
                lap_times = self.loader.load_lap_times(track_name, race_num)
                track_info = get_track_info(track_name)
                
                if 'value' not in lap_times.columns or len(lap_times) == 0:
                    continue
                
                # Calculate metrics
                lap_values = lap_times['value'].dropna()
                
                # Field spread (difference between fastest and slowest)
                vehicle_best_laps = lap_times.groupby('vehicle_id')['value'].min()
                field_spread = vehicle_best_laps.max() - vehicle_best_laps.min()
                field_spread_pct = (field_spread / vehicle_best_laps.min()) * 100
                
                # Average consistency
                vehicle_consistency = []
                for vehicle in lap_times['vehicle_id'].unique():
                    v_laps = lap_times[lap_times['vehicle_id'] == vehicle]['value'].dropna()
                    if len(v_laps) > 1:
                        cv = v_laps.std() / v_laps.mean() * 100
                        vehicle_consistency.append(cv)
                
                avg_consistency = np.mean(vehicle_consistency) if vehicle_consistency else 0
                
                difficulty_scores.append({
                    'track': track_info.name,
                    'track_short': track_name,
                    'length_km': track_info.length_km,
                    'turns': track_info.turns,
                    'field_spread_pct': field_spread_pct,
                    'avg_consistency_cv': avg_consistency,
                    'difficulty_score': field_spread_pct * 0.6 + avg_consistency * 0.4
                })
                
            except Exception as e:
                print(f"Could not analyze {track_name}: {e}")
        
        if not difficulty_scores:
            return pd.DataFrame()
        
        df = pd.DataFrame(difficulty_scores)
        df = df.sort_values('difficulty_score', ascending=False)
        df['difficulty_rank'] = range(1, len(df) + 1)
        
        return df
    
    def get_championship_simulation(self, points_system: Optional[Dict[int, int]] = None) -> pd.DataFrame:
        """
        Simulate championship standings based on results from all tracks
        
        Args:
            points_system: Dict mapping position to points (default: F1 style)
        """
        if points_system is None:
            # Default F1-style points
            points_system = {
                1: 25, 2: 18, 3: 15, 4: 12, 5: 10,
                6: 8, 7: 6, 8: 4, 9: 2, 10: 1
            }
        
        all_results = []
        
        for track_name in self.tracks:
            for race_num in [1, 2]:
                try:
                    results = self.loader.load_results(track_name, race_num)
                    
                    if 'POS' in results.columns and 'NO' in results.columns:
                        # Assign points
                        results['points'] = results['POS'].apply(
                            lambda pos: points_system.get(int(pos), 0) if pd.notna(pos) else 0
                        )
                        all_results.append(results[['NO', 'points', 'track_name', 'race_number']])
                        
                except Exception as e:
                    continue
        
        if not all_results:
            return pd.DataFrame()
        
        combined = pd.concat(all_results, ignore_index=True)
        
        # Calculate championship standings
        standings = combined.groupby('NO').agg({
            'points': 'sum',
            'track_name': 'count'
        }).reset_index()
        
        standings.columns = ['vehicle_number', 'total_points', 'races_completed']
        standings = standings.sort_values('total_points', ascending=False)
        standings['championship_position'] = range(1, len(standings) + 1)
        
        return standings
    
    def analyze_track_type_performance(self, vehicle_id: str, race_num: int = 1) -> Dict:
        """
        Analyze performance by track characteristics
        - Short vs Long tracks
        - High turn count vs Low turn count
        - Clockwise vs Counterclockwise
        """
        performance = self.get_vehicle_performance_matrix(vehicle_id, race_num)
        
        if performance.empty:
            return {}
        
        # Add track characteristics
        for idx, row in performance.iterrows():
            track_info = get_track_info(row['track_short'])
            performance.at[idx, 'turns'] = track_info.turns
            performance.at[idx, 'direction'] = track_info.direction
        
        # Categorize tracks
        median_length = performance['track_length_km'].median()
        median_turns = performance['turns'].median()
        
        analysis = {
            'short_tracks': performance[performance['track_length_km'] <= median_length]['avg_speed_kmh'].mean(),
            'long_tracks': performance[performance['track_length_km'] > median_length]['avg_speed_kmh'].mean(),
            'technical_tracks': performance[performance['turns'] >= median_turns]['best_lap_sec'].mean(),
            'flowing_tracks': performance[performance['turns'] < median_turns]['best_lap_sec'].mean(),
            'clockwise': performance[performance['direction'] == 'clockwise']['avg_speed_kmh'].mean(),
            'counterclockwise': performance[performance['direction'] == 'counterclockwise']['avg_speed_kmh'].mean()
        }
        
        # Determine strengths
        strengths = []
        if analysis['short_tracks'] > analysis['long_tracks']:
            strengths.append("Better on short tracks")
        else:
            strengths.append("Better on long tracks")
        
        if analysis['technical_tracks'] < analysis['flowing_tracks']:
            strengths.append("Excels on technical tracks")
        else:
            strengths.append("Excels on flowing tracks")
        
        analysis['strengths'] = strengths
        
        return analysis


def generate_cross_track_report(vehicle_id: str, race_num: int = 1):
    """Generate comprehensive cross-track performance report"""
    analyzer = CrossTrackAnalyzer()
    
    print(f"\n{'='*70}")
    print(f"CROSS-TRACK PERFORMANCE REPORT")
    print(f"Vehicle: {vehicle_id} | Race: {race_num}")
    print(f"{'='*70}\n")
    
    # Performance matrix
    print("Performance Across All Tracks:")
    print("-" * 70)
    performance = analyzer.get_vehicle_performance_matrix(vehicle_id, race_num)
    if not performance.empty:
        print(performance[['track', 'best_lap_sec', 'avg_speed_kmh', 'laps_completed']].to_string(index=False))
    else:
        print("No data available")
    
    # Strongest tracks
    print("\n\nStrongest Tracks:")
    print("-" * 70)
    strongest = analyzer.find_strongest_tracks(vehicle_id, race_num)
    for i, track in enumerate(strongest, 1):
        print(f"{i}. {track['track']}: {track['best_lap_sec']:.3f}s @ {track['avg_speed_kmh']:.1f} km/h")
    
    # Track type analysis
    print("\n\nTrack Type Performance:")
    print("-" * 70)
    track_analysis = analyzer.analyze_track_type_performance(vehicle_id, race_num)
    if track_analysis:
        for strength in track_analysis.get('strengths', []):
            print(f"  • {strength}")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    # Example analysis
    generate_cross_track_report("GR86-013", race_num=1)
    
    # Track difficulty ranking
    print("\n\nTrack Difficulty Ranking:")
    print("="*70)
    analyzer = CrossTrackAnalyzer()
    difficulty = analyzer.get_track_difficulty_ranking(race_num=1)
    if not difficulty.empty:
        print(difficulty[['difficulty_rank', 'track', 'length_km', 'turns', 'difficulty_score']].to_string(index=False))
