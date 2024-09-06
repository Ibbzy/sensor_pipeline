from fastapi import FastAPI
from sensors.video_capture import capture_video
from sensors.audio_capture import capture_audio
from app.cloud_storage import upload_to_gcs
from app.util import generate_filename
import os

app = FastAPI()

# Constants
LOCAL_VIDEO_PATH = "local_storage/video/"
LOCAL_AUDIO_PATH = "local_storage/audio/"

UPLOAD_FILES_TO_GCS = os.getenv("UPLOAD_FILES_TO_GCS", False)
BUCKET_NAME = os.getenv("SENSOR_BUCKET_NAME")
if UPLOAD_FILES_TO_GCS and not BUCKET_NAME:
    raise ValueError("Bucket name not found. Please set the SENSOR_BUCKET_NAME environment variable.")

@app.get("/")
def health_check():
    return {"status": "Healthy"}

@app.get("/capture/video")
def capture_video_endpoint():
    filename = generate_filename("video", "mp4")
    filename = "test.mp4"
    local_video_path = os.path.join(LOCAL_VIDEO_PATH, filename)
    
    capture_video(local_video_path)  # Pass the path where video will be saved

    video_url = None
    if UPLOAD_FILES_TO_GCS:
        video_url = upload_to_gcs(local_video_path, BUCKET_NAME, filename)
    
    return {"message": "Video captured", "url": video_url}

@app.get("/capture/audio")
def capture_audio_endpoint():
    filename = generate_filename("audio", "wav")
    local_audio_path = os.path.join(LOCAL_AUDIO_PATH, filename)

    capture_audio(local_audio_path)  # Pass the path where audio will be saved

    audio_url = None
    if UPLOAD_FILES_TO_GCS:
        audio_url = upload_to_gcs(local_audio_path, BUCKET_NAME, filename)

    return {"message": "Audio captured", "url": audio_url}
