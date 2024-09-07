from fastapi import FastAPI
from sensors.video_capture import capture_video
from sensors.audio_capture import capture_audio
from sensors.image_capture import capture_image
from app.sensor_data_handler import capture_and_upload_data
from models.image_processing import detect_labels, blur_labels
import os

import logging

DETECT_LABELS = os.getenv("UPLOAD_FILES_TO_GCS", "False").lower() == "true"
BLUR_ALL_IMAGES = os.getenv("BLUR_ALL_IMAGES", "False").lower() == "true"

# Configure logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.get("/")
def health_check():
    """Basic health check endpoint."""
    return {"status": "Healthy"}

@app.get("/capture/video")
def capture_video_endpoint():
    """Endpoint for capturing video data."""
    video_url = capture_and_upload_data("video", "mp4", capture_video)
    return {"message": "Video captured", "url": video_url}

@app.get("/capture/audio")
def capture_audio_endpoint():
    """Endpoint for capturing audio data."""
    audio_url = capture_and_upload_data("audio", "wav", capture_audio)
    return {"message": "Audio captured", "url": audio_url}

@app.get("/capture/image")
def capture_image_endpoint(target_labels = None):
    """Endpoint for capturing image data."""
    image_url = capture_and_upload_data("image", "jpg", capture_image)
    
    labels = detect_labels(image_url) if DETECT_LABELS else []
    target_labels = ["*"] if BLUR_ALL_IMAGES else (target_labels or [])
    
    blur_labels(image_url, labels, target_labels)

    return {"message": "Video captured successfully", "url": image_url, "labels": [label.description for label in labels]}