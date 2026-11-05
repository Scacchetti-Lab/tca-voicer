from httpx import AsyncClient
from httpx_sse import aconnect_sse
from app.config import Settings
from app.schemas.sse import TextChunk, TitleGenerate, ErrorSSE, InteractionId

async def generate_ai_reply(message: str, interact_id: str | None, env: Settings):
    payload = {
        "message": message,
        "previous_interact_id": interact_id,
        "chat_model": "VOICE"
    }
    
    async with AsyncClient(timeout=90) as client:
        try:
            async for e, data in send_to_chatbot(client, payload, env):
                match e:
                    case "delta":
                        yield TextChunk(data["text"])
                    case "title":
                        yield TitleGenerate(data["title"])
                    case "done":
                        yield InteractionId(data["interaction_id"])
                    case "error":
                        yield ErrorSSE(data["message"])
        except Exception:
            raise


async def send_to_chatbot(client: AsyncClient, payload: dict[str, str], env: Settings):
    header = {"X-ACCESS-KEY": env.voxen_secret_key}
    url = f'{env.voxen_url}/v2/chat/stream/message'
    
    async with aconnect_sse(client, "POST", url, headers=header, json=payload) as event:
        event.response.raise_for_status()

        async for sse in event.aiter_sse():
            yield sse.event, sse.json()