import pandas as pd
import os

def inspect_gps(file_path):
    print(f"\n--- Inspecting GPS in {file_path} ---")
    try:
        # Read a chunk
        df = pd.read_csv(file_path, nrows=10000)
        
        # Filter for GPS columns
        gps_cols = ['VBOX_Lat_Min', 'VBOX_Long_Minutes', 'lap', 'Laptrigger_lapdist_dls']
        
        # Check if columns exist
        available_cols = [c for c in gps_cols if c in df.columns]
        
        if not available_cols:
            print("No GPS columns found.")
            return

        print(df[available_cols].head(10).to_string())
        
        # Check for non-nulls
        print("\nNon-null counts:")
        print(df[available_cols].count())
            
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

base_dir = "barber"
file_path = os.path.join(base_dir, "R1_barber_telemetry_data.csv")
inspect_gps(file_path)
