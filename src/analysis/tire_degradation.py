"""
Tire Degradation Analysis - KILLER FEATURE
Predicts when tires need changing based on telemetry patterns
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, List
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


class TireDegradationAnalyzer:
    """Analyze tire wear patterns and predict pit stop timing"""
    
    def __init__(self):
        self.degradation_model = None
        
    def analyze_lap_degradation(self, analysis_df: pd.DataFrame, vehicle_number: int) -> pd.DataFrame:
        """
        Analyze how lap times degrade over a stint
        Returns DataFrame with lap-by-lap degradation metrics
        """
        vehicle_laps = analysis_df[analysis_df['NUMBER'] == vehicle_number].copy()
        
        if len(vehicle_laps) == 0:
            return pd.DataFrame()
        
        # Sort by lap number
        vehicle_laps = vehicle_laps.sort_values('LAP_NUMBER')
        
        # Calculate rolling average lap time (3-lap window)
        vehicle_laps['lap_time_rolling'] = vehicle_laps['lap_time_seconds'].rolling(
            window=3, min_periods=1
        ).mean()
        
        # Calculate degradation from best lap
        best_lap_time = vehicle_laps['lap_time_seconds'].min()
        vehicle_laps['delta_to_best'] = vehicle_laps['lap_time_seconds'] - best_lap_time
        
        # Calculate lap-to-lap delta
        vehicle_laps['lap_to_lap_delta'] = vehicle_laps['lap_time_seconds'].diff()
        
        # Estimate tire life percentage (simplified model)
        # Assumes linear degradation from lap 1 to typical stint length (15 laps)
        stint_length = 15
        vehicle_laps['estimated_tire_life'] = 100 - (
            (vehicle_laps['LAP_NUMBER'] / stint_length) * 100
        )
        vehicle_laps['estimated_tire_life'] = vehicle_laps['estimated_tire_life'].clip(0, 100)
        
        return vehicle_laps
    
    def predict_pit_window(
        self, 
        analysis_df: pd.DataFrame, 
        vehicle_number: int,
        current_lap: int,
        total_laps: int
    ) -> Dict:
        """
        Predict optimal pit window based on tire degradation
        
        Returns:
            dict with pit_lap, confidence, laps_remaining, time_loss_per_lap
        """
        vehicle_laps = self.analyze_lap_degradation(analysis_df, vehicle_number)
        
        if len(vehicle_laps) < 5:
            return {
                'pit_lap': None,
                'confidence': 0,
                'message': 'Insufficient data'
            }
        
        # Calculate degradation rate (seconds per lap)
        recent_laps = vehicle_laps[vehicle_laps['LAP_NUMBER'] >= current_lap - 5]
        
        if len(recent_laps) < 3:
            recent_laps = vehicle_laps.tail(5)
        
        # Fit linear model to predict degradation
        X = recent_laps['LAP_NUMBER'].values.reshape(-1, 1)
        y = recent_laps['delta_to_best'].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        degradation_rate = model.coef_[0]  # seconds per lap
        
        # Predict when degradation exceeds threshold (1.5 seconds slower than best)
        threshold = 1.5
        current_delta = model.predict([[current_lap]])[0]
        
        if degradation_rate > 0.01:  # Tires are degrading
            laps_until_threshold = (threshold - current_delta) / degradation_rate
            pit_lap = int(current_lap + laps_until_threshold)
            
            # Ensure pit lap is reasonable
            pit_lap = max(current_lap + 1, min(pit_lap, total_laps - 2))
            
            confidence = min(100, len(recent_laps) * 20)  # More data = more confidence
            
            return {
                'pit_lap': pit_lap,
                'laps_remaining': int(laps_until_threshold),
                'degradation_rate': round(degradation_rate, 3),
                'current_delta': round(current_delta, 3),
                'confidence': confidence,
                'message': f'Pit recommended in {int(laps_until_threshold)} laps'
            }
        else:
            return {
                'pit_lap': total_laps - 1,
                'laps_remaining': total_laps - current_lap,
                'degradation_rate': round(degradation_rate, 3),
                'confidence': 50,
                'message': 'Tires stable, can extend stint'
            }
    
    def analyze_sector_degradation(self, analysis_df: pd.DataFrame, vehicle_number: int) -> Dict:
        """
        Analyze which sectors degrade most over a stint
        Helps identify if front or rear tires are wearing faster
        """
        vehicle_laps = analysis_df[analysis_df['NUMBER'] == vehicle_number].copy()
        
        if len(vehicle_laps) < 5:
            return {}
        
        # Calculate sector degradation
        sectors = ['S1_SECONDS', 'S2_SECONDS', 'S3_SECONDS']
        degradation = {}
        
        for sector in sectors:
            if sector in vehicle_laps.columns:
                # Compare first 3 laps vs last 3 laps
                early_laps = vehicle_laps.head(3)[sector].mean()
                late_laps = vehicle_laps.tail(3)[sector].mean()
                
                degradation[sector] = {
                    'early_avg': round(early_laps, 3),
                    'late_avg': round(late_laps, 3),
                    'delta': round(late_laps - early_laps, 3),
                    'percent_change': round(((late_laps - early_laps) / early_laps) * 100, 2)
                }
        
        return degradation
    
    def compare_to_competitors(
        self, 
        analysis_df: pd.DataFrame, 
        vehicle_number: int,
        current_lap: int
    ) -> List[Dict]:
        """
        Compare tire degradation to competitors
        Identify if you're wearing tires faster/slower
        """
        # Get all vehicles' degradation at current lap
        all_vehicles = analysis_df['NUMBER'].unique()
        
        comparisons = []
        
        for competitor in all_vehicles:
            if competitor == vehicle_number:
                continue
            
            comp_laps = analysis_df[
                (analysis_df['NUMBER'] == competitor) & 
                (analysis_df['LAP_NUMBER'] <= current_lap)
            ]
            
            if len(comp_laps) < 3:
                continue
            
            # Calculate average degradation rate
            comp_laps = comp_laps.sort_values('LAP_NUMBER')
            best_lap = comp_laps['lap_time_seconds'].min()
            recent_avg = comp_laps.tail(3)['lap_time_seconds'].mean()
            
            degradation = recent_avg - best_lap
            
            comparisons.append({
                'vehicle_number': competitor,
                'degradation': round(degradation, 3),
                'recent_avg_lap': round(recent_avg, 3)
            })
        
        # Sort by degradation (least to most)
        comparisons.sort(key=lambda x: x['degradation'])
        
        return comparisons


if __name__ == "__main__":
    # Test tire degradation analysis
    import sys
    sys.path.append('.')
    from src.data_loader import RaceDataLoader
    
    loader = RaceDataLoader()
    analysis = loader.load_analysis_endurance(race_num=1)
    
    analyzer = TireDegradationAnalyzer()
    
    # Test with vehicle #13 (race winner)
    vehicle_num = 13
    print(f"\n🔍 Analyzing tire degradation for vehicle #{vehicle_num}")
    
    degradation = analyzer.analyze_lap_degradation(analysis, vehicle_num)
    print(f"\n✓ Analyzed {len(degradation)} laps")
    print(f"  Best lap: {degradation['lap_time_seconds'].min():.3f}s")
    print(f"  Worst lap: {degradation['lap_time_seconds'].max():.3f}s")
    print(f"  Average degradation: {degradation['delta_to_best'].mean():.3f}s")
    
    # Predict pit window at lap 15
    pit_prediction = analyzer.predict_pit_window(analysis, vehicle_num, current_lap=15, total_laps=27)
    print(f"\n🏁 Pit Window Prediction (Lap 15):")
    print(f"  Recommended pit lap: {pit_prediction['pit_lap']}")
    print(f"  Laps remaining on tires: {pit_prediction['laps_remaining']}")
    print(f"  Degradation rate: {pit_prediction['degradation_rate']}s/lap")
    print(f"  Confidence: {pit_prediction['confidence']}%")
    print(f"  Message: {pit_prediction['message']}")
    
    # Sector analysis
    sector_deg = analyzer.analyze_sector_degradation(analysis, vehicle_num)
    print(f"\n📊 Sector Degradation:")
    for sector, data in sector_deg.items():
        print(f"  {sector}: {data['delta']:+.3f}s ({data['percent_change']:+.2f}%)")
    
    print("\n✅ Tire degradation analysis complete!")
