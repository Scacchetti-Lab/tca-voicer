from re import split
from fastapi import UploadFile
from filetype import is_audio
from app.config import Settings
from urllib.parse import urlparse
from base64 import b64encode

from app.constants.constants import MP4_AUDIO_BRANDS

async def is_valid_audio_file(audio: UploadFile):
    if await is_mp4_audio(audio):
        return True
    header = await audio.read(8192)
    await audio.seek(0)
    return is_audio(header)

async def is_valid_callback_url(url: str, env: Settings):
    host = urlparse(url).hostname
    callbacks = env.callback_urls.split('|')
    return host in callbacks

async def is_mp4_audio(file: UploadFile) -> bool:
    try:
        await file.seek(0)
        header = await file.read(12)
        return header[4:8] == b"ftyp" and header[8:12] in MP4_AUDIO_BRANDS
    except (IOError, OSError):
        return False
    finally:
        await file.seek(0)

def to_base64(item: bytes):
    return b64encode(item).decode('ascii')

def format_chunk(prompt: str):
    delta = split(r'(?<=[.!?])\s+', prompt)
    return delta[:-1], delta[-1]