from typing import cast
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from httpx import HTTPStatusError
from pydantic import ValidationError
from starlette.types import ExceptionHandler
from app.constants.fastapi_doc import fastapi_data
from app.exception.global_exception import global_handler, http_exc_handler, validation_handler
from app.schemas.healthcheck import HealthCheck
from app.routers import voice
from contextlib import asynccontextmanager
from app.dependencies import get_whisper

@asynccontextmanager
async def lifespan(app: FastAPI):
    get_whisper()
    yield

app = FastAPI(
    title=fastapi_data["title"],
    summary=fastapi_data["summary"],
    description=fastapi_data["description"],
    contact=fastapi_data["contact"],
    version=fastapi_data["version"],
    license_info=fastapi_data["license"],
    redoc_url=None,
    lifespan=lifespan
)

@app.get("/", 
         response_model=HealthCheck, 
         summary="Teste o status da API",
         tags=["Healthcheck"])
def get_healthcheck() -> HealthCheck:
    return HealthCheck()

app.add_api_route("/health", get_healthcheck, methods=["GET"], tags=["Healthcheck"], response_model=HealthCheck, summary="Teste o status da API")
app.include_router(voice.router, prefix="/v1/voice", tags=["Voicer"])
app.add_exception_handler(Exception, global_handler)
app.add_exception_handler(HTTPStatusError, cast(ExceptionHandler, http_exc_handler))
app.add_exception_handler(ValidationError, cast(ExceptionHandler, validation_handler))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)