"""
RaceIQ Dashboard Visualizations
Creates charts and graphs for race strategy analysis
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path
import sys
sys.path.append('.')

from src.data_loader import RaceDataLoader
from src.analysis.tire_degradation import TireDegradationAnalyzer
from src.analysis.racing_line import RacingLineAnalyzer

# Set style
sns.set_style("darkgrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

class RaceIQDashboard:
    """Generate visualizations for RaceIQ"""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.loader = RaceDataLoader()
        self.tire_analyzer = TireDegradationAnalyzer()
        self.line_analyzer = RacingLineAnalyzer()
        
    def plot_tire_degradation(self, analysis_df: pd.DataFrame, vehicle_number: int):
        """Plot tire degradation over race stint"""
        degradation = self.tire_analyzer.analyze_lap_degradation(analysis_df, vehicle_number)
        
        if len(degradation) == 0:
            print(f"No data for vehicle #{vehicle_number}")
            return
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        
        # Plot 1: Lap times with degradation
        ax1.plot(degradation['LAP_NUMBER'], degradation['lap_time_seconds'], 
                'o-', linewidth=2, markersize=6, label='Lap Time', color='#e74c3c')
        ax1.plot(degradation['LAP_NUMBER'], degradation['lap_time_rolling'], 
                '--', linewidth=2, label='3-Lap Average', color='#3498db')
        ax1.axhline(y=degradation['lap_time_seconds'].min(), 
                   linestyle=':', color='green', label='Best Lap', alpha=0.7)
        
        ax1.set_xlabel('Lap Number', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Lap Time (seconds)', fontsize=12, fontweight='bold')
        ax1.set_title(f'Vehicle #{vehicle_number} - Tire Degradation Analysis', 
                     fontsize=14, fontweight='bold')
        ax1.legend(loc='upper left')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Tire life estimation
        ax2.fill_between(degradation['LAP_NUMBER'], 0, degradation['estimated_tire_life'],
                        alpha=0.6, color='#2ecc71', label='Tire Life %')
        ax2.plot(degradation['LAP_NUMBER'], degradation['estimated_tire_life'],
                'o-', linewidth=2, markersize=4, color='#27ae60')
        ax2.axhline(y=50, linestyle='--', color='orange', label='50% Life', alpha=0.7)
        ax2.axhline(y=20, linestyle='--', color='red', label='Critical (20%)', alpha=0.7)
        
        ax2.set_xlabel('Lap Number', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Estimated Tire Life (%)', fontsize=12, fontweight='bold')
        ax2.set_title('Tire Life Estimation', fontsize=12, fontweight='bold')
        ax2.set_ylim(0, 105)
        ax2.legend(loc='upper right')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        output_file = self.output_dir / f'tire_degradation_vehicle_{vehicle_number}.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {output_file}")
        plt.close()
        
    def plot_sector_comparison(self, analysis_df: pd.DataFrame, vehicle_number: int):
        """Plot sector times comparison"""
        vehicle_laps = analysis_df[analysis_df['NUMBER'] == vehicle_number].copy()
        
        if len(vehicle_laps) == 0:
            return
        
        fig, axes = plt.subplots(1, 3, figsize=(16, 5))
        
        sectors = ['S1_SECONDS', 'S2_SECONDS', 'S3_SECONDS']
        colors = ['#e74c3c', '#3498db', '#2ecc71']
        
        for idx, (sector, color) in enumerate(zip(sectors, colors)):
            ax = axes[idx]
            
            # Plot sector times
            ax.plot(vehicle_laps['LAP_NUMBER'], vehicle_laps[sector], 
                   'o-', linewidth=2, markersize=5, color=color, alpha=0.7)
            
            # Add best sector line
            best_sector = vehicle_laps[sector].min()
            ax.axhline(y=best_sector, linestyle='--', color='green', 
                      label=f'Best: {best_sector:.3f}s', alpha=0.7)
            
            ax.set_xlabel('Lap Number', fontsize=11, fontweight='bold')
            ax.set_ylabel('Time (seconds)', fontsize=11, fontweight='bold')
            ax.set_title(f'Sector {idx+1}', fontsize=12, fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3)
        
        plt.suptitle(f'Vehicle #{vehicle_number} - Sector Analysis', 
                    fontsize=14, fontweight='bold', y=1.02)
        plt.tight_layout()
        
        output_file = self.output_dir / f'sector_analysis_vehicle_{vehicle_number}.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {output_file}")
        plt.close()
        
    def plot_race_pace_comparison(self, analysis_df: pd.DataFrame, top_n: int = 5):
        """Compare race pace of top finishers"""
        # Get top N finishers
        top_vehicles = analysis_df.groupby('NUMBER')['lap_time_seconds'].mean().nsmallest(top_n)
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        colors = plt.cm.Set3(np.linspace(0, 1, top_n))
        
        for idx, (vehicle_num, _) in enumerate(top_vehicles.items()):
            vehicle_laps = analysis_df[analysis_df['NUMBER'] == vehicle_num].copy()
            vehicle_laps = vehicle_laps.sort_values('LAP_NUMBER')
            
            ax.plot(vehicle_laps['LAP_NUMBER'], vehicle_laps['lap_time_seconds'],
                   'o-', linewidth=2, markersize=4, label=f'Car #{vehicle_num}',
                   color=colors[idx], alpha=0.8)
        
        ax.set_xlabel('Lap Number', fontsize=12, fontweight='bold')
        ax.set_ylabel('Lap Time (seconds)', fontsize=12, fontweight='bold')
        ax.set_title('Race Pace Comparison - Top 5 Finishers', 
                    fontsize=14, fontweight='bold')
        ax.legend(loc='upper right', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        output_file = self.output_dir / 'race_pace_comparison.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {output_file}")
        plt.close()
        
    def create_strategy_dashboard(self, vehicle_number: int, current_lap: int = 15):
        """Create comprehensive strategy dashboard for a vehicle"""
        analysis = self.loader.load_analysis_endurance(race_num=1)
        
        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
        
        # 1. Tire degradation
        ax1 = fig.add_subplot(gs[0, :])
        degradation = self.tire_analyzer.analyze_lap_degradation(analysis, vehicle_number)
        ax1.plot(degradation['LAP_NUMBER'], degradation['lap_time_seconds'], 
                'o-', linewidth=2, markersize=5, color='#e74c3c')
        ax1.axvline(x=current_lap, linestyle='--', color='orange', 
                   label=f'Current Lap: {current_lap}', linewidth=2)
        ax1.set_title(f'Vehicle #{vehicle_number} - Live Race Strategy Dashboard', 
                     fontsize=14, fontweight='bold')
        ax1.set_xlabel('Lap Number')
        ax1.set_ylabel('Lap Time (s)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Pit prediction
        ax2 = fig.add_subplot(gs[1, 0])
        pit_pred = self.tire_analyzer.predict_pit_window(analysis, vehicle_number, current_lap, 27)
        
        info_text = f"""
        PIT WINDOW PREDICTION
        
        Recommended Pit Lap: {pit_pred['pit_lap']}
        Laps Remaining: {pit_pred['laps_remaining']}
        Degradation Rate: {pit_pred['degradation_rate']}s/lap
        Confidence: {pit_pred['confidence']}%
        
        Status: {pit_pred['message']}
        """
        ax2.text(0.1, 0.5, info_text, fontsize=11, verticalalignment='center',
                family='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        ax2.axis('off')
        
        # 3. Lap potential
        ax3 = fig.add_subplot(gs[1, 1])
        potential = self.line_analyzer.calculate_potential_lap_time(analysis, vehicle_number)
        
        potential_text = f"""
        LAP TIME POTENTIAL
        
        Actual Best: {potential['actual_best']}s
        Theoretical Best: {potential['theoretical_best']}s
        Improvement: {potential['improvement_potential']}s
        
        Best Sectors:
        S1: {potential['best_s1']}s
        S2: {potential['best_s2']}s
        S3: {potential['best_s3']}s
        """
        ax3.text(0.1, 0.5, potential_text, fontsize=11, verticalalignment='center',
                family='monospace', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
        ax3.axis('off')
        
        # 4. Sector degradation
        ax4 = fig.add_subplot(gs[2, :])
        sector_deg = self.tire_analyzer.analyze_sector_degradation(analysis, vehicle_number)
        
        sectors = list(sector_deg.keys())
        deltas = [sector_deg[s]['delta'] for s in sectors]
        colors_bar = ['red' if d > 0 else 'green' for d in deltas]
        
        ax4.bar(range(len(sectors)), deltas, color=colors_bar, alpha=0.7)
        ax4.set_xticks(range(len(sectors)))
        ax4.set_xticklabels(['Sector 1', 'Sector 2', 'Sector 3'])
        ax4.set_ylabel('Degradation (seconds)')
        ax4.set_title('Sector Degradation (Early vs Late Stint)')
        ax4.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax4.grid(True, alpha=0.3, axis='y')
        
        plt.suptitle(f'RaceIQ - Real-Time Strategy Dashboard', 
                    fontsize=16, fontweight='bold', y=0.98)
        
        output_file = self.output_dir / f'strategy_dashboard_vehicle_{vehicle_number}.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {output_file}")
        plt.close()


if __name__ == "__main__":
    print("🎨 Generating RaceIQ visualizations...")
    
    dashboard = RaceIQDashboard()
    analysis = dashboard.loader.load_analysis_endurance(race_num=1)
    
    # Generate visualizations for race winner (car #13)
    vehicle_num = 13
    
    print(f"\n📊 Creating visualizations for vehicle #{vehicle_num}...")
    dashboard.plot_tire_degradation(analysis, vehicle_num)
    dashboard.plot_sector_comparison(analysis, vehicle_num)
    dashboard.create_strategy_dashboard(vehicle_num, current_lap=15)
    
    print("\n📈 Creating race pace comparison...")
    dashboard.plot_race_pace_comparison(analysis, top_n=5)
    
    print(f"\n✅ All visualizations saved to '{dashboard.output_dir}' directory!")
    print("\n🏁 RaceIQ Dashboard complete!")
