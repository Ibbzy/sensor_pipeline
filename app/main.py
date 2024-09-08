from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sensors.video_sensor import VideoSensor
from sensors.audio_sensor import AudioSensor
from sensors.image_sensor import ImageSensor
from processing.image_processing import ImageProcessingPipeline
from app.sensor_data_handler import upload_sensor_data
from app.util import generate_filename

import aiofiles
import os

import logging


SUPPORTED_SENSOR_TYPES = ["video", "audio", "image"]


EXTENSION_MAP = {
    "video": "mp4",
    "audio": "wav",
    "image": "jpg",
}

SENSOR_MAP = {
    "video": VideoSensor(),
    "audio": AudioSensor(),
    "image": ImageSensor(),
}

PROCESSING_MAP = {
    "video": None,
    "audio": None,
    "image": ImageProcessingPipeline(),
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

@app.get("/capture/")
async def capture_sensor_data(sensor_type: str):
    
    if sensor_type not in SENSOR_MAP:
        raise HTTPException(status_code=400, detail="Unsupported sensor type")
    
    file_extension = EXTENSION_MAP.get(sensor_type)
    filename = generate_filename(sensor_type, file_extension)
    file_location = f"local_storage/{sensor_type}/{filename}"
    
    sensor = SENSOR_MAP.get(sensor_type)
    sensor.capture(file_location)
    file_url = upload_sensor_data(file_location, sensor_type)
    return {"message": f"{sensor_type.capitalize()} captured and uploaded successfully", "url": file_url}


@app.post("/upload/")
async def upload_data_endpoint(
    file: UploadFile = File(...), 
    sensor_type: str = Form(...)
):
    
    if sensor_type not in PROCESSING_MAP:
        raise HTTPException(status_code=400, detail="Unsupported sensor type")

    # Save the file locally
    _, file_extension = os.path.splitext(file.filename)
    filename = generate_filename(sensor_type, file_extension)
    file_location = f"local_storage/{sensor_type}/{filename}"
    async with aiofiles.open(file_location, 'wb') as out_file:
        content = await file.read()  # Read the file in chunks
        await out_file.write(content)

    processing_pipeline = PROCESSING_MAP.get(sensor_type)
    if processing_pipeline:
        processing_pipeline.process(file_location)

    file_url = upload_sensor_data(file_location, sensor_type)
    return {"message": f"{sensor_type.capitalize()} uploaded successfully", "url": file_url}