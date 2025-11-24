from src.multi_track_loader import MultiTrackLoader
from src.analysis.track_geometry import TrackGeometryGenerator
import pandas as pd

def debug():
    print("Initializing loader...")
    loader = MultiTrackLoader()
    generator = TrackGeometryGenerator(loader)
    
    track_name = "barber"
    print(f"Generating geometry for {track_name}...")
    
    # Manually call the logic to see where it fails
    try:
        df = loader.load_telemetry(track_name, 1)
        print(f"Loaded telemetry: {len(df)} rows")
        print(f"Columns: {df.columns.tolist()}")
        
        lap_num = 2
        lap_df = df[df['lap'] == lap_num]
        print(f"Lap {lap_num} rows: {len(lap_df)}")
        
        if lap_df.empty:
            print("Lap 2 empty, trying lap 1")
            lap_df = df[df['lap'] == 1]
            print(f"Lap 1 rows: {len(lap_df)}")
            
        gps_cols = ['VBOX_Lat_Min', 'VBOX_Long_Minutes']
        gps_df = lap_df[lap_df['telemetry_name'].isin(gps_cols)]
        print(f"GPS rows: {len(gps_df)}")
        
        if not gps_df.empty:
            print("Sample GPS data:")
            print(gps_df.head())
            
            pivoted = gps_df.pivot_table(
                index='timestamp', 
                columns='telemetry_name', 
                values='telemetry_value'
            ).reset_index()
            print(f"Pivoted rows: {len(pivoted)}")
            print(pivoted.head())
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug()
