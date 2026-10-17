from re import split
from httpx import post
from wave import open
from fastapi import File
from io import BytesIO
from app.config import Settings
from app.constants.constants import SPEAKERS

"""
Lista de Tarefas

[] Fazer Tratativas de erro caso algo falhe
[] Retornar os status code HTTP corretos
[] Caso algo falhe, retornar o audio padrao e generico
"""


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
    blocks = splited_blocks(user_text, max_chars=250)
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