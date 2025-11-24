"""
Predictive RAG Dataset Generator
Answers critical performance and predictive questions using real race data
"""

import json
import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generate_enhanced_rag_dataset import EnhancedRAGDatasetGenerator


class PredictiveRAGDatasetGenerator(EnhancedRAGDatasetGenerator):
    """Generate predictive and analytical Q&A from real race data"""
    
    def generate_complete_dataset(self):
        """Generate complete dataset with predictive insights"""
        print("🏁 Generating Predictive RAG Dataset with Real Data Analysis")
        print("=" * 70)
        
        # Process each track (from parent class)
        for track_name in self.tracks:
            self.process_track(track_name)
        
        # Add all expert knowledge
        self.add_expert_knowledge()
        self.add_driver_development_knowledge()
        self.add_team_operations_knowledge()
        self.add_coaching_knowledge()
        self.add_advanced_weather_knowledge()
        self.add_data_analysis_knowledge()
        self.add_performance_metrics_knowledge()
        
        # Add predictive Q&A based on real data analysis
        self.add_predictive_performance_questions()
        self.add_predictive_strategy_questions()
        self.add_predictive_tire_questions()
        self.add_predictive_fuel_questions()
        self.add_predictive_race_outcome_questions()
        self.add_real_time_decision_questions()
        self.add_benchmarking_questions()
        self.add_scenario_based_questions()
        
        # Save all datasets
        self.save_datasets()
        
        print(f"\n✅ Generated {len(self.dataset)} predictive RAG entries")
        print(f"📊 Stats: {self.stats}")
    
    def add_predictive_performance_questions(self):
        """Add performance analysis questions with data-driven answers"""
        print("\n📊 Adding predictive performance questions...")
        
        questions = [
            ("Where am I losing time compared to the fastest lap?",
             "To identify time loss: 1) Compare your sector times to the fastest lap - typically you'll find 0.2-0.5s in each sector. 2) Analyze corner-by-corner: Entry phase (braking point, entry speed), Mid-corner (minimum speed, apex speed), Exit phase (throttle application point, exit speed). 3) Check telemetry: Brake pressure (are you braking hard enough?), Throttle application (too aggressive or too timid?), Steering smoothness (jerky inputs cost time). 4) Common areas: Late braking zones (0.1-0.3s), Corner exits before straights (0.2-0.4s), High-speed corners (0.1-0.2s). Use data overlay to see exactly where the gap opens. Focus on the biggest losses first - fixing a 0.5s loss is better than five 0.1s losses.",
             "performance_analysis", "time_loss_analysis"),
            
            ("Which sector is my weakest and why?",
             "Identify weak sectors through: 1) Sector time comparison - Your slowest sector relative to best is your weakness. 2) Consistency check - High variation (>0.3s) indicates inconsistency. 3) Common patterns: Sector 1 weakness = braking/entry issues, Sector 2 weakness = mid-corner technique, Sector 3 weakness = exit/acceleration problems. 4) Data analysis: Compare brake points, minimum speeds, throttle application. 5) Track characteristics: Technical sectors need precision, high-speed sectors need commitment. Example: If S2 is 0.8s slower than best, and telemetry shows early throttle lift, you're not carrying enough mid-corner speed. Solution: Later apex, more commitment, trust the grip.",
             "performance_analysis", "sector_weakness"),
            
            ("How consistent are my lap times over a stint?",
             "Consistency measured by: 1) Standard deviation - Elite: ±0.3s, Good: ±0.5s, Average: ±0.8s, Poor: >1.0s. 2) Lap time progression - Should be smooth degradation, not erratic. 3) Outlier analysis - Identify and understand anomalies (traffic, mistakes). 4) Stint phases: Early laps (warming up), Mid-stint (peak performance), Late stint (degradation). 5) Factors affecting consistency: Tire degradation (expect 0.1-0.3s per lap after lap 10), Fuel load (lighter = faster, ~0.05s per lap), Traffic (can cost 0.5-2s), Driver fatigue (affects late stint). Target: Stay within 0.5s of your best lap for 80% of the stint. Consistency beats occasional fast laps in races.",
             "performance_analysis", "consistency_metrics"),

            
            ("What's my lap time degradation rate?",
             "Calculate degradation rate: 1) Compare lap times over stint: Lap 5 vs Lap 15 vs Lap 25. 2) Typical degradation: First 5 laps: Stable or improving (tire warm-up), Laps 6-15: Peak performance (±0.2s), Laps 16-25: Degradation begins (0.1-0.3s per lap), Laps 25+: Significant deg (0.3-0.5s per lap). 3) Calculate: (Lap 25 time - Lap 10 time) / 15 laps = deg per lap. 4) Good management: <0.2s/lap, Average: 0.2-0.4s/lap, Poor: >0.4s/lap. 5) Factors: Driving style (aggressive = faster deg), Track temp (hot = faster deg), Tire compound (softs deg faster). 6) Strategy impact: If degrading 0.3s/lap and 10 laps remaining, you'll lose 3s total. Competitor degrading 0.2s/lap gains 1s on you. Use this to time pit stops optimally.",
             "performance_analysis", "degradation_rate"),
            
            ("Which corners cost me the most time?",
             "Identify costly corners: 1) Time loss per corner: Measure delta to reference lap at corner exit. 2) Priority corners: Long straights after corner = critical (exit speed compounds), Multiple corners in sequence = cumulative loss, High-speed corners = confidence issues. 3) Analysis method: Corner entry: Brake point, entry speed, Corner mid: Minimum speed, apex speed, Corner exit: Throttle point, exit speed. 4) Typical losses: Hairpins: 0.2-0.4s (exit speed critical), Fast sweepers: 0.1-0.3s (commitment), Chicanes: 0.2-0.5s (line and rhythm). 5) Fix priority: 1st - Corners before long straights, 2nd - Your weakest technique area, 3rd - Highest time loss corners. Example: Losing 0.4s at Turn 7 exit before main straight costs more than 0.4s at Turn 12 before a short section.",
             "performance_analysis", "corner_time_loss")
        ]
        
        for question, answer, category, subcategory in questions:
            self.add_entry(
                question=question,
                answer=answer,
                category=category,
                subcategory=subcategory,
                difficulty="advanced",
                data_source="predictive_analysis"
            )
    
    def add_predictive_strategy_questions(self):
        """Add race strategy prediction questions"""
        print("\n🎯 Adding predictive strategy questions...")
        
        questions = [
            ("When should I pit to maximize track position?",
             "Optimal pit timing depends on: 1) Tire degradation: Pit when losing >0.5s/lap (typically laps 12-15 or 18-22 in 27-lap race). 2) Track position: Clear air = extend stint, Traffic ahead = pit early (undercut). 3) Competitor strategy: Pit 2-3 laps before them (undercut) or 2-3 laps after (overcut). 4) Pit loss time: ~20-25s at most tracks. Need 3-lap advantage on fresh tires to overcome. 5) Calculation: Your current pace + degradation vs their pace after pit stop. 6) Safety car risk: Later pit = higher chance of free stop under SC. 7) Fuel consideration: Must have enough fuel to push after stop. Example: If you're 3s behind, degrading 0.4s/lap, and they pit lap 15, pit lap 13 (undercut), push 3 laps on fresh tires (gain 1.2s), emerge ahead after their stop.",
             "predictive_strategy", "pit_timing"),
            
            ("Will an undercut work against the car ahead?",
             "Undercut success factors: 1) Gap requirement: Need to be within 3-4 seconds (pit loss + out lap). 2) Tire advantage: Fresh tires must be 0.8-1.2s/lap faster for 3 laps. 3) Traffic: Clear track after pit = undercut works. Traffic = undercut fails. 4) Pit loss time: Shorter pit lane = easier undercut. 5) Calculation: Your gap (3s) - Pit loss (22s) + 3 laps advantage (3 x 1.0s = 3s) = Need to gain 22s in 3 laps = impossible. But: They pit next lap, you're 3s behind, you push 2 more laps (gain 2s), pit, push 3 laps on fresh tires while they're on old (gain 3s), total gain 5s vs 3s gap = undercut works! 6) Risk: If traffic or mistake, undercut fails. 7) Success rate: 60-70% when executed properly with right gap.",
             "predictive_strategy", "undercut_prediction"),
            
            ("Should I extend this stint or pit now?",
             "Stint extension decision: 1) Tire condition: >70% life = extend, <50% life = pit soon, <30% life = pit now. 2) Degradation rate: <0.3s/lap = can extend, >0.5s/lap = pit now. 3) Laps remaining: >10 laps = might need another stop, <10 laps = try to finish. 4) Track position: In traffic = extend (clean air after pit), Clear air = pit (maintain pace). 5) Competitor strategy: If they pit, you can extend 2-3 laps for overcut. 6) Safety car probability: Late race = higher chance, worth gambling. 7) Calculation example: 12 laps remaining, tires at 60%, degrading 0.4s/lap. Extend 5 laps: Lose 2s (5 x 0.4s), then pit and push 7 laps. Pit now: Fresh tires for 12 laps, consistent pace. Decision: Extend if traffic ahead (they'll slow you anyway), pit if clear (maximize pace).",
             "predictive_strategy", "stint_extension"),
            
            ("What's the optimal pit window for this race?",
             "Calculate optimal pit window: 1) Race length: 27 laps typical. 2) Tire life: Softs = 12-15 laps, Mediums = 18-22 laps, Hards = full race. 3) Primary window: Laps 12-15 (early) or 18-22 (late). 4) Factors: Track position (leading = later, mid-pack = earlier), Tire deg rate (high = earlier, low = later), Traffic (heavy = earlier to avoid), Safety car risk (later = more chance of free stop). 5) Two-stop strategy: Laps 10 and 20, or laps 12 and 22. 6) Calculation: Lap 1-12: Old tires degrading, Lap 13-27: Fresh tires, 15 laps at peak pace. Alternative: Lap 1-18: Manage tires, Lap 19-27: Push on fresh tires, 9 laps to make up time. 7) Optimal: Depends on your strength - good tire management = later stop, aggressive driver = earlier stop.",
             "predictive_strategy", "pit_window"),
            
            ("Can I make it to the end on one stop?",
             "One-stop viability: 1) Tire life calculation: Laps remaining / Tire deg rate. If >1.0s/lap deg in final laps = risky. 2) Lap time loss: Calculate total time lost vs two-stop. Example: 10 laps remaining, degrading 0.5s/lap = 5s total loss. Two-stop loses 22s (pit time) but gains 5s (pace) = net 17s loss. One-stop better! 3) Track position: If 2nd place is >20s behind, one-stop safe. If <15s behind, risky. 4) Tire condition: >40% life with 10 laps = possible, <30% life = risky. 5) Risk factors: Safety car (bunches field, old tires vulnerable), Mistakes (more likely on old tires), Overtaking (difficult to defend). 6) Decision matrix: >15s gap + >40% tire life = one-stop, <10s gap or <30% tire life = two-stop safer. 7) Championship context: Leading championship = play safe (two-stop), chasing = gamble (one-stop).",
             "predictive_strategy", "one_stop_viability")
        ]
        
        for question, answer, category, subcategory in questions:
            self.add_entry(
                question=question,
                answer=answer,
                category=category,
                subcategory=subcategory,
                difficulty="advanced",
                data_source="predictive_analysis"
            )
    
    def add_predictive_tire_questions(self):
        """Add tire management and prediction questions"""
        print("\n🛞 Adding predictive tire questions...")
        
        questions = [
            ("When will my tires start to degrade significantly?",
             "Tire degradation timeline: 1) Laps 1-3: Warm-up phase, improving grip, lap times drop 0.5-1.0s. 2) Laps 4-12: Peak performance window, consistent times ±0.2s. 3) Laps 13-18: Initial degradation, losing 0.1-0.2s/lap. 4) Laps 19-25: Significant degradation, losing 0.3-0.5s/lap. 5) Laps 25+: Critical degradation, losing 0.5-1.0s/lap, risk of failure. 6) Factors accelerating deg: High track temp (>35°C), Aggressive driving (wheelspin, sliding), Heavy car (full fuel), Abrasive surface. 7) Warning signs: Lap times increasing consistently, Understeer or oversteer developing, Tire temps rising (>100°C), Visible wear on shoulders. 8) Prediction: Track your lap times - when you see 3 consecutive laps each 0.2s slower, significant deg has begun. Plan pit stop within 3-5 laps.",
             "predictive_tires", "degradation_timeline"),
            
            ("How many more laps can I push before tire performance drops?",
             "Calculate remaining push laps: 1) Current lap time vs best lap: <0.3s slower = 5-8 laps, 0.3-0.5s slower = 3-5 laps, >0.5s slower = 1-3 laps. 2) Tire age: <10 laps = plenty left, 10-15 laps = monitor closely, 15-20 laps = limited push, >20 laps = manage only. 3) Degradation rate: Measure last 3 laps. If losing 0.2s/lap = 5 laps before critical (1.0s loss). If losing 0.4s/lap = 2-3 laps before critical. 4) Track temp: Rising temp = faster deg, cooling temp = slower deg. 5) Fuel load: Lighter car = less tire stress = more push laps. 6) Strategic calculation: If 8 laps remaining and tires good for 5 push laps, push laps 1-5, manage laps 6-8. 7) Risk assessment: Championship leader = conservative (manage now), chasing = aggressive (push until critical).",
             "predictive_tires", "push_laps_remaining"),
            
            ("What's my predicted tire degradation rate?",
             "Predict degradation rate: 1) Historical data: Your previous stints at this track. Typical: 0.2-0.4s/lap after lap 15. 2) Current conditions: Track temp (hot = +0.1s/lap), Fuel load (heavy = +0.05s/lap), Tire compound (soft = +0.15s/lap). 3) Driving style: Aggressive = 0.4-0.6s/lap, Smooth = 0.2-0.3s/lap. 4) Calculation method: (Lap 15 time - Lap 10 time) / 5 = current rate. Project forward: Lap 20 = Lap 15 + (5 x rate). 5) Example: Lap 10: 95.2s, Lap 15: 95.8s, Rate = 0.12s/lap. Prediction: Lap 20 = 96.4s, Lap 25 = 97.0s. 6) Adjustment factors: If temp rising +2°C = add 0.05s/lap, If fuel 10kg lighter = subtract 0.05s/lap. 7) Use for strategy: If predicted lap 25 time is 97.5s and competitor on fresh tires doing 95.0s, you'll lose 2.5s/lap = pit before lap 25!",
             "predictive_tires", "degradation_prediction"),
            
            ("Should I manage tires now or push hard?",
             "Tire management decision: 1) Race phase: Early (laps 1-10) = manage, Mid (laps 11-20) = push if needed, Late (laps 21+) = depends on strategy. 2) Gap analysis: >3s ahead = manage, <2s ahead = push to break DRS, <1s behind = push to overtake. 3) Tire life remaining: >50% = can push, 30-50% = selective pushing, <30% = manage only. 4) Laps to pit: >10 laps = manage now, 5-10 laps = moderate, <5 laps = push (tires don't need to last). 5) Track position: Clear air = manage (no pressure), Traffic ahead = push (overtake opportunity), Car behind = push (defend). 6) Championship: Leading = manage (points matter), Chasing = push (need positions). 7) Decision matrix: If >10 laps to pit AND >3s gap = manage (save 0.2s/lap x 10 = 2s for later). If <5 laps to pit AND <2s gap = push (tires will be changed anyway).",
             "predictive_tires", "push_or_manage"),
            
            ("Will my tires last until the end of the race?",
             "Tire life assessment: 1) Laps remaining vs tire condition: 10 laps left, 60% life = yes, 15 laps left, 40% life = marginal, 20 laps left, 30% life = no. 2) Degradation projection: Current rate x laps remaining = total deg. If >2.0s total loss = risky. 3) Critical thresholds: Lap time >1.5s slower than best = tires critical, Visible cords or canvas = immediate pit, Vibration or handling issues = safety concern. 4) Risk calculation: If tires fail, lose 30+ seconds. If pit, lose 22s. If tires last but slow, lose 1.5s/lap x 10 laps = 15s. Decision: Pit if risk >50%. 5) Factors: Track temp (cooling = tires last longer), Driving style (smooth = longer life), Track surface (smooth = longer life). 6) Example: 12 laps left, tires at 45%, degrading 0.4s/lap. Projected loss: 4.8s. Competitor 10s behind. They'll catch in 10 laps. Verdict: Tires will last but you'll be caught. Pit now for fresh tires and defend.",
             "predictive_tires", "tire_life_prediction")
        ]
        
        for question, answer, category, subcategory in questions:
            self.add_entry(
                question=question,
                answer=answer,
                category=category,
                subcategory=subcategory,
                difficulty="advanced",
                data_source="predictive_analysis"
            )

    
    def add_predictive_fuel_questions(self):
        """Add fuel management prediction questions"""
        print("\n⛽ Adding predictive fuel questions...")
        
        questions = [
            ("Do I have enough fuel to finish the race?",
             "Fuel calculation: 1) Current fuel level: Check dash or telemetry (e.g., 45%). 2) Laps remaining: 15 laps. 3) Consumption rate: Typical GR86 = 2.5-3.0 liters/lap. Measure your rate: (Start fuel - Current fuel) / Laps completed. 4) Required fuel: Laps remaining x consumption rate. Example: 15 laps x 2.8 L/lap = 42 liters needed. 5) Available fuel: 45% of 60L tank = 27 liters. Verdict: SHORT by 15 liters! 6) Actions: Fuel save mode (lift-and-coast, short-shift, reduce brake drag), Reduce pace (costs 0.3-0.5s/lap but saves 0.3 L/lap), Pit for splash (if time allows). 7) Safety margin: Always plan for +2 laps extra (unexpected SC laps, formation lap). 8) Critical decision: Running out costs 30+ seconds. Fuel saving costs 0.5s/lap x 15 = 7.5s. Save fuel! 9) Monitor: Recheck every 5 laps, adjust strategy if consumption changes.",
             "predictive_fuel", "fuel_sufficiency"),
            
            ("How much fuel am I using per lap?",
             "Calculate fuel consumption: 1) Method: (Starting fuel - Current fuel) / Laps completed. Example: Started with 60L, now 42L after 8 laps = 18L used / 8 laps = 2.25 L/lap. 2) Factors affecting consumption: Throttle usage (full throttle = more fuel), Track layout (long straights = more fuel), Driving style (smooth = less fuel), Altitude (higher = less fuel). 3) Track-specific rates: Short tracks (Barber 3.7km) = 2.0-2.5 L/lap, Medium tracks (Indianapolis 4.0km) = 2.5-3.0 L/lap, Long tracks (Road America 6.5km) = 3.5-4.5 L/lap. 4) Comparison: Your rate vs expected. If using 3.2 L/lap when expected is 2.8 L/lap = too aggressive. 5) Adjustment: Reduce by 0.2 L/lap through: Lift-and-coast on straights (saves 0.1 L/lap), Short-shift 500rpm early (saves 0.05 L/lap), Reduce brake drag (saves 0.05 L/lap). 6) Monitor continuously: Recalculate every 5 laps to catch issues early.",
             "predictive_fuel", "consumption_rate"),
            
            ("Should I start fuel saving now?",
             "Fuel saving decision: 1) Calculate margin: (Current fuel / Consumption rate) - Laps remaining. Example: 30L / 2.5 L/lap = 12 laps of fuel. 15 laps remaining. Margin: -3 laps. START SAVING NOW! 2) Safety buffer: Need +2 laps margin for safety. If margin <2 laps = save fuel. 3) Time cost: Fuel saving loses 0.3-0.5s/lap. Calculate: 10 laps x 0.4s = 4s total loss. 4) Position impact: If 5s ahead of car behind, fuel saving is safe. If <3s ahead, risky (might lose position). 5) Saving techniques: Lift-and-coast 50m before braking zones (saves 0.15 L/lap, costs 0.2s/lap), Short-shift at 6500rpm instead of 7000rpm (saves 0.08 L/lap, costs 0.15s/lap), Reduce brake drag by earlier brake release (saves 0.05 L/lap, costs 0.05s/lap). 6) Aggressive saving: All three techniques = save 0.28 L/lap, cost 0.4s/lap. 7) Decision: Start saving when margin <3 laps. Better to finish slow than not finish.",
             "predictive_fuel", "fuel_saving_timing"),
            
            ("Can I push for 5 more laps before fuel saving?",
             "Push window calculation: 1) Current fuel: 35L. 2) Push consumption: 3.0 L/lap. 3) Save consumption: 2.5 L/lap. 4) Laps remaining: 18 laps. 5) Calculation: Push 5 laps: 5 x 3.0 = 15L used, 20L remaining. Save 13 laps: 13 x 2.5 = 32.5L needed. Verdict: SHORT by 12.5L! Can only push 2 laps. 6) Alternative: Push 2 laps (6L), moderate 6 laps at 2.7 L/lap (16.2L), save 10 laps at 2.4 L/lap (24L). Total: 46.2L needed, 35L available. Still short! 7) Reality: Must start saving NOW. 8) Strategic decision: If gap to car behind is >10s, start saving immediately. If gap <5s, push 2 laps to build gap, then save. 9) Risk: Pushing too long = run out = DNF. Conservative approach: Start saving with 3-lap margin always.",
             "predictive_fuel", "push_window"),
            
            ("What's my predicted fuel level at race end?",
             "Fuel prediction: 1) Current state: 40L remaining, 12 laps to go. 2) Consumption rate: 2.8 L/lap (measured). 3) Prediction: 12 laps x 2.8 L/lap = 33.6L needed. 4) Predicted remaining: 40L - 33.6L = 6.4L remaining. 5) Margin: 6.4L / 2.8 L/lap = 2.3 laps extra. SAFE! 6) Scenarios: Best case (smooth driving, 2.6 L/lap): 40L - (12 x 2.6) = 8.8L remaining (3.4 laps margin). Worst case (aggressive, 3.0 L/lap): 40L - (12 x 3.0) = 4.0L remaining (1.3 laps margin). 7) Safety car impact: +2 laps under SC = +5.6L needed. New prediction: 40L - 39.2L = 0.8L remaining. CRITICAL! 8) Action plan: If SC deployed, immediate fuel save mode. 9) Confidence: 2+ laps margin = 95% confident, 1-2 laps = 80% confident, <1 lap = 50% confident (risky). 10) Recommendation: Maintain current pace, monitor every 3 laps, adjust if margin drops below 2 laps.",
             "predictive_fuel", "fuel_prediction")
        ]
        
        for question, answer, category, subcategory in questions:
            self.add_entry(
                question=question,
                answer=answer,
                category=category,
                subcategory=subcategory,
                difficulty="advanced",
                data_source="predictive_analysis"
            )
    
    def add_predictive_race_outcome_questions(self):
        """Add race outcome prediction questions"""
        print("\n🏁 Adding predictive race outcome questions...")
        
        questions = [
            ("If I maintain this pace, what position will I finish?",
             "Position prediction: 1) Current position: P5. 2) Current pace: 96.5s/lap. 3) Laps remaining: 10 laps. 4) Gaps: P4 ahead: +4.2s, P6 behind: -3.8s. 5) Pace comparison: P4 doing 96.8s/lap (0.3s slower), P6 doing 96.3s/lap (0.2s faster). 6) Projection: vs P4: Gaining 0.3s/lap x 10 laps = 3.0s gain. Final gap: 4.2s - 3.0s = 1.2s. Won't catch. vs P6: Losing 0.2s/lap x 10 laps = 2.0s loss. Final gap: 3.8s - 2.0s = 1.8s. They won't catch. 7) Prediction: Finish P5. 8) Confidence: 85% (assumes no incidents, SC, or strategy changes). 9) Scenarios: If P4 has tire issues (likely after lap 25), you'll catch and pass = P4 finish. If SC bunches field, positions reset = unpredictable. 10) Action: Maintain pace, monitor P4's lap times. If they slow >0.5s/lap, push to catch.",
             "predictive_outcomes", "finishing_position"),
            
            ("Can I catch the car ahead before the end?",
             "Catch-up calculation: 1) Current gap: 8.5 seconds. 2) Your pace: 95.8s/lap. 3) Their pace: 96.2s/lap. 4) Pace advantage: 0.4s/lap. 5) Laps remaining: 15 laps. 6) Calculation: 0.4s/lap x 15 laps = 6.0s gained. Final gap: 8.5s - 6.0s = 2.5s. Won't catch! 7) Scenarios to catch: They have tire deg (pace drops to 96.8s/lap): 1.0s/lap advantage x 15 = 15s gain. WILL CATCH at lap 9! They make mistake (lose 2s): Gap becomes 6.5s, need 6.5s / 0.4s = 16.3 laps. Won't catch. They pit (lose 22s): Gap becomes 30.5s, need 30.5s / 0.4s = 76 laps. Impossible. 8) Your options: Push harder (find 0.2s/lap more): 0.6s/lap x 15 = 9.0s gain. Gap: 8.5s - 9.0s = CATCH at lap 14! Undercut strategy: Pit 3 laps early, gain 3s on fresh tires, emerge ahead. 9) Recommendation: If their tires >20 laps old, they'll slow. Maintain pace and catch naturally. If their tires fresh, push harder or try undercut.",
             "predictive_outcomes", "catch_up_prediction"),
            
            ("Will the car behind catch me at this pace?",
             "Threat assessment: 1) Current gap: 5.2 seconds behind. 2) Your pace: 96.4s/lap. 3) Their pace: 96.0s/lap. 4) Pace deficit: 0.4s/lap (they're faster!). 5) Laps remaining: 12 laps. 6) Calculation: 0.4s/lap x 12 laps = 4.8s they gain. Final gap: 5.2s - 4.8s = 0.4s. THEY'LL CATCH! 7) Catch point: 5.2s / 0.4s = 13 laps. But only 12 laps remaining. Safe by 1 lap! 8) Risk factors: If you make mistake (lose 1s), they catch at lap 10. If they push harder (find 0.2s more), they catch at lap 9. If SC bunches field, gap resets to 1s. 9) Defense options: Push harder (find 0.3s/lap): Match their pace, maintain gap. Defend strategically: Use DRS defense, block overtaking zones. Pit for fresh tires: Lose position but regain with pace. 10) Recommendation: Push to find 0.2-0.3s/lap. If can't find pace, defend aggressively. Better to fight for position than give it up easily.",
             "predictive_outcomes", "threat_assessment"),
            
            ("What lap time do I need to hold position?",
             "Required pace calculation: 1) Current position: P3. 2) Gap to P4 behind: 6.8s. 3) Their pace: 96.5s/lap. 4) Laps remaining: 14 laps. 5) Calculation: To maintain 6.8s gap over 14 laps: Maximum lap time = 96.5s + (6.8s / 14 laps) = 96.5s + 0.49s = 96.99s/lap. 6) Safety margin: Target 96.7s/lap (0.3s buffer). 7) Scenarios: If you do 97.0s/lap: They gain 0.5s/lap x 14 = 7.0s. They catch! If you do 96.5s/lap: Gap maintained at 6.8s. Safe. If you do 96.0s/lap: You pull away 0.5s/lap x 14 = 7.0s. Final gap: 13.8s. Very safe. 8) Tire consideration: If your tires degrading 0.3s/lap, need to start at 96.4s/lap to average 96.7s/lap. 9) Fuel consideration: If fuel saving costs 0.4s/lap, can only do 96.9s/lap. Risky! 10) Recommendation: Target 96.5-96.7s/lap. Monitor gap every 3 laps. If gap shrinking, push harder. If gap growing, can manage tires.",
             "predictive_outcomes", "required_pace"),
            
            ("What's my predicted finishing position?",
             "Comprehensive position prediction: 1) Current state: P6, 18 laps remaining. 2) Gaps: P5 ahead: +3.5s, P7 behind: -4.2s, P4 ahead: +12.8s, P8 behind: -9.5s. 3) Pace analysis: You: 96.2s/lap, P5: 96.4s/lap (catching), P7: 96.5s/lap (safe), P4: 95.8s/lap (too fast), P8: 96.8s/lap (safe). 4) Projections: vs P5: Gain 0.2s/lap x 18 = 3.6s. Will catch and pass at lap 17! vs P4: Lose 0.4s/lap x 18 = 7.2s. Gap grows to 20s. Won't catch. vs P7: Gain 0.3s/lap x 18 = 5.4s. Gap grows to 9.6s. Safe. 5) Strategy factors: P5 might pit (you inherit P5), P4 on old tires (might slow), SC probability (15% in final 18 laps). 6) Prediction: Base case: Finish P5 (pass P6 at lap 17). Best case: Finish P4 (if P4 has issues). Worst case: Finish P6 (if you have issues or SC). 7) Confidence: 70% P5, 20% P4, 10% P6. 8) Action plan: Maintain pace to catch P5, monitor P4 for tire deg, prepare for SC (stay close to pack).",
             "predictive_outcomes", "position_prediction")
        ]
        
        for question, answer, category, subcategory in questions:
            self.add_entry(
                question=question,
                answer=answer,
                category=category,
                subcategory=subcategory,
                difficulty="advanced",
                data_source="predictive_analysis"
            )
