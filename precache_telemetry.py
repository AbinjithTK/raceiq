"""
Pre-cache telemetry data for demo
Run this before the demo to ensure instant loading
"""

from src.telemetry_processor import get_telemetry_processor
import time

def precache_demo_laps():
    """Pre-cache commonly used laps for smooth demo"""
    processor = get_telemetry_processor()
    
    # Laps to cache for demo
    demo_laps = [
        ('barber', 1, [5, 10, 15, 20]),
        # Add more tracks/laps as needed
    ]
    
    print("\n" + "="*60)
    print("PRE-CACHING TELEMETRY FOR DEMO")
    print("="*60)
    
    total_start = time.time()
    cached_count = 0
    
    for track, race, laps in demo_laps:
        print(f"\n📍 Track: {track.upper()}, Race: {race}")
        print("-" * 60)
        
        telemetry_file = f"{track}/R{race}_{track}_telemetry_data.csv"
        
        for lap in laps:
            # Check if already cached
            if processor.is_cached(track, race, lap):
                print(f"  ✅ Lap {lap:2d} - Already cached")
                cached_count += 1
                continue
            
            # Process and cache
            print(f"  🔄 Lap {lap:2d} - Processing...")
            start = time.time()
            
            try:
                result = processor.process_lap_telemetry(
                    telemetry_file,
                    lap,
                    track,
                    race,
                    sample_rate=50
                )
                
                elapsed = time.time() - start
                print(f"     ✅ Cached {len(result)} points in {elapsed:.1f}s")
                cached_count += 1
                
            except Exception as e:
                print(f"     ❌ Error: {e}")
    
    total_elapsed = time.time() - total_start
    
    print("\n" + "="*60)
    print("CACHING COMPLETE")
    print("="*60)
    print(f"Cached laps: {cached_count}")
    print(f"Total time: {total_elapsed:.1f}s")
    print(f"\n✅ Demo ready! Telemetry will load instantly.")
    print("="*60)


if __name__ == "__main__":
    precache_demo_laps()
