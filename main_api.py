from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from podcast_generator import generate_podcast

load_dotenv()

app = FastAPI()

class PodcastRequest(BaseModel):
    topic: str
    output_audio_filename: str = "podcast.mp3"
    output_script_filename: str = "script.txt"
    host_voice: str = "Aria"
    guest_voice: str = "Daniel"

class PodcastResponse(BaseModel):
    success: bool
    audio_path: str
    script_path: str

@app.post("/generate_podcast", response_model=PodcastResponse)
async def generate_podcast_api(req: PodcastRequest):
    try:
        result = generate_podcast(
            topic=req.topic,
            output_audio_file=req.output_audio_filename,
            output_script_file=req.output_script_filename,
            host_voice=req.host_voice,
            guest_voice=req.guest_voice
        )
        return PodcastResponse(success=True, **result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
