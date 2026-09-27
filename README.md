# AI Hindi Female Voice Changer

Mobile-friendly FastAPI website using ElevenLabs Speech-to-Speech.

## Features
- Android Chrome microphone recording
- Hindi/multilingual speech-to-speech
- Target Voice ID: `Be3X8pg7kLN4vyyMC3QN`
- Background-noise removal
- MP3 output
- Automatic playback when browser policy allows
- API key stays server-side

## Render deployment
Build command:
`pip install -r requirements.txt`

Start command:
`uvicorn main:app --host 0.0.0.0 --port $PORT`

Environment variable:
`ELEVENLABS_API_KEY`

Never put the API key in index.html or GitHub.
