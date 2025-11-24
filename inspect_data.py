import pandas as pd
import os

def inspect_csv(file_path):
    print(f"\n--- Inspecting {file_path} ---")
    try:
        # Read only the first few rows to get columns
        if 'telemetry' in file_path:
             df = pd.read_csv(file_path, nrows=5)
        else:
             df = pd.read_csv(file_path, delimiter=';', nrows=5)
        
        print(f"Columns ({len(df.columns)}):")
        for col in df.columns:
            print(f"  - {col}")
            
        print("\nSample Data:")
        print(df.head(2).to_string())
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

base_dir = "barber"
files = [
    "R1_barber_telemetry_data.csv",
    "26_Weather_Race 1_Anonymized.CSV",
    "03_Provisional Results_Race 1_Anonymized.CSV"
]

for f in files:
    inspect_csv(os.path.join(base_dir, f))
