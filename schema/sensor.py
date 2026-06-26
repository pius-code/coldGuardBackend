from pydantic import BaseModel


class SensorCreate(BaseModel):
    temperature: float
    humidity: float
    light_intensity: float
