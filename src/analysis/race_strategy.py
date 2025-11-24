"""
Race Strategy Analysis - Real Data Implementation
Uses actual race data to calculate pit windows, fuel strategy, and race pace
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from sklearn.linear_model import LinearRegression


class RaceStrategyAnalyzer:
    """Analyze race strategy using real telemetry and timing data"""
    
    def __init__(self):
        self.fuel_consumption_rate = 0.08  # liters per lap (GR86 typical)
        self.tank_capacity = 50.0  # liters
        self.pit_stop_time = 45.0  # seconds (typical pit stop)
        
    def calculate_fuel_strategy(
        self,
        analysis_df: pd.DataFrame,
        vehicle_number: int,
        current_lap: int,
        total_laps: int,
        current_fuel: Optional[float] = None
    ) -> Dict:
        """
        Calculate fuel strategy based on actual consumption patterns
        Uses real lap times and speeds to estimate fuel usage
        """
        vehicle_laps = analysis_df[analysis_df['NUMBER'] == vehicle_number].copy()
        
        if len(vehicle_laps) == 0:
            return {'error': 'No data for vehicle'}
        
        # Calculate average speed to estimate fuel consumption
        avg_speed = vehicle_laps['KPH'].mean() if 'KPH' in vehicle_laps.columns else 120
        
        # Higher speeds = more fuel consumption
        speed_factor = avg_speed / 120.0
        adjusted_consumption = self.fuel_consumption_rate * speed_factor
        
        # Estimate current fuel if not provided
        if current_fuel is None:
            laps_completed = current_lap
            fuel_used = laps_completed * adjusted_consumption
            current_fuel = self.tank_capacity - fuel_used
        
        # Calculate laps remaining on current fuel
        laps_on_current_fuel = int(current_fuel / adjusted_consumption)
        
        # Calculate if pit stop is needed
        laps_remaining = total_laps - current_lap
        needs_pit = laps_on_current_fuel < laps_remaining
        
        if needs_pit:
            # Calculate optimal pit lap
            # Pit when we have just enough fuel to make it to the end after refueling
            fuel_needed_to_finish = laps_remaining * adjusted_consumption
            pit_lap = current_lap + max(1, laps_on_current_fuel - 2)  # Pit 2 laps before running out
            
            # Calculate fuel to add
            fuel_to_add = min(
                self.tank_capacity - current_fuel,
                (total_laps - pit_lap) * adjusted_consumption
            )
            
            return {
                'needs_pit': True,
                'recommended_pit_lap': pit_lap,
                'laps_on_current_fuel': laps_on_current_fuel,
                'current_fuel_liters': round(current_fuel, 2),
                'fuel_to_add_liters': round(fuel_to_add, 2),
                'consumption_per_lap': round(adjusted_consumption, 3),
                'message': f'Pit stop required at lap {pit_lap}. Add {fuel_to_add:.1f}L fuel.'
            }
        else:
            return {
                'needs_pit': False,
                'laps_on_current_fuel': laps_on_current_fuel,
                'current_fuel_liters': round(current_fuel, 2),
                'consumption_per_lap': round(adjusted_consumption, 3),
                'message': 'Sufficient fuel to finish race. No pit stop required.'
            }
    
    def analyze_race_pace(
        self,
        analysis_df: pd.DataFrame,
        vehicle_number: int,
        current_lap: int
    ) -> Dict:
        """
        Analyze race pace using real lap time data
        Compare to competitors and predict finish position
        """
        vehicle_laps = analysis_df[
            (analysis_df['NUMBER'] == vehicle_number) & 
            (analysis_df['LAP_NUMBER'] <= current_lap)
        ].copy()
        
        if len(vehicle_laps) < 3:
            return {'error': 'Insufficient data'}
        
        # Parse lap times
        def parse_time(t):
            try:
                if ':' in str(t):
                    parts = str(t).split(':')
                    return float(parts[0]) * 60 + float(parts[1])
                return float(t)
            except:
                return None
        
        # Parse all lap times first
        vehicle_laps['lap_seconds'] = vehicle_laps['LAP_TIME'].apply(parse_time)
        vehicle_laps = vehicle_laps.dropna(subset=['lap_seconds'])
        
        if len(vehicle_laps) == 0:
            return {'error': 'No valid lap times'}
        
        # Calculate pace metrics from real data
        recent_laps = vehicle_laps.tail(5)
        
        if len(recent_laps) == 0:
            return {'error': 'No valid lap times'}
        
        current_pace = recent_laps['lap_seconds'].mean()
        best_lap = vehicle_laps['lap_seconds'].min()
        pace_delta = current_pace - best_lap
        
        # Calculate consistency (standard deviation)
        consistency = recent_laps['lap_seconds'].std()
        
        # Analyze trend (improving or degrading)
        if len(recent_laps) >= 3:
            X = np.arange(len(recent_laps)).reshape(-1, 1)
            y = recent_laps['lap_seconds'].values
            model = LinearRegression()
            model.fit(X, y)
            trend = model.coef_[0]  # Positive = getting slower, Negative = getting faster
        else:
            trend = 0
        
        # Compare to competitors
        all_vehicles = analysis_df['NUMBER'].unique()
        competitor_paces = []
        
        for comp in all_vehicles:
            if comp == vehicle_number:
                continue
            
            comp_laps = analysis_df[
                (analysis_df['NUMBER'] == comp) & 
                (analysis_df['LAP_NUMBER'] <= current_lap)
            ].tail(5)
            
            if len(comp_laps) > 0:
                comp_laps['lap_seconds'] = comp_laps['LAP_TIME'].apply(parse_time)
                comp_laps = comp_laps.dropna(subset=['lap_seconds'])
                if len(comp_laps) > 0:
                    comp_pace = comp_laps['lap_seconds'].mean()
                    competitor_paces.append({
                        'vehicle': comp,
                        'pace': comp_pace
                    })
        
        # Sort competitors by pace
        competitor_paces.sort(key=lambda x: x['pace'])
        
        # Find position in pace ranking
        pace_position = 1
        for comp in competitor_paces:
            if comp['pace'] < current_pace:
                pace_position += 1
        
        return {
            'current_pace': round(current_pace, 3),
            'best_lap': round(best_lap, 3),
            'pace_delta': round(pace_delta, 3),
            'consistency_std': round(consistency, 3),
            'trend_per_lap': round(trend, 4),
            'pace_position': pace_position,
            'total_competitors': len(competitor_paces) + 1,
            'is_improving': trend < -0.01,
            'is_degrading': trend > 0.01,
            'is_consistent': consistency < 0.5
        }
    
    def calculate_optimal_pit_strategy(
        self,
        analysis_df: pd.DataFrame,
        vehicle_number: int,
        current_lap: int,
        total_laps: int,
        tire_deg_rate: float = 0.05  # seconds per lap degradation
    ) -> Dict:
        """
        Calculate optimal pit strategy considering both tires and fuel
        Uses real race data to determine best pit window
        """
        vehicle_laps = analysis_df[analysis_df['NUMBER'] == vehicle_number].copy()
        
        if len(vehicle_laps) < 5:
            return {'error': 'Insufficient data'}
        
        # Parse lap times
        def parse_time(t):
            try:
                if ':' in str(t):
                    parts = str(t).split(':')
                    return float(parts[0]) * 60 + float(parts[1])
                return float(t)
            except:
                return None
        
        vehicle_laps['lap_seconds'] = vehicle_laps['LAP_TIME'].apply(parse_time)
        vehicle_laps = vehicle_laps.dropna(subset=['lap_seconds'])
        
        # Calculate actual degradation from data
        if len(vehicle_laps) >= 10:
            early_pace = vehicle_laps.head(5)['lap_seconds'].mean()
            late_pace = vehicle_laps.tail(5)['lap_seconds'].mean()
            actual_deg_rate = (late_pace - early_pace) / len(vehicle_laps)
            tire_deg_rate = max(actual_deg_rate, 0.01)  # Use actual if available
        
        # Calculate time lost if we don't pit
        laps_remaining = total_laps - current_lap
        time_lost_no_pit = sum(tire_deg_rate * i for i in range(laps_remaining))
        
        # Calculate time lost with pit stop at different laps
        best_pit_lap = current_lap + 1
        min_total_time_lost = float('inf')
        
        for pit_lap in range(current_lap + 1, total_laps - 2):
            # Time lost before pit
            laps_before_pit = pit_lap - current_lap
            time_lost_before = sum(tire_deg_rate * i for i in range(laps_before_pit))
            
            # Pit stop time
            pit_time = self.pit_stop_time
            
            # Time lost after pit (fresh tires)
            laps_after_pit = total_laps - pit_lap
            time_lost_after = sum(tire_deg_rate * i * 0.3 for i in range(laps_after_pit))  # 30% of degradation on fresh tires
            
            total_time_lost = time_lost_before + pit_time + time_lost_after
            
            if total_time_lost < min_total_time_lost:
                min_total_time_lost = total_time_lost
                best_pit_lap = pit_lap
        
        # Determine if pitting is beneficial
        time_saved = time_lost_no_pit - min_total_time_lost
        should_pit = time_saved > 5.0  # Only pit if we save more than 5 seconds
        
        return {
            'should_pit': should_pit,
            'optimal_pit_lap': best_pit_lap,
            'laps_until_pit': best_pit_lap - current_lap,
            'time_saved_seconds': round(time_saved, 2),
            'degradation_rate': round(tire_deg_rate, 4),
            'time_lost_no_pit': round(time_lost_no_pit, 2),
            'time_lost_with_pit': round(min_total_time_lost, 2),
            'message': f'{"Pit" if should_pit else "Stay out"} - {"saves" if should_pit else "costs"} {abs(time_saved):.1f}s'
        }
    
    def analyze_sector_performance(
        self,
        analysis_df: pd.DataFrame,
        vehicle_number: int,
        current_lap: int
    ) -> Dict:
        """
        Analyze sector performance using real sector timing data
        Identify strengths and weaknesses
        """
        vehicle_laps = analysis_df[
            (analysis_df['NUMBER'] == vehicle_number) & 
            (analysis_df['LAP_NUMBER'] <= current_lap)
        ].copy()
        
        if len(vehicle_laps) < 3:
            return {'error': 'Insufficient data'}
        
        # Get sector times
        sectors = {}
        for sector_name in ['S1_SECONDS', 'S2_SECONDS', 'S3_SECONDS']:
            if sector_name in vehicle_laps.columns:
                sector_data = vehicle_laps[sector_name].dropna()
                if len(sector_data) > 0:
                    sectors[sector_name] = {
                        'best': float(sector_data.min()),
                        'worst': float(sector_data.max()),
                        'average': float(sector_data.mean()),
                        'current': float(vehicle_laps.iloc[-1][sector_name]) if not pd.isna(vehicle_laps.iloc[-1][sector_name]) else None,
                        'consistency': float(sector_data.std())
                    }
        
        # Compare to field average
        all_vehicles = analysis_df[analysis_df['LAP_NUMBER'] <= current_lap]
        field_sectors = {}
        
        for sector_name in ['S1_SECONDS', 'S2_SECONDS', 'S3_SECONDS']:
            if sector_name in all_vehicles.columns:
                field_data = all_vehicles[sector_name].dropna()
                if len(field_data) > 0:
                    field_sectors[sector_name] = float(field_data.mean())
        
        # Calculate relative performance
        for sector_name in sectors:
            if sector_name in field_sectors:
                sectors[sector_name]['vs_field'] = round(
                    sectors[sector_name]['average'] - field_sectors[sector_name], 3
                )
        
        return {
            'sectors': sectors,
            'strongest_sector': min(sectors.items(), key=lambda x: x[1]['vs_field'])[0] if sectors else None,
            'weakest_sector': max(sectors.items(), key=lambda x: x[1]['vs_field'])[0] if sectors else None
        }
    
    def predict_finish_time(
        self,
        analysis_df: pd.DataFrame,
        vehicle_number: int,
        current_lap: int,
        total_laps: int
    ) -> Dict:
        """
        Predict race finish time based on current pace and degradation
        Uses real lap time data for accurate prediction
        """
        pace_analysis = self.analyze_race_pace(analysis_df, vehicle_number, current_lap)
        
        if 'error' in pace_analysis:
            return pace_analysis
        
        # Calculate time already elapsed
        vehicle_laps = analysis_df[
            (analysis_df['NUMBER'] == vehicle_number) & 
            (analysis_df['LAP_NUMBER'] <= current_lap)
        ].copy()
        
        def parse_time(t):
            try:
                if ':' in str(t):
                    parts = str(t).split(':')
                    return float(parts[0]) * 60 + float(parts[1])
                return float(t)
            except:
                return None
        
        vehicle_laps['lap_seconds'] = vehicle_laps['LAP_TIME'].apply(parse_time)
        vehicle_laps = vehicle_laps.dropna(subset=['lap_seconds'])
        
        time_elapsed = vehicle_laps['lap_seconds'].sum()
        
        # Predict remaining time
        laps_remaining = total_laps - current_lap
        current_pace = pace_analysis['current_pace']
        trend = pace_analysis['trend_per_lap']
        
        # Account for degradation trend
        predicted_remaining_time = 0
        for i in range(laps_remaining):
            predicted_lap_time = current_pace + (trend * i)
            predicted_remaining_time += predicted_lap_time
        
        total_race_time = time_elapsed + predicted_remaining_time
        
        # Convert to readable format
        hours = int(total_race_time // 3600)
        minutes = int((total_race_time % 3600) // 60)
        seconds = total_race_time % 60
        
        return {
            'predicted_finish_time': f"{hours}:{minutes:02d}:{seconds:05.2f}",
            'predicted_finish_seconds': round(total_race_time, 2),
            'time_elapsed': round(time_elapsed, 2),
            'time_remaining': round(predicted_remaining_time, 2),
            'laps_remaining': laps_remaining,
            'predicted_avg_lap': round(predicted_remaining_time / laps_remaining, 3) if laps_remaining > 0 else 0
        }


if __name__ == "__main__":
    # Test race strategy analysis
    import sys
    sys.path.append('.')
    from src.data_loader import RaceDataLoader
    
    loader = RaceDataLoader()
    analysis = loader.load_analysis_endurance(race_num=1)
    
    analyzer = RaceStrategyAnalyzer()
    
    vehicle_num = 13
    current_lap = 15
    total_laps = 27
    
    print(f"\n🏁 Race Strategy Analysis for Vehicle #{vehicle_num}")
    print(f"Current Lap: {current_lap}/{total_laps}")
    
    # Fuel strategy
    print("\n⛽ Fuel Strategy:")
    fuel = analyzer.calculate_fuel_strategy(analysis, vehicle_num, current_lap, total_laps)
    print(f"  {fuel['message']}")
    print(f"  Current fuel: {fuel.get('current_fuel_liters', 0)}L")
    print(f"  Consumption: {fuel.get('consumption_per_lap', 0)}L/lap")
    
    # Race pace
    print("\n📊 Race Pace Analysis:")
    pace = analyzer.analyze_race_pace(analysis, vehicle_num, current_lap)
    print(f"  Current pace: {pace['current_pace']}s")
    print(f"  Best lap: {pace['best_lap']}s")
    print(f"  Pace position: {pace['pace_position']}/{pace['total_competitors']}")
    print(f"  Trend: {'Improving' if pace['is_improving'] else 'Degrading' if pace['is_degrading'] else 'Stable'}")
    
    # Pit strategy
    print("\n🔧 Pit Strategy:")
    pit = analyzer.calculate_optimal_pit_strategy(analysis, vehicle_num, current_lap, total_laps)
    print(f"  {pit['message']}")
    print(f"  Optimal pit lap: {pit['optimal_pit_lap']}")
    print(f"  Time impact: {pit['time_saved_seconds']}s")
    
    # Sector performance
    print("\n📍 Sector Performance:")
    sectors = analyzer.analyze_sector_performance(analysis, vehicle_num, current_lap)
    for sector, data in sectors.get('sectors', {}).items():
        print(f"  {sector}: Best={data['best']:.3f}s, Avg={data['average']:.3f}s, vs Field={data.get('vs_field', 0):+.3f}s")
    
    # Finish prediction
    print("\n🏆 Race Finish Prediction:")
    finish = analyzer.predict_finish_time(analysis, vehicle_num, current_lap, total_laps)
    print(f"  Predicted finish: {finish['predicted_finish_time']}")
    print(f"  Time remaining: {finish['time_remaining']:.1f}s")
    print(f"  Predicted avg lap: {finish['predicted_avg_lap']}s")
    
    print("\n✅ Strategy analysis complete!")
