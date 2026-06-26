from beanie import Document
from datetime import datetime


class Sensor(Document):
    dateTime: datetime = None
    temperature: float
    humidity: float
    light_intensity: float

    class Settings:
        name = "sensor readings"
