from fastapi import FastAPI
from app.constants.fastapi_doc import fastapi_data
from app.schemas.healthcheck import HealthCheck

app = FastAPI(
    title=fastapi_data["title"],
    summary=fastapi_data["summary"],
    description=fastapi_data["description"],
    contact=fastapi_data["contact"],
    version=fastapi_data["version"],
    license_info=fastapi_data["license"],
    redoc_url=None,
);

@app.get("/", 
         response_model=HealthCheck, 
         summary="Teste o status da API",
         tags=["Healthcheck"])
def get_healthcheck() -> HealthCheck:
    return HealthCheck()

app.add_api_route("/health", get_healthcheck, methods=["GET"], tags=["Healthcheck"], response_model=HealthCheck, summary="Teste o status da API")