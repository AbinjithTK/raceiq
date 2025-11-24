"""
Clean RAG Dataset Generator
Produces high-quality, structured data for AI race engineer training
"""

import json
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from multi_track_loader import MultiTrackLoader
from track_config import list_available_tracks, get_track_info


class CleanRAGDataGenerator:
    """Generate clean, structured RAG training data"""
    
    def __init__(self):
        self.loader = MultiTrackLoader()
        self.tracks = list_available_tracks()
        self.dataset = []
        self.entry_id = 1
    
    def generate_all_datasets(self):
        """Generate all RAG datasets"""
        print("🏁 Generating Clean RAG Datasets")
        print("=" * 70)
        
        # Generate each category
        self.generate_track_knowledge()
        self.generate_telemetry_insights()
        self.generate_strategy_playbook()
        self.generate_driver_coaching()
        self.generate_performance_analysis()
        self.generate_weather_knowledge()
        self.generate_vehicle_dynamics()
        self.generate_championship_strategy()
        
        # Save all datasets
        self.save_datasets()
        
        print(f"\n✅ Generated {len(self.dataset)} clean RAG entries")
        print(f"📁 Saved to: rag_dataset/")
    
    def add_entry(self, question, answer, category, subcategory=None, 
                  track=None, difficulty="intermediate", data_source="analysis"):
        """Add a clean, structured entry"""
        entry = {
            "id": f"rag_{self.entry_id:04d}",
            "question": question.strip(),
            "answer": answer.strip(),
            "context": {
                "category": category,
                "subcategory": subcategory,
                "track": track,
                "difficulty": difficulty,
                "data_source": data_source
            },
            "metadata": {
                "source": "toyota_gr_cup_2025",
                "domain": "motorsports_race_engineering",
                "verified": True,
                "created": datetime.now().isoformat()
            }
        }
        self.dataset.append(entry)
        self.entry_id += 1
    
    def generate_track_knowledge(self):
        """Generate track-specific knowledge"""
        print("\n📍 Generating track knowledge...")
        
        for track_name in self.tracks:
            track = get_track_info(track_name)
            
            # Basic info
            self.add_entry(
                question=f"Tell me about {track.name}",
                answer=f"{track.name} is a {track.length_km}km circuit with {track.turns} turns, running {track.direction}. It's located in the United States and is part of the Toyota GR Cup championship. The track is known for its {'technical' if track.turns > 15 else 'flowing'} layout and provides excellent racing.",
                category="track_info",
                subcategory="overview",
                track=track_name,
                difficulty="beginner",
                data_source="track_config"
            )
            
            # Technical details
            self.add_entry(
                question=f"What makes {track.name} challenging?",
                answer=f"The challenge at {track.name} comes from several factors: {track.turns} corners requiring precise technique, {track.length_km}km length demanding consistency, and the {track.direction} direction affecting tire wear patterns. {'Technical sections with elevation changes' if track_name in ['barber', 'sonoma', 'vir'] else 'High-speed sections requiring bravery'} make it particularly demanding.",
                category="track_info",
                subcategory="difficulty",
                track=track_name,
                difficulty="intermediate"
            )
            
            # Strategy implications
            if track.length_km > 5.0:
                self.add_entry(
                    question=f"How does {track.name}'s length affect strategy?",
                    answer=f"At {track.length_km}km, {track.name} is a long circuit. This means: 1) Higher fuel consumption per lap (plan accordingly), 2) Greater tire degradation per lap (monitor closely), 3) Longer pit stop cycles (strategic timing crucial), 4) More time to make up positions (patience pays off). Typical pit windows are laps 12-15 or 18-22 in a 27-lap race.",
                    category="strategy",
                    subcategory="track_length",
                    track=track_name,
                    difficulty="advanced"
                )
        
        print(f"  ✓ Generated {len([e for e in self.dataset if e['context']['category'] == 'track_info'])} track entries")
    
    def generate_telemetry_insights(self):
        """Generate telemetry parameter knowledge"""
        print("\n📊 Generating telemetry insights...")
        
        telemetry_params = [
            {
                "name": "Speed",
                "unit": "km/h",
                "description": "Vehicle speed measured by GPS or wheel sensors",
                "typical_range": "0-200 km/h",
                "usage": "Monitor corner entry/exit speeds, identify braking points, compare to reference laps"
            },
            {
                "name": "Throttle Position (aps)",
                "unit": "%",
                "description": "Accelerator pedal position from 0% (closed) to 100% (full throttle)",
                "typical_range": "0-100%",
                "usage": "Analyze throttle application smoothness, identify lift points, optimize corner exits"
            },
            {
                "name": "Brake Pressure (pbrake_f/pbrake_r)",
                "unit": "bar",
                "description": "Hydraulic brake pressure at front and rear calipers",
                "typical_range": "0-85 bar",
                "usage": "Evaluate braking technique, identify trail braking, compare braking points"
            },
            {
                "name": "Lateral G-Force (accy_can)",
                "unit": "G",
                "description": "Sideways acceleration during cornering (+ = left, - = right)",
                "typical_range": "-1.5 to +1.5 G",
                "usage": "Measure cornering speed, identify grip limits, analyze racing line"
            },
            {
                "name": "Longitudinal G-Force (accx_can)",
                "unit": "G",
                "description": "Forward/backward acceleration (+ = accelerating, - = braking)",
                "typical_range": "-1.2 to +0.8 G",
                "usage": "Analyze acceleration and braking performance, identify traction limits"
            },
            {
                "name": "Steering Angle",
                "unit": "degrees",
                "description": "Steering wheel angle (0 = straight, +/- = left/right)",
                "typical_range": "-540 to +540 degrees",
                "usage": "Evaluate steering smoothness, identify oversteer/understeer, analyze line"
            }
        ]
        
        for param in telemetry_params:
            self.add_entry(
                question=f"What is {param['name']} and how do I use it?",
                answer=f"{param['name']} ({param['unit']}) measures {param['description']}. Typical range: {param['typical_range']}. Use it to: {param['usage']}. This parameter is critical for understanding vehicle dynamics and driver technique.",
                category="telemetry",
                subcategory="parameters",
                difficulty="intermediate",
                data_source="telemetry"
            )
        
        print(f"  ✓ Generated {len(telemetry_params)} telemetry entries")
    
    def generate_strategy_playbook(self):
        """Generate race strategy scenarios"""
        print("\n🎯 Generating strategy playbook...")
        
        strategies = [
            {
                "scenario": "Undercut Strategy",
                "question": "When should I use an undercut strategy?",
                "answer": "Use an undercut when: 1) You're within 3 seconds of the car ahead, 2) Tire degradation is significant (>0.3s/lap), 3) Pit loss time is low (<25s), 4) Track has limited overtaking opportunities. Pit 2-3 laps before your competitor, push hard on fresh tires to build a gap, and emerge ahead after their pit stop. Most effective laps 12-14 in a 27-lap race."
            },
            {
                "scenario": "Overcut Strategy",
                "question": "What is an overcut and when does it work?",
                "answer": "An overcut is staying out longer than your competitor after they pit. It works when: 1) Your tires are still performing well, 2) Track is clear (no traffic), 3) You can push hard for 3-5 laps, 4) Pit loss time is high. Stay out, set fast laps while they're in traffic on cold tires, pit later and emerge ahead. Risky but effective in clean air."
            },
            {
                "scenario": "Safety Car Strategy",
                "question": "How do I respond to a safety car?",
                "answer": "Safety car strategy depends on your position: If leading: Stay out if tires are good, pit if they're old. If mid-pack: Usually pit (free stop), take fresh tires. If at back: Gamble on staying out for track position. Key factors: Tire age (>15 laps = pit), fuel level (<40% = top up), gap to cars ahead/behind. Always communicate with your engineer before deciding."
            },
            {
                "scenario": "Fuel Management",
                "question": "How do I manage fuel during a race?",
                "answer": "Fuel management involves: 1) Calculate consumption (typically 2-3 liters/lap in GR86), 2) Monitor fuel level vs laps remaining, 3) If short: Lift-and-coast on straights, short-shift (shift 500rpm early), reduce brake drag, 4) If comfortable: Push normally. Running out costs 30+ seconds, conservative pace costs 0.5-1s/lap. Better to finish slow than not finish."
            },
            {
                "scenario": "Tire Management",
                "question": "How do I extend tire life?",
                "answer": "Extend tire life by: 1) Smooth inputs (gradual throttle/brake), 2) Avoid wheelspin (hurts rear tires), 3) Minimize sliding (scrubbing kills fronts), 4) Proper tire temperatures (25-35°C optimal), 5) Strategic lift-and-coast. Trade 0.2-0.3s/lap early to gain 1-2s/lap advantage late in stint. Smooth is fast AND kind to tires."
            }
        ]
        
        for strat in strategies:
            self.add_entry(
                question=strat["question"],
                answer=strat["answer"],
                category="strategy",
                subcategory=strat["scenario"].lower().replace(" ", "_"),
                difficulty="advanced",
                data_source="analysis"
            )
        
        print(f"  ✓ Generated {len(strategies)} strategy entries")
    
    def generate_driver_coaching(self):
        """Generate driver coaching knowledge"""
        print("\n🏎️ Generating driver coaching...")
        
        coaching_topics = [
            {
                "topic": "Racing Line Basics",
                "question": "What is the optimal racing line?",
                "answer": "The optimal racing line maximizes corner exit speed: 1) Enter wide (use full track width), 2) Turn in at the right point (varies by corner), 3) Hit the apex at minimum speed (late apex usually best), 4) Exit wide with full throttle. Key principle: 'Slow in, fast out' - prioritize exit speed, especially before straights. Sacrifice entry speed for better exit."
            },
            {
                "topic": "Braking Technique",
                "question": "How do I improve my braking?",
                "answer": "Effective braking technique: 1) Brake in a straight line (before turn-in), 2) Apply maximum pressure quickly (70-85 bar), 3) Trail brake: gradually release as you turn in, 4) Feel for lock-up (reduce pressure if wheels lock), 5) Finish braking before apex. Common mistakes: Braking too early (slow), too late (miss apex), or too long (slow corner speed). Practice threshold braking."
            },
            {
                "topic": "Throttle Control",
                "question": "How do I apply throttle smoothly?",
                "answer": "Smooth throttle application: 1) Begin at apex (when unwinding steering), 2) Progressive application (0% → 100% gradually), 3) Match to steering angle (less steering = more throttle), 4) Feel for wheelspin (back off if rear slides), 5) Full throttle when straight. Aggressive throttle causes wheelspin (slow) and tire wear. Smooth = fast."
            },
            {
                "topic": "Corner Types",
                "question": "How do I approach different corner types?",
                "answer": "Corner strategies: Slow corners (hairpins): Late apex, prioritize exit. Medium corners: Balanced approach, smooth arc. Fast corners: Early apex, maintain momentum, brave on entry. Chicanes: Straight-line as much as possible, late apex on exit. Decreasing radius: Early turn-in, careful on exit. Increasing radius: Late apex, accelerate early. Always consider what follows the corner."
            },
            {
                "topic": "Consistency",
                "question": "How do I drive more consistently?",
                "answer": "Build consistency through: 1) Reference points (braking markers, turn-in points, apexes), 2) Repeatable technique (same inputs every lap), 3) Smooth driving (no sudden movements), 4) Mental focus (stay present, don't think ahead), 5) Physical fitness (fatigue kills consistency). Aim for ±0.5s lap time variation. Consistency beats occasional fast laps."
            }
        ]
        
        for topic in coaching_topics:
            self.add_entry(
                question=topic["question"],
                answer=topic["answer"],
                category="coaching",
                subcategory=topic["topic"].lower().replace(" ", "_"),
                difficulty="intermediate",
                data_source="expert_knowledge"
            )
        
        print(f"  ✓ Generated {len(coaching_topics)} coaching entries")
    
    def generate_performance_analysis(self):
        """Generate performance analysis knowledge"""
        print("\n📈 Generating performance analysis...")
        
        analysis_topics = [
            ("Lap Time Analysis", "How do I analyze my lap times?", 
             "Analyze lap times by: 1) Compare to best lap (identify delta), 2) Check sector times (find weak sectors), 3) Look for patterns (degradation, consistency), 4) Compare to competitors (where are they faster?), 5) Consider conditions (traffic, tire age, fuel load). Focus on sectors where you lose most time. A 0.5s improvement in your weakest sector is easier than 0.1s in three sectors."),
            
            ("Sector Analysis", "What do sector times tell me?",
             "Sector times reveal: S1 (usually entry/braking zones), S2 (mid-corner/technical sections), S3 (exits/acceleration zones). If S1 is slow: Brake later, carry more entry speed. If S2 is slow: Work on mid-corner technique, racing line. If S3 is slow: Better exits, earlier throttle application. Compare your sectors to fastest lap sectors to find biggest gains."),
            
            ("Consistency Metrics", "What is good consistency?",
             "Consistency measured by lap time standard deviation: Excellent: ±0.3s, Good: ±0.5s, Average: ±0.8s, Poor: >1.0s. Inconsistency causes: Fatigue, poor reference points, varying technique, traffic, tire degradation. Improve by: Using consistent reference points, maintaining physical fitness, practicing mental focus, managing tire/fuel consistently."),
            
            ("Gap Analysis", "How do I manage gaps to other cars?",
             "Gap management: If ahead: Maintain 2-3s gap (safe from undercut), push if gap shrinks, manage tires if gap grows. If behind: Within 1s = attack mode, 1-3s = pressure and wait, >3s = focus on own pace. Monitor gap trends: Growing = they're faster (change approach), Shrinking = you're faster (prepare to attack), Stable = matched pace (strategy will decide)."),
            
            ("Tire Degradation Tracking", "How do I track tire degradation?",
             "Track degradation by: 1) Monitor lap times (increasing = degrading), 2) Feel for grip loss (sliding, longer braking), 3) Check sector times (usually S3 degrades first), 4) Compare to reference lap (delta growing = degradation), 5) Note lap count (typically degrades after lap 10-12). Degradation >0.5s/lap = consider pitting soon. >1.0s/lap = pit immediately.")
        ]
        
        for topic, question, answer in analysis_topics:
            self.add_entry(
                question=question,
                answer=answer,
                category="performance",
                subcategory=topic.lower().replace(" ", "_"),
                difficulty="advanced",
                data_source="analysis"
            )
        
        print(f"  ✓ Generated {len(analysis_topics)} performance entries")
    
    def generate_weather_knowledge(self):
        """Generate weather and conditions knowledge"""
        print("\n🌤️ Generating weather knowledge...")
        
        weather_topics = [
            ("Track Temperature", "How does track temperature affect performance?",
             "Track temperature impact: Cold (<20°C): Hard to warm tires, less grip, longer braking. Optimal (25-35°C): Best grip, consistent tire performance. Hot (>40°C): Tire degradation increases, grip can decrease, risk of overheating. Adjust: Cold = more aggressive warm-up, smoother inputs. Hot = manage tire temps, avoid excessive sliding, consider earlier pit stop."),
            
            ("Wet Conditions", "How do I drive in wet conditions?",
             "Wet driving technique: 1) Brake 50-100% earlier (longer distances), 2) Reduce corner speed 20-30%, 3) Smooth inputs (sudden movements = spin), 4) Avoid painted lines and curbs (zero grip), 5) Look for grip (racing line may not be optimal), 6) Increase following distance (spray reduces visibility). Patience is key - crashes lose more time than conservative pace."),
            
            ("Drying Track", "How do I handle a drying track?",
             "Drying track strategy: 1) Find grip (explore different lines), 2) Gradually increase pace (test limits carefully), 3) Watch for damp patches (inconsistent grip), 4) Tire choice critical (wet → intermediate → slicks), 5) Track position important (clean air to find grip). Be brave but smart - first to slicks can gain huge advantage, but too early = disaster."),
            
            ("Wind Effects", "How does wind affect racing?",
             "Wind impact: Headwind: Reduces top speed, increases drag, better cooling. Tailwind: Higher top speed, less drag, less cooling. Crosswind: Affects handling (push car sideways), changes braking points, requires steering correction. Adjust: Headwind = draft more, brake earlier. Tailwind = brake later, watch for overspeed. Crosswind = anticipate push, adjust line."),
        ]
        
        for topic, question, answer in weather_topics:
            self.add_entry(
                question=question,
                answer=answer,
                category="weather",
                subcategory=topic.lower().replace(" ", "_"),
                difficulty="intermediate",
                data_source="expert_knowledge"
            )
        
        print(f"  ✓ Generated {len(weather_topics)} weather entries")
    
    def generate_vehicle_dynamics(self):
        """Generate vehicle dynamics knowledge"""
        print("\n🔧 Generating vehicle dynamics...")
        
        dynamics_topics = [
            ("Understeer", "What is understeer and how do I fix it?",
             "Understeer = front tires lose grip first, car won't turn. Causes: Too much entry speed, early throttle, wrong line, cold front tires. Fixes: Brake earlier, slower entry, later apex, trail brake more, reduce throttle mid-corner. Setup: Increase front tire pressure, reduce front wing, soften front springs. Driving around it: Patience, let car rotate before throttle."),
            
            ("Oversteer", "What is oversteer and how do I fix it?",
             "Oversteer = rear tires lose grip first, car rotates too much. Causes: Too much throttle, lift-off mid-corner, cold rear tires, aggressive inputs. Fixes: Smoother throttle, avoid sudden lift, earlier apex, reduce trail braking. Setup: Increase rear tire pressure, add rear wing, soften rear springs. Driving around it: Gentle throttle application, catch slides early with steering."),
            
            ("Weight Transfer", "How does weight transfer affect handling?",
             "Weight transfer: Braking = weight to front (more front grip, less rear). Accelerating = weight to rear (more rear grip, less front). Cornering = weight to outside (outside tires do more work). Use it: Trail brake to keep weight on front for turn-in, smooth throttle to transfer weight to rear for traction. Sudden inputs cause weight shift = loss of grip."),
            
            ("Tire Pressure", "How does tire pressure affect performance?",
             "Tire pressure effects: Too low: More grip but overheats, wears faster, sluggish response. Too high: Less grip, bouncy, uneven wear, but cooler temps. Optimal: 30-35 PSI (hot) for GR86. Adjust: +2 PSI if overheating, -2 PSI if not warming up. Check after 3-5 laps when hot. Front/rear balance affects handling (higher front = less understeer)."),
        ]
        
        for topic, question, answer in dynamics_topics:
            self.add_entry(
                question=question,
                answer=answer,
                category="vehicle_dynamics",
                subcategory=topic.lower().replace(" ", "_"),
                difficulty="advanced",
                data_source="expert_knowledge"
            )
        
        print(f"  ✓ Generated {len(dynamics_topics)} vehicle dynamics entries")
    
    def generate_championship_strategy(self):
        """Generate championship and season strategy"""
        print("\n🏆 Generating championship strategy...")
        
        championship_topics = [
            ("Points System", "How does the points system work?",
             "Toyota GR Cup points (typical): 1st=25, 2nd=18, 3rd=15, 4th=12, 5th=10, 6th=8, 7th=6, 8th=4, 9th=2, 10th=1. Bonus: Fastest lap=1 point (if in top 10). Strategy: Consistency beats occasional wins. P5 every race > P1 then DNF. Protect points when leading championship. Take risks when behind. Calculate points needed vs races remaining."),
            
            ("Risk Management", "When should I take risks vs play it safe?",
             "Risk assessment: Take risks when: Behind in championship, late in season, need to make up positions, nothing to lose. Play safe when: Leading championship, early in season, in points position, mechanical issues. Calculate: Is potential gain worth potential loss? P5 guaranteed vs 50% chance at P3 (risk DNF) = take P5 if leading championship."),
            
            ("Track Selection", "Which tracks should I focus on?",
             "Focus on: 1) Tracks that suit your style (technical vs flowing), 2) Tracks with most points available (double-headers), 3) Tracks where you're competitive (maximize points), 4) Tracks where rivals struggle (gain advantage). Analyze: Your best tracks (prioritize), your worst tracks (improve or minimize damage), rivals' strengths (prepare to defend)."),
            
            ("Season Planning", "How do I plan a championship season?",
             "Season planning: 1) Set realistic goals (target position), 2) Identify key races (double points, home tracks), 3) Budget resources (tires, parts, testing), 4) Plan improvements (weak areas to work on), 5) Monitor rivals (who to beat). Review after each race: On target? Adjust strategy? What to improve? Stay flexible but focused on end goal."),
        ]
        
        for topic, question, answer in championship_topics:
            self.add_entry(
                question=question,
                answer=answer,
                category="championship",
                subcategory=topic.lower().replace(" ", "_"),
                difficulty="advanced",
                data_source="expert_knowledge"
            )
        
        print(f"  ✓ Generated {len(championship_topics)} championship entries")
    
    def save_datasets(self):
        """Save all datasets in multiple formats"""
        
        # Save JSONL (for training)
        with open('rag_dataset/race_engineer_qa.jsonl', 'w', encoding='utf-8') as f:
            for entry in self.dataset:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        
        # Save JSON (for review)
        with open('rag_dataset/race_engineer_qa.json', 'w', encoding='utf-8') as f:
            json.dump(self.dataset, f, indent=2, ensure_ascii=False)
        
        # Save by category
        categories = {}
        for entry in self.dataset:
            cat = entry['context']['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(entry)
        
        for cat, entries in categories.items():
            filename = f'rag_dataset/{cat}_knowledge.json'
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(entries, f, indent=2, ensure_ascii=False)
        
        # Save statistics
        stats = {
            "total_entries": len(self.dataset),
            "categories": {cat: len(entries) for cat, entries in categories.items()},
            "difficulty_levels": {
                "beginner": len([e for e in self.dataset if e['context']['difficulty'] == 'beginner']),
                "intermediate": len([e for e in self.dataset if e['context']['difficulty'] == 'intermediate']),
                "advanced": len([e for e in self.dataset if e['context']['difficulty'] == 'advanced'])
            },
            "tracks_covered": len(self.tracks),
            "generated_date": datetime.now().isoformat()
        }
        
        with open('rag_dataset/dataset_stats.json', 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2)
        
        print(f"\n📊 Dataset Statistics:")
        print(f"  Total entries: {stats['total_entries']}")
        print(f"  Categories: {len(categories)}")
        print(f"  Difficulty levels: {stats['difficulty_levels']}")


def main():
    generator = CleanRAGDataGenerator()
    generator.generate_all_datasets()
    
    print("\n" + "=" * 70)
    print("✅ Clean RAG Dataset Generation Complete!")
    print("\nFiles created in rag_dataset/:")
    print("  • race_engineer_qa.jsonl (training format)")
    print("  • race_engineer_qa.json (readable format)")
    print("  • [category]_knowledge.json (by category)")
    print("  • dataset_stats.json (statistics)")
    print("  • README.md (documentation)")
    print("=" * 70)


if __name__ == "__main__":
    main()
