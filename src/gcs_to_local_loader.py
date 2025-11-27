"""
Download data from Google Cloud Storage to local filesystem
Works on AWS or any cloud platform
"""

import os
import requests
from pathlib import Path

# GCS bucket with public access
GCS_BUCKET_BASE = "https://storage.googleapis.com/raceiq-data-bucket"

# Files to download
DATA_FILES = {
    'barber': [
        '03_Provisional Results_Race 1_Anonymized.CSV',
        '05_Provisional Results by Class_Race 1_Anonymized.CSV',
        '23_AnalysisEnduranceWithSections_Race 1_Anonymized.CSV',
        '99_Best 10 Laps By Driver_Race 1_Anonymized.CSV',
        'R1_barber_lap_time.csv',
        'R1_barber_lap_start.csv',
        'R1_barber_lap_end.csv',
    ],
    'indianapolis': [
        '03_Provisional Results_Race 1_Anonymized.CSV',
        '05_Provisional Results by Class_Race 1_Anonymized.CSV',
        '23_AnalysisEnduranceWithSections_Race 1_Anonymized.CSV',
        '99_Best 10 Laps By Driver_Race 1_Anonymized.CSV',
        'R1_indianapolis_lap_time.csv',
    ],
    'rag_dataset': [
        'race_engineer_enhanced.jsonl',
    ]
}


def download_file(url: str, local_path: str) -> bool:
    """Download a file from URL to local path"""
    try:
        # Create directory if it doesn't exist
        Path(local_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Download file
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Save to local file
        with open(local_path, 'wb') as f:
            f.write(response.content)
        
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False


def download_all_data(base_path: str = "/tmp/raceiq_data") -> bool:
    """Download all required data files from GCS"""
    
    print(f"📥 Downloading race data to {base_path}...")
    
    success_count = 0
    total_count = 0
    
    for folder, files in DATA_FILES.items():
        for filename in files:
            total_count += 1
            
            # Construct GCS URL
            gcs_url = f"{GCS_BUCKET_BASE}/{folder}/{filename}"
            
            # Local path
            local_path = os.path.join(base_path, folder, filename)
            
            # Download
            if download_file(gcs_url, local_path):
                success_count += 1
                print(f"  ✅ {folder}/{filename}")
            else:
                print(f"  ❌ {folder}/{filename}")
    
    print(f"\n📊 Downloaded {success_count}/{total_count} files")
    return success_count == total_count


def ensure_data_available(base_path: str = "/tmp/raceiq_data") -> str:
    """Ensure data is available, download if needed"""
    
    # Check if data already exists
    barber_check = os.path.join(base_path, "barber", "03_Provisional Results_Race 1_Anonymized.CSV")
    
    if os.path.exists(barber_check):
        print(f"✅ Data already available at {base_path}")
        return base_path
    
    # Download data
    print(f"📥 Data not found, downloading from GCS...")
    download_all_data(base_path)
    
    return base_path
