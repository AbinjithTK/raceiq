"""
Google Cloud Storage data loader
Downloads race data from GCS bucket on startup
"""

import os
from pathlib import Path
from google.cloud import storage
import logging

logger = logging.getLogger(__name__)

BUCKET_NAME = "raceiq-data-bucket"
DATA_FOLDERS = [
    "barber",
    "COTA", 
    "indianapolis",
    "road-america",
    "sebring",
    "Sonoma",
    "virginia-international-raceway",
    "rag_dataset"
]


def download_folder_from_gcs(bucket_name: str, folder_name: str, local_path: str = "/tmp"):
    """Download a folder from GCS to local filesystem"""
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        
        # List all blobs in the folder
        blobs = bucket.list_blobs(prefix=f"{folder_name}/")
        
        downloaded_count = 0
        for blob in blobs:
            # Skip if it's just the folder itself
            if blob.name.endswith('/'):
                continue
                
            # Create local file path
            local_file_path = Path(local_path) / blob.name
            local_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Download the file
            blob.download_to_filename(str(local_file_path))
            downloaded_count += 1
            
        logger.info(f"Downloaded {downloaded_count} files from {folder_name}")
        return True
        
    except Exception as e:
        logger.error(f"Error downloading {folder_name}: {e}")
        return False


def download_all_race_data(local_path: str = "/tmp"):
    """Download all race data folders from GCS"""
    logger.info(f"Downloading race data to {local_path}...")
    
    success_count = 0
    for folder in DATA_FOLDERS:
        if download_folder_from_gcs(BUCKET_NAME, folder, local_path):
            success_count += 1
    
    logger.info(f"Successfully downloaded {success_count}/{len(DATA_FOLDERS)} folders")
    return success_count == len(DATA_FOLDERS)


def get_data_path() -> str:
    """Get the path where data is stored (local or downloaded)"""
    # In production (Cloud Run), download to /tmp
    if os.getenv("K_SERVICE"):  # Cloud Run environment variable
        data_path = "/tmp"
        if not Path(data_path, "barber").exists():
            logger.info("Running in Cloud Run, downloading data from GCS...")
            download_all_race_data(data_path)
        return data_path
    else:
        # Local development - use current directory
        return "."
