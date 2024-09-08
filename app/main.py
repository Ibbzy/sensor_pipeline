from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from sensors.video_capture import capture_video
from sensors.audio_capture import capture_audio
from sensors.image_capture import capture_image
from app.sensor_data_handler import capture_and_upload_data, upload_sensor_data
from models.image_processing import process_image
from app.util import generate_filename

import aiofiles
import os

import logging


SUPPORTED_SENSOR_TYPES = ["video", "audio", "image"]
SENSOR_TYPE_PROCESSORS = {
    "video": None,
    "audio": None,
    "image": process_image
}

# Configure logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Allow all origins, methods, and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def health_check():
    """Basic health check endpoint."""
    return {"status": "Healthy"}

@app.post("/upload/")
async def upload_data_endpoint(
    file: UploadFile = File(...), 
    sensor_type: str = Form(...)
):
    
    if sensor_type not in SUPPORTED_SENSOR_TYPES:
        return {"message": "Unsupported sensor type"}

    # Save the file locally
    _, extension = os.path.splitext(file.filename)
    filename = generate_filename(sensor_type, extension)
    file_path = f"local_storage/{sensor_type}/{filename}"
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()  # Read the file in chunks
        await out_file.write(content)
    
    # Process based on sensor type
    processor = SENSOR_TYPE_PROCESSORS[sensor_type]
    if processor:
        processor(file_path)
    file_url = upload_sensor_data(file_path, sensor_type)
    return {"url": file_url, "sensor_type": sensor_type, "message": "File uploaded successfully"}


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
    _, labels = process_image(image_url, target_labels)

    return {"message": "Image captured successfully", "url": image_url, "labels": labels}