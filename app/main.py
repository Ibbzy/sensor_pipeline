from fastapi import FastAPI, HTTPException
from sensors.video_capture import capture_video
from sensors.audio_capture import capture_audio
from app.cloud_storage import upload_to_gcs
from app.util import generate_filename, get_partitioned_path
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Constants
UPLOAD_FILES_TO_GCS = os.getenv("UPLOAD_FILES_TO_GCS", "False").lower() == "true"
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
        return None
    except Exception as e:
        logging.error(f"Error during {sensor_type} upload: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to upload {sensor_type}: {str(e)}")

@app.get("/")
def health_check():
    """Basic health check endpoint."""
    return {"status": "Healthy"}

@app.get("/capture/video")
def capture_video_endpoint():
    """Endpoint for capturing video data."""
    local_video_path = capture_sensor_data("video", "mp4", capture_video)
    video_url = upload_sensor_data(local_video_path, "video")
    return {"message": "Video captured", "url": video_url}

@app.get("/capture/audio")
def capture_audio_endpoint():
    """Endpoint for capturing audio data."""
    local_audio_path = capture_sensor_data("audio", "wav", capture_audio)
    audio_url = upload_sensor_data(local_audio_path, "audio")
    return {"message": "Audio captured", "url": audio_url}
