"""
RAG Dataset Generator for AI Race Engineer Training
Extracts insights from Toyota GR Cup telemetry and race data to create
question-answer pairs for training a conversational AI race engineer.
"""

import pandas as pd
import numpy as np
import json
from typing import List, Dict, Tuple
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from multi_track_loader import MultiTrackLoader
from track_config import list_available_tracks, get_track_info
from analysis.tire_degradation import TireDegradationAnalyzer
from analysis.cross_track_analysis import CrossTrackAnalyzer


class RaceEngineerRAGGenerator:
    """Generate training data for AI race engineer from real race data"""
    
    def __init__(self):
        self.loader = MultiTrackLoader()
        self.tire_analyzer = TireDegradationAnalyzer()
        self.cross_analyzer = CrossTrackAnalyzer()
        self.tracks = list_available_tracks()
        self.dataset = []
    
    def generate_complete_dataset(self, output_file: str = "race_engineer_rag_dataset.jsonl"):
        """Generate complete RAG dataset from all available data"""
        
        print("🏁 Generating RAG Dataset for AI Race Engineer Training")
        print("=" * 70)
        
        # 1. Track-specific insights
        print("\n📍 Generating track-specific insights...")
        self.generate_track_insights()
        
        # 2. Lap time analysis
        print("\n⏱️ Generating lap time analysis...")
        self.generate_lap_time_insights()
        
        # 3. Tire degradation patterns
        print("\n🛞 Generating tire degradation insights...")
        self.generate_tire_insights()
        
        # 4. Sector performance
        print("\n📊 Generating sector performance insights...")
        self.generate_sector_insights()
        
        # 5. Cross-track comparisons
        print("\n🌍 Generating cross-track insights...")
        self.generate_cross_track_insights()
        
        # 6. Race strategy
        print("\n🎯 Generating race strategy insights...")
        self.generate_strategy_insights()
        
        # 7. Vehicle performance
        print("\n🏎️ Generating vehicle performance insights...")
        self.generate_vehicle_insights()
        
        # 8. Weather and conditions
        print("\n🌤️ Generating weather insights...")
        self.generate_weather_insights()
        
        # Save dataset
        self.save_dataset(output_file)
        
        print(f"\n✅ Dataset generated: {len(self.dataset)} entries")
        print(f"📁 Saved to: {output_file}")
    
    def generate_track_insights(self):
        """Generate Q&A about track characteristics"""
        
        for track_name in self.tracks:
            try:
                track_info = get_track_info(track_name)
                
                # Basic track info
                self.add_entry(
                    question=f"What are the characteristics of {track_info.name}?",
                    answer=f"{track_info.name} is a {track_info.length_km}km ({track_info.length_km * 0.621371:.2f} mile) circuit with {track_info.turns} turns, running {track_info.direction}. It's known for its technical layout and challenging corners.",
                    context={
                        "track": track_name,
                        "category": "track_info",
                        "data_source": "track_config"
                    }
                )
                
                # Track difficulty
                self.add_entry(
                    question=f"How difficult is {track_info.name}?",
                    answer=f"With {track_info.turns} turns over {track_info.length_km}km, {track_info.name} presents a {'highly technical' if track_info.turns > 15 else 'balanced'} challenge. The {track_info.direction} direction requires specific setup considerations.",
                    context={
                        "track": track_name,
                        "category": "track_difficulty",
                        "turns": track_info.turns,
                        "length": track_info.length_km
                    }
                )
                
                # Track comparison
                if track_info.length_km > 5.0:
                    self.add_entry(
                        question=f"Is {track_info.name} a long or short track?",
                        answer=f"{track_info.name} is a long circuit at {track_info.length_km}km. This means longer lap times, more fuel consumption, and greater tire degradation per lap. Strategy becomes crucial for managing resources.",
                        context={"track": track_name, "category": "track_length"}
                    )
                
            except Exception as e:
                print(f"  ⚠️ Error processing {track_name}: {e}")
    
    def generate_lap_time_insights(self):
        """Generate Q&A about lap times and performance"""
        
        for track_name in self.tracks[:3]:  # Sample first 3 tracks
            try:
                lap_times = self.loader.load_lap_times(track_name, race_num=1)
                
                if 'value' in lap_times.columns:
                    # Convert milliseconds to seconds
                    lap_times['lap_sec'] = lap_times['value'] / 1000
                    
                    # Best lap analysis
                    best_lap = lap_times['lap_sec'].min()
                    avg_lap = lap_times['lap_sec'].mean()
                    
                    self.add_entry(
                        question=f"What was the fastest lap time at {track_name}?",
                        answer=f"The fastest lap at {track_name} was {best_lap:.3f} seconds ({best_lap/60:.0f}:{best_lap%60:.3f}). The average lap time was {avg_lap:.3f} seconds, showing a {((avg_lap-best_lap)/best_lap*100):.1f}% difference between the fastest and average pace.",
                        context={
                            "track": track_name,
                            "category": "lap_times",
                            "best_lap": float(best_lap),
                            "avg_lap": float(avg_lap)
                        }
                    )
                    
                    # Consistency analysis
                    lap_std = lap_times['lap_sec'].std()
                    self.add_entry(
                        question=f"How consistent were lap times at {track_name}?",
                        answer=f"Lap time consistency at {track_name} showed a standard deviation of {lap_std:.3f} seconds. {'Excellent' if lap_std < 1.0 else 'Good' if lap_std < 2.0 else 'Variable'} consistency indicates {'stable' if lap_std < 1.0 else 'developing'} track conditions and driver performance.",
                        context={
                            "track": track_name,
                            "category": "consistency",
                            "std_dev": float(lap_std)
                        }
                    )
                    
            except Exception as e:
                print(f"  ⚠️ Error processing lap times for {track_name}: {e}")
    
    def generate_tire_insights(self):
        """Generate Q&A about tire degradation"""
        
        # Generic tire degradation knowledge
        self.add_entry(
            question="How does tire degradation affect lap times?",
            answer="Tire degradation typically causes lap times to increase by 0.1-0.3 seconds per lap in the Toyota GR86. As the tire compound wears, grip decreases, requiring earlier braking points and slower corner speeds. Monitoring degradation helps determine optimal pit stop timing.",
            context={"category": "tire_degradation", "type": "general"}
        )
        
        self.add_entry(
            question="When should I pit for fresh tires?",
            answer="Pit for fresh tires when: 1) Lap times degrade by more than 1 second from your best, 2) You're losing positions due to pace, 3) A safety car provides a 'free' stop, or 4) Your strategy calls for an undercut. In a 27-lap race, typical pit windows are laps 12-15 or 18-22.",
            context={"category": "pit_strategy", "type": "tire_management"}
        )
        
        self.add_entry(
            question="What causes faster tire degradation?",
            answer="Tire degradation accelerates with: aggressive driving (hard braking, wheelspin), high track temperatures, abrasive track surfaces, and high-speed corners with sustained lateral loads. Smooth inputs and proper tire temperature management extend tire life.",
            context={"category": "tire_degradation", "type": "causes"}
        )
    
    def generate_sector_insights(self):
        """Generate Q&A about sector performance"""
        
        for track_name in self.tracks[:2]:  # Sample 2 tracks
            try:
                analysis = self.loader.load_analysis(track_name, race_num=1)
                
                if 'S1' in analysis.columns and 'S2' in analysis.columns and 'S3' in analysis.columns:
                    # Sector time analysis
                    s1_avg = analysis['S1'].mean()
                    s2_avg = analysis['S2'].mean()
                    s3_avg = analysis['S3'].mean()
                    
                    slowest_sector = max([('S1', s1_avg), ('S2', s2_avg), ('S3', s3_avg)], key=lambda x: x[1])
                    
                    self.add_entry(
                        question=f"Which sector is most challenging at {track_name}?",
                        answer=f"At {track_name}, {slowest_sector[0]} is the most time-consuming sector with an average time of {slowest_sector[1]:.3f} seconds. This sector requires particular focus for lap time improvement. Sector times: S1={s1_avg:.3f}s, S2={s2_avg:.3f}s, S3={s3_avg:.3f}s.",
                        context={
                            "track": track_name,
                            "category": "sector_analysis",
                            "slowest_sector": slowest_sector[0]
                        }
                    )
                    
            except Exception as e:
                print(f"  ⚠️ Error processing sectors for {track_name}: {e}")
    
    def generate_cross_track_insights(self):
        """Generate Q&A about performance across tracks"""
        
        self.add_entry(
            question="Which tracks are most similar in the Toyota GR Cup?",
            answer="Indianapolis and Sonoma are similar in length (both ~4.0km) but differ in character - Indianapolis combines oval banking with technical infield, while Sonoma is purely road course with elevation. Road America and Sebring are both long tracks (6.5km and 6.0km) requiring strong endurance and consistency.",
            context={"category": "track_comparison", "type": "similarity"}
        )
        
        self.add_entry(
            question="What's the difference between clockwise and counterclockwise tracks?",
            answer="Most tracks (Barber, Indianapolis, Sebring, Road America, Sonoma, VIR) run clockwise, while COTA runs counterclockwise. Counterclockwise tracks put different stresses on the car and driver - right-side tires work harder, and drivers experience different g-forces. Setup and driving technique must adapt accordingly.",
            context={"category": "track_direction", "type": "technical"}
        )
    
    def generate_strategy_insights(self):
        """Generate Q&A about race strategy"""
        
        self.add_entry(
            question="What's an undercut strategy?",
            answer="An undercut is pitting earlier than your competitor to gain track position. Fresh tires provide 1-2 seconds per lap advantage, allowing you to build a gap while they're on old tires. When they pit, you emerge ahead. Most effective when tire degradation is high and pit loss time is low.",
            context={"category": "race_strategy", "type": "undercut"}
        )
        
        self.add_entry(
            question="How do I manage fuel in a race?",
            answer="In Toyota GR Cup races, fuel management involves: 1) Calculating fuel consumption per lap (typically 2-3 liters), 2) Monitoring fuel level vs laps remaining, 3) Adjusting driving style if needed (lift-and-coast, short-shifting), 4) Planning pit stops to refuel if required. Running out of fuel costs more time than a slightly conservative pace.",
            context={"category": "race_strategy", "type": "fuel_management"}
        )
        
        self.add_entry(
            question="When should I push hard vs conserve?",
            answer="Push hard when: 1) Qualifying or setting fastest lap, 2) Defending position, 3) On fresh tires with clear track, 4) Final laps with nothing to lose. Conserve when: 1) Managing tire life for strategy, 2) Fuel-saving mode, 3) Maintaining comfortable gap, 4) Learning track in practice. Balance speed with sustainability.",
            context={"category": "race_strategy", "type": "pace_management"}
        )
    
    def generate_vehicle_insights(self):
        """Generate Q&A about vehicle performance"""
        
        self.add_entry(
            question="What are the key telemetry parameters to monitor?",
            answer="Critical telemetry includes: Speed (km/h), Throttle position (0-100%), Brake pressure (bar), Steering angle (degrees), Lateral/longitudinal G-forces, Gear selection, and Engine RPM. GPS position tracks racing line. Monitoring these helps identify areas for improvement and diagnose issues.",
            context={"category": "telemetry", "type": "parameters"}
        )
        
        self.add_entry(
            question="How do I analyze my braking performance?",
            answer="Analyze braking by examining: 1) Brake pressure (should be firm and consistent), 2) Braking point (earlier = safer, later = faster), 3) Trail braking (gradual release into corner), 4) Deceleration G-forces (higher = better). Compare your braking zones to faster drivers to find time gains.",
            context={"category": "driving_technique", "type": "braking"}
        )
        
        self.add_entry(
            question="What's the optimal racing line?",
            answer="The optimal racing line maximizes corner exit speed by: 1) Late apex in most corners, 2) Widest entry for shallow angle, 3) Hitting apex at minimum speed, 4) Unwinding steering on exit for maximum acceleration. Prioritize exits leading to straights - 'slow in, fast out' is faster overall.",
            context={"category": "driving_technique", "type": "racing_line"}
        )
    
    def generate_weather_insights(self):
        """Generate Q&A about weather and conditions"""
        
        self.add_entry(
            question="How does track temperature affect performance?",
            answer="Higher track temperatures (>40°C) increase tire degradation and reduce grip. Lower temperatures (<20°C) make it harder to bring tires up to operating temperature. Optimal track temp is 25-35°C. Adjust tire pressures and driving style based on conditions - smoother inputs in extreme temperatures.",
            context={"category": "weather", "type": "temperature"}
        )
        
        self.add_entry(
            question="What changes in wet conditions?",
            answer="In wet conditions: 1) Braking distances increase 50-100%, 2) Corner speeds reduce 20-30%, 3) Racing line changes (avoid painted lines, seek grip), 4) Visibility decreases, 5) Tire choice becomes critical (wet vs intermediate). Smooth inputs and patience are essential - crashes lose more time than conservative pace.",
            context={"category": "weather", "type": "wet_conditions"}
        )
    
    def add_entry(self, question: str, answer: str, context: Dict):
        """Add a Q&A entry to the dataset"""
        entry = {
            "question": question,
            "answer": answer,
            "context": context,
            "source": "toyota_gr_cup_telemetry",
            "domain": "motorsports_race_engineering"
        }
        self.dataset.append(entry)
    
    def save_dataset(self, output_file: str):
        """Save dataset in JSONL format for RAG training"""
        with open(output_file, 'w', encoding='utf-8') as f:
            for entry in self.dataset:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        
        # Also save as regular JSON for easier viewing
        json_file = output_file.replace('.jsonl', '.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.dataset, f, indent=2, ensure_ascii=False)
    
    def generate_statistics(self):
        """Generate statistics about the dataset"""
        categories = {}
        for entry in self.dataset:
            cat = entry['context'].get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1
        
        print("\n📊 Dataset Statistics:")
        print("-" * 70)
        print(f"Total entries: {len(self.dataset)}")
        print(f"\nBy category:")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print(f"  {cat}: {count}")


def main():
    """Generate RAG dataset"""
    generator = RaceEngineerRAGGenerator()
    generator.generate_complete_dataset()
    generator.generate_statistics()
    
    print("\n" + "=" * 70)
    print("✅ RAG Dataset Generation Complete!")
    print("\nUse this dataset to train an AI race engineer that can:")
    print("  • Answer questions about track characteristics")
    print("  • Provide lap time analysis and improvement tips")
    print("  • Explain tire degradation and pit strategy")
    print("  • Analyze sector performance")
    print("  • Compare performance across tracks")
    print("  • Give race strategy advice")
    print("  • Interpret telemetry data")
    print("  • Advise on weather conditions")
    print("=" * 70)


if __name__ == "__main__":
    main()
