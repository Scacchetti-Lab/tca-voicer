from asyncio import to_thread
from fastapi import UploadFile
from app.dependencies import get_whisper
from app.helpers.voice import format_chunk, to_base64
from app.schemas.commons import VoiceChatRequest
from app.schemas.sse import BotAudioChunk, TextChunk
from .bot import generate_ai_reply
from .qwen import generate_audio
import httpx
from app.config import Settings

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

async def tts_request(prompt: str, env: Settings, speaker):
    response = generate_audio(prompt, env, speaker)
    async for v in response:
        yield BotAudioChunk(to_base64(v))

async def process_voicechat(audio: UploadFile, request: VoiceChatRequest, env: Settings):
    transcript = await read_audio(audio)
    sse_response = generate_ai_reply(transcript, request.interact_id, env)

    raw = ''
    async for item in sse_response:
        match item:
            case TextChunk(text=text):
                yield item
                reply, raw = format_chunk(raw + text)
                
                for w in reply:
                    async for chunk in tts_request(w, env, request.speaker):
                        yield chunk
            case _:
                yield item
    if raw.strip():
        async for chunk in tts_request(raw.strip(), env, request.speaker):
            yield chunk