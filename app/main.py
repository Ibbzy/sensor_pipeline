from fastapi import FastAPI
from sensors.video_capture import capture_video
from sensors.audio_capture import capture_audio

app = FastAPI()

@app.get("/")
def read_root():
    return {"Healthy": "True"}

@app.get("/capture/video")
def capture_video_route():
    capture_video()
    return {"message": "Video captured successfully"}

@app.get("/capture/audio")
def capture_audio_route():
    capture_audio()
    return {"message": "Audio captured successfully"}
