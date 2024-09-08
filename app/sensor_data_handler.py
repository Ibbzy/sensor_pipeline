
from fastapi import HTTPException
from app.cloud_storage import upload_to_gcs
from app.util import generate_filename, get_partitioned_path
import os
import logging


# Constants
UPLOAD_FILES_TO_GCS = False # os.getenv("UPLOAD_FILES_TO_GCS", "False").lower() == "true"
BUCKET_NAME = os.getenv("SENSOR_BUCKET_NAME")
if UPLOAD_FILES_TO_GCS and not BUCKET_NAME:
    raise ValueError("Bucket name not found. Please set the SENSOR_BUCKET_NAME environment variable.")

def capture_sensor_data(sensor_type: str, extension: str, capture_func) -> str:
    """Capture sensor data (audio/video) and save it locally."""
    try:
        filename = generate_filename(sensor_type, extension)
        local_path = f"local_storage/{sensor_type}/{filename}"

        logging.info(f"Starting {sensor_type} capture...")
        capture_func(local_path)
        logging.info(f"{sensor_type.capitalize()} capture complete: {local_path}")

        return local_path

    except Exception as e:
        logging.error(f"Error during {sensor_type} capture: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to capture {sensor_type}: {str(e)}")

def upload_sensor_data(local_path: str, sensor_type: str):
    """Upload captured sensor data to GCS, if required."""
    try:
        if UPLOAD_FILES_TO_GCS:
            logging.info(f"Uploading {sensor_type} to GCS...")
            filename = os.path.basename(local_path)
            destination_blob_name = get_partitioned_path(sensor_type, filename)
            file_url = upload_to_gcs(local_path, BUCKET_NAME, destination_blob_name)
            logging.info(f"{sensor_type.capitalize()} uploaded successfully: {file_url}")
            return file_url
        return local_path
    except Exception as e:
        logging.error(f"Error during {sensor_type} upload: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to upload {sensor_type}: {str(e)}")
    
def capture_and_upload_data(sensor_type: str, extension: str, capture_func):
    """Capture and upload sensor data to GCS."""
    local_path = capture_sensor_data(sensor_type, extension, capture_func)
    url = upload_sensor_data(local_path, sensor_type)
    return url