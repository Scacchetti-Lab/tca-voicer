from pydantic import BaseModel
from datetime import datetime

class HealthCheck(BaseModel):
    app_name: str = "API TCA-Voicer"
    status: str = "OK"
    started_in: str = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")