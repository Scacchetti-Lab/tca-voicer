from fastapi import APIRouter, WebSocket, BackgroundTasks

router = APIRouter()


@router.post('/bot')
async def voice_talk_websocker(background_tasks: BackgroundTasks):
    pass


@router.post('/meeting')
async def transcribe_meeeting(background_tasks: BackgroundTasks):
    pass