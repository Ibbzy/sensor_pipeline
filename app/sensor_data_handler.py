
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
