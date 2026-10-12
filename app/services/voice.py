import logging
from json import dumps

from fastapi import UploadFile
from faster_whisper import WhisperModel, BatchedInferencePipeline
import httpx
from app.config import Settings

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("tca-voicer")

def save_transcripted_file(filename: str, batch: str, path: str):
    with open(f'{path}/{filename}.txt', 'a+') as f:
        f.writelines(batch)

async def read_audio(audio: UploadFile, env: Settings):
    model = WhisperModel(env.whisper_model, device="cpu", compute_type="int8") 
    bathced_model = BatchedInferencePipeline(model=model)
    segments, _ = bathced_model.transcribe(
        audio=audio.file,
        batch_size=8,
        language='pt'
    )

    transcript = ''
    for segment in segments:
        transcript += segment.text
    return transcript


async def process_webhook(audio: UploadFile, callback_url: str, job_id: str, env: Settings):
    try:
        transcript = await read_audio(audio, env)

        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                callback_url,
                json={"jobId": job_id, "transcript": transcript},
                headers={"X-VOICER-SECRET": env.vc_webhook_key},
            )
            resp.raise_for_status()
    except Exception:
        log.exception("Falha ao processar o job %s", job_id)