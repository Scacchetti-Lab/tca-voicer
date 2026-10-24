from re import split
from httpx import post
from wave import open
from pathlib import Path
import struct
from io import BytesIO
from app.config import Settings
from app.constants.constants import SPEAKERS
from app.helpers.normalize_prompt import normalize_transcript

"""
Lista de Tarefas

[] Fazer Tratativas de erro caso algo falhe
[] Retornar os status code HTTP corretos
[] Caso algo falhe, retornar o audio padrao e generico
"""

base_path = Path(__file__).resolve().parent
ryan_error_path = str(base_path / "/app/audios/ryan_error.wav")
sohee_error_path = str(base_path / "/app/audios/sohee_error.wav")

def splited_blocks(texto, max_chars=300):
    paragraph = texto.strip().split('\n\n')
    blocks = []
    for p in paragraph:
        p = p.strip()
        if not p:
            continue
        if len(p) <= max_chars:
            blocks.append(p)
        else:
            frases = split(r'(?<=[.!?])\s+', p)
            current = ""
            for phrase in frases:
                if len(current) + len(phrase) < max_chars:
                    current += " " + phrase
                else:
                    blocks.append(current.strip())
                    current = phrase
            if current:
                blocks.append(current.strip())
    return blocks

def generate_audio(user_text, env: Settings, speaker: SPEAKERS = "ryan"):
    message = normalize_transcript(user_text)
    blocks = splited_blocks(message, max_chars=250)
    complet_pcm = b""

    for b in blocks:
        payload = {
            "text": b,
            "speaker": speaker,
            "language": "Portuguese",
            "instruct": "Speak with a Brazilian Portuguese accent, warm and casual tone.",
            "rate": 1.18,
            "temperature": 0.3,
            "seed": 42
        }
        response = post(f"{env.tts_host_url}/v1/tts", json=payload, timeout=60)
        response.raise_for_status()
        with open(BytesIO(response.content), 'rb') as wf:
            complet_pcm += wf.readframes(wf.getnframes())

    chat_audio = BytesIO()
    with open(chat_audio, 'wb') as wav_out:
        wav_out.setnchannels(1)
        wav_out.setsampwidth(2)
        wav_out.setframerate(24000)
        wav_out.writeframes(complet_pcm)

    chat_audio.seek(0)
    return chat_audio


def get_error_audio(speaker: SPEAKERS = "ryan"):
    base_path = sohee_error_path if speaker == "sohee" else ryan_error_path
    return base_path