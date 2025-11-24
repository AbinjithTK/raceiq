import pandas as pd
import os

def inspect_gps_long(file_path):
    print(f"\n--- Inspecting GPS in {file_path} ---")
    try:
        # Read a larger chunk to ensure we hit GPS data
        df = pd.read_csv(file_path, nrows=100000)
        
        # Filter for GPS channels
        gps_channels = ['VBOX_Lat_Min', 'VBOX_Long_Minutes']
        gps_data = df[df['telemetry_name'].isin(gps_channels)]
        
        if gps_data.empty:
            print("No GPS data found in first 100k rows.")
            return

        print(gps_data.head(10).to_string())
        
        # Show unique values to see format
        for channel in gps_channels:
            vals = df[df['telemetry_name'] == channel]['telemetry_value'].head(5).values
            print(f"\nSample {channel}: {vals}")
            
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

base_dir = "barber"
file_path = os.path.join(base_dir, "R1_barber_telemetry_data.csv")
inspect_gps_long(file_path)
