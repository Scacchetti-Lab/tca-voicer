from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, BackgroundTasks, status
from fastapi.responses import JSONResponse
from app.dependencies import get_settings
from app.helpers.voice import is_valid_audio_file
from app.services.voice import read_audio
from pathlib import Path
from app.schemas.commons import BaseResponse
from app.constants.constants import DEFAULT_AUDIO_EXT
from app.config import Settings

router = APIRouter()


@router.post('/chat')
async def voice_chat(audio: UploadFile, background_tasks: BackgroundTasks, env: Annotated[Settings, Depends(get_settings)]):
    ext = Path(audio.filename or '').suffix.lower()
    if ext not in DEFAULT_AUDIO_EXT:
        return JSONResponse(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, 
            content=BaseResponse(status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, 
                                 data=None, 
                                 message='Extensão de arquivo inválida'))
    
    if not is_valid_audio_file(audio):
        return JSONResponse(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, 
            content=BaseResponse(status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, 
                                 data=None, 
                                 message='Arquivo mal formato. Envie outro'))
    
    data = await read_audio(audio, env)


@router.post('/webhook/read-audio', status_code=status.HTTP_102_PROCESSING, response_model=JSONResponse)
async def transcribe_meeeting(audio: UploadFile, background_tasks: BackgroundTasks, env: Annotated[Settings, Depends(get_settings)]) -> JSONResponse:
    ext = Path(audio.filename or '').suffix.lower()
    if ext not in DEFAULT_AUDIO_EXT:
        return JSONResponse(content=BaseResponse(status=status.HTTP_400_BAD_REQUEST, data=None, message='Extensão de arquivo inválida'))
    if not is_valid_audio_file(audio):
        return JSONResponse(content=BaseResponse(status=status.HTTP_400_BAD_REQUEST, data=None, message='Arquivo mal formato. Envie outro'))

    background_tasks.add_task(read_audio, audio, env)
    return JSONResponse(
        content=BaseResponse(status=
                             status.HTTP_102_PROCESSING, 
                             data=None, 
                             message=f'Arquivo {(audio.filename or '.').split('.')[0]} está sendo processado!'),
        status_code=status.HTTP_102_PROCESSING
    )