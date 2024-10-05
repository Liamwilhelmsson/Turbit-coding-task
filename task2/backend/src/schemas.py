from pydantic import BaseModel
from datetime import datetime


class TurbineDataResponse(BaseModel):
    turbine_id: int
    timestamp: datetime
    wind_speed_ms: float
    power_output_kw: float
