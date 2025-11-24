import pandas as pd
import os

def get_telemetry_channels(file_path):
    print(f"\n--- Finding Channels in {file_path} ---")
    try:
        # Read a chunk to get a representative sample of channels
        # 1 million rows should be enough to see all channels cycling through
        df = pd.read_csv(file_path, nrows=1000000)
        
        channels = df['telemetry_name'].unique()
        print(f"Found {len(channels)} unique channels:")
        for channel in sorted(channels):
            print(f"  - {channel}")
            
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

base_dir = "barber"
file_path = os.path.join(base_dir, "R1_barber_telemetry_data.csv")
get_telemetry_channels(file_path)
