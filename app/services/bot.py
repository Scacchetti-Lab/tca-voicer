import httpx
from app.config import Settings
from app.schemas.commons import ResponseBaseModel, BaseResponse

async def send_message(message: str, env: Settings) -> BaseResponse:
    chat_request = {
        "message": message,
        "previous_interact_id": None,
        "chat_model": "VOICE"
    }
    header = {"X-ACCESS-KEY": env.voxen_secret_key}
    response = None

    async with httpx.AsyncClient() as client:
        try:
            ares = await client.post(
                f'{env.voxen_url}/v1/chat/messages',
                json=chat_request,
                headers=header,
                timeout=90
            )
            resp = ResponseBaseModel.model_validate_json(ares.text)
            default_message = "Falha ao enviar mensagem ao bot" if not resp.is_valid else "Processamento concluído!"
            
            response = BaseResponse(
                    status=resp.status, 
                    data=resp.content,
                    message=resp.message or default_message
                )
        finally:
            await client.aclose()
    return response