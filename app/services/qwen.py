from re import split

from httpx import AsyncClient
from app.config import Settings
from app.constants.constants import SPEAKERS
from app.helpers.normalize_prompt import normalize_transcript

async def generate_audio(delta: str, env: Settings, speaker: SPEAKERS = "ryan"):
    message = normalize_transcript(delta)
    if not message:
        return
    
    payload = {
        "text": message,
        "speaker": speaker,
        "language": "Portuguese",
        "emotion": "calm",
        "instruct": "Fale em português do Brasil, com voz calma, tranquila e amigável, em ritmo moderado e pausado, com tom acolhedor e profissional, pronunciando cada palavra com clareza e sem sotaque estrangeiro.",
        "rate": 0.95,
        "volume": 1.0,
        "temperature": 0.4,
        "top_k": 50,
        "top_p": 0.9,
        "rep_penalty": 1.05,
        "seed": 42
    }
    url = f"{env.tts_host_url}/v1/tts/stream"
    async with AsyncClient(timeout=60) as client: 
        async with client.stream('POST', url, json=payload) as resp:
            resp.raise_for_status()
            async for chunk in resp.aiter_bytes():
                yield chunk
    