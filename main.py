import os
from pathlib import Path
import httpx
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, Response
from fastapi.middleware.cors import CORSMiddleware

BASE_DIR = Path(__file__).resolve().parent
VOICE_ID = "qaDtMQq9uwKXGoMZ6p7R"
MODEL_ID = "eleven_multilingual_sts_v2"

app = FastAPI(title="AI Hindi Female Voice Changer")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def home():
    return FileResponse(BASE_DIR / "index.html")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/convert")
async def convert_voice(audio: UploadFile = File(...)):
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise HTTPException(500, "ELEVENLABS_API_KEY is not configured on the server.")

    audio_bytes = await audio.read()
    if not audio_bytes:
        raise HTTPException(400, "Audio file is empty.")

    url = f"https://api.elevenlabs.io/v1/speech-to-speech/{VOICE_ID}"
    params = {"output_format": "mp3_44100_128"}
    files = {"audio": (audio.filename or "recording.webm", audio_bytes, audio.content_type or "audio/webm")}
    data = {"model_id": MODEL_ID, "remove_background_noise": "true"}
    headers = {"xi-api-key": api_key}

    try:
        async with httpx.AsyncClient(timeout=180) as client:
            response = await client.post(url, params=params, headers=headers, files=files, data=data)
    except httpx.RequestError as exc:
        raise HTTPException(502, f"ElevenLabs connection failed: {exc}") from exc

    if response.status_code != 200:
        raise HTTPException(response.status_code, f"ElevenLabs error: {response.text[:2000]}")

    return Response(response.content, media_type="audio/mpeg")
