from typing import Annotated

from traceback import format_exc
from fastapi import APIRouter, Depends, File, Form, UploadFile, BackgroundTasks, status
from fastapi.sse import EventSourceResponse, ServerSentEvent
from fastapi.responses import JSONResponse
from app.dependencies import get_settings
from app.helpers.voice import is_valid_audio_file
from app.schemas.sse import BotAudioChunk, ErrorSSE, InteractionId, TextChunk, TitleGenerate
from app.services.voice import process_webhook, process_voicechat
from pathlib import Path
from app.schemas.commons import BaseResponse, VoiceChatRequest
from app.constants.constants import DEFAULT_AUDIO_EXT, SPEAKERS
from app.config import Settings

router = APIRouter()

@router.post('/chatbot', response_class=EventSourceResponse)
async def process_chat_request(
    env: Annotated[Settings, Depends(get_settings)], 
    audio: UploadFile = File(), 
    speaker: SPEAKERS = Form(),
    interact_id: str | None = Form(None)):
    try:
        request = VoiceChatRequest(speaker=speaker, interact_id=interact_id)

        response = process_voicechat(audio, request, env)
        interact_id = None
        async for item in response:
            match item:
                case TextChunk(text=text):
                    yield ServerSentEvent(event="text", data={"text": text})
                case BotAudioChunk(bot_audio=bot_audio):
                    yield ServerSentEvent(event="audio", data={"bot_audio": bot_audio})
                case TitleGenerate(title=title):
                    yield ServerSentEvent(event="title", data={"title": title})
                case ErrorSSE(message=message):
                    yield ServerSentEvent(event="error", data={"message": message})
                    return
                case InteractionId(interaction_id=id):
                    interact_id = id

        if not interact_id: raise Exception()
        yield ServerSentEvent(event="done", data={"interaction_id": interact_id})
    except Exception as ex:
        print(ex)
        print(format_exc())
        yield ServerSentEvent(event="error", data={"message": 'Ocorreu um erro durante o processamento do voicer'})


@router.post('/meeting/transcript', status_code=status.HTTP_202_ACCEPTED, response_class=JSONResponse)
async def transcribe_meeeting(
    audio: UploadFile, 
    job_id: Annotated[str, Form()], 
    callback_url: Annotated[str, Form()], 
    background_tasks: BackgroundTasks, 
    env: Annotated[Settings, Depends(get_settings)]
) -> JSONResponse:
    
    ext = Path(audio.filename or '').suffix[1:].lower()
    if ext not in DEFAULT_AUDIO_EXT:
        return JSONResponse(content=BaseResponse(status=status.HTTP_400_BAD_REQUEST, data=None, message='Extensão de arquivo inválida').model_dump())
    if not await is_valid_audio_file(audio):
        return JSONResponse(content=BaseResponse(status=status.HTTP_400_BAD_REQUEST, data=None, message='Arquivo mal formato. Envie outro').model_dump())

    background_tasks.add_task(process_webhook, audio,callback_url, job_id, env)
    return JSONResponse(
        content=BaseResponse(status=status.HTTP_202_ACCEPTED, 
                             data=None, 
                             message=f'Arquivo {(audio.filename or '.').split('.')[0]} está sendo processado!').model_dump(),
        status_code=status.HTTP_202_ACCEPTED
    )