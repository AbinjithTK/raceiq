import pandas as pd
import os

def inspect_csv(file_path):
    print(f"\n--- Inspecting {file_path} ---")
    try:
        # Read only the first few rows
        if 'telemetry' in file_path:
             # Telemetry is comma separated
             df = pd.read_csv(file_path, nrows=2)
        else:
             # Others might be semicolon
             try:
                 df = pd.read_csv(file_path, delimiter=';', nrows=2)
                 if len(df.columns) < 2:
                     df = pd.read_csv(file_path, delimiter=',', nrows=2)
             except:
                 df = pd.read_csv(file_path, delimiter=',', nrows=2)
        
        print(f"Column Count: {len(df.columns)}")
        print("Columns:")
        for col in sorted(df.columns):
            print(f"  {col}")
            
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

base_dir = "barber"
files = [
    "R1_barber_telemetry_data.csv",
    "26_Weather_Race 1_Anonymized.CSV"
]

for f in files:
    inspect_csv(os.path.join(base_dir, f))
