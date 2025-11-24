"""
Enhanced RAG Dataset Generator with Advanced Racing Knowledge
Incorporates professional-level insights on driver development, team operations, and data analysis
"""

import json
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generate_full_rag_dataset import FullRAGDatasetGenerator


class EnhancedRAGDatasetGenerator(FullRAGDatasetGenerator):
    """Enhanced generator with advanced racing knowledge"""
    
    def generate_complete_dataset(self):
        """Generate complete dataset with enhanced content"""
        print("🏁 Generating Enhanced Multi-Track RAG Dataset")
        print("=" * 70)
        
        # Process each track (from parent class)
        for track_name in self.tracks:
            self.process_track(track_name)
        
        # Add expert knowledge (from parent class)
        self.add_expert_knowledge()
        
        # Add enhanced professional knowledge
        self.add_driver_development_knowledge()
        self.add_team_operations_knowledge()
        self.add_coaching_knowledge()
        self.add_advanced_weather_knowledge()
        self.add_data_analysis_knowledge()
        self.add_performance_metrics_knowledge()
        
        # Save all datasets
        self.save_datasets()
        
        print(f"\n✅ Generated {len(self.dataset)} enhanced RAG entries")
        print(f"📊 Stats: {self.stats}")
    
    def add_driver_development_knowledge(self):
        """Add advanced driver development insights"""
        print("\n🎓 Adding driver development knowledge...")
        
        development_topics = [
            ("Continuous Development", 
             "How should a driver continuously improve their skills?",
             "Continuous development requires: 1) Telemetry analysis - Review data after every session to identify braking points, throttle application, and racing line improvements. 2) Coach feedback - Work with experienced coaches who can spot technique issues you can't feel. 3) Video analysis - Compare your onboard footage to faster drivers. 4) Simulator practice - Refine techniques in a controlled environment. 5) Physical training - Maintain fitness for concentration and reaction times. The best drivers never stop learning and refining their craft."),
            
            ("Adaptability Training",
             "How do I develop adaptability for different conditions?",
             "Adaptability is crucial for championship success: 1) Practice in rain - Seek wet weather testing to master reduced grip and aquaplaning. 2) Temperature extremes - Experience both hot (tire degradation) and cold (tire warm-up) conditions. 3) Wind practice - Learn to handle crosswinds and their effect on braking/cornering. 4) Track variety - Race on different circuit types (technical vs flowing, short vs long). 5) Tire compounds - Experience different tire behaviors. Adaptable drivers can perform in any condition, giving them a competitive edge."),
            
            ("Mental Fortitude",
             "How do I develop mental strength for racing?",
             "Mental fortitude separates good drivers from great ones: 1) Pressure management - Practice staying calm under pressure through visualization and breathing techniques. 2) Incident recovery - Learn to quickly reset mentally after mistakes or contact. 3) Concentration training - Build stamina for 45+ minute races through meditation and focus exercises. 4) Race simulation - Practice full-length races in the simulator to build mental endurance. 5) Sports psychology - Work with a mental coach to develop resilience. Mental strength is as important as physical skill in endurance racing."),
            
            ("Feedback Skills",
             "How do I give better feedback to my engineer?",
             "Effective feedback is critical for car setup: 1) Be specific - Instead of 'car feels bad', say 'front end pushes in Turn 3 mid-corner'. 2) Consistent terminology - Use agreed terms (understeer/oversteer, entry/mid/exit). 3) Prioritize issues - Focus on the biggest problems first. 4) Quantify when possible - 'Braking 10m later than yesterday' vs 'braking later'. 5) Separate car from driver - Distinguish between setup issues and driving mistakes. Good feedback helps your engineer make the right changes quickly."),
            
            ("Simulator Training",
             "How should I use a simulator for training?",
             "Effective simulator use accelerates development: 1) Learn new tracks - Build muscle memory for corners and braking points before arriving. 2) Practice conditions - Experience rain, night, different temperatures. 3) Setup testing - Try setup changes without using track time. 4) Race craft - Practice overtaking, defending, and racecraft scenarios. 5) Consistency work - Focus on repeatable laps, not just fast laps. The simulator is a tool for deliberate practice, not just entertainment. Treat it seriously for maximum benefit.")
        ]
        
        for topic, question, answer in development_topics:
            self.add_entry(
                question=question,
                answer=answer,
                category="driver_development",
                subcategory=topic.lower().replace(" ", "_"),
                difficulty="advanced",
                data_source="professional_knowledge"
            )
    
    def add_team_operations_knowledge(self):
        """Add team operations and strategy insights"""
        print("\n👥 Adding team operations knowledge...")
        
        team_topics = [
            ("Race Strategy Planning",
             "How does a team develop race strategy?",
             "Professional race strategy involves: 1) Pre-race simulations - Use historical data to model different pit stop scenarios, fuel loads, and tire strategies. 2) Real-time analysis - Monitor live telemetry and timing to adjust strategy during the race. 3) Scenario planning - Prepare for safety cars, weather changes, and incidents. 4) Competitor tracking - Watch rival strategies and react accordingly. 5) Risk assessment - Balance aggressive vs conservative approaches based on championship position. Data-driven strategy can gain 5-10 seconds per race through optimal decisions."),
            
            ("Data Analysis Team",
             "What does a data analysis team do in racing?",
             "A professional data team provides critical insights: 1) Telemetry review - Analyze thousands of data points per lap (speed, throttle, brake, G-forces, tire temps). 2) Performance comparison - Compare driver to driver, lap to lap, corner to corner. 3) Setup optimization - Identify which setup changes improve performance. 4) Predictive modeling - Forecast tire degradation, fuel consumption, and pit windows. 5) Real-time support - Provide live feedback to race engineer during sessions. Expert analysts can find 0.5-1.0s per lap through data insights."),
            
            ("Pit Crew Operations",
             "How important is pit crew performance?",
             "Pit crew excellence is crucial for race outcomes: 1) Consistency - A well-drilled crew executes 15-20 second stops repeatedly without errors. 2) Practice - Top teams practice pit stops daily, not just at races. 3) Communication - Clear signals and calls prevent mistakes under pressure. 4) Equipment - Proper tools, wheel guns, and jacks maintained to perfection. 5) Contingency planning - Prepared for issues like stuck wheels or fuel rig problems. A 2-second faster pit stop can mean the difference between winning and losing. Flawless execution gains positions."),
            
            ("Driver Support Systems",
             "What support does a professional team provide drivers?",
             "Comprehensive driver support includes: 1) Simulator access - High-fidelity sim for track learning and setup testing. 2) Race engineer - Dedicated engineer who knows the driver's style and preferences. 3) Data review - Post-session analysis with engineers and coaches. 4) Physical training - Fitness programs tailored for racing demands. 5) Mental coaching - Sports psychologists for mental performance. 6) Nutrition - Proper diet and hydration plans for race weekends. Professional support helps drivers perform at their peak consistently."),
            
            ("Engineer-Driver Relationship",
             "How should a race engineer work with their driver?",
             "The engineer-driver relationship is critical: 1) Trust building - Develop mutual respect and understanding over time. 2) Communication style - Learn how the driver prefers to receive information (detailed vs concise). 3) Setup philosophy - Understand driver preferences (stable vs responsive, understeer vs oversteer). 4) Race management - Provide calm, clear instructions during high-pressure moments. 5) Development focus - For young drivers, balance performance with learning and growth. A strong engineer-driver partnership can find 0.5-1.0s per lap through better communication and setup.")
        ]
        
        for topic, question, answer in team_topics:
            self.add_entry(
                question=question,
                answer=answer,
                category="team_operations",
                subcategory=topic.lower().replace(" ", "_"),
                difficulty="advanced",
                data_source="professional_knowledge"
            )
    
    def add_coaching_knowledge(self):
        """Add advanced coaching and technical knowledge"""
        print("\n🏫 Adding advanced coaching knowledge...")
        
        coaching_topics = [
            ("Technical Feedback Analysis",
             "How does a coach analyze driver performance?",
             "Professional coaching involves deep analysis: 1) Telemetry comparison - Overlay driver data with reference laps to identify specific areas for improvement. 2) Video review - Analyze onboard footage for steering inputs, visual reference points, and body position. 3) Corner-by-corner breakdown - Focus on entry, mid-corner, and exit phases separately. 4) Pattern recognition - Identify consistent mistakes or technique issues across multiple corners. 5) Setup vs driver - Distinguish between car problems and driver technique. Good coaches can identify 0.2-0.5s improvements in specific corners."),
            
            ("Communication with Drivers",
             "How should a coach communicate with drivers?",
             "Effective coaching communication requires: 1) Clear language - Use specific, actionable instructions ('brake 5m later at Turn 1' not 'brake later'). 2) Positive framing - Focus on what to do, not what not to do. 3) Timing - Give feedback when the driver is receptive, not immediately after a mistake. 4) Demonstration - Show data or video to illustrate points. 5) Listening - Understand the driver's perspective and feelings about the car. 6) Patience - Allow time for drivers to process and implement changes. Strong communication accelerates driver development."),
            
            ("Young Driver Development",
             "How do you develop young racing talent?",
             "Developing young drivers requires: 1) Fundamentals first - Master basic techniques before advanced concepts. 2) Data literacy - Teach drivers to read and understand telemetry. 3) Adaptability training - Expose them to different cars, tracks, and conditions. 4) Race craft - Practice overtaking, defending, and wheel-to-wheel racing. 5) Mental development - Build confidence and resilience through experience. 6) Gradual progression - Don't rush development; allow time to master each level. 7) Feedback culture - Create environment where mistakes are learning opportunities. Patient, structured development produces better long-term results."),
            
            ("Setup Adjustments from Feedback",
             "How do you translate driver feedback into setup changes?",
             "Converting feedback to setup requires expertise: 1) Understand the complaint - 'Understeer' can mean different things at different phases. 2) Identify the phase - Entry, mid-corner, or exit determines the solution. 3) Consider conditions - Temperature, track evolution, and tire wear affect handling. 4) Systematic changes - Adjust one thing at a time to isolate effects. 5) Verify with data - Check if telemetry supports the driver's feeling. 6) Test and iterate - Make change, test, review, adjust. Common fixes: Understeer entry = more front brake bias. Understeer mid = soften front, stiffen rear. Oversteer exit = reduce rear spring rate or add rear wing."),
            
            ("Race Instruction Delivery",
             "How should a coach give instructions during a race?",
             "In-race coaching requires special skills: 1) Calm tone - Keep voice steady even in critical moments. 2) Concise messages - Drivers can't process long explanations while racing. 3) Timing - Give info at appropriate moments (not mid-corner). 4) Prioritize - Focus on most important information only. 5) Positive reinforcement - Acknowledge good performance. 6) Strategic updates - Gaps, pit windows, competitor positions. 7) Emergency clarity - In incidents, give clear, direct instructions. Example: 'Gap 2.5 seconds, push for 3 laps then pit' vs long explanation. Clear, calm communication helps drivers perform under pressure.")
        ]
        
        for topic, question, answer in coaching_topics:
            self.add_entry(
                question=question,
                answer=answer,
                category="coaching_advanced",
                subcategory=topic.lower().replace(" ", "_"),
                difficulty="advanced",
                data_source="professional_knowledge"
            )
    
    def add_advanced_weather_knowledge(self):
        """Add detailed weather impact knowledge"""
        print("\n🌦️ Adding advanced weather knowledge...")
        
        weather_topics = [
            ("Rain and Wet Conditions Impact",
             "How does rain fundamentally change racing?",
             "Rain transforms racing dynamics: 1) Grip reduction - Wet tracks have 30-50% less grip than dry, increasing braking distances by 50-100%. 2) Aquaplaning risk - Standing water causes tires to lose contact with track surface above certain speeds. 3) Tire strategy - Critical decisions: When to switch from wets to intermediates to slicks as track dries. Wrong timing costs 10-30 seconds. 4) Driver skill amplification - Mistakes are easier to make and harder to recover from. The best wet-weather drivers gain 1-2 seconds per lap. 5) Visibility - Spray from cars ahead reduces vision, requiring trust and instinct. 6) Racing line changes - Dry line may not be fastest; look for grip off-line."),
            
            ("Temperature Effects on Performance",
             "How does temperature affect car and driver performance?",
             "Temperature has multiple critical effects: 1) Tire performance - Cold (<15°C): Hard to warm tires, less grip. Optimal (25-35°C): Best performance. Hot (>40°C): Accelerated degradation, potential overheating. 2) Track temp - Hot track increases tire wear by 20-40%, requiring earlier pit stops or pace management. 3) Engine cooling - High temps risk overheating; teams may reduce power or increase cooling (costs speed). 4) Driver fatigue - Cockpit temps above 50°C increase fatigue, affecting concentration and reaction times. 5) Brake performance - Cold brakes need warming; hot brakes risk fade. Temperature management is crucial for consistent performance."),

            
            ("Wind Effects on Racing",
             "How does wind affect car performance and strategy?",
             "Wind significantly impacts racing: 1) Aerodynamic balance - Headwind increases downforce and drag (slower straights, better corners). Tailwind reduces downforce (faster straights, less grip in corners). 2) Crosswind effects - Pushes car sideways, especially in high-speed corners, requiring steering corrections and affecting braking points. 3) Consistency challenges - Changing wind direction lap-to-lap makes car behavior unpredictable. 4) Strategic implications - Strong headwind on main straight may favor later pit stops (less time lost). 5) Driver adaptation - Must adjust braking points and corner entry speeds based on wind. Strong winds can change lap times by 0.5-1.5 seconds."),
            
            ("Visibility in Poor Conditions",
             "How do drivers handle poor visibility?",
             "Poor visibility requires special skills: 1) Rain spray - Following cars create walls of spray; must rely on memory and instinct for braking points. 2) Fog conditions - Reduce speed, increase following distance, use reference points on track edges. 3) Night racing - Headlights create shadows and depth perception issues; memorize track features. 4) Sun glare - Blinding at certain corners; use visor, adjust line to avoid direct sun. 5) Trust and experience - Experienced drivers can maintain pace with limited vision by trusting their preparation. 6) Safety first - Better to lose 2-3 seconds per lap than crash. Visibility issues separate experienced drivers from novices."),
            
            ("Tire Choice in Changing Conditions",
             "How do you make tire choice decisions in changing weather?",
             "Tire strategy in mixed conditions is critical: 1) Track wetness assessment - Full wets for standing water, intermediates for damp, slicks for dry. 2) Timing the switch - Too early to slicks = no grip and tire damage. Too late = losing 2-3 seconds per lap. 3) Track drying patterns - Some corners dry faster (sun exposure, wind, racing line). 4) Risk vs reward - Leading: Conservative approach. Mid-pack: Can gamble for positions. 5) Weather radar - Monitor approaching rain to time pit stops. 6) Competitor watching - See what others do, learn from their mistakes. One perfect tire call can win a race; one bad call can lose it. This is where experience and data analysis combine.")
        ]
        
        for topic, question, answer in weather_topics:
            self.add_entry(
                question=question,
                answer=answer,
                category="weather_advanced",
                subcategory=topic.lower().replace(" ", "_"),
                difficulty="advanced",
                data_source="professional_knowledge"
            )
    
    def add_data_analysis_knowledge(self):
        """Add quantitative metrics and data analysis knowledge"""
        print("\n📊 Adding data analysis knowledge...")
        
        data_topics = [
            ("Speed Execution Analysis",
             "How do teams analyze speed execution through data?",
             "Advanced speed analysis involves: 1) Corner phase breakdown - Divide each corner into entry, mid-corner (apex), and exit phases. Measure speed at each point. 2) Braking analysis - Track brake pressure, brake point location, trail braking profile. Compare to reference lap. 3) Throttle application - Measure throttle position vs steering angle. Smooth correlation = good technique. 4) Lateral G-force - Peak lateral G indicates cornering speed. Compare across laps to track consistency. 5) Minimum speed point - Where driver reaches slowest speed in corner. Earlier = better exit. Teams can identify 0.1-0.3s improvements per corner through detailed analysis."),
            
            ("Lap Time Consistency Metrics",
             "What metrics measure driver consistency?",
             "Consistency is measured through: 1) Lap time standard deviation - Elite drivers: ±0.3s, Good: ±0.5s, Average: ±0.8s. 2) Sector time variation - Analyze consistency in each sector separately. 3) Stint degradation curve - How lap times increase with tire wear. Consistent drivers have smoother curves. 4) Mistake frequency - Count lock-ups, track limits, spins per session. 5) Reference lap delta - How close each lap is to personal best. Consistent drivers can maintain 99% of best pace for entire stint. Consistency is often more valuable than raw speed in endurance racing."),
            
            ("Car Management Metrics",
             "How is car management measured quantitatively?",
             "Car management tracking includes: 1) Tire management - Thermal cameras show tire temperature distribution. Even temps = good management. Track stint length vs predicted. 2) Brake management - Monitor brake disc temps, pad wear. Smooth braking preserves brakes for full race. 3) Fuel consumption - Compare actual vs predicted consumption. Efficient drivers save 1-2 laps of fuel. 4) Component stress - Measure G-forces, curb strikes, gear shifts. Smooth drivers reduce wear. 5) Degradation rate - Compare lap time drop-off to teammates. Good management = slower degradation. Teams can quantify how much time car management saves over a race."),
            
            ("Adaptability Measurement",
             "How do teams measure driver adaptability?",
             "Adaptability is quantified through: 1) Wet vs dry pace - Compare lap time percentage in wet vs dry. Adaptable drivers lose less time in wet. 2) New track learning - Measure improvement rate at unfamiliar circuits. Fast learners reach 98% pace in fewer laps. 3) Setup sensitivity - Test performance with different setups. Adaptable drivers perform well with various configurations. 4) Simulator correlation - Compare sim pace to real-world pace across conditions. 5) Tire compound adaptation - Performance across different tire compounds. 6) Temperature range - Consistency across hot and cold conditions. Adaptable drivers are valuable for teams racing in varied conditions."),
            
            ("Junior Driver Statistics",
             "What statistics predict junior driver success?",
             "Key junior racing metrics include: 1) Win ratio - Wins divided by races entered. Elite: >20%, Good: 10-20%. 2) Podium rate - Top 3 finishes percentage. Consistent performers: >40%. 3) Pole position rate - Qualifying performance indicator. >15% shows raw speed. 4) Points per race - Average points scored. Accounts for consistency and speed. 5) Teammate comparison - Head-to-head qualifying and race results vs teammate. Should win >60%. 6) Incident rate - Crashes and penalties per race. Lower is better. 7) Wet weather performance - Specific wet race results. Separates talent. These stats help teams identify promising talent for development programs.")
        ]
        
        for topic, question, answer in data_topics:
            self.add_entry(
                question=question,
                answer=answer,
                category="data_analysis",
                subcategory=topic.lower().replace(" ", "_"),
                difficulty="advanced",
                data_source="professional_knowledge"
            )
    
    def add_performance_metrics_knowledge(self):
        """Add performance measurement and benchmarking knowledge"""
        print("\n📈 Adding performance metrics knowledge...")
        
        metrics_topics = [
            ("Telemetry Data Points",
             "What telemetry data points are most important?",
             "Critical telemetry parameters: 1) Speed trace - Shows speed at every point on track. Compare to reference to find time loss. 2) Throttle position - 0-100% application. Smooth progression indicates good technique. 3) Brake pressure - Front and rear pressure in bar. Peak pressure and trail braking visible. 4) Steering angle - Wheel position in degrees. Smooth inputs = fast, jerky = slow. 5) Lateral G-force - Cornering force. Peak G shows grip limit usage. 6) Longitudinal G-force - Acceleration/braking force. Shows traction usage. 7) Gear selection - Which gear in each corner. 8) Tire temperatures - Surface temps indicate tire management. Teams analyze thousands of data points per lap to find improvements."),
            
            ("Corner Phase Analysis",
             "How do you analyze performance in corner phases?",
             "Corner phase breakdown is essential: 1) Entry phase - From brake point to turn-in. Measure: Brake point location, peak brake pressure, entry speed. Goal: Maximum entry speed without compromising exit. 2) Mid-corner phase - Turn-in to apex. Measure: Minimum speed, apex speed, lateral G-force. Goal: Carry maximum speed through apex. 3) Exit phase - Apex to corner exit. Measure: Throttle application point, exit speed, acceleration. Goal: Earliest full throttle for best straight-line speed. Compare each phase to reference lap. Often find 0.1-0.2s per phase = 0.3-0.6s per corner. Focus on weakest phase first for biggest gains."),
            
            ("Benchmark Comparison",
             "How do you benchmark driver performance?",
             "Benchmarking methods: 1) Teammate comparison - Most direct comparison with same car. Should be within 0.2-0.3s in qualifying. 2) Reference lap - Create ideal lap from best sectors. Shows theoretical maximum. 3) Historical data - Compare to previous years at same track. 4) Simulator correlation - Validate real-world pace against sim predictions. 5) Class leaders - Compare to fastest in class across multiple tracks. 6) Improvement rate - Track progress over season. Good development = consistent improvement. Benchmarking identifies strengths to leverage and weaknesses to improve."),
            
            ("Real-time Performance Monitoring",
             "How do teams monitor performance during a race?",
             "Live monitoring includes: 1) Sector times - Real-time comparison to best and competitors. Identify pace changes immediately. 2) Gap management - Track gaps to cars ahead/behind. Adjust strategy accordingly. 3) Tire degradation - Monitor lap time drop-off. Predict pit window. 4) Fuel consumption - Track usage vs prediction. Adjust strategy if needed. 5) Brake temps - Watch for overheating. May need cooling lap. 6) Incident detection - Identify lock-ups, track limits, mistakes. Provide feedback. 7) Weather changes - Monitor conditions, prepare for tire changes. Real-time data allows teams to react quickly to changing situations."),
            
            ("Post-Session Analysis Process",
             "What's the process for post-session data analysis?",
             "Systematic post-session review: 1) Initial overview - Review lap times, sector times, incidents. Identify patterns. 2) Telemetry comparison - Overlay driver vs reference lap. Find specific areas of time loss. 3) Video correlation - Match telemetry to video. See what driver is doing differently. 4) Driver debrief - Discuss findings with driver. Get their perspective on car behavior. 5) Setup correlation - Determine if setup changes had desired effect. 6) Action items - Create specific list of improvements for next session. 7) Documentation - Record findings for future reference. Thorough analysis between sessions is crucial for continuous improvement. Teams that analyze well improve faster.")
        ]
        
        for topic, question, answer in metrics_topics:
            self.add_entry(
                question=question,
                answer=answer,
                category="performance_metrics",
                subcategory=topic.lower().replace(" ", "_"),
                difficulty="advanced",
                data_source="professional_knowledge"
            )
    
    def save_datasets(self):
        """Save enhanced datasets"""
        print("\n💾 Saving enhanced datasets...")
        
        # Create output directory
        os.makedirs('rag_dataset', exist_ok=True)
        
        # Save JSONL (for training)
        with open('rag_dataset/race_engineer_enhanced.jsonl', 'w', encoding='utf-8') as f:
            for entry in self.dataset:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        print("  ✓ Saved race_engineer_enhanced.jsonl")
        
        # Save JSON (for review)
        with open('rag_dataset/race_engineer_enhanced.json', 'w', encoding='utf-8') as f:
            json.dump(self.dataset, f, indent=2, ensure_ascii=False)
        print("  ✓ Saved race_engineer_enhanced.json")
        
        # Save by category
        categories = {}
        for entry in self.dataset:
            cat = entry['context']['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(entry)
        
        for cat, entries in categories.items():
            filename = f'rag_dataset/{cat}_enhanced.json'
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(entries, f, indent=2, ensure_ascii=False)
        print(f"  ✓ Saved {len(categories)} category files")
        
        # Save by track
        tracks = {}
        for entry in self.dataset:
            track = entry['context'].get('track')
            if track:
                if track not in tracks:
                    tracks[track] = []
                tracks[track].append(entry)
        
        for track, entries in tracks.items():
            filename = f'rag_dataset/track_{track}_enhanced.json'
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(entries, f, indent=2, ensure_ascii=False)
        print(f"  ✓ Saved {len(tracks)} track-specific files")
        
        # Save statistics
        stats = {
            "total_entries": len(self.dataset),
            "processing_stats": self.stats,
            "categories": {cat: len(entries) for cat, entries in categories.items()},
            "tracks": {track: len(entries) for track, entries in tracks.items()},
            "difficulty_levels": {
                "beginner": len([e for e in self.dataset if e['context']['difficulty'] == 'beginner']),
                "intermediate": len([e for e in self.dataset if e['context']['difficulty'] == 'intermediate']),
                "advanced": len([e for e in self.dataset if e['context']['difficulty'] == 'advanced'])
            },
            "data_sources": {},
            "generated_date": datetime.now().isoformat()
        }
        
        # Count data sources
        for entry in self.dataset:
            source = entry['context']['data_source']
            stats['data_sources'][source] = stats['data_sources'].get(source, 0) + 1
        
        with open('rag_dataset/enhanced_dataset_stats.json', 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2)
        print("  ✓ Saved enhanced_dataset_stats.json")
        
        print(f"\n📊 Final Statistics:")
        print(f"  Total entries: {stats['total_entries']}")
        print(f"  Tracks processed: {self.stats['tracks_processed']}")
        print(f"  Races processed: {self.stats['races_processed']}")
        print(f"  Files analyzed: {self.stats['files_analyzed']}")
        print(f"  Categories: {len(categories)}")
        print(f"  Difficulty levels: {stats['difficulty_levels']}")


def main():
    print("🏁 Toyota GR Cup Enhanced RAG Dataset Generator")
    print("=" * 70)
    print("Extracting data from all 7 tracks and 14 races...")
    print("Adding professional-level racing knowledge...")
    print()
    
    generator = EnhancedRAGDatasetGenerator()
    generator.generate_complete_dataset()
    
    print("\n" + "=" * 70)
    print("✅ Enhanced RAG Dataset Generation Complete!")
    print("\nDataset includes:")
    print("  • Real race data from all tracks")
    print("  • Professional driver development knowledge")
    print("  • Team operations and strategy")
    print("  • Advanced coaching techniques")
    print("  • Weather impact analysis")
    print("  • Data analysis methodologies")
    print("  • Performance metrics and benchmarking")
    print("=" * 70)


if __name__ == "__main__":
    main()
