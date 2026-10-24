from pydantic import BaseModel
from typing import Any

class BaseResponse(BaseModel):
    status: int
    data: Any
    message: str

class ChatContent(BaseModel):
    title: str
    reply: str
    previous_interaction_id: str | None = None
    tokens_used: int = 0

class ResponseBaseModel(BaseModel):
    status: int
    content: ChatContent
    message: str | None
    is_valid: bool

class VoiceResult(BaseModel):
    status: int
    message: str | None = None
    transcript: str | None = None   
    chat_content: ChatContent | None = None       
    audio: bytes | None = None