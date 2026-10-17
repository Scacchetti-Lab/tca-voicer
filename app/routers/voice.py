from typing import Annotated

from fastapi import APIRouter, Depends, Form, UploadFile, BackgroundTasks, WebSocketDisconnect, status, WebSocket
from fastapi.responses import JSONResponse
from app.dependencies import get_settings
from app.helpers.voice import is_valid_audio_file
from app.services.voice import process_webhook, process_voicechat
from pathlib import Path
from app.schemas.commons import BaseResponse
from app.constants.constants import DEFAULT_AUDIO_EXT
from app.config import Settings

router = APIRouter()


@router.websocket('/ws/chat')
async def voice_chat(ws: WebSocket, env: Annotated[Settings, Depends(get_settings)]):
    await ws.accept()
    try:
        while True:
            user_audio = await ws.receive_bytes()
            chat_audio = await process_voicechat(user_audio, env)

            if not chat_audio:
                return await ws.send_json(
                    BaseResponse(status=status.HTTP_409_CONFLICT, data=None, message="")
                )
            print(f'Tamanho do chat audio: {len(chat_audio)}')
            await ws.send_bytes(chat_audio)
    except WebSocketDisconnect:
        pass
    except Exception:
        import traceback; traceback.print_exc()
        await ws.send_json(
            BaseResponse(status=500, data=None, message="Arquivo não processado!").model_dump()
        )
        await ws.close(code=1011)


@router.post('/meeting/transcript', status_code=status.HTTP_202_ACCEPTED, response_class=JSONResponse)
async def transcribe_meeeting(audio: UploadFile, job_id: Annotated[str, Form()], callback_url: Annotated[str, Form()], background_tasks: BackgroundTasks, env: Annotated[Settings, Depends(get_settings)]) -> JSONResponse:
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