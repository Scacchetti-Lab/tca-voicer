from fastapi import UploadFile
from filetype import is_audio
from app.config import Settings
from urllib.parse import urlparse

async def is_valid_audio_file(audio: UploadFile):
    header = await audio.read(8192)
    await audio.seek(0)
    return is_audio(header)

async def is_valid_callback_url(url: str, env: Settings):
    host = urlparse(url).hostname
    callbacks = env.callback_urls.split('|')
    return host in callbacks