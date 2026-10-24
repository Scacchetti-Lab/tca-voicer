from asyncio import to_thread
from fastapi import UploadFile
from app.constants.constants import SPEAKERS
from app.dependencies import get_whisper
from app.helpers.normalize_prompt import normalize_transcript
from app.schemas.commons import VoiceResult
from .bot import send_message
from .qwen import generate_audio, get_error_audio
import httpx
from app.config import Settings
from io import BytesIO

def save_transcripted_file(filename: str, batch: str, path: str):
    with open(f'{path}/{filename}.txt', 'a+') as f:
        f.writelines(batch)

def _transcrever(audio: UploadFile) -> str:
    segments, _ = get_whisper().transcribe(
        audio=audio.file,
        batch_size=8,
        language="pt",
    )
    return "".join(segment.text for segment in segments)


async def read_audio(audio: UploadFile) -> str:
    return await to_thread(_transcrever, audio)

async def process_webhook(audio: UploadFile, callback_url: str, job_id: str, env: Settings):
    transcript = await read_audio(audio)

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            callback_url,
            json={"jobId": job_id, "transcript": transcript},
            headers={"X-VOICER-SECRET": env.vc_webhook_key},
        )
        resp.raise_for_status()

async def process_voicechat(audio: bytes, speaker: SPEAKERS, env: Settings) -> VoiceResult:
    upload_file = UploadFile(file=BytesIO(audio), filename="user_audio.wav")
    transcript = await read_audio(upload_file)
    result = await send_message(transcript, env)

    chat_audio = await to_thread(generate_audio, result.data.reply, env, speaker)
    return VoiceResult(
        status=result.status,
        message=result.message,
        transcript=transcript,
        chat_content=result.data,
        audio=chat_audio.read1()
    )
        