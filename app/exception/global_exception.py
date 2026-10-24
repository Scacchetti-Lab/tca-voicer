import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
import traceback

from httpx import HTTPStatusError
from pydantic import ValidationError

from app.schemas.commons import BaseResponse

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("tca-voicer")

async def global_handler(request: Request, exc: Exception):
    log.exception(f"Falha ao processar a requisição: {exc}")

    print(traceback.format_exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=BaseResponse(status=500, data=None, message="Falha ao processar a requisição").model_dump()
    )

async def http_exc_handler(request: Request, exc: HTTPStatusError):
    log.exception(f"Falha ao processar a requisição: {exc}")

    print(traceback.format_exc)
    return JSONResponse(
        status_code=exc.response.status_code,
        content=BaseResponse(status=exc.response.status_code, data=None, message=exc.response.text).model_dump()
    )

async def validation_handler(_, exc: ValidationError):
    log.exception(f"Falha ao converter string para objeto: {exc}")

    print(traceback.format_exc)
    print(exc.from_exception_data)
    return JSONResponse(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        content=BaseResponse(status=406, data=None, message="Falha ao converter string para objeto").model_dump()
    )